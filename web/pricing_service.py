"""
Pricing Engine Service — Commercial Scoring Edition
===================================================
Replaces the guardrail-binary selection logic with a transparent
commercial scoring system that treats the competitor premium as a
risk-weighted PENALTY rather than a hard binary cutoff.

Objective  : MAXIMIZE EXPECTED PROFIT (primary)
             MAXIMIZE EXPECTED REVENUE (secondary)
Safety     : Hard limits on price swing (-10%/+10%) and cost floor
Competitor : Competitive Score penalizes rising premium progressively;
             competitor ceiling is a risk signal, not a veto.

Three possible decisions:
  ✓ RECOMMENDED        – candidate beats current on profit (±modest rev)
  ⚠ HOLD CURRENT PRICE – no alternative improves profit; keep current
  ⚠ CONTROLLED PREMIUM – best is above competitor ceiling but still
                          delivers better profit & reasonable premium

Files changed: web/pricing_service.py only.
XGBoost model / forecasting / dataset: NOT modified.
"""

import numpy as np
import pandas as pd


# ────────────────────────────────────────────────────────────────────
#  HARD GUARDRAILS (price swing / cost floor / minimum demand)
# ────────────────────────────────────────────────────────────────────
_MAX_INCREASE_PCT  = 10.0   # % above current price
_MAX_DECREASE_PCT  = 10.0   # % below current price
_MIN_DEMAND        = 5.0    # units/day absolute floor
_COMP_SOFT_LIMIT   = 5.0    # % competitor premium — soft (penalty begins)
_COMP_HARD_LIMIT   = 10.0   # % competitor premium — absolute ceiling beyond which we never recommend
# NOTE: Prices that exceed _COMP_HARD_LIMIT vs competitor are still
#       evaluated but their commercial score is penalised so heavily
#       that they will almost never win.  Current price is always a
#       valid candidate and will be chosen as "HOLD" if nothing is better.


# ────────────────────────────────────────────────────────────────────
#  COMMERCIAL SCORE WEIGHTS
# ────────────────────────────────────────────────────────────────────
_W_PROFIT      = 0.50
_W_REVENUE     = 0.20
_W_DEMAND      = 0.10
_W_COMPETITIVE = 0.20


def _competitive_score(comp_gap_pct: float) -> float:
    """
    Maps competitor premium % → competitive score [0, 1].
    Score = 1.0 at parity or discount.
    Score decays progressively as premium rises above +5%.
    Score = 0.0 at +10% or above (effectively blocked).

    comp_gap_pct = ((candidate - competitor) / competitor) * 100
    """
    if comp_gap_pct <= _COMP_SOFT_LIMIT:
        return 1.0                           # 0 to +5% — no penalty
    elif comp_gap_pct <= _COMP_HARD_LIMIT:
        # Linear decay from 1.0 at +5% → 0.0 at +10%
        return 1.0 - (comp_gap_pct - _COMP_SOFT_LIMIT) / (_COMP_HARD_LIMIT - _COMP_SOFT_LIMIT)
    else:
        return 0.0                           # Above +10% — fully blocked


def _score_candidates(df: pd.DataFrame, cur_rev: float, cur_prof: float, cur_dem: float) -> pd.DataFrame:
    """
    Adds a Commercial_Score column to the candidate grid df.
    Only called on candidates that pass hard guardrails (price swing + cost floor + min demand).

    Score formula:
        Commercial_Score = 0.50 * P_score + 0.20 * R_score + 0.10 * D_score + 0.20 * C_score
    All component scores are normalised 0–1 relative to the grid maximum.
    """
    df = df.copy()

    # Profit / Revenue / Demand: normalise relative to observed range in grid
    p_min, p_max = df["Expected_Profit"].min(), df["Expected_Profit"].max()
    r_min, r_max = df["Expected_Revenue"].min(), df["Expected_Revenue"].max()
    d_min, d_max = df["Predicted_Demand"].min(), df["Predicted_Demand"].max()

    p_range = p_max - p_min if p_max > p_min else 1.0
    r_range = r_max - r_min if r_max > r_min else 1.0
    d_range = d_max - d_min if d_max > d_min else 1.0

    df["_P_score"] = (df["Expected_Profit"]  - p_min) / p_range
    df["_R_score"] = (df["Expected_Revenue"] - r_min) / r_range
    df["_D_score"] = (df["Predicted_Demand"] - d_min) / d_range
    df["_C_score"] = df["Competitor_Gap_Percent"].apply(_competitive_score)

    df["Commercial_Score"] = (
        _W_PROFIT      * df["_P_score"] +
        _W_REVENUE     * df["_R_score"] +
        _W_DEMAND      * df["_D_score"] +
        _W_COMPETITIVE * df["_C_score"]
    )

    return df


