"""
Comprehensive deployment validation script.
Tests every component required for the Streamlit Cloud deployment.
Run: python validate_deployment.py
"""

import os
import sys
import traceback
import numpy as np
import pandas as pd

results = {}

def check(label, fn):
    try:
        fn()
        results[label] = "PASS"
        print(f"  [{label}] PASS")
    except Exception as e:
        results[label] = f"FAIL: {e}"
        print(f"  [{label}] FAIL: {e}")
        traceback.print_exc()


# 1. DATASET LOAD
print("\n=== 1. DATASET LOAD ===")
df_master = pd.DataFrame()

def test_dataset_load():
    global df_master
    path = os.path.join("dashboard", "Dynamic_Pricing_Data_Enriched.csv")
    if not os.path.exists(path):
        path = os.path.join("data", "dataset.csv")
    df_master = pd.read_csv(path)
    if "Date" in df_master.columns:
        df_master["Date"] = pd.to_datetime(df_master["Date"])
    assert len(df_master) > 0, "Empty dataset"
    print(f"    Rows: {len(df_master)}, Cols: {len(df_master.columns)}")

check("DATASET LOAD", test_dataset_load)


# 2. PREPROCESSOR pkl
print("\n=== 2. PREPROCESSOR (pkl) ===")
preprocessor = None

def test_preprocessor_pkl():
    global preprocessor
    import joblib
    pipe_path = os.path.join("models", "preprocessing_pipeline.pkl")
    assert os.path.exists(pipe_path), f"{pipe_path} missing"
    pipe = joblib.load(pipe_path)
    sample = df_master.dropna().head(5)
    X = pipe.transform(sample)
    assert X.shape[1] == 53, f"Expected 53 features, got {X.shape[1]}"
    preprocessor = pipe
    print(f"    Output shape: {X.shape}")

check("PREPROCESSOR (pkl)", test_preprocessor_pkl)


# 3. PREPROCESSOR RECONSTRUCTION
print("\n=== 3. PREPROCESSOR RECONSTRUCTION ===")
preprocessor_recon = None

def test_preprocessor_reconstruct():
    global preprocessor_recon
    categorical_cols = ['Product_ID', 'Store_ID', 'Category', 'Region']
    numerical_cols = [
        'Our_Price', 'Competitor_Price', 'Price_Difference', 'Price_Ratio',
        'Price_Premium_Percent', 'Discount_Percent', 'Promotion_Flag',
        'DayOfWeek', 'Month', 'Quarter', 'Is_Weekend', 'Season',
        'Demand_Lag_1', 'Demand_Lag_7', 'Demand_Lag_14', 'Demand_Lag_28',
        'Demand_Rolling_Mean_7', 'Demand_Rolling_Mean_14', 'Demand_Rolling_Mean_28', 'Demand_Rolling_Std_7'
    ]
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    df = df_master.copy()
    df_clean = df.dropna(subset=[c for c in numerical_cols if c in df.columns]).copy()

    if 'Date' in df_clean.columns:
        unique_dates = np.sort(df_clean['Date'].unique())
        train_end_idx = int(len(unique_dates) * 0.70)
        train_dates = unique_dates[:train_end_idx]
        train_df = df_clean[df_clean['Date'].isin(train_dates)].copy()
    else:
        train_df = df_clean

    pipe = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ],
        remainder='drop'
    )
    pipe.fit(train_df)

    sample = df_clean.head(5)
    X = pipe.transform(sample)
    assert X.shape[1] == 53, f"Expected 53 features, got {X.shape[1]}"
    preprocessor_recon = pipe
    print(f"    Reconstructed output shape: {X.shape}")

check("PREPROCESSOR (reconstruct)", test_preprocessor_reconstruct)


# 4. FEATURE SHAPE
print("\n=== 4. FEATURE SHAPE ===")

def test_feature_shape():
    sample = df_master.dropna().head(5)
    X = preprocessor.transform(sample)
    assert X.shape[1] == 53, f"Feature count {X.shape[1]} != 53"
    print(f"    Feature count: {X.shape[1]} (expected 53)")

check("FEATURE SHAPE", test_feature_shape)


# 5. DEMAND MODEL
print("\n=== 5. DEMAND MODEL LOAD ===")
model = None

def test_demand_model():
    global model
    import xgboost as xgb
    json_path = os.path.join("models", "demand_model.json")
    assert os.path.exists(json_path), f"{json_path} missing"
    m = xgb.XGBRegressor()
    m.load_model(json_path)
    model = m
    print(f"    Loaded from native JSON: {json_path}, type: {type(m).__name__}")

