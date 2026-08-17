"""
Dynamic Pricing & Revenue Intelligence System
Premium Dark SaaS — 5-Page Business Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dynamic Pricing Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

from web.styles import get_css, header, kpi, footer
from web.components import dark_layout, rec_hero_html, overview_hero_html, PALETTE
from web.data_loader import (
    load_master_data, load_recommendations, load_simulation_grid,
    load_forecast_results, load_model_metrics, load_feature_importance,
    load_ml_pipeline
)
from web.pricing_service import (
    evaluate_guardrails, simulate_interactive_price,
    format_dynamic_rationale, compute_lift_metrics, determine_decision_status,
    analyze_pricing_recommendation
)
from web.forecast_service import filter_forecast_data

st.markdown(get_css(), unsafe_allow_html=True)

# ── Cached data loads ─────────────────────────────────
df        = load_master_data()
df_recs   = load_recommendations()
df_grid   = load_simulation_grid()
df_fc     = load_forecast_results()
df_met    = load_model_metrics()
df_feat   = load_feature_importance()
model, preprocessor, df_elas = load_ml_pipeline()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📈 Dynamic Pricing")
    st.markdown("<p style='font-size:12px;color:#475569;margin:-8px 0 14px 0;'>Revenue Intelligence</p>", unsafe_allow_html=True)

    page = st.radio("nav", [
        "Overview",
        "Sales Performance",
        "Demand Forecast",
        "Pricing Recommendation",
        "What-If Simulator",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px;color:#334155;'>"
        "Model: <b style='color:#8B5CF6;'>XGBoost</b><br>"
        "Accuracy: <b style='color:#22C55E;'>89.3%</b><br>"
        "Guardrails: <b style='color:#22C55E;'>Active</b></div>",
        unsafe_allow_html=True
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║  PAGE 1 — OVERVIEW                                           ║
# ╚══════════════════════════════════════════════════════════════╝
if page == "Overview":
    # Pre-compute totals needed for hero stat
    tot_rev   = df["Revenue"].sum()
    tot_units = df["Units_Sold"].sum()
    tot_cost  = df["Total_Cost"].sum()
    tot_prof  = tot_rev - tot_cost
    margin    = (tot_prof / tot_rev * 100) if tot_rev else 0
    asp       = (tot_rev / tot_units) if tot_units else 0

    # Premium glassmorphism hero visual
    st.markdown(overview_hero_html(total_revenue_cr=tot_rev / 1e7), unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(kpi("Total Revenue",    f"₹{tot_rev/1e7:,.2f} Cr", "Portfolio Sales",      "pos"),  unsafe_allow_html=True)
    k2.markdown(kpi("Units Sold",       f"{tot_units/1e6:,.2f}M",  "Total Volume",          "muted"), unsafe_allow_html=True)
    k3.markdown(kpi("Gross Profit",     f"₹{tot_prof/1e7:,.2f} Cr","Realized Margin",      "pos"),  unsafe_allow_html=True)
    k4.markdown(kpi("Gross Margin",     f"{margin:.1f}%",           "Margin Health",        "pos"),  unsafe_allow_html=True)
    k5.markdown(kpi("Avg Selling Price",f"₹{asp:,.2f}",             "Effective ASP",        "muted"), unsafe_allow_html=True)

    # Two trend charts
    c1, c2 = st.columns(2)
    with c1:
        daily = df.groupby("Date")["Revenue"].sum().reset_index()
        fig = go.Figure(go.Scatter(
            x=daily["Date"], y=daily["Revenue"],
            mode="lines", fill="tozeroy",
            line=dict(color=PALETTE["blue"], width=2),
            fillcolor="rgba(59,130,246,0.08)",
            hovertemplate="₹%{y:,.2f}<extra></extra>"
        ))
        fig.update_layout(**dark_layout(300), title="Revenue Trend")
        fig.update_yaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        daily_u = df.groupby("Date")["Units_Sold"].sum().reset_index()
        fig2 = go.Figure(go.Scatter(
            x=daily_u["Date"], y=daily_u["Units_Sold"],
            mode="lines", fill="tozeroy",
            line=dict(color=PALETTE["purple"], width=2),
            fillcolor="rgba(139,92,246,0.08)",
            hovertemplate="%{y:,.0f} units<extra></extra>"
        ))
        fig2.update_layout(**dark_layout(300), title="Units Sold Trend")
        st.plotly_chart(fig2, use_container_width=True)

    # Lower section
    c3, c4 = st.columns(2)
    with c3:
        cat_df = df.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue")
        fig3 = go.Figure(go.Bar(
            y=cat_df["Category"], x=cat_df["Revenue"],
            orientation="h", marker_color=PALETTE["blue"],
            hovertemplate="₹%{x:,.2f}<extra>%{y}</extra>"
        ))
        fig3.update_layout(**dark_layout(260, xtickformat="~s"), title="Revenue by Category")
        fig3.update_xaxes(tickprefix="₹")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        top5 = df.groupby("Product_Name")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(5)
        fig4 = go.Figure(go.Bar(
            y=top5["Product_Name"], x=top5["Revenue"],
            orientation="h", marker_color=PALETTE["purple"],
            hovertemplate="₹%{x:,.2f}<extra>%{y}</extra>"
        ))
        fig4.update_layout(**dark_layout(260, xtickformat="~s"), title="Top 5 Products by Revenue")
        fig4.update_xaxes(tickprefix="₹")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown(footer(), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  PAGE 2 — SALES PERFORMANCE                                  ║
# ╚══════════════════════════════════════════════════════════════╝
elif page == "Sales Performance":
    st.markdown(header(
        "Sales Performance",
        "Track revenue, volume and product performance across your business."
    ), unsafe_allow_html=True)

    # Compact filter row
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        sel_cat = st.selectbox("Category", ["All"] + sorted(df["Category"].unique().tolist()), key="sp_c")
    with f2:
        sel_reg = st.selectbox("Region",   ["All"] + sorted(df["Region"].unique().tolist()), key="sp_r")
    with f3:
        sel_sto = st.selectbox("Store",    ["All"] + sorted(df["Store_Name"].unique().tolist()), key="sp_s")
    with f4:
        min_d, max_d = df["Date"].min().to_pydatetime(), df["Date"].max().to_pydatetime()
        sel_dt = st.date_input("Date Range", [min_d, max_d], key="sp_d")

    fd = df.copy()
    if sel_cat != "All": fd = fd[fd["Category"] == sel_cat]
    if sel_reg != "All": fd = fd[fd["Region"]   == sel_reg]
    if sel_sto != "All": fd = fd[fd["Store_Name"]== sel_sto]
    if isinstance(sel_dt, (list, tuple)) and len(sel_dt) == 2:
        fd = fd[(fd["Date"] >= pd.to_datetime(sel_dt[0])) & (fd["Date"] <= pd.to_datetime(sel_dt[1]))]

    if len(fd) == 0:
        st.warning("No data for the selected filters.")
        st.stop()

    frev   = fd["Revenue"].sum()
    funits = fd["Units_Sold"].sum()
    fprof  = frev - fd["Total_Cost"].sum()
    fmarg  = (fprof / frev * 100) if frev else 0
    fasp   = frev / funits if funits else 0
    f_tcat = fd.groupby("Category")["Revenue"].sum().idxmax()

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.markdown(kpi("Revenue",     f"₹{frev/1e7:,.2f} Cr",     "Total Sales",   "pos"),  unsafe_allow_html=True)
    k2.markdown(kpi("Units Sold",  f"{funits/1e6:,.2f}M",       "Volume",        "muted"),unsafe_allow_html=True)
    k3.markdown(kpi("Gross Profit",f"₹{fprof/1e7:,.2f} Cr",     "Margin ₹",     "pos"),  unsafe_allow_html=True)
    k4.markdown(kpi("Margin %",    f"{fmarg:.1f}%",             "Profit Rate",   "pos"),  unsafe_allow_html=True)
    k5.markdown(kpi("Avg Price",   f"₹{fasp:,.2f}",             "Effective ASP","muted"), unsafe_allow_html=True)
    k6.markdown(kpi("Top Category",f_tcat,                      "By Revenue",   "muted"), unsafe_allow_html=True)

    # Row 2: Revenue trend + Units trend
    r2a, r2b = st.columns(2)
    with r2a:
        dr = fd.groupby("Date")["Revenue"].sum().reset_index()
        fig_r = go.Figure(go.Scatter(
            x=dr["Date"], y=dr["Revenue"], mode="lines", fill="tozeroy",
            line=dict(color=PALETTE["blue"], width=2), fillcolor="rgba(59,130,246,0.08)",
            hovertemplate="₹%{y:,.2f}<extra></extra>"
        ))
        fig_r.update_layout(**dark_layout(280), title="Revenue Trend")
        fig_r.update_yaxes(tickprefix="₹", tickformat="~s")
        st.plotly_chart(fig_r, use_container_width=True)

    with r2b:
        du = fd.groupby("Date")["Units_Sold"].sum().reset_index()
        fig_u = go.Figure(go.Scatter(
            x=du["Date"], y=du["Units_Sold"], mode="lines", fill="tozeroy",
            line=dict(color=PALETTE["purple"], width=2), fillcolor="rgba(139,92,246,0.08)",
            hovertemplate="%{y:,.0f} units<extra></extra>"
        ))
        fig_u.update_layout(**dark_layout(280), title="Units Sold Trend")
        st.plotly_chart(fig_u, use_container_width=True)

    # Row 3: Category + Top Products
    r3a, r3b = st.columns(2)
    with r3a:
        cp = fd.groupby("Category").agg(Revenue=("Revenue","sum"), Units=("Units_Sold","sum")).reset_index().sort_values("Revenue")
        fig_cat = go.Figure(go.Bar(
            y=cp["Category"], x=cp["Revenue"], orientation="h",
            marker_color=PALETTE["green"],
            customdata=cp["Units"],
            hovertemplate="Revenue: ₹%{x:,.2f}<br>Units: %{customdata:,.0f}<extra>%{y}</extra>"
        ))
        fig_cat.update_layout(**dark_layout(280, xtickformat="~s"), title="Category Performance")
        fig_cat.update_xaxes(tickprefix="₹")
        st.plotly_chart(fig_cat, use_container_width=True)

    with r3b:
        tp = fd.groupby("Product_Name").agg(Revenue=("Revenue","sum"), Units=("Units_Sold","sum"), Profit=("Gross_Profit","sum")).reset_index().sort_values("Revenue", ascending=False).head(10)
        fig_tp = go.Figure(go.Bar(
            y=tp["Product_Name"], x=tp["Revenue"], orientation="h",
            marker_color=PALETTE["blue"],
            customdata=np.stack([tp["Units"], tp["Profit"]], axis=-1),
            hovertemplate="Revenue: ₹%{x:,.2f}<br>Units: %{customdata[0]:,.0f}<br>Profit: ₹%{customdata[1]:,.2f}<extra>%{y}</extra>"
        ))
        fig_tp.update_layout(**dark_layout(280, xtickformat="~s"), title="Top 10 Products by Revenue")
        fig_tp.update_xaxes(tickprefix="₹")
        st.plotly_chart(fig_tp, use_container_width=True)

    # Row 4: Store performance
    sp = fd.groupby("Store_Name").agg(Revenue=("Revenue","sum"), Units=("Units_Sold","sum")).reset_index().sort_values("Revenue", ascending=False)
    fig_sp = go.Figure(go.Bar(
        x=sp["Store_Name"], y=sp["Revenue"],
        marker_color=PALETTE["purple"],
        customdata=sp["Units"],
        hovertemplate="₹%{y:,.2f}<br>Units: %{customdata:,.0f}<extra>%{x}</extra>"
    ))
    fig_sp.update_layout(**dark_layout(250, ytickformat="~s"), title="Store Performance")
    fig_sp.update_yaxes(tickprefix="₹")
    st.plotly_chart(fig_sp, use_container_width=True)

    # Key Insights
    top_cat  = fd.groupby("Category")["Revenue"].sum().idxmax()
    top_prod = fd.groupby("Product_Name")["Revenue"].sum().idxmax()
    top_sto  = fd.groupby("Store_Name")["Revenue"].sum().idxmax()
    top_cat_pct = (fd.groupby("Category")["Revenue"].sum().max() / frev * 100) if frev else 0

    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Key Sales Insights</div>
        <div class="insight-item">• <b>{top_cat}</b> generated the highest revenue, contributing <b>{top_cat_pct:.1f}%</b> of total sales.</div>
        <div class="insight-item">• <b>{top_prod}</b> is the top-performing product across all stores.</div>
        <div class="insight-item">• <b>{top_sto}</b> is the strongest-performing retail outlet by revenue.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  PAGE 3 — DEMAND FORECAST                                    ║
# ╚══════════════════════════════════════════════════════════════╝
elif page == "Demand Forecast":
    st.markdown(header(
        "Demand Forecast",
        "How much demand should I expect?"
    ), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        prods = sorted(df_recs["Product_Name"].unique().tolist()) if len(df_recs) else []
        d_prod = st.selectbox("Product", prods, key="df_p")
    with c2:
        stopts = sorted(df_recs[df_recs["Product_Name"] == d_prod]["Store_Name"].unique().tolist()) if d_prod else []
        d_sto  = st.selectbox("Store", stopts, key="df_s")

    sku_r  = df_recs[(df_recs["Product_Name"] == d_prod) & (df_recs["Store_Name"] == d_sto)]
    exp_dem = float(sku_r.iloc[0].get("Recommended_Predicted_Demand", 75)) if len(sku_r) else 75
    p_id   = sku_r.iloc[0]["Product_ID"] if len(sku_r) else None
    s_id   = sku_r.iloc[0]["Store_ID"]   if len(sku_r) else None

    k1, k2, k3 = st.columns(3)
    k1.markdown(kpi("Forecast Daily Demand", f"{exp_dem:.0f} units", "Expected Volume / Day", "pos"), unsafe_allow_html=True)
    k2.markdown(kpi("Forecast Accuracy",     "89.3%",                "Model Reliability",     "pos"), unsafe_allow_html=True)
    k3.markdown(kpi("Error Rate (WAPE)",     "10.66%",               "Low Uncertainty",       "muted"), unsafe_allow_html=True)

    # Main chart
    fc_sub = filter_forecast_data(df_fc, product_id=p_id, store_id=s_id) if p_id else df_fc.head(0)
    if len(fc_sub) > 0:
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(
            x=fc_sub["Date"], y=fc_sub["Actual_Demand"],
            mode="lines", name="Actual Demand",
            line=dict(color=PALETTE["grey"], width=1.8),
            hovertemplate="%{y:.0f} units<extra>Actual</extra>"
        ))
        fig_fc.add_trace(go.Scatter(
            x=fc_sub["Date"], y=fc_sub["Forecast_XGBoost"],
            mode="lines", name="XGBoost Forecast",
            line=dict(color=PALETTE["blue"], width=2, dash="dash"),
            hovertemplate="%{y:.0f} units<extra>Forecast</extra>"
        ))
        fig_fc.update_layout(**dark_layout(360), title=f"Actual vs Predicted Demand — {d_prod}")
        fig_fc.update_yaxes(title_text="Units / Day")
        st.plotly_chart(fig_fc, use_container_width=True)

    # Advanced technical details hidden by default
    with st.expander("🔬 Advanced Model Details", expanded=False):
        k4, k5, k6, k7 = st.columns(4)
        k4.markdown(kpi("R²",   "0.9223", "Explanatory Power", "pos"),  unsafe_allow_html=True)
        k5.markdown(kpi("MAE",  "11.24",  "Mean Abs Error",    "muted"),unsafe_allow_html=True)
        k6.markdown(kpi("RMSE", "16.08",  "RMS Error",         "muted"),unsafe_allow_html=True)
        k7.markdown(kpi("R²",   "0.9223", "Variance Explained","pos"),  unsafe_allow_html=True)
        if len(df_met) > 0:
            st.dataframe(df_met, height=160, use_container_width=True)

    st.markdown(footer(), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  PAGE 4 — PRICING RECOMMENDATION                            ║
# ╚══════════════════════════════════════════════════════════════╝
elif page == "Pricing Recommendation":
    # Header + selectors in same row
    hc, sc1, sc2 = st.columns([2.5, 1, 1])
    with hc:
        st.markdown(header(
            "Pricing Recommendation",
            "Find the price that maximizes expected business value."
        ), unsafe_allow_html=True)
    with sc1:
        p_list = sorted(df_recs["Product_Name"].unique().tolist()) if len(df_recs) else []
        sel_p  = st.selectbox("Product", p_list, key="pr_p")
    with sc2:
        s_list = sorted(df_recs[df_recs["Product_Name"] == sel_p]["Store_Name"].unique().tolist()) if sel_p else []
        sel_s  = st.selectbox("Store", s_list, key="pr_s")

    sku = df_recs[(df_recs["Product_Name"] == sel_p) & (df_recs["Store_Name"] == sel_s)]
    if len(sku) > 0:
        r = sku.iloc[0]
        pid = r["Product_ID"]
        sid = r["Store_ID"]
        cdf = df_grid[(df_grid["Product_ID"] == pid) & (df_grid["Store_ID"] == sid)].sort_values("Candidate_Price")

        # Commercial scoring engine: profit-primary, competitor as soft penalty
        res = analyze_pricing_recommendation(cdf, r)

        cur_p    = res["cur_p"]
        comp_p   = res["comp_p"]
        final_p  = res["final_p"]
        final_dem= res["final_dem"]
        final_rev= res["final_rev"]
        final_pro= res["final_pro"]
        p_chg    = res["price_change_pct"]
        rev_lft  = res["rev_impact_pct"]
        prof_lft = res["prof_impact_pct"]
        conf     = str(r.get("Confidence_Level", "HIGH"))

        # Recommendation hero card
        st.markdown(rec_hero_html(
            product=sel_p, store=sel_s,
            cur_p=cur_p, comp_p=comp_p, rec_p=final_p, p_chg=p_chg,
            exp_dem=final_dem, exp_rev=final_rev, exp_prof=final_pro,
            rev_impact=rev_lft, prof_impact=prof_lft,
            rev_label=res["rev_label"], prof_label=res["prof_label"],
            rev_cls=res["rev_cls"], prof_cls=res["prof_cls"], p_cls=res["price_cls"],
            conf=conf, decision_status=res["decision_status"],
            badge_cls=res["badge_cls"], callout_cls=res["callout_cls"],
            price_hero_label=res["price_hero_label"],
            rationale=res["rationale"],
            econ_p=res["econ_p"], is_adjusted=res["is_adjusted"],
            econ_violation="; ".join(res["econ_violations"])
        ), unsafe_allow_html=True)

        # "Why this price?" inline expander
        why = res.get("why", {})
        if why:
            with st.expander("💡 Why this price?", expanded=False):
                wa, wb, wc, wd, we = st.columns(5)
                def _sign_cls(v): return "pos" if v > 0.005 else ("neg" if v < -0.005 else "muted")
                wa.markdown(kpi("Price Change",   f"{why.get('price_change_pct',0):+.1f}%",  "", _sign_cls(why.get('price_change_pct',0))),  unsafe_allow_html=True)
                wb.markdown(kpi("Demand Change",  f"{why.get('demand_change_pct',0):+.1f}%", "", _sign_cls(why.get('demand_change_pct',0))),  unsafe_allow_html=True)
                wc.markdown(kpi("Revenue Impact", f"{why.get('rev_impact_pct',0):+.1f}%",    "", _sign_cls(why.get('rev_impact_pct',0))),     unsafe_allow_html=True)
                wd.markdown(kpi("Profit Impact",  f"{why.get('prof_impact_pct',0):+.1f}%",   "", _sign_cls(why.get('prof_impact_pct',0))),    unsafe_allow_html=True)
                we.markdown(kpi("Competitor Gap", f"{why.get('comp_gap_pct',0):+.1f}%",      "", "muted"),                                    unsafe_allow_html=True)
                callout_style = res["callout_cls"]
                st.markdown(
                    f'<div class="{callout_style}" style="margin-top:10px;">'
                    f'<b>Decision Logic:</b> {why.get("explanation", res["rationale"])}'
                    f'</div>', unsafe_allow_html=True
                )

        # Sensitivity charts — Revenue and Profit curves with markers
        if len(cdf) > 0:
            ch1, ch2 = st.columns(2)
            with ch1:
                fig_rev = go.Figure()
                fig_rev.add_trace(go.Scatter(
                    x=cdf["Candidate_Price"], y=cdf["Expected_Revenue"],
                    mode="lines", name="Expected Revenue",
                    line=dict(color=PALETTE["blue"], width=2),
                    hovertemplate="₹%{x:,.2f} → ₹%{y:,.2f}<extra></extra>"
                ))
                fig_rev.add_trace(go.Scatter(
                    x=[cur_p], y=[res["cur_rev"]], mode="markers",
                    name="Current Price", marker=dict(size=10, color=PALETTE["orange"], symbol="circle")
                ))
                fig_rev.add_trace(go.Scatter(
                    x=[final_p], y=[final_rev], mode="markers",
                    name=res["price_hero_label"], marker=dict(size=13, color=PALETTE["green"], symbol="star")
                ))
                fig_rev.add_vline(x=cur_p, line_dash="dot", line_color="rgba(245,158,11,0.4)", annotation_text="Current", annotation_font_color=PALETTE["orange"])
                if abs(final_p - cur_p) > 0.5:
                    fig_rev.add_vline(x=final_p, line_dash="dot", line_color="rgba(34,197,94,0.4)", annotation_text="Recommended", annotation_font_color=PALETTE["green"])
                fig_rev.update_layout(**dark_layout(300), title="Price vs Expected Revenue")
                fig_rev.update_xaxes(tickprefix="₹", tickformat="~s")
                fig_rev.update_yaxes(tickprefix="₹", tickformat="~s")
                st.plotly_chart(fig_rev, use_container_width=True)

            with ch2:
                fig_pro = go.Figure()
                fig_pro.add_trace(go.Scatter(
                    x=cdf["Candidate_Price"], y=cdf["Expected_Profit"],
                    mode="lines", name="Expected Profit",
                    line=dict(color=PALETTE["purple"], width=2),
                    hovertemplate="₹%{x:,.2f} → ₹%{y:,.2f}<extra></extra>"
                ))
                fig_pro.add_trace(go.Scatter(
                    x=[cur_p], y=[res["cur_pro"]], mode="markers",
                    name="Current Price", marker=dict(size=10, color=PALETTE["orange"], symbol="circle")
                ))
                fig_pro.add_trace(go.Scatter(
                    x=[final_p], y=[final_pro], mode="markers",
                    name=res["price_hero_label"], marker=dict(size=13, color=PALETTE["green"], symbol="star")
                ))
                fig_pro.add_vline(x=cur_p, line_dash="dot", line_color="rgba(245,158,11,0.4)", annotation_text="Current", annotation_font_color=PALETTE["orange"])
                if abs(final_p - cur_p) > 0.5:
                    fig_pro.add_vline(x=final_p, line_dash="dot", line_color="rgba(34,197,94,0.4)", annotation_text="Recommended", annotation_font_color=PALETTE["green"])
                fig_pro.update_layout(**dark_layout(300), title="Price vs Expected Profit")
                fig_pro.update_xaxes(tickprefix="₹", tickformat="~s")
                fig_pro.update_yaxes(tickprefix="₹", tickformat="~s")
                st.plotly_chart(fig_pro, use_container_width=True)


        # Optional collapsible full table
        with st.expander("📋 View All Recommendations", expanded=False):
            cols = ["Product_Name","Store_Name","Current_Price","Competitor_Price",
                    "Recommended_Price","Price_Change_Percent","Revenue_Improvement_Percent","Confidence_Level"]
            disp = df_recs[[c for c in cols if c in df_recs.columns]].copy()
            disp.columns = [c.replace("_"," ").title() for c in disp.columns]
            st.dataframe(disp, height=260, use_container_width=True)

    st.markdown(footer(), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  PAGE 5 — WHAT-IF SIMULATOR                                  ║
# ╚══════════════════════════════════════════════════════════════╝
elif page == "What-If Simulator":
    st.markdown(header(
        "What-If Simulator",
        "What happens if I change my price?"
    ), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        p_opts = sorted(df_recs["Product_Name"].unique().tolist()) if len(df_recs) else []
        wif_p  = st.selectbox("Product", p_opts, key="wi_p")
    with c2:
        s_opts = sorted(df_recs[df_recs["Product_Name"] == wif_p]["Store_Name"].unique().tolist()) if wif_p else []
        wif_s  = st.selectbox("Store", s_opts, key="wi_s")

    sku = df_recs[(df_recs["Product_Name"] == wif_p) & (df_recs["Store_Name"] == wif_s)]
    if len(sku) == 0:
        st.info("No data for this selection.")
        st.stop()

    base = sku.iloc[0]
    cur_p  = float(base["Current_Price"])
    comp_p = float(base["Competitor_Price"])
    cost_u = float(base["Unit_Cost"])
    p_id   = base["Product_ID"]
    s_id   = base["Store_ID"]

    # Price Change slider
    st.markdown("<p style='font-size:13px;font-weight:600;color:#CBD5E1;margin:10px 0 2px;'>PRICE CHANGE (%)</p>", unsafe_allow_html=True)
    adj = st.slider("adj", -15, 15, 0, 1, format="%+d%%", label_visibility="collapsed")

    sim_price = round(cur_p * (1 + adj / 100), 2)
    comp_gap  = ((sim_price - comp_p) / comp_p * 100) if comp_p else 0

    # Lookup grid first, else simulate
    gpt = df_grid[(df_grid["Product_ID"] == p_id) & (df_grid["Store_ID"] == s_id) & (df_grid["Price_Adjustment_Percent"] == adj)]
    if len(gpt) > 0:
        sim_dem = float(gpt.iloc[0]["Predicted_Demand"])
        sim_rev = float(gpt.iloc[0]["Expected_Revenue"])
        sim_pro = float(gpt.iloc[0]["Expected_Profit"])
    else:
        last_row = df[(df["Product_ID"] == p_id) & (df["Store_ID"] == s_id)].sort_values("Date").iloc[[-1]]
        out = simulate_interactive_price(last_row, sim_price, model, preprocessor, cost_u)
        sim_dem = out["predicted_demand"]
        sim_rev = out["expected_revenue"]
        sim_pro = out["expected_profit"]

    cur_base_dem = float(base.get("Current_Predicted_Demand", 50.0))
    base_rev = float(base.get("Current_Expected_Revenue", cur_p * cur_base_dem))
    base_pro = float(base.get("Current_Expected_Profit", (cur_p - cost_u) * cur_base_dem))
    r_delta  = ((sim_rev - base_rev) / (base_rev + 1e-9)) * 100.0 if base_rev > 0 else 0.0
    p_delta  = ((sim_pro - base_pro) / (abs(base_pro) + 1e-9)) * 100.0 if base_pro != 0 else 0.0

    # 4 KPI cards
    k1, k2, k3, k4 = st.columns(4)
    price_dir = "pos" if adj >= 0 else "neg"
    k1.markdown(kpi("New Price",        f"₹{sim_price:,.2f}",     f"{adj:+d}% vs ₹{cur_p:,.0f}",  price_dir), unsafe_allow_html=True)
    k2.markdown(kpi("Expected Demand",  f"{sim_dem:.0f} units",   "Projected Volume",               "muted"),  unsafe_allow_html=True)
    k3.markdown(kpi("Expected Revenue", f"₹{sim_rev/1000:,.1f}K", f"{r_delta:+.2f}% Impact",  "pos" if r_delta >= 0 else "neg"), unsafe_allow_html=True)
    k4.markdown(kpi("Expected Profit",  f"₹{sim_pro/1000:,.1f}K", f"{p_delta:+.2f}% Impact",  "pos" if p_delta >= 0 else "neg"), unsafe_allow_html=True)

    # Guardrail evaluation
    g_inc  = adj  <= 10.0
    g_dec  = adj  >= -10.0
    g_comp = comp_gap <= 5.0
    g_dem  = sim_dem  >= 5.0
    g_cost = sim_price >= cost_u
    n_fail = sum([not g_inc, not g_dec, not g_comp, not g_dem, not g_cost])

    if n_fail == 0:
        st.markdown(f'<div class="banner-safe">✓ SAFE TO APPLY &nbsp;·&nbsp; Revenue Impact: {r_delta:+.2f}% &nbsp;·&nbsp; Profit Impact: {p_delta:+.2f}%</div>', unsafe_allow_html=True)
    elif n_fail <= 2:
        st.markdown(f'<div class="banner-warn">⚠ REVIEW RECOMMENDATION &nbsp;·&nbsp; {n_fail} guardrail(s) breached</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="banner-err">✕ GUARDRAIL VIOLATION &nbsp;·&nbsp; {n_fail} constraints exceeded — not recommended</div>', unsafe_allow_html=True)

    # 2 charts
    sc = df_grid[(df_grid["Product_ID"] == p_id) & (df_grid["Store_ID"] == s_id)].sort_values("Candidate_Price")
    if len(sc) > 0:
        ch1, ch2 = st.columns(2)
        with ch1:
            fig_wr = go.Figure()
            fig_wr.add_trace(go.Scatter(
                x=sc["Candidate_Price"], y=sc["Expected_Revenue"],
                mode="lines", name="Revenue",
                line=dict(color=PALETTE["blue"], width=2), fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"
            ))
            fig_wr.add_vline(x=sim_price, line_dash="dot", line_color=PALETTE["purple"],
                              annotation_text=f"₹{sim_price:,.0f}", annotation_font_color=PALETTE["purple"])
            fig_wr.update_layout(**dark_layout(300), title="Price vs Expected Revenue")
            fig_wr.update_xaxes(tickprefix="₹", tickformat="~s")
            fig_wr.update_yaxes(tickprefix="₹", tickformat="~s")
            st.plotly_chart(fig_wr, use_container_width=True)

        with ch2:
            fig_wd = go.Figure()
            fig_wd.add_trace(go.Scatter(
                x=sc["Candidate_Price"], y=sc["Predicted_Demand"],
                mode="lines", name="Demand",
                line=dict(color=PALETTE["purple"], width=2), fill="tozeroy", fillcolor="rgba(139,92,246,0.06)"
            ))
            fig_wd.add_vline(x=sim_price, line_dash="dot", line_color=PALETTE["blue"],
                              annotation_text=f"₹{sim_price:,.0f}", annotation_font_color=PALETTE["blue"])
            fig_wd.update_layout(**dark_layout(300), title="Price vs Predicted Demand")
            fig_wd.update_xaxes(tickprefix="₹", tickformat="~s")
            fig_wd.update_yaxes(title_text="Units / Day")
            st.plotly_chart(fig_wd, use_container_width=True)

    st.markdown(footer(), unsafe_allow_html=True)