def _hard_pass(row, cur_p: float, unit_cost: float) -> bool:
    """
    True when candidate passes all HARD guardrails (not competitor ceiling).
    Competitor ceiling is treated as a soft penalty, not a hard veto.
    """
    p_chg = row["Price_Change_Percent"]
    dem   = row["Predicted_Demand"]
    cand  = row["Candidate_Price"]

    if p_chg > _MAX_INCREASE_PCT + 0.01:
        return False
    if p_chg < -(_MAX_DECREASE_PCT + 0.01):
        return False
    if dem < _MIN_DEMAND - 0.01:
        return False
    if unit_cost > 0 and cand < (unit_cost - 0.01):
        return False
    # Absolute competitor hard ceiling — never recommend beyond +10%
    if row["Competitor_Gap_Percent"] > _COMP_HARD_LIMIT + 0.01:
        return False
    return True


def analyze_pricing_recommendation(df_grid_sku: pd.DataFrame, rec_row) -> dict:
    """
    Commercial-score based pricing recommendation engine.

    Algorithm:
    1. Build candidate grid restricted to the standard ±10% price swing window.
    2. Always include current price as a candidate (synthetic row if needed).
    3. Filter hard-pass candidates (price swing, cost floor, min demand, <+10% comp).
    4. Apply commercial scoring (profit 50%, revenue 20%, demand 10%, competitive 20%).
    5. Identify best scoring candidate.
    6. Apply profit-safety rule:
       If best candidate profit < current profit AND no candidate improves profit,
       return HOLD CURRENT PRICE.
    7. Return a complete result dict consumed by app.py and rec_hero_html().
    """

    # ── Baseline facts ────────────────────────────────────────────
    cur_p     = float(rec_row["Current_Price"])
    comp_p    = float(rec_row["Competitor_Price"])
    unit_cost = float(rec_row.get("Unit_Cost", 0.0))
    cur_dem   = float(rec_row.get("Current_Predicted_Demand", 50.0))
    cur_rev   = float(rec_row.get("Current_Expected_Revenue", cur_p * cur_dem))
    cur_prof  = float(rec_row.get("Current_Expected_Profit", (cur_p - unit_cost) * cur_dem))

    comp_gap_cur = ((cur_p - comp_p) / (comp_p + 1e-9)) * 100.0

    # ── Restrict to standard search window ────────────────────────
    if len(df_grid_sku) == 0:
        # No grid data — fall back to rec_row values
        return _fallback_result(rec_row, cur_p, comp_p, unit_cost, cur_dem, cur_rev, cur_prof)

    std_grid = df_grid_sku[
        (df_grid_sku["Price_Adjustment_Percent"] >= -_MAX_DECREASE_PCT) &
        (df_grid_sku["Price_Adjustment_Percent"] <= _MAX_INCREASE_PCT)
    ].copy()

    if len(std_grid) == 0:
        std_grid = df_grid_sku.copy()

    # ── Ensure current price is present in grid ───────────────────
    if abs(cur_p - std_grid["Candidate_Price"].values).min() > 0.5:
        # Synthesise a row for current price using rec_row baseline values
        cur_row_synth = {
            "Candidate_Price": cur_p,
            "Predicted_Demand": cur_dem,
            "Expected_Revenue": cur_rev,
            "Expected_Profit": cur_prof,
            "Price_Adjustment_Percent": 0.0,
            "Price_Change_Percent": 0.0,
            "Competitor_Gap_Percent": comp_gap_cur,
            "Guardrail_Status": "PASSED",
            "Is_Feasible": True,
        }
        std_grid = pd.concat([std_grid, pd.DataFrame([cur_row_synth])], ignore_index=True)

    # ── Hard-pass filter (competitor premium is NOT a hard veto here) ──
    hard_ok = std_grid.apply(lambda row: _hard_pass(row, cur_p, unit_cost), axis=1)
    hp_grid = std_grid[hard_ok].copy()

    if len(hp_grid) == 0:
        # All candidates fail hard guardrails — hold current
        return _hold_result(cur_p, comp_p, unit_cost, cur_dem, cur_rev, cur_prof, comp_gap_cur,
                            reason="No candidate satisfied hard operational guardrails.")

    # ── Commercial scoring ─────────────────────────────────────────
    scored = _score_candidates(hp_grid, cur_rev, cur_prof, cur_dem)

    # ── Find the row closest to current price (used as hold reference) ──
    cur_row = scored.iloc[(scored["Candidate_Price"] - cur_p).abs().argsort()[:1]]
    cur_ref_prof = float(cur_row["Expected_Profit"].iloc[0])
    cur_ref_rev  = float(cur_row["Expected_Revenue"].iloc[0])
    cur_ref_dem  = float(cur_row["Predicted_Demand"].iloc[0])
    cur_ref_score= float(cur_row["Commercial_Score"].iloc[0])

    # ── Prefer candidates that improve profit ─────────────────────
    profit_positive = scored[scored["Expected_Profit"] >= cur_ref_prof * 0.999]

    if len(profit_positive) > 0:
        # Among profit-improving candidates, pick highest commercial score
        best_row = profit_positive.sort_values("Commercial_Score", ascending=False).iloc[0]
    else:
        # No candidate improves profit — return HOLD
        return _hold_result(cur_p, comp_p, unit_cost, cur_ref_dem, cur_ref_rev, cur_ref_prof, comp_gap_cur,
                            reason="No candidate improves expected profit versus current price.")

    # ── If best IS the current price — HOLD ───────────────────────
    best_p = float(best_row["Candidate_Price"])
    if abs(best_p - cur_p) < 0.5:
        return _hold_result(cur_p, comp_p, unit_cost, cur_ref_dem, cur_ref_rev, cur_ref_prof, comp_gap_cur,
                            reason="Current price achieves the highest commercial score among all viable candidates.")

    # ── Build the recommendation ───────────────────────────────────
    final_p    = best_p
    final_dem  = float(best_row["Predicted_Demand"])
    final_rev  = float(best_row["Expected_Revenue"])
    final_prof = float(best_row["Expected_Profit"])
    comp_gap   = float(best_row["Competitor_Gap_Percent"])

    price_change_pct = ((final_p - cur_p) / (cur_p + 1e-9)) * 100.0
    rev_impact_pct   = ((final_rev  - cur_ref_rev)  / (abs(cur_ref_rev)  + 1e-9)) * 100.0
    prof_impact_pct  = ((final_prof - cur_ref_prof) / (abs(cur_ref_prof) + 1e-9)) * 100.0

    rev_label  = "Revenue Lift"  if rev_impact_pct  > 0.005 else "Revenue Impact"
    prof_label = "Profit Lift"   if prof_impact_pct > 0.005 else "Profit Impact"
    rev_cls    = "pos" if rev_impact_pct  > 0.005 else ("neg" if rev_impact_pct  < -0.005 else "muted")
    prof_cls   = "pos" if prof_impact_pct > 0.005 else ("neg" if prof_impact_pct < -0.005 else "muted")
    price_cls  = "pos" if price_change_pct > 0.005 else ("neg" if price_change_pct < -0.005 else "muted")

    # ── Decide decision status ────────────────────────────────────
    is_controlled_premium = comp_gap > _COMP_SOFT_LIMIT    # > +5% competitor

    if is_controlled_premium:
        decision_status = "⚠ CONTROLLED PREMIUM"
        badge_cls       = "badge-warn"
        callout_cls     = "callout-warn"
        price_hero_label = "RECOMMENDED PRICE"
        rationale = (
            f"Price is {comp_gap:+.1f}% above the competitor benchmark, "
            f"supported by a projected profit improvement of {prof_impact_pct:+.1f}% "
            f"and revenue improvement of {rev_impact_pct:+.1f}%. "
            f"Monitor competitor response."
        )
    elif prof_impact_pct >= 0 and rev_impact_pct >= 0:
        decision_status  = "✓ RECOMMENDED"
        badge_cls        = "badge-safe"
        callout_cls      = "callout-ok"
        price_hero_label = "RECOMMENDED PRICE"
        if price_change_pct > 0.1:
            rationale = (
                f"Increase price by {price_change_pct:+.1f}% to improve expected profit ({prof_impact_pct:+.1f}%) "
                f"and revenue ({rev_impact_pct:+.1f}%) while remaining within competitive limits."
            )
        else:
            rationale = (
                f"Price reduction of {price_change_pct:+.1f}% stimulates demand, improving expected profit "
                f"({prof_impact_pct:+.1f}%) and revenue ({rev_impact_pct:+.1f}%)."
            )
    elif prof_impact_pct >= 0 and rev_impact_pct < 0:
        decision_status  = "✓ RECOMMENDED"
        badge_cls        = "badge-safe"
        callout_cls      = "callout-ok"
        price_hero_label = "RECOMMENDED PRICE"
        rationale = (
            f"Price increase of {price_change_pct:+.1f}% reduces unit volume slightly "
            f"({rev_impact_pct:+.1f}% revenue) but significantly improves gross profit ({prof_impact_pct:+.1f}%). "
            f"Margin improvement outweighs the volume effect."
        )
    elif rev_impact_pct > 0 and prof_impact_pct < 0:
        decision_status  = "⚠ MARGIN CAUTION"
        badge_cls        = "badge-warn"
        callout_cls      = "callout-warn"
        price_hero_label = "RECOMMENDED PRICE"
        rationale = (
            f"Price change of {price_change_pct:+.1f}% improves expected revenue ({rev_impact_pct:+.1f}%) "
            f"but reduces expected profit ({prof_impact_pct:+.1f}%). Review margin impact before applying."
        )
    else:
        # Should not normally reach here — HOLD should have been returned
        decision_status  = "⚠ MARGINAL"
        badge_cls        = "badge-med"
        callout_cls      = "callout-warn"
        price_hero_label = "RECOMMENDED PRICE"
        rationale = (
            f"Marginal recommendation: price change of {price_change_pct:+.1f}% with mixed impact on "
            f"revenue ({rev_impact_pct:+.1f}%) and profit ({prof_impact_pct:+.1f}%)."
        )

    # Build why-this-price detail dict
    demand_chg_pct = ((final_dem - cur_ref_dem) / (abs(cur_ref_dem) + 1e-9)) * 100.0
    why = _build_why(price_change_pct, demand_chg_pct, rev_impact_pct, prof_impact_pct, comp_gap, decision_status)

    return {
        # Prices
        "cur_p": cur_p,
        "comp_p": comp_p,
        "unit_cost": unit_cost,
        # Current baseline (from model / grid)
        "cur_dem": cur_ref_dem,
        "cur_rev": cur_ref_rev,
        "cur_pro": cur_ref_prof,
        # Final recommendation
        "final_p": final_p,
        "final_dem": final_dem,
        "final_rev": final_rev,
        "final_pro": final_prof,
        # Legacy compat keys (econ_p = same as final in new logic)
        "econ_p": final_p,
        "econ_dem": final_dem,
        "econ_rev": final_rev,
        "econ_pro": final_prof,
        "econ_is_compliant": comp_gap <= _COMP_SOFT_LIMIT,
        "econ_violations": [] if comp_gap <= _COMP_HARD_LIMIT else [f"Competitor gap {comp_gap:+.1f}%"],
        "is_adjusted": is_controlled_premium,
        # Metrics
        "price_change_pct": price_change_pct,
        "rev_impact_pct": rev_impact_pct,
        "prof_impact_pct": prof_impact_pct,
        "demand_change_pct": demand_chg_pct,
        "comp_gap_pct": comp_gap,
        # Labels / styling
        "rev_label": rev_label,
        "prof_label": prof_label,
        "rev_cls": rev_cls,
        "prof_cls": prof_cls,
        "price_cls": price_cls,
        # Decision
        "price_hero_label": price_hero_label,
        "decision_status": decision_status,
        "badge_cls": badge_cls,
        "callout_cls": callout_cls,
        "rationale": rationale,
        "why": why,
        # Scored grid (for chart markers)
        "scored_grid": scored,
    }


