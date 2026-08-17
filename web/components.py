"""
Shared Plotly layout and reusable component renderers.
"""

import plotly.graph_objects as go
import plotly.express as px

PALETTE = dict(
    blue="#3B82F6",
    purple="#8B5CF6",
    green="#22C55E",
    orange="#F59E0B",
    red="#EF4444",
    grey="#64748B",
    text="#F8FAFC",
    sub="#94A3B8",
    card="#111827",
    bg="#0B1120",
)

def dark_layout(height: int = 320, ytickformat: str = None, xtickformat: str = None) -> dict:
    """Returns a standardized dark-theme Plotly layout dict."""
    layout = dict(
        template="plotly_dark",
        height=height,
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        margin=dict(l=14, r=14, t=36, b=14),
        font=dict(family="Inter, sans-serif", size=12, color="#94A3B8"),
        title_font=dict(size=14, color="#CBD5E1", family="Inter, sans-serif"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=11, color="#94A3B8"),
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(bgcolor="#1E293B", font_size=12, font_family="Inter, sans-serif", font_color="#F8FAFC"),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False,
            tickfont=dict(size=11, color="#64748B"), linecolor="rgba(255,255,255,0.05)",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False,
            tickfont=dict(size=11, color="#64748B"), linecolor="rgba(255,255,255,0.05)",
        ),
    )
    if ytickformat:
        layout["yaxis"]["tickformat"] = ytickformat
    if xtickformat:
        layout["xaxis"]["tickformat"] = xtickformat
    return layout

def rec_hero_html(product, store, cur_p, comp_p, rec_p, p_chg,
                  exp_dem, exp_rev, exp_prof, rev_impact, prof_impact,
                  rev_label, prof_label, rev_cls, prof_cls, p_cls,
                  conf, decision_status, badge_cls, callout_cls,
                  price_hero_label, rationale,
                  econ_p=None, is_adjusted=False, econ_violation=""):
    """
    Renders the dominant pricing recommendation hero card.
    Strictly flush unindented to prevent markdown parser code-block escaping.
    """
    conf_badge = {
        "HIGH":   '<span class="badge-hi">● HIGH Confidence</span>',
        "MEDIUM": '<span class="badge-med">● MEDIUM Confidence</span>',
    }.get(conf, '<span class="badge-warn">● LOW Confidence</span>')

    decision_badge = f'<span class="{badge_cls}">{decision_status}</span>'

    # Secondary economic optimum note when adjusted
    econ_opt_section = ""
    if is_adjusted and econ_p is not None and abs(econ_p - rec_p) > 0.01:
        econ_opt_section = (
            f'<div style="display:flex; justify-content:space-between; align-items:center; '
            f'background:rgba(245,158,11,0.05); border:1px dashed rgba(245,158,11,0.25); '
            f'border-radius:8px; padding:6px 12px; margin:10px 0 4px 0; font-size:12px; color:#94A3B8;">'
            f'<span><b>Economic Optimal Price:</b> ₹{econ_p:,.2f}</span>'
            f'<span><b>Final Compliant Price:</b> ₹{rec_p:,.2f}</span>'
            f'<span style="color:#F59E0B;">(Adjusted for guardrail compliance)</span>'
            f'</div>'
        )

    # Build unindented HTML without blank lines to guarantee native HTML rendering in Streamlit
    html = (
        f'<div class="rec-card">'
        f'<div class="rec-card-header">'
        f'<div>'
        f'<div class="rec-product-title">🎯 {product}</div>'
        f'<div class="rec-product-sub">Retail Outlet: {store}</div>'
        f'</div>'
        f'<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">'
        f'{conf_badge}'
        f'{decision_badge}'
        f'</div>'
        f'</div>'
        f'<div class="price-row">'
        f'<div class="p-node">'
        f'<div class="p-node-label">Current Price</div>'
        f'<div class="p-node-val">₹{cur_p:,.2f}</div>'
        f'<div style="font-size:10px; color:#64748B; margin-top:3px;">Catalog Base</div>'
        f'</div>'
        f'<div class="p-node-hero">'
        f'<div class="p-node-label-hero">{price_hero_label}</div>'
        f'<div class="p-node-val-hero">₹{rec_p:,.2f}</div>'
        f'<div class="kpi-sub {p_cls}" style="font-size:12px; font-weight:700; margin-top:4px;">{p_chg:+.1f}% Price Change</div>'
        f'</div>'
        f'<div class="p-node">'
        f'<div class="p-node-label">Competitor Price</div>'
        f'<div class="p-node-val">₹{comp_p:,.2f}</div>'
        f'<div style="font-size:10px; color:#64748B; margin-top:3px;">Market Benchmark</div>'
        f'</div>'
        f'</div>'
        f'{econ_opt_section}'
        f'<div class="outcome-row">'
        f'<div class="out-cell">'
        f'<div class="out-label">Expected Demand</div>'
        f'<div class="out-val">{exp_dem:.0f}</div>'
        f'<div class="out-sub muted">units / day</div>'
        f'</div>'
        f'<div class="out-cell">'
        f'<div class="out-label">Expected Revenue</div>'
        f'<div class="out-val">₹{exp_rev/1000:,.1f}K</div>'
        f'<div class="out-sub {rev_cls}">{rev_impact:+.2f}% {rev_label}</div>'
        f'</div>'
        f'<div class="out-cell">'
        f'<div class="out-label">Expected Profit</div>'
        f'<div class="out-val">₹{exp_prof/1000:,.1f}K</div>'
        f'<div class="out-sub {prof_cls}">{prof_impact:+.2f}% {prof_label}</div>'
        f'</div>'
        f'<div class="out-cell">'
        f'<div class="out-label">{prof_label}</div>'
        f'<div class="out-val {prof_cls}">{prof_impact:+.1f}%</div>'
        f'<div class="out-sub muted">vs Baseline</div>'
        f'</div>'
        f'</div>'
        f'<div class="{callout_cls}">'
        f'<b>Decision:</b> {rationale}'
        f'</div>'
        f'</div>'
    )
    return html


