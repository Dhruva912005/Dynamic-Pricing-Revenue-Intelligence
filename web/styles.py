"""
Premium Dark SaaS CSS Design System
Dynamic Pricing & Revenue Intelligence Platform
"""

def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Global Reset ─────────────────────────────────── */
    html, body, [class*="css"], .stMarkdown, p, span, div, label {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        color: #F8FAFC;
    }

    /* Dark canvas background */
    .stApp, .main {
        background-color: #0B1120 !important;
    }

    /* Remove Streamlit default top padding */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* ── Sidebar ──────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #070D1A !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] > div {
        background: #070D1A !important;
    }
    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        margin: 2px 0 !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(139,92,246,0.15) !important;
        color: #C4B5FD !important;
    }
    [data-testid="stSidebar"] .stRadio > div [aria-checked="true"] + label,
    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"]:has(input:checked) {
        background: rgba(139,92,246,0.2) !important;
        color: #A78BFA !important;
    }
    [data-testid="stSidebar"] * { color: #94A3B8 !important; }
    [data-testid="stSidebar"] .stMarkdown h3 { color: #F8FAFC !important; font-size: 15px !important; }

    /* ════════════════════════════════════════════════════
       DROPDOWN / SELECTBOX — FULL DARK THEME FIX
       Covers: closed state, popover portal, options,
       hover, selected, multiselect, date input.
    ════════════════════════════════════════════════════ */

    /* ── Closed selectbox container ─────────────────── */
    div[data-baseweb="select"] {
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        min-height: 38px !important;
        cursor: pointer !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(139,92,246,0.50) !important;
    }
    /* Selected value text */
    div[data-baseweb="select"] [data-testid="stSelectboxLabel"],
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [role="combobox"] {
        color: #F8FAFC !important;
        font-size: 14px !important;
        background-color: transparent !important;
    }
    /* Dropdown arrow/icon */
    div[data-baseweb="select"] svg {
        fill: #CBD5E1 !important;
        color: #CBD5E1 !important;
    }

    /* ── Popover overlay (renders in portal, outside shadow DOM) */
    /* BaseWeb renders the dropdown list in a fixed-position overlay  */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] > div > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.60) !important;
        overflow: hidden !important;
    }

    /* ── Menu list container ────────────────────────── */
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #111827 !important;
        border: none !important;
        max-height: 300px !important;
        overflow-y: auto !important;
        padding: 4px !important;
    }
    /* Scrollbar styling */
    div[data-baseweb="menu"]::-webkit-scrollbar { width: 6px !important; }
    div[data-baseweb="menu"]::-webkit-scrollbar-track { background: #0F172A !important; }
    div[data-baseweb="menu"]::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.4) !important; border-radius: 4px !important; }

    /* ── Individual options ─────────────────────────── */
    li[role="option"],
    div[role="option"] {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        font-size: 14px !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: background-color 0.12s ease !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
    }
    /* Selected / highlighted option */
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"],
    li[role="option"].highlighted,
    div[role="option"].highlighted {
        background-color: #312E81 !important;
        color: #FFFFFF !important;
    }
    /* BaseWeb uses data-highlighted on hovered option */
    li[data-highlighted="true"],
    div[data-highlighted="true"] {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
    }

    /* ── All text inside any BaseWeb component ───────── */
    [data-baseweb] * {
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] *,
    [data-baseweb="select"] * {
        color: #F8FAFC !important;
    }
    /* Override any white backgrounds injected by BaseWeb */
    [data-baseweb="popover"] [style*="background: rgb(255"],
    [data-baseweb="popover"] [style*="background-color: rgb(255"],
    [data-baseweb="popover"] [style*="background:white"],
    [data-baseweb="popover"] [style*="background: white"] {
        background-color: #111827 !important;
        background: #111827 !important;
    }

    /* ── Multiselect ─────────────────────────────────── */
    div[data-baseweb="tag"] {
        background-color: rgba(139,92,246,0.20) !important;
        border: 1px solid rgba(139,92,246,0.40) !important;
        border-radius: 4px !important;
        color: #C4B5FD !important;
    }
    div[data-baseweb="tag"] span { color: #C4B5FD !important; }
    div[data-baseweb="tag"] [role="presentation"] { color: #A78BFA !important; }

    /* ── Date input ──────────────────────────────────── */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: #111827 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    div[data-baseweb="input"]:hover,
    div[data-baseweb="base-input"]:hover {
        border-color: rgba(139,92,246,0.50) !important;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    .stDateInput input,
    .stTextInput input {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        font-size: 14px !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        border: none !important;
    }
    .stDateInput > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
    }

    /* ── Streamlit selectbox label ───────────────────── */
    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label {
        color: #94A3B8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
    }

    /* Slider */
    .stSlider > div > div > div { background: #8B5CF6 !important; }
    .stSlider div[data-testid="stTickBar"] { color: #94A3B8 !important; }

    /* ── Expander ─────────────────────────────────────── */
    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary { color: #94A3B8 !important; font-size: 13px !important; }

    /* ── DataFrames ───────────────────────────────────── */
    .stDataFrame { background: #111827 !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 10px !important; }
    .stDataFrame table { background: #111827 !important; }
    .stDataFrame th { background: #151E2E !important; color: #94A3B8 !important; font-size: 12px !important; }
    .stDataFrame td { color: #CBD5E1 !important; font-size: 12px !important; border-color: rgba(255,255,255,0.05) !important; }

    /* ── Page Header ──────────────────────────────────── */
    .pg-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 0.85rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    .pg-title {
        font-size: 26px;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .pg-sub {
        font-size: 13px;
        color: #64748B;
        margin: 4px 0 0 0;
    }

    /* ── KPI Cards ────────────────────────────────────── */
    .kpi {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: border-color 0.2s ease;
    }
    .kpi:hover { border-color: rgba(139,92,246,0.35); }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 4px;
    }
    .kpi-val {
        font-size: 22px;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.2;
    }
    .kpi-sub { font-size: 11px; font-weight: 500; margin-top: 3px; }
    .pos { color: #22C55E; }
    .neg { color: #EF4444; }
    .muted { color: #64748B; }
    .warn { color: #F59E0B; }

    /* ── Section Heading ──────────────────────────────── */
    .sec-head {
        font-size: 15px;
        font-weight: 600;
        color: #CBD5E1;
        margin: 14px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ── Recommendation Hero Card ─────────────────────── */
    .rec-card {
        background: #111827;
        border: 1px solid rgba(139,92,246,0.30);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 0 28px rgba(139,92,246,0.08);
    }
    .rec-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .rec-product-title { font-size: 16px; font-weight: 700; color: #F8FAFC; }
    .rec-product-sub { font-size: 12px; color: #64748B; margin-top: 2px; }

    /* 3-column price comparison */
    .price-row {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 14px;
        align-items: center;
        text-align: center;
        margin-bottom: 16px;
    }
    .p-node {
        background: #151E2E;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 12px 14px;
    }
    .p-node-hero {
        background: linear-gradient(135deg, #1E1040 0%, #0F1B3B 100%);
        border: 1.5px solid rgba(139,92,246,0.50);
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 0 20px rgba(139,92,246,0.12);
    }
    .p-node-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 4px; }
    .p-node-label-hero { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #A78BFA; margin-bottom: 6px; }
    .p-node-val { font-size: 19px; font-weight: 700; color: #F8FAFC; }
    .p-node-val-hero { font-size: 28px; font-weight: 800; color: #C4B5FD; letter-spacing: -0.02em; }

    /* Outcome KPI row inside rec card */
    .outcome-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 4px;
    }
    .out-cell {
        background: #0F172A;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
        padding: 10px 12px;
        text-align: center;
    }
    .out-label { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #64748B; margin-bottom: 3px; }
    .out-val { font-size: 17px; font-weight: 700; color: #F8FAFC; }
    .out-sub { font-size: 10px; font-weight: 600; margin-top: 2px; }

    /* Status badges */
    .badge-safe { background: rgba(34,197,94,0.15); color: #4ADE80; border: 1px solid rgba(34,197,94,0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
    .badge-warn { background: rgba(245,158,11,0.15); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
    .badge-err  { background: rgba(239,68,68,0.15);  color: #FCA5A5; border: 1px solid rgba(239,68,68,0.25);  font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
    .badge-hi   { background: rgba(139,92,246,0.15); color: #C4B5FD; border: 1px solid rgba(139,92,246,0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
    .badge-med  { background: rgba(59,130,246,0.15); color: #93C5FD; border: 1px solid rgba(59,130,246,0.25); font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }

    /* Callout boxes */
    .callout-ok {
        background: rgba(34,197,94,0.08);
        border-left: 3px solid #22C55E;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #86EFAC;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }
    .callout-warn {
        background: rgba(245,158,11,0.08);
        border-left: 3px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #FCD34D;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }
    .callout-err {
        background: rgba(239,68,68,0.08);
        border-left: 3px solid #EF4444;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        color: #FCA5A5;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 10px;
    }

    /* Decision Banner */
    .banner-safe {
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.30);
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        color: #4ADE80;
        margin-top: 12px;
    }
    .banner-warn {
        background: rgba(245,158,11,0.10);
        border: 1px solid rgba(245,158,11,0.30);
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        color: #FCD34D;
        margin-top: 12px;
    }
    .banner-err {
        background: rgba(239,68,68,0.10);
        border: 1px solid rgba(239,68,68,0.30);
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        color: #FCA5A5;
        margin-top: 12px;
    }

    /* Insight box */
    .insight-box {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 10px;
    }
    .insight-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #8B5CF6; margin-bottom: 8px; }
    .insight-item { font-size: 13px; color: #CBD5E1; margin-bottom: 5px; }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 14px 0 6px 0;
        font-size: 11px;
        color: #334155;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 20px;
    }

    /* ═══════════════════════════════════════════════════════
       OVERVIEW HERO — glassmorphism card + animated orbs
    ═══════════════════════════════════════════════════════ */

    /* Two-column hero wrapper */
    .hero-row {
        display: flex;
        align-items: center;
        gap: 32px;
        padding: 28px 0 24px 0;
        margin-bottom: 8px;
    }
    .hero-left {
        flex: 0 0 55%;
        max-width: 55%;
    }
    .hero-right {
        flex: 0 0 45%;
        max-width: 45%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Responsive: stack on narrow viewports */
    @media (max-width: 900px) {
        .hero-row { flex-direction: column; }
        .hero-left, .hero-right { flex: 0 0 100%; max-width: 100%; }
    }

    /* Hero text */
    .hero-eyebrow {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #06B6D4;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(90deg, #8B5CF6, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 14px;
    }
    .hero-desc {
        font-size: 13px;
        color: #64748B;
        line-height: 1.65;
        max-width: 420px;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 18px;
        background: rgba(139,92,246,0.12);
        border: 1px solid rgba(139,92,246,0.28);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #A78BFA;
    }
    .hero-pill-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #22C55E;
        display: inline-block;
        animation: pulse-dot 2.5s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.75); }
    }

    /* Orb scene container */
    .hero-visual {
        position: relative;
        width: 320px;
        height: 220px;
        flex-shrink: 0;
    }
    @media (min-width: 1600px) {
        .hero-visual { width: 380px; height: 260px; }
    }

    /* Glowing background orbs */
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(38px);
        opacity: 0.55;
        pointer-events: none;
    }
    .orb-teal {
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, #14B8A6 0%, #06B6D4 55%, transparent 100%);
        top: -30px;
        right: 10px;
        animation: float-orb-a 10s ease-in-out infinite;
    }
    .orb-blue {
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, #3B82F6 0%, #8B5CF6 60%, transparent 100%);
        bottom: -10px;
        left: 10px;
        animation: float-orb-b 12s ease-in-out infinite;
    }
    @keyframes float-orb-a {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-14px) scale(1.04); }
    }
    @keyframes float-orb-b {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(10px) scale(0.97); }
    }

    /* Glassmorphism card */
    .glass-card {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 230px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 24px;
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        box-shadow: 0 8px 40px rgba(0,0,0,0.38), 0 0 0 1px rgba(255,255,255,0.06) inset;
        padding: 22px 22px 20px 22px;
        animation: card-breathe 8s ease-in-out infinite;
    }
    @keyframes card-breathe {
        0%, 100% { box-shadow: 0 8px 40px rgba(0,0,0,0.38), 0 0 0 1px rgba(255,255,255,0.06) inset, 0 0 24px rgba(139,92,246,0.08); }
        50% { box-shadow: 0 8px 48px rgba(0,0,0,0.42), 0 0 0 1px rgba(255,255,255,0.09) inset, 0 0 36px rgba(139,92,246,0.16); }
    }

    /* DP icon mark */
    .dp-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 50%, #06B6D4 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 900;
        color: #fff;
        letter-spacing: -0.04em;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(139,92,246,0.35);
    }

    /* Card inner text */
    .gc-eyebrow {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.45);
        margin-bottom: 4px;
    }
    .gc-title {
        font-size: 17px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-bottom: 2px;
    }
    .gc-sub {
        font-size: 11px;
        font-weight: 600;
        background: linear-gradient(90deg, #8B5CF6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
    }
    .gc-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.10);
        margin: 0 0 14px 0;
    }
    .gc-stat-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .gc-stat-label {
        font-size: 10px;
        color: rgba(255,255,255,0.45);
        font-weight: 600;
    }
    .gc-stat-val {
        font-size: 15px;
        font-weight: 800;
        color: #34D399;
        letter-spacing: -0.01em;
    }
    .gc-arrow {
        font-size: 12px;
        color: #34D399;
        margin-right: 3px;
    }
    </style>
    """

def header(title: str, subtitle: str):
    return f'<div class="pg-header"><div><div class="pg-title">{title}</div><div class="pg-sub">{subtitle}</div></div></div>'

def kpi(label: str, value: str, sub: str = "", cls: str = "muted"):
    return f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-val">{value}</div><div class="kpi-sub {cls}">{sub}</div></div>'

def footer():
    return '<div class="app-footer">Dataset: Synthetic econometrically calibrated retail panel data for pricing simulation and model validation.</div>'