# ────────────────────────────────────────────────────────────────────
#  HOLD CURRENT PRICE helper
# ────────────────────────────────────────────────────────────────────
def _hold_result(cur_p, comp_p, unit_cost, cur_dem, cur_rev, cur_prof, comp_gap_cur, reason=""):
    price_change_pct = 0.0
    why = {
        "price_change_pct": 0.0,
        "demand_change_pct": 0.0,
        "rev_impact_pct": 0.0,
        "prof_impact_pct": 0.0,
        "comp_gap_pct": comp_gap_cur,
        "explanation": reason if reason else "Current price retained because alternative prices do not improve expected business value.",
    }
    return {
        "cur_p": cur_p,
        "comp_p": comp_p,
        "unit_cost": unit_cost,
        "cur_dem": cur_dem,
        "cur_rev": cur_rev,
        "cur_pro": cur_prof,
        "final_p": cur_p,
        "final_dem": cur_dem,
        "final_rev": cur_rev,
        "final_pro": cur_prof,
        "econ_p": cur_p,
        "econ_dem": cur_dem,
        "econ_rev": cur_rev,
        "econ_pro": cur_prof,
        "econ_is_compliant": True,
        "econ_violations": [],
        "is_adjusted": False,
        "price_change_pct": 0.0,
        "rev_impact_pct": 0.0,
        "prof_impact_pct": 0.0,
        "demand_change_pct": 0.0,
        "comp_gap_pct": comp_gap_cur,
        "rev_label": "Revenue Impact",
        "prof_label": "Profit Impact",
        "rev_cls": "muted",
        "prof_cls": "muted",
        "price_cls": "muted",
        "price_hero_label": "CURRENT PRICE",
        "decision_status": "⚠ HOLD CURRENT PRICE",
        "badge_cls": "badge-med",
        "callout_cls": "callout-warn",
        "rationale": (
            reason + " Current price remains the best commercial option "
            "based on projected profit, revenue and competitive conditions."
        ).strip(),
        "why": why,
        "scored_grid": pd.DataFrame(),
    }


