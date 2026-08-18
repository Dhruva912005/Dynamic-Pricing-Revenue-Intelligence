"""
Full Pipeline Execution Script
Runs the entire end-to-end data pipeline, modeling, optimization, and exports all models and CSVs.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

# Ensure working directory is project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.data_loader import load_data, validate_data_quality, clean_data
from src.feature_engineering import (
    create_time_features,
    create_lag_and_rolling_features,
    create_pricing_features,
    build_feature_pipeline
)
from src.modeling import (
    chronological_train_val_test_split,
    calculate_metrics,
    train_baseline_models,
    train_random_forest,
    train_xgboost,
    save_model_artifacts
)
from src.pricing_optimizer import DynamicPricingEngine

print("--- STEP 1: LOAD & VALIDATE DATA ---")
df_raw = load_data("data/dataset.csv")
audit = validate_data_quality(df_raw)
print(f"Data audit completed. Suitable: {audit['is_suitable_for_dynamic_pricing']}, Mean Corr: {audit['mean_price_demand_correlation']:.3f}")

print("\n--- STEP 2: FEATURE ENGINEERING ---")
df = clean_data(df_raw)
df = create_time_features(df)
df = create_lag_and_rolling_features(df)
df = create_pricing_features(df)
df_ml = df.dropna().reset_index(drop=True)
print(f"ML Feature Dataset: {df_ml.shape[0]} rows, {df_ml.shape[1]} columns.")

print("\n--- STEP 3: CHRONOLOGICAL SPLIT & PREPROCESSING ---")
train_df, val_df, test_df = chronological_train_val_test_split(df_ml, train_ratio=0.70, val_ratio=0.15)

categorical_cols = ['Product_ID', 'Store_ID', 'Category', 'Region']
numerical_cols = [
    'Our_Price', 'Competitor_Price', 'Price_Difference', 'Price_Ratio',
    'Price_Premium_Percent', 'Discount_Percent', 'Promotion_Flag',
    'DayOfWeek', 'Month', 'Quarter', 'Is_Weekend', 'Season',
    'Demand_Lag_1', 'Demand_Lag_7', 'Demand_Lag_14', 'Demand_Lag_28',
    'Demand_Rolling_Mean_7', 'Demand_Rolling_Mean_14', 'Demand_Rolling_Mean_28', 'Demand_Rolling_Std_7'
]

preprocessor = build_feature_pipeline(categorical_cols, numerical_cols)
X_train = preprocessor.fit_transform(train_df)
y_train = train_df['Units_Sold'].values
X_val = preprocessor.transform(val_df)
y_val = val_df['Units_Sold'].values
X_test = preprocessor.transform(test_df)
y_test = test_df['Units_Sold'].values

feature_metadata = {
    "categorical_cols": categorical_cols,
    "numerical_cols": numerical_cols,
    "total_transformed_features": int(X_train.shape[1])
}

print("\n--- STEP 4: MODEL TRAINING & BENCHMARK ---")
naive_metrics, ma_metrics, _, _ = train_baseline_models(train_df, test_df)

rf_model, _ = train_random_forest(X_train, y_train, X_val, y_val, random_state=42)
y_rf_test = np.clip(rf_model.predict(X_test), 0, None)
rf_test_metrics = calculate_metrics(y_test, y_rf_test)
rf_test_metrics["Model"] = "Random Forest Regressor"

xgb_model, _ = train_xgboost(X_train, y_train, X_val, y_val, random_state=42)
y_xgb_test = np.clip(xgb_model.predict(X_test), 0, None)
xgb_test_metrics = calculate_metrics(y_test, y_xgb_test)
xgb_test_metrics["Model"] = "XGBoost Regressor (Tuned)"

metrics_df = pd.DataFrame([naive_metrics, ma_metrics, rf_test_metrics, xgb_test_metrics])[
    ['Model', 'MAE', 'RMSE', 'R2', 'WAPE_%', 'sMAPE_%', 'Approx_Forecast_Accuracy_%']
]
print(metrics_df)

print("\n--- STEP 5: SAVE MODEL ARTIFACTS ---")
save_model_artifacts(
    model=xgb_model,
    preprocessor=preprocessor,
    feature_names=feature_metadata,
    metrics_df=metrics_df,
    models_dir=os.path.join(BASE_DIR, "models"),
    outputs_dir=os.path.join(BASE_DIR, "outputs")
)

# Save test forecasts
test_results = test_df.copy()
test_results['Actual_Demand'] = y_test
test_results['Forecast_XGBoost'] = np.round(y_xgb_test, 1)
test_results['Forecast_Error'] = test_results['Forecast_XGBoost'] - test_results['Actual_Demand']
test_results[['Date', 'Product_ID', 'Product_Name', 'Store_ID', 'Category', 'Our_Price', 'Actual_Demand', 'Forecast_XGBoost', 'Forecast_Error']].to_csv(
    os.path.join(BASE_DIR, "outputs", "forecast_results.csv"), index=False
)

print("\n--- STEP 6: ELASTICITY & DYNAMIC PRICING ENGINE ---")
engine = DynamicPricingEngine(
    model_path=os.path.join(BASE_DIR, "models", "demand_model.pkl"),
    pipeline_path=os.path.join(BASE_DIR, "models", "preprocessing_pipeline.pkl"),
    features_path=os.path.join(BASE_DIR, "models", "feature_columns.json")
)

elasticity_df = DynamicPricingEngine.estimate_price_elasticity(df)
joblib.dump(elasticity_df, os.path.join(BASE_DIR, "models", "elasticity_model.pkl"))
print(f"Computed elasticities for {len(elasticity_df)} products.")

latest_date = df['Date'].max()
latest_df = df[df['Date'] == latest_date].copy()

all_recs = []
for _, row in latest_df.iterrows():
    row_df = pd.DataFrame([row])
    p_id = row['Product_ID']
    s_id = row['Store_ID']
    hist_series = df[(df['Product_ID'] == p_id) & (df['Store_ID'] == s_id)]['Our_Price']
    
    r = engine.optimize_price(
        row_df,
        hist_prices_series=hist_series,
        objective="MAX_REVENUE",
        max_increase_pct=10.0,
        max_decrease_pct=10.0,
        max_competitor_premium_pct=5.0
    )
    r_dict = {k: v for k, v in r.items() if k != "Simulation_Grid"}
    all_recs.append(r_dict)

recs_df = pd.DataFrame(all_recs)
recs_df.to_csv(os.path.join(BASE_DIR, "outputs", "pricing_recommendations.csv"), index=False)
print(f"Generated and exported {len(recs_df)} pricing recommendations to outputs/pricing_recommendations.csv.")

# Save unified dataset for Power BI ingestion
df_pbi = df.copy()
# Join recommendation data onto latest state
recs_subset = recs_df[['Product_ID', 'Store_ID', 'Recommended_Price', 'Revenue_Improvement_Percent', 'Price_Change_Percent', 'Confidence_Level', 'Recommendation_Reason']]
df_pbi = df_pbi.merge(recs_subset, on=['Product_ID', 'Store_ID'], how='left')
df_pbi.to_csv(os.path.join(BASE_DIR, "dashboard", "Dynamic_Pricing_Data_Enriched.csv"), index=False)
print("Saved Power BI enriched dataset to dashboard/Dynamic_Pricing_Data_Enriched.csv.")
print("\nPipeline execution complete!")