check("DEMAND MODEL", test_demand_model)


# 6. ACTUAL PREDICTION
print("\n=== 6. ACTUAL PREDICTION ===")

def test_actual_prediction():
    sample = df_master.dropna().head(5)
    X = preprocessor.transform(sample)
    preds = model.predict(X)
    assert len(preds) == 5
    assert not np.isnan(preds).any(), "NaN predictions"
    print(f"    Predictions (first 5): {np.round(preds, 2)}")

check("ACTUAL PREDICTION", test_actual_prediction)


# 7. PREDICTION WITH RECONSTRUCTED PREPROCESSOR
print("\n=== 7. PREDICTION (reconstructed preprocessor) ===")

def test_recon_prediction():
    sample = df_master.dropna().head(5)
    X_orig = preprocessor.transform(sample)
    X_recon = preprocessor_recon.transform(sample)
    preds_orig = model.predict(X_orig)
    preds_recon = model.predict(X_recon)
    max_diff = np.max(np.abs(preds_orig - preds_recon))
    print(f"    Orig preds:  {np.round(preds_orig, 2)}")
    print(f"    Recon preds: {np.round(preds_recon, 2)}")
    print(f"    Max prediction diff: {max_diff:.4f}")
    if max_diff > 5.0:
        print("    WARNING: large prediction difference between pkl and reconstructed preprocessor")

check("PREDICTION (recon vs pkl)", test_recon_prediction)


# 8. ELASTICITY DATA
print("\n=== 8. ELASTICITY DATA ===")
elasticity_df = None

def test_elasticity():
    global elasticity_df
    csv_path = os.path.join("models", "elasticity_model.csv")
    assert os.path.exists(csv_path), f"{csv_path} missing"
    df_el = pd.read_csv(csv_path)
    assert len(df_el) > 0
    elasticity_df = df_el
    print(f"    Rows: {len(df_el)}, Cols: {df_el.columns.tolist()}")

check("ELASTICITY DATA", test_elasticity)


# 9. PRICING ENGINE
print("\n=== 9. PRICING ENGINE ===")
recs_df = pd.DataFrame()

def test_pricing_engine():
    global recs_df
    path = os.path.join("dashboard", "Pricing_Recommendations_Enriched.csv")
    if not os.path.exists(path):
        path = os.path.join("outputs", "pricing_recommendations.csv")
    assert os.path.exists(path), f"Recs file not found at {path}"
    recs_df = pd.read_csv(path)
    assert len(recs_df) > 0
    req_cols = ["Product_ID", "Store_ID", "Current_Price", "Competitor_Price",
                "Recommended_Price", "Confidence_Level"]
    missing = [c for c in req_cols if c not in recs_df.columns]
    assert not missing, f"Missing columns: {missing}"
    print(f"    Rows: {len(recs_df)}, Required cols: OK")

check("PRICING ENGINE", test_pricing_engine)


# 10. GUARDRAILS
print("\n=== 10. GUARDRAILS ===")

def test_guardrails():
    from web.pricing_service import evaluate_guardrails
    result = evaluate_guardrails(
        candidate_price=350.0,
        current_price=380.0,
        competitor_price=338.72,
        unit_cost=200.0,
        predicted_demand=50.0,
        max_increase_pct=10.0,
        max_decrease_pct=10.0,
        max_competitor_premium_pct=5.0
    )
    assert "is_feasible" in result
    print(f"    Guardrail status: {result['status_label']}, feasible: {result['is_feasible']}")

check("GUARDRAILS", test_guardrails)


# 11. WHAT-IF SIMULATOR
print("\n=== 11. WHAT-IF SIMULATOR ===")

def test_whatif_simulator():
    from web.pricing_service import simulate_interactive_price
    sample_row = df_master.dropna().tail(1).copy()
    if "Our_Price" not in sample_row.columns:
        return
    result = simulate_interactive_price(
        base_row_df=sample_row,
        candidate_price=float(sample_row["Our_Price"].iloc[0]) * 1.05,
        model=model,
        preprocessor=preprocessor,
        unit_cost=float(sample_row.get("Unit_Cost", pd.Series([200])).iloc[0])
    )
    assert result is not None
    assert "predicted_demand" in result
    assert not np.isnan(result["predicted_demand"])
    print(f"    Simulated demand: {result['predicted_demand']:.2f}, revenue: {result['expected_revenue']:.2f}")

check("WHAT-IF SIMULATOR", test_whatif_simulator)


# 12. PRICING RECOMMENDATION ANALYSIS
print("\n=== 12. PRICING RECOMMENDATION ANALYSIS ===")