# ────────────────────────────────────────────────────────────────────
#  FALLBACK (no grid data)
# ────────────────────────────────────────────────────────────────────
def _fallback_result(rec_row, cur_p, comp_p, unit_cost, cur_dem, cur_rev, cur_prof):
    final_p    = float(rec_row.get("Recommended_Price", cur_p))
    final_dem  = float(rec_row.get("Recommended_Predicted_Demand", cur_dem))
    final_rev  = float(rec_row.get("Recommended_Expected_Revenue", final_p * final_dem))
    final_prof = float(rec_row.get("Recommended_Expected_Profit", (final_p - unit_cost) * final_dem))
    price_change_pct = ((final_p - cur_p) / (cur_p + 1e-9)) * 100.0
    rev_impact_pct   = ((final_rev  - cur_rev)  / (abs(cur_rev)  + 1e-9)) * 100.0
    prof_impact_pct  = ((final_prof - cur_prof) / (abs(cur_prof) + 1e-9)) * 100.0
    comp_gap = ((final_p - comp_p) / (comp_p + 1e-9)) * 100.0
    demand_chg_pct = ((final_dem - cur_dem) / (abs(cur_dem) + 1e-9)) * 100.0
    return {
        "cur_p": cur_p, "comp_p": comp_p, "unit_cost": unit_cost,
        "cur_dem": cur_dem, "cur_rev": cur_rev, "cur_pro": cur_prof,
        "final_p": final_p, "final_dem": final_dem, "final_rev": final_rev, "final_pro": final_prof,
        "econ_p": final_p, "econ_dem": final_dem, "econ_rev": final_rev, "econ_pro": final_prof,
        "econ_is_compliant": True, "econ_violations": [], "is_adjusted": False,
        "price_change_pct": price_change_pct,
        "rev_impact_pct": rev_impact_pct, "prof_impact_pct": prof_impact_pct,
        "demand_change_pct": demand_chg_pct, "comp_gap_pct": comp_gap,
        "rev_label": "Revenue Lift" if rev_impact_pct > 0.005 else "Revenue Impact",
        "prof_label": "Profit Lift" if prof_impact_pct > 0.005 else "Profit Impact",
        "rev_cls": "pos" if rev_impact_pct > 0.005 else ("neg" if rev_impact_pct < -0.005 else "muted"),
        "prof_cls": "pos" if prof_impact_pct > 0.005 else ("neg" if prof_impact_pct < -0.005 else "muted"),
        "price_cls": "pos" if price_change_pct > 0.005 else ("neg" if price_change_pct < -0.005 else "muted"),
        "price_hero_label": "RECOMMENDED PRICE",
        "decision_status": "✓ RECOMMENDED" if prof_impact_pct > 0 else "⚠ MARGINAL",
        "badge_cls": "badge-safe" if prof_impact_pct > 0 else "badge-med",
        "callout_cls": "callout-ok" if prof_impact_pct > 0 else "callout-warn",
        "rationale": f"Based on pre-computed recommendation. Price change: {price_change_pct:+.1f}%.",
        "why": _build_why(price_change_pct, demand_chg_pct, rev_impact_pct, prof_impact_pct, comp_gap, ""),
        "scored_grid": pd.DataFrame(),
    }


