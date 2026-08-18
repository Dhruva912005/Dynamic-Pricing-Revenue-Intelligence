"""
Premium Dark SaaS CSS Design System
Dynamic Pricing & Revenue Intelligence Platform

Key Design Principles:
1. Material Symbols / Icon Font Protection:
   Never override font-family globally with !important on span/div/* which destroys
   Streamlit's internal Material Icons (preventing raw ligature text like
   'keyboard_double_arrow_right' or '_arrow_right' from leaking into the UI).
2. Clean Flexbox/Grid Layouts:
   Zero negative margins, responsive grid wrappers with media queries for 
   Desktop (1920-1280px), Tablet (1024-768px), and Mobile (<768px).
3. Section Headings & Emojis:
   All headers and expanders use inline-flex alignment with explicit gaps so icons
   never sit on top of or collide with text.
4. Tables & Overflow:
   Responsive tables with overflow-x: auto and clean container bounding.
"""

def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Global Typography & Background ───────────────── */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #0B1120 !important;
        color: #F8FAFC;
        line-height: 1.5;
        letter-spacing: normal;
    }

    /* ── Protect Streamlit Material Icons & Ligatures ─── */
    /* Streamlit uses Google Material Symbols/Icons for expanders, sidebar buttons, etc. */
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] button,
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [class*="material-symbols"],
    [class*="material-icons"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* ── Main Canvas Padding & Responsive Sizing ──────── */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
    }

    /* ── Sidebar Layout & Branding ────────────────────── */
    [data-testid="stSidebar"] {
        background: #070D1A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: #070D1A !important;
        padding: 1.5rem 1rem !important;
    }

    /* Sidebar Brand Section */
    .sidebar-brand {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .sidebar-title {
        font-size: 16px;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 8px;
        line-height: 1.3;
    }
    .sidebar-sub {
        font-size: 12px;
        font-weight: 500;
        color: #64748B;
        line-height: 1.3;
    }

    /* Sidebar Navigation Radios */
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(139, 92, 246, 0.12) !important;
        color: #C4B5FD !important;
        border-color: rgba(139, 92, 246, 0.25) !important;
    }
    [data-testid="stSidebar"] .stRadio > div [aria-checked="true"] + label,
    [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
        background: rgba(139, 92, 246, 0.20) !important;
        color: #A78BFA !important;
        font-weight: 600 !important;
        border-color: rgba(139, 92, 246, 0.40) !important;
    }

    /* ── Dropdown / Selectbox / Inputs Dark Theme ──────── */
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        min-height: 40px !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(139, 92, 246, 0.50) !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input {
        color: #F8FAFC !important;
        font-size: 13px !important;
    }

    /* Popover Menu Portal */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #111827 !important;
    }
    li[role="option"],
    div[role="option"] {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background-color: #1E293B !important;
        color: #C4B5FD !important;
    }

    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label {
        color: #94A3B8 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        margin-bottom: 4px !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    .stTextInput input,
    .stDateInput input {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-size: 13px !important;
    }

    /* ── Streamlit Expander Standardized ──────────────── */
    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] summary {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        color: #CBD5E1 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        line-height: 1.4 !important;
    }
    [data-testid="stExpander"] summary:hover {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #F8FAFC !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #8B5CF6 !important;
        font-size: 18px !important;
        flex-shrink: 0 !important;
        margin-right: 4px !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding: 14px 16px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* ── DataFrames & Tables ───────────────────────────── */
    .stDataFrame {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    .stDataFrame table {
        background: #111827 !important;
        width: 100% !important;
    }
    .stDataFrame th {
        background: #151E2E !important;
        color: #94A3B8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 10px 12px !important;
    }
    .stDataFrame td {
        color: #CBD5E1 !important;
        font-size: 12px !important;
        padding: 8px 12px !important;
        border-color: rgba(255, 255, 255, 0.04) !important;
    }

    /* ── Page Header Component ────────────────────────── */
    .pg-header {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding-bottom: 0.85rem;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        width: 100%;
    }
    .pg-title {
        font-size: 24px;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.3;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .pg-sub {
        font-size: 13px;
        color: #64748B;
        margin: 0;
        line-height: 1.4;
    }

    /* ── Section Header Component ─────────────────────── */
    .sec-head, .section-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 15px;
        font-weight: 600;
        color: #CBD5E1;
        margin: 16px 0 10px 0;
        line-height: 1.4;
        width: 100%;
    }
    .section-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .section-title {
        font-size: 15px;
        font-weight: 600;
        color: #CBD5E1;
    }

    /* ── KPI Cards ────────────────────────────────────── */
    .kpi {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        width: 100%;
        box-sizing: border-box;
        transition: border-color 0.2s ease, transform 0.15s ease;
    }
    .kpi:hover {
        border-color: rgba(139, 92, 246, 0.35);
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-val {
        font-size: 20px;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.2;
        letter-spacing: -0.01em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-sub {
        font-size: 11px;
        font-weight: 500;
        line-height: 1.3;
    }
    .pos { color: #22C55E; }
    .neg { color: #EF4444; }
    .muted { color: #64748B; }
    .warn { color: #F59E0B; }

    /* ── Recommendation Hero Card ─────────────────────── */
    .rec-card {
        background: #111827;
        border: 1px solid rgba(139, 92, 246, 0.30);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 24px rgba(139, 92, 246, 0.06);
        width: 100%;
        box-sizing: border-box;
    }
    .rec-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .rec-product-title {
        font-size: 16px;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .rec-product-sub {
        font-size: 12px;
        color: #64748B;
        margin-top: 2px;
    }

    /* Price Comparison Row */
    .price-row {
        display: grid;
        grid-template-columns: 1fr 1.6fr 1fr;
        gap: 12px;
        align-items: stretch;
        text-align: center;
        margin-bottom: 16px;
        width: 100%;
    }
    .p-node {
        background: #151E2E;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 12px 14px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 4px;
    }
    .p-node-hero {
        background: linear-gradient(135deg, #1E1040 0%, #0F1B3B 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.50);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.12);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 4px;
    }
    .p-node-label {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
    }
    .p-node-label-hero {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #A78BFA;
    }
    .p-node-val {
        font-size: 18px;
        font-weight: 700;
        color: #F8FAFC;
    }
    .p-node-val-hero {
        font-size: 24px;
        font-weight: 800;
        color: #C4B5FD;
        letter-spacing: -0.02em;
    }

    /* Outcome KPIs Grid */
    .outcome-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 8px;
        width: 100%;
    }
    .out-cell {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 10px 12px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 3px;
    }
    .out-label {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
    }
    .out-val {
        font-size: 16px;
        font-weight: 700;
        color: #F8FAFC;
    }
    .out-sub {
        font-size: 10px;
        font-weight: 600;
    }

    @media (max-width: 900px) {
        .price-row {
            grid-template-columns: 1fr;
            gap: 10px;
        }
        .outcome-row {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 500px) {
        .outcome-row {
            grid-template-columns: 1fr;
        }
    }

    /* Status Badges */
    .badge-safe { background: rgba(34, 197, 94, 0.15); color: #4ADE80; border: 1px solid rgba(34, 197, 94, 0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-warn { background: rgba(245, 158, 11, 0.15); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-err  { background: rgba(239, 68, 68, 0.15);  color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.25);  font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-hi   { background: rgba(139, 92, 246, 0.15); color: #C4B5FD; border: 1px solid rgba(139, 92, 246, 0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-med  { background: rgba(59, 130, 246, 0.15); color: #93C5FD; border: 1px solid rgba(59, 130, 246, 0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 4px; }

    /* Callouts & Decision Banners */
    .callout-ok {
        background: rgba(34, 197, 94, 0.08);
        border-left: 3px solid #22C55E;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #86EFAC;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }
    .callout-warn {
        background: rgba(245, 158, 11, 0.08);
        border-left: 3px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #FCD34D;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }
    .callout-err {
        background: rgba(239, 68, 68, 0.08);
        border-left: 3px solid #EF4444;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #FCA5A5;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }

    .banner-safe {
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.30);
        border-radius: 12px;
        padding: 12px 18px;
        text-align: center;
        font-size: 15px;
        font-weight: 700;
        color: #4ADE80;
        margin-top: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .banner-warn {
        background: rgba(245, 158, 11, 0.10);
        border: 1px solid rgba(245, 158, 11, 0.30);
        border-radius: 12px;
        padding: 12px 18px;
        text-align: center;
        font-size: 15px;
        font-weight: 700;
        color: #FCD34D;
        margin-top: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .banner-err {
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(239, 68, 68, 0.30);
        border-radius: 12px;
        padding: 12px 18px;
        text-align: center;
        font-size: 15px;
        font-weight: 700;
        color: #FCA5A5;
        margin-top: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }

    /* Insight Box */
    .insight-box {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .insight-title {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #8B5CF6;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .insight-item {
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.5;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 16px 0 8px 0;
        font-size: 11px;
        color: #475569;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 24px;
        width: 100%;
    }

    /* ── Overview Hero Section ────────────────────────── */
    .hero-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 32px;
        padding: 20px 0 20px 0;
        margin-bottom: 8px;
        width: 100%;
        flex-wrap: wrap;
    }
    .hero-left {
        flex: 1 1 500px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .hero-right {
        flex: 0 0 auto;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .hero-eyebrow {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #06B6D4;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
        letter-spacing: -0.03em;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 15px;
        font-weight: 600;
        background: linear-gradient(90deg, #8B5CF6, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-desc {
        font-size: 13px;
        color: #64748B;
        line-height: 1.6;
        max-width: 520px;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.28);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #A78BFA;
        width: fit-content;
    }
    .hero-pill-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22C55E;
        display: inline-block;
    }

    /* Hero Glass Card Scene */
    .hero-visual {
        position: relative;
        width: 260px;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .glass-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        padding: 16px 18px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .dp-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 50%, #06B6D4 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 900;
        color: #fff;
        margin-bottom: 4px;
    }
    .gc-eyebrow {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.45);
    }
    .gc-title {
        font-size: 15px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.01em;
    }
    .gc-sub {
        font-size: 11px;
        font-weight: 600;
        color: #A78BFA;
    }
    .gc-divider {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin: 6px 0;
    }
    .gc-stat-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .gc-stat-label {
        font-size: 10px;
        color: rgba(255, 255, 255, 0.50);
        font-weight: 600;
    }
    .gc-stat-val {
        font-size: 14px;
        font-weight: 800;
        color: #34D399;
    }
    </style>
    """

def header(title: str, subtitle: str):
    return (
        f'<div class="pg-header">'
        f'<div class="pg-title">{title}</div>'
        f'<div class="pg-sub">{subtitle}</div>'
        f'</div>'
    )

def kpi(label: str, value: str, sub: str = "", cls: str = "muted"):
    return (
        f'<div class="kpi">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-val">{value}</div>'
        f'<div class="kpi-sub {cls}">{sub}</div>'
        f'</div>'
    )

def footer():
    return '<div class="app-footer">Dynamic Pricing & Revenue Intelligence Platform · Econometrically Calibrated ML Models</div>'
