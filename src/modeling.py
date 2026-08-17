"""
Demand Forecasting & ML Modeling Module
Implements chronological splitting, baseline models, Random Forest, XGBoost,
rigorous retail regression metrics (MAE, RMSE, R2, WAPE, sMAPE), and pipeline serialization.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

def chronological_train_val_test_split(df, train_ratio=0.70, val_ratio=0.15):
    """
    Splits panel time-series chronologically to guarantee zero future leakage.
    """
    unique_dates = np.sort(df['Date'].unique())
    n_dates = len(unique_dates)
    
    train_end_idx = int(n_dates * train_ratio)
    val_end_idx = int(n_dates * (train_ratio + val_ratio))
    
    train_dates = unique_dates[:train_end_idx]
    val_dates = unique_dates[train_end_idx:val_end_idx]
    test_dates = unique_dates[val_end_idx:]
    
    train_df = df[df['Date'].isin(train_dates)].copy()
    val_df = df[df['Date'].isin(val_dates)].copy()
    test_df = df[df['Date'].isin(test_dates)].copy()
    
    return train_df, val_df, test_df

def calculate_metrics(y_true, y_pred):
    """
    Computes industry-standard retail demand forecasting metrics.
    """
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    # Clip negative predictions to zero
    y_pred = np.clip(y_pred, 0, None)
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # WAPE = Sum(|y - y_hat|) / Sum(y) * 100
    sum_true = np.sum(y_true)
    wape = (np.sum(np.abs(y_true - y_pred)) / (sum_true + 1e-6)) * 100.0
    
    # sMAPE = (100 / n) * Sum( 2*|y - y_hat| / (|y| + |y_hat| + eps) )
    smape = np.mean(2.0 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-6)) * 100.0
    
    approx_accuracy = max(0.0, 100.0 - wape)
    
    return {
        "MAE": round(float(mae), 3),
        "RMSE": round(float(rmse), 3),
        "R2": round(float(r2), 4),
        "WAPE_%": round(float(wape), 2),
        "sMAPE_%": round(float(smape), 2),
        "Approx_Forecast_Accuracy_%": round(float(approx_accuracy), 2)
    }

def train_baseline_models(train_df, test_df):
    """
    Trains and evaluates Naive (Lag 1) and Moving Average (7-Day) baselines.
    """
    # 1. Naive Baseline (Lag 1)
    y_test = test_df['Units_Sold'].values
    y_naive = test_df['Demand_Lag_1'].fillna(train_df['Units_Sold'].mean()).values
    naive_metrics = calculate_metrics(y_test, y_naive)
    naive_metrics["Model"] = "Naive Baseline (Lag 1)"
    
    # 2. Moving Average Baseline (7-Day)
    y_ma = test_df['Demand_Rolling_Mean_7'].fillna(train_df['Units_Sold'].mean()).values
    ma_metrics = calculate_metrics(y_test, y_ma)
    ma_metrics["Model"] = "7-Day Moving Average"
    
    return naive_metrics, ma_metrics, y_naive, y_ma

def train_random_forest(X_train, y_train, X_val, y_val, random_state=42):
    """
    Trains Random Forest Regressor with robust tree parameters.
    """
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=random_state
    )
    rf.fit(X_train, y_train)
    val_preds = rf.predict(X_val)
    val_metrics = calculate_metrics(y_val, val_preds)
    return rf, val_metrics

def train_xgboost(X_train, y_train, X_val, y_val, random_state=42):
    """
    Trains XGBoost Regressor tuned for retail demand estimation.
    """
    model = xgb.XGBRegressor(
        n_estimators=180,
        learning_rate=0.06,
        max_depth=6,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    val_preds = model.predict(X_val)
    val_metrics = calculate_metrics(y_val, val_preds)
    return model, val_metrics

def save_model_artifacts(model, preprocessor, feature_names, metrics_df, models_dir="models", outputs_dir="outputs"):
    """
    Saves trained model, preprocessing pipeline, feature metadata, and metrics table.
    """
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(models_dir, "demand_model.pkl"))
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessing_pipeline.pkl"))
    
    with open(os.path.join(models_dir, "feature_columns.json"), "w") as f:
        json.dump(feature_names, f, indent=4)
        
    metrics_df.to_csv(os.path.join(outputs_dir, "model_metrics.csv"), index=False)
    print(f"Artifacts successfully saved to '{models_dir}/' and '{outputs_dir}/'.")
