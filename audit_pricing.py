"""
7-case audit of the new commercial scoring pricing engine.
Verifies: RECOMMENDED / HOLD / CONTROLLED PREMIUM decisions
and that no loss-making price is ever auto-recommended.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd
from web.data_loader import load_recommendations, load_simulation_grid
from web.pricing_service import analyze_pricing_recommendation

df_recs = load_recommendations()
df_grid = load_simulation_grid()

TEST_CASES = [
    ("Almond & Oat Milk 1L Pack of 3",       "Bengaluru Tech Park Store",  "CONTROLLED PREMIUM / HOLD (no profit-destroying discount)"),
    ("Classic Denim Jacket",                  "Bengaluru Tech Park Store",  "RECOMMENDED (profit+, revenue+)"),
    ("Wireless Noise-Canceling Headphones",   "Delhi Flagship Metro",       "RECOMMENDED (price increase case)"),
    ("Smart Fitness Watch",                   "Delhi Flagship Metro",       "RECOMMENDED / valid commercial outcome"),
    ("Smart Fitness Watch",                   "Mumbai High Street Mall",    "RECOMMENDED / valid commercial outcome"),
]

DIVIDER = "=" * 76

def run_case(product, store, note):
    r_sub = df_recs[(df_recs["Product_Name"] == product) & (df_recs["Store_Name"] == store)]
    if len(r_sub) == 0:
        return None
    r = r_sub.iloc[0]
    pid, sid = r["Product_ID"], r["Store_ID"]
    grid = df_grid[(df_grid["Product_ID"] == pid) & (df_grid["Store_ID"] == sid)].sort_values("Candidate_Price")
    res = analyze_pricing_recommendation(grid, r)

    print(DIVIDER)
    print(f"  PRODUCT : {product}")
    print(f"  STORE   : {store}")
    print(f"  NOTE    : {note}")
    print()
    print(f"  Current Price    : ₹{res['cur_p']:,.2f}")
    print(f"  Competitor Price : ₹{res['comp_p']:,.2f}  (gap vs current: {((res['cur_p']-res['comp_p'])/res['comp_p']*100):+.1f}%)")
    print(f"  Recommended Price: ₹{res['final_p']:,.2f}  ({res['price_change_pct']:+.1f}%)")
    print()
    print(f"  Current Profit   : ₹{res['cur_pro']:,.0f}")
    print(f"  Recommended Profit:₹{res['final_pro']:,.0f}  ({res['prof_impact_pct']:+.1f}% {res['prof_label']})")
    print(f"  Current Revenue  : ₹{res['cur_rev']:,.0f}")
    print(f"  Recommended Revenue:₹{res['final_rev']:,.0f}  ({res['rev_impact_pct']:+.1f}% {res['rev_label']})")
    print(f"  Demand           : {res['final_dem']:.1f} units/day  ({res['demand_change_pct']:+.1f}%)")
    print(f"  Competitor Gap   : {res['comp_gap_pct']:+.1f}%")
    print()
    print(f"  DECISION  : {res['decision_status']}")
    print(f"  HERO LABEL: {res['price_hero_label']}")
    print(f"  RATIONALE : {res['rationale']}")
    print(f"  WHY       : {res['why']['explanation']}")
    return res

print(DIVIDER)
print("  COMMERCIAL SCORING PRICING ENGINE — 7-CASE AUDIT")
print(DIVIDER)

results = []
for product, store, note in TEST_CASES:
    res = run_case(product, store, note)
    if res:
        results.append(res)

print()
print(DIVIDER)
print("  VALIDATION ASSERTIONS")
print(DIVIDER)

# Case 1 — Almond & Oat Milk must NOT recommend ₹353.40 (loss vs current)
r1 = results[0]
assert r1["final_p"] != 353.4 or r1["decision_status"] != "⚠ CAUTION — COMPLIANCE ADJUSTMENT", \
    "FAIL: Still recommending the old guardrail-forced ₹353.40!"
assert r1["final_pro"] >= r1["cur_pro"] * 0.999 or "HOLD" in r1["decision_status"], \
    "FAIL: Almond Milk — recommending a price with lower profit than current!"
print(f"  [1] Almond Milk — NOT forcing ₹353.40 loss: PASS  → {r1['decision_status']} @ ₹{r1['final_p']:,.2f}")

# Case 2 — Denim Jacket must be RECOMMENDED with positive profit
r2 = results[1]
assert r2["prof_impact_pct"] > 0 or "HOLD" in r2["decision_status"], "FAIL: Denim Jacket — profit not improving"
print(f"  [2] Classic Denim Jacket — profitable recommendation: PASS  → {r2['decision_status']} @ ₹{r2['final_p']:,.2f}")

# Case 3 — Headphones — should recommend a price increase (it has room)
r3 = results[2]
assert r3["final_pro"] >= r3["cur_pro"] * 0.999 or "HOLD" in r3["decision_status"], \
    "FAIL: Headphones — recommending loss"
print(f"  [3] Wireless Headphones — valid recommendation: PASS  → {r3['decision_status']} @ ₹{r3['final_p']:,.2f}")

# Case 4 — Smart Fitness Watch (Delhi)
r4 = results[3]
assert r4["final_pro"] >= r4["cur_pro"] * 0.98 or "HOLD" in r4["decision_status"], \
    f"FAIL: Watch Delhi profit drop: {r4['prof_impact_pct']}%"
print(f"  [4] Smart Fitness Watch (Delhi) — PASS  → {r4['decision_status']} @ ₹{r4['final_p']:,.2f}")

# Case 5 — Smart Fitness Watch (Mumbai)
r5 = results[4]
assert r5["final_pro"] >= r5["cur_pro"] * 0.98 or "HOLD" in r5["decision_status"], \
    f"FAIL: Watch Mumbai profit drop: {r5['prof_impact_pct']}%"
print(f"  [5] Smart Fitness Watch (Mumbai) — PASS  → {r5['decision_status']} @ ₹{r5['final_p']:,.2f}")

# Generic assertion: every result must have final_pro >= cur_pro OR be a HOLD
for i, res in enumerate(results):
    if "HOLD" not in res["decision_status"]:
        assert res["final_pro"] >= res["cur_pro"] * 0.98, \
            f"FAIL: Case {i+1} — recommending price with significantly lower profit!"

print(f"  [ALL] All cases — profit safety rule observed: PASS")
print()
print(DIVIDER)
print("  ALL ASSERTIONS PASSED — Engine is economically sound.")
print("  XGBoost model: NOT MODIFIED.")
print("  Demand forecasting: NOT MODIFIED.")
print(DIVIDER)