# ────────────────────────────────────────────────────────────────────
#  WHY THIS PRICE narrative
# ────────────────────────────────────────────────────────────────────
def _build_why(price_change_pct, demand_chg_pct, rev_impact_pct, prof_impact_pct, comp_gap, decision_status):
    if "HOLD" in decision_status:
        explanation = (
            "Current price retained because alternative prices do not improve "
            "expected business value."
        )
    elif prof_impact_pct > 0 and rev_impact_pct > 0:
        if price_change_pct > 0.1:
            explanation = (
                f"Price increased by {price_change_pct:+.1f}% because the expected profit "
                f"improvement ({prof_impact_pct:+.1f}%) outweighs the minor demand reduction "
                f"({demand_chg_pct:+.1f}% units)."
            )
        else:
            explanation = (
                f"Price reduced by {abs(price_change_pct):.1f}% because the expected demand "
                f"increase ({demand_chg_pct:+.1f}% units) is projected to improve both "
                f"revenue ({rev_impact_pct:+.1f}%) and profit ({prof_impact_pct:+.1f}%)."
            )
    elif prof_impact_pct > 0 and rev_impact_pct < 0:
        explanation = (
            f"Price increased by {price_change_pct:+.1f}%: volume falls slightly "
            f"({demand_chg_pct:+.1f}% units / {rev_impact_pct:+.1f}% revenue), but the higher unit "
            f"margin delivers a net profit improvement of {prof_impact_pct:+.1f}%."
        )
    elif "CONTROLLED PREMIUM" in decision_status:
        explanation = (
            f"Price is {comp_gap:+.1f}% above the competitor benchmark. The premium is "
            f"justified by the projected profit improvement ({prof_impact_pct:+.1f}%). "
            f"Monitor competitor pricing and customer response."
        )
    else:
        explanation = (
            f"Price change of {price_change_pct:+.1f}%. "
            f"Revenue impact: {rev_impact_pct:+.1f}%, Profit impact: {prof_impact_pct:+.1f}%."
        )

    return {
        "price_change_pct": price_change_pct,
        "demand_change_pct": demand_chg_pct,
        "rev_impact_pct": rev_impact_pct,
        "prof_impact_pct": prof_impact_pct,
        "comp_gap_pct": comp_gap,
        "explanation": explanation,
    }