def overview_hero_html(total_revenue_cr: float = 0.0) -> str:
    """
    Renders the premium glassmorphism two-column hero for the Overview page.
    Left: headline text + status pill.
    Right: animated orbs + glass card with DP icon mark and live revenue stat.

    Args:
        total_revenue_cr: Portfolio revenue in Crores (e.g. 6.18)
    """
    rev_str = f"₹{total_revenue_cr:,.2f} Cr"
    return (
        '<div class="hero-row">'

        # ── Left column ────────────────────────────────────
        '<div class="hero-left">'
        '<div class="hero-eyebrow">Revenue Intelligence Platform</div>'
        '<div class="hero-title">Dynamic Pricing</div>'
        '<div class="hero-subtitle">Revenue Intelligence</div>'
        '<div class="hero-desc">'
        'Understand sales, demand, and pricing opportunities at a glance. '
        'Powered by XGBoost demand forecasting and econometric price optimization '
        'with live guardrail enforcement.'
        '</div>'
        '<div class="hero-pill">'
        '<span class="hero-pill-dot"></span>'
        'XGBoost &nbsp;·&nbsp; 89.3% Accuracy &nbsp;·&nbsp; Guardrails Active'
        '</div>'
        '</div>'

        # ── Right column — visual scene ────────────────────
        '<div class="hero-right">'
        '<div class="hero-visual">'

        # Background orbs
        '<div class="orb orb-teal"></div>'
        '<div class="orb orb-blue"></div>'

        # Glass card
        '<div class="glass-card">'

        # DP icon mark
        '<div class="dp-icon">DP</div>'

        '<div class="gc-eyebrow">Dynamic Pricing</div>'
        '<div class="gc-title">Revenue Intelligence</div>'
        '<div class="gc-sub">AI-Driven Price Optimization</div>'

        '<hr class="gc-divider">'

        '<div class="gc-stat-row">'
        '<span class="gc-stat-label">↑ Portfolio Revenue</span>'
        f'<span class="gc-stat-val">{rev_str}</span>'
        '</div>'

        '</div>'   # .glass-card
        '</div>'   # .hero-visual
        '</div>'   # .hero-right

        '</div>'   # .hero-row
    )