def test_rec_analysis():
    from web.pricing_service import analyze_pricing_recommendation
    sim_grid_path = "dashboard/Pricing_Simulation_Grid.csv"
    sim_grid = pd.read_csv(sim_grid_path) if os.path.exists(sim_grid_path) else pd.DataFrame()
    if len(recs_df) == 0:
        return
    rec_row = recs_df.iloc[0]
    pid = rec_row["Product_ID"]
    sid = rec_row["Store_ID"]
    if len(sim_grid) > 0:
        cdf = sim_grid[(sim_grid["Product_ID"] == pid) & (sim_grid["Store_ID"] == sid)].sort_values("Candidate_Price")
    else:
        cdf = pd.DataFrame()
    res = analyze_pricing_recommendation(cdf, rec_row)
    assert "final_p" in res
    assert "rev_label" in res
    assert "prof_label" in res
    safe_decision = res['decision_status'].encode('ascii', 'replace').decode('ascii')
    print(f"    Final price: {res['final_p']:.2f}, Decision: {safe_decision}")
    print(f"    rev_impact: {res['rev_impact_pct']:+.2f}% -> label: '{res['rev_label']}'")
    print(f"    prof_impact: {res['prof_impact_pct']:+.2f}% -> label: '{res['prof_label']}'")
    if res["rev_impact_pct"] < 0:
        assert res["rev_label"] == "Revenue Impact", f"Negative revenue needs 'Revenue Impact', got '{res['rev_label']}'"
    if res["prof_impact_pct"] < 0:
        assert res["prof_label"] == "Profit Impact", f"Negative profit needs 'Profit Impact', got '{res['prof_label']}'"

check("PRICING RECOMMENDATION ANALYSIS", test_rec_analysis)


# 13. PLOTLY
print("\n=== 13. PLOTLY GRAPHS ===")

def test_plotly():
    import plotly.graph_objects as go
    fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[10, 20, 30], mode="lines"))
    fig.update_layout(template="plotly_dark", height=300)
    _ = fig.to_json()
    print("    Plotly figure created OK")

check("PLOTLY GRAPHS", test_plotly)


# 14. STREAMLIT IMPORT
print("\n=== 14. STREAMLIT IMPORT ===")

def test_streamlit():
    import streamlit as st
    print(f"    Streamlit version: {st.__version__}")

check("STREAMLIT IMPORT", test_streamlit)


# 15. load_ml_pipeline() E2E SIMULATION
print("\n=== 15. load_ml_pipeline() LOGIC SIMULATION ===")

def test_load_ml_pipeline():
    import xgboost as xgb
    import joblib

    m_out = None
    json_path = os.path.join("models", "demand_model.json")
    pkl_path  = os.path.join("models", "demand_model.pkl")

    if os.path.exists(json_path):
        try:
            m_out = xgb.XGBRegressor()
            m_out.load_model(json_path)
        except Exception as e:
            m_out = None

    if m_out is None and os.path.exists(pkl_path):
        m_out = joblib.load(pkl_path)

    assert m_out is not None, "model load failed"

    pre_out = None
    pipe_path = os.path.join("models", "preprocessing_pipeline.pkl")
    if os.path.exists(pipe_path):
        try:
            pre_out = joblib.load(pipe_path)
            _ = pre_out.transform(df_master.dropna().head(2))
        except Exception as e:
            print(f"    PKL failed ({e}) -> using reconstructed")
            pre_out = None

    if pre_out is None:
        pre_out = preprocessor_recon

    assert pre_out is not None

    el_out = pd.read_csv("models/elasticity_model.csv")
    assert len(el_out) > 0

    sample = df_master.dropna().head(3)
    X = pre_out.transform(sample)
    preds = m_out.predict(X)
    assert not np.isnan(preds).any()
    print(f"    Model: {type(m_out).__name__}")
    print(f"    Preprocessor: {type(pre_out).__name__}")
    print(f"    Elasticity rows: {len(el_out)}")
    print(f"    Predictions: {np.round(preds, 2)}")

check("load_ml_pipeline() E2E", test_load_ml_pipeline)


# FINAL REPORT
print("\n" + "=" * 60)
print("FINAL VALIDATION REPORT")
print("=" * 60)
all_pass = True
for label, status in results.items():
    icon = "PASS" if status == "PASS" else "FAIL"
    print(f"  {icon}: {label}: {status}")
    if status != "PASS":
        all_pass = False

print()
if all_pass:
    print("ALL CHECKS PASSED -- Safe to deploy.")
else:
    print("SOME CHECKS FAILED -- Fix before deploying.")