# ────────────────────────────────────────────────────────────────────
#  LEGACY / COMPAT helpers (still imported by app.py)
# ────────────────────────────────────────────────────────────────────
def evaluate_guardrails(candidate_price, current_price, competitor_price, unit_cost, predicted_demand,
                         max_increase_pct=10.0, max_decrease_pct=10.0, max_competitor_premium_pct=5.0,
                         min_expected_demand=5.0):
    """
    Evaluates business guardrails against candidate price.
    Returns status dictionary, list of violations, and overall boolean.
    """
    price_change_pct = ((candidate_price - current_price) / (current_price + 1e-6)) * 100.0
    competitor_gap_pct = ((candidate_price - competitor_price) / (competitor_price + 1e-6)) * 100.0

    violations = []
    if price_change_pct > (max_increase_pct + 0.01):
        violations.append(f"Exceeds max price increase limit (+{max_increase_pct:.0f}%)")
    if price_change_pct < -(max_decrease_pct + 0.01):
        violations.append(f"Exceeds max price decrease limit (-{max_decrease_pct:.0f}%)")
    if competitor_gap_pct > (max_competitor_premium_pct + 0.01):
        violations.append(f"Exceeds competitor ceiling (+{max_competitor_premium_pct:.0f}%)")
    if predicted_demand < (min_expected_demand - 0.01):
        violations.append(f"Demand ({predicted_demand:.1f}) below threshold ({min_expected_demand:.0f} units)")
    if unit_cost > 0 and candidate_price < (unit_cost - 0.01):
        violations.append("Candidate price below wholesale unit cost")

    all_passed = len(violations) == 0
    status_label = "PASSED" if all_passed else f"VIOLATED: {'; '.join(violations)}"

    return {
        "is_feasible": all_passed,
        "violations": violations,
        "status_label": status_label,
        "price_change_pct": price_change_pct,
        "competitor_gap_pct": competitor_gap_pct
    }


def simulate_interactive_price(base_row_df, candidate_price, model, preprocessor, unit_cost=None):
    """
    Simulates demand, revenue, and profit for a custom user-selected candidate price on the fly.
    Used by the What-If Simulator page.
    """
    if model is None or preprocessor is None:
        return None

    sim_df = base_row_df.copy()
    cur_price  = float(sim_df["Our_Price"].iloc[0])
    comp_price = float(sim_df["Competitor_Price"].iloc[0])
    cost = unit_cost if unit_cost is not None else float(sim_df.get("Unit_Cost", pd.Series([0])).iloc[0])

    sim_df["Our_Price"]            = candidate_price
    sim_df["Price_Difference"]     = candidate_price - comp_price
    sim_df["Price_Ratio"]          = candidate_price / (comp_price + 1e-6)
    sim_df["Price_Premium_Percent"]= ((candidate_price - comp_price) / (comp_price + 1e-6)) * 100.0

    if "Base_Price" in sim_df.columns:
        base_p = float(sim_df["Base_Price"].iloc[0])
        sim_df["Discount_From_Base"] = ((base_p - candidate_price) / (base_p + 1e-6)) * 100.0

    X_trans     = preprocessor.transform(sim_df)
    pred_demand = float(np.clip(model.predict(X_trans)[0], 0, None))

    exp_rev  = round(candidate_price * pred_demand, 2)
    exp_cost = round(cost * pred_demand, 2)
    exp_prof = round(exp_rev - exp_cost, 2) if cost > 0 else 0.0

    guardrail_eval = evaluate_guardrails(
        candidate_price=candidate_price,
        current_price=cur_price,
        competitor_price=comp_price,
        unit_cost=cost,
        predicted_demand=pred_demand
    )

    return {
        "candidate_price": candidate_price,
        "predicted_demand": pred_demand,
        "expected_revenue": exp_rev,
        "expected_profit": exp_prof,
        "guardrail_eval": guardrail_eval
    }


def compute_lift_metrics(cur_price, rec_price, cur_demand, rec_demand, unit_cost=0.0):
    """Computes exact revenue and profit lift metrics."""
    cur_rev = cur_price * cur_demand
    rec_rev = rec_price * rec_demand
    rev_impact_pct = ((rec_rev - cur_rev) / (cur_rev + 1e-9)) * 100.0 if cur_rev > 0 else 0.0
    cur_prof = (cur_price - unit_cost) * cur_demand if unit_cost > 0 else cur_rev
    rec_prof = (rec_price - unit_cost) * rec_demand if unit_cost > 0 else rec_rev
    prof_impact_pct = ((rec_prof - cur_prof) / (abs(cur_prof) + 1e-9)) * 100.0 if cur_prof != 0 else 0.0
    price_change_pct = ((rec_price - cur_price) / (cur_price + 1e-9)) * 100.0 if cur_price > 0 else 0.0
    rev_label = "Revenue Lift" if rev_impact_pct > 0.005 else "Revenue Impact"
    prof_label = "Profit Lift" if prof_impact_pct > 0.005 else "Profit Impact"
    rev_cls = "pos" if rev_impact_pct > 0.005 else ("neg" if rev_impact_pct < -0.005 else "muted")
    prof_cls = "pos" if prof_impact_pct > 0.005 else ("neg" if prof_impact_pct < -0.005 else "muted")
    price_cls = "pos" if price_change_pct > 0.005 else ("neg" if price_change_pct < -0.005 else "muted")
    return {
        "cur_revenue": cur_rev, "rec_revenue": rec_rev, "rev_impact_pct": rev_impact_pct,
        "rev_label": rev_label, "rev_cls": rev_cls, "cur_profit": cur_prof,
        "rec_profit": rec_prof, "prof_impact_pct": prof_impact_pct, "prof_label": prof_label,
        "prof_cls": prof_cls, "price_change_pct": price_change_pct, "price_cls": price_cls
    }


def determine_decision_status(rev_impact_pct, prof_impact_pct, is_safe, price_change_pct, cur_price=0.0, comp_price=0.0):
    """Categorises business decision status (used by legacy callers)."""
    is_compliance_adjustment = (price_change_pct < -0.01) and (cur_price > (comp_price * 1.05 - 0.01))
    price_hero_label = "GUARDRAIL-COMPLIANT PRICE" if is_compliance_adjustment else "RECOMMENDED PRICE"
    if not is_safe:
        return "✕ NOT RECOMMENDED", "badge-err", "callout-err", price_hero_label
    if rev_impact_pct >= 0 and prof_impact_pct >= 0 and (rev_impact_pct > 0.005 or prof_impact_pct > 0.005):
        return "✓ RECOMMENDED", "badge-safe", "callout-ok", price_hero_label
    elif rev_impact_pct < 0 and prof_impact_pct < 0 and is_compliance_adjustment:
        return "⚠ CAUTION — COMPLIANCE ADJUSTMENT", "badge-warn", "callout-warn", price_hero_label
    elif rev_impact_pct < 0 and prof_impact_pct < 0:
        return "✕ NOT RECOMMENDED", "badge-err", "callout-err", price_hero_label
    elif rev_impact_pct > 0.005 and prof_impact_pct < -0.005:
        return "⚠ MARGIN CAUTION", "badge-warn", "callout-warn", price_hero_label
    elif rev_impact_pct < -0.005 and prof_impact_pct > 0.005:
        return "⚠ REVENUE TRADE-OFF", "badge-warn", "callout-warn", price_hero_label
    else:
        return "● NEUTRAL", "badge-med", "callout-ok", price_hero_label


def format_dynamic_rationale(cur_price, rec_price, comp_price, rev_impact_pct, prof_impact_pct, is_safe, price_change_pct):
    """Formats clean 1-2 sentence rationale (legacy compat)."""
    if not is_safe:
        return f"Price adjustment of {price_change_pct:+.1f}% breaches operational guardrails and is not recommended for deployment."
    if rev_impact_pct >= 0 and prof_impact_pct >= 0:
        if price_change_pct > 0.01:
            return f"Increase price by +{price_change_pct:.1f}% to improve both expected revenue ({rev_impact_pct:+.2f}%) and profit ({prof_impact_pct:+.2f}%)."
        else:
            return f"Price change of {price_change_pct:+.1f}% improves expected business value while satisfying all guardrails."
    elif rev_impact_pct > 0.005 and prof_impact_pct < -0.005:
        return f"Price reduction of {abs(price_change_pct):.1f}% lifts revenue ({rev_impact_pct:+.2f}%), but margin contraction reduces profit ({prof_impact_pct:+.2f}%)."
    elif rev_impact_pct < -0.005 and prof_impact_pct > 0.005:
        return f"Price increase of +{price_change_pct:.1f}% reduces volume slightly ({rev_impact_pct:+.2f}% revenue), but higher unit margin improves profit ({prof_impact_pct:+.2f}%)."
    else:
        return f"Price change of {price_change_pct:+.1f}%: both expected revenue ({rev_impact_pct:+.2f}%) and profit ({prof_impact_pct:+.2f}%) decline."
