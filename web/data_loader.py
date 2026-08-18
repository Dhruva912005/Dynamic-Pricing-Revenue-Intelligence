"""
Data loading and caching module for Streamlit Web Application.
Uses portable artifacts (JSON/CSV) with automatic fallback reconstruction
for zero-failure Cloud deployments.
"""

import os
import logging
import joblib
import pandas as pd
import numpy as np
import streamlit as st

logger = logging.getLogger(__name__)

@st.cache_data(show_spinner=False)
def load_master_data():
    """
    Loads the enriched historical retail panel dataset.
    Falls back gracefully if enriched file is missing.
    """
    path = os.path.join("dashboard", "Dynamic_Pricing_Data_Enriched.csv")
    if not os.path.exists(path):
        path = os.path.join("data", "dataset.csv")
    
    if not os.path.exists(path):
        st.error(f"Dataset file not found at '{path}'. Please ensure dataset exists.")
        return pd.DataFrame()
        
    df = pd.read_csv(path)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data(show_spinner=False)
def load_recommendations():
    """
    Loads pre-computed optimized pricing recommendations with guardrails.
    """
    path = os.path.join("dashboard", "Pricing_Recommendations_Enriched.csv")
    if not os.path.exists(path):
        path = os.path.join("outputs", "pricing_recommendations.csv")
        
    if not os.path.exists(path):
        st.error(f"Recommendations file not found at '{path}'.")
        return pd.DataFrame()
        
    df = pd.read_csv(path)
    return df

@st.cache_data(show_spinner=False)
def load_simulation_grid():
    """
    Loads candidate price grid (-15% to +15%) for What-If scenario simulations.
    """
    path = os.path.join("dashboard", "Pricing_Simulation_Grid.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def load_model_metrics():
    """
    Loads validated model benchmark metrics.
    """
    path = os.path.join("outputs", "model_metrics.csv")
    if not os.path.exists(path):
        path = os.path.join("dashboard", "Model_Evaluation_Metrics.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def load_forecast_results():
    """
    Loads holdout test partition demand forecasts.
    """
    path = os.path.join("outputs", "forecast_results.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data(show_spinner=False)
def load_feature_importance():
    """
    Loads XGBoost Gini feature importance contributions.
    """
    path = os.path.join("dashboard", "Feature_Importance.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)

def reconstruct_preprocessor(df=None):
    """
    Reconstructs and fits the exact ColumnTransformer preprocessor from the dataset.
    This guarantees 100% version compatibility across any scikit-learn environment,
    eliminating fragile pickle deserialization errors.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    
    categorical_cols = ['Product_ID', 'Store_ID', 'Category', 'Region']
    numerical_cols = [
        'Our_Price', 'Competitor_Price', 'Price_Difference', 'Price_Ratio',
        'Price_Premium_Percent', 'Discount_Percent', 'Promotion_Flag',
        'DayOfWeek', 'Month', 'Quarter', 'Is_Weekend', 'Season',
        'Demand_Lag_1', 'Demand_Lag_7', 'Demand_Lag_14', 'Demand_Lag_28',
        'Demand_Rolling_Mean_7', 'Demand_Rolling_Mean_14', 'Demand_Rolling_Mean_28', 'Demand_Rolling_Std_7'
    ]
    
    if df is None or len(df) == 0:
        df = load_master_data()

    # Drop initial lag warm-up NaNs so fitting matches training distribution exactly
    df_clean = df.dropna(subset=[c for c in numerical_cols if c in df.columns]).copy()
        
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ],
        remainder='drop'
    )
    
    # Chronological training partition (first 70% of dates)
    if 'Date' in df_clean.columns:
        unique_dates = np.sort(df_clean['Date'].unique())
        train_end_idx = int(len(unique_dates) * 0.70)
        train_dates = unique_dates[:train_end_idx]
        train_df = df_clean[df_clean['Date'].isin(train_dates)].copy()
    else:
        train_df = df_clean
        
    preprocessor.fit(train_df)
    return preprocessor

@st.cache_resource(show_spinner=False)
def load_ml_pipeline():
    """
    Robust ML Pipeline Loader:
    1. Loads XGBoost model (prefers portable native JSON, falls back to PKL).
    2. Loads Preprocessing Pipeline (tries PKL, auto-reconstructs on ANY deserialization error).
    3. Loads Elasticity table (prefers CSV, falls back to PKL).
    """
    # 1. Load Demand Model
    model = None
    json_model_path = os.path.join("models", "demand_model.json")
    pkl_model_path = os.path.join("models", "demand_model.pkl")
    
    if os.path.exists(json_model_path):
        try:
            import xgboost as xgb
            model = xgb.XGBRegressor()
            model.load_model(json_model_path)
        except Exception as e:
            logger.warning(f"Native JSON model load failed: {e}. Falling back to pickle.")
            model = None

    if model is None and os.path.exists(pkl_model_path):
        try:
            model = joblib.load(pkl_model_path)
        except Exception as e:
            logger.error(f"Pickle model load failed: {e}")
            model = None

    # 2. Load Preprocessing Pipeline
    preprocessor = None
    pipe_path = os.path.join("models", "preprocessing_pipeline.pkl")
    if os.path.exists(pipe_path):
        try:
            preprocessor = joblib.load(pipe_path)
            # Verify preprocessor transforms without error
            dummy = load_master_data().head(2)
            if len(dummy) > 0:
                _ = preprocessor.transform(dummy)
        except Exception as e:
            logger.warning(f"Deserializing preprocessing_pipeline.pkl encountered compatibility error ({e}). Reconstructing preprocessor from project data.")
            preprocessor = None

    if preprocessor is None:
        try:
            preprocessor = reconstruct_preprocessor()
        except Exception as e:
            logger.error(f"Preprocessor reconstruction failed: {e}")
            preprocessor = None

    # 3. Load Elasticity Table
    elasticity_df = None
    csv_el_path = os.path.join("models", "elasticity_model.csv")
    pkl_el_path = os.path.join("models", "elasticity_model.pkl")

    if os.path.exists(csv_el_path):
        try:
            elasticity_df = pd.read_csv(csv_el_path)
        except Exception as e:
            logger.warning(f"CSV elasticity load failed: {e}")
            elasticity_df = None

    if elasticity_df is None and os.path.exists(pkl_el_path):
        try:
            elasticity_df = joblib.load(pkl_el_path)
        except Exception as e:
            logger.error(f"Pickle elasticity load failed: {e}")
            elasticity_df = None

    return model, preprocessor, elasticity_df

def run_startup_diagnostics():
    """
    Validates the end-to-end operational health of the application.
    Returns a dict with diagnostic check statuses.
    """
    diag = {}
    
    df = load_master_data()
    diag["dataset_loaded"] = len(df) > 0
    diag["dataset_rows"] = len(df)
    
    model, preprocessor, elas = load_ml_pipeline()
    diag["model_available"] = model is not None
    diag["preprocessor_available"] = preprocessor is not None
    diag["elasticity_available"] = elas is not None and len(elas) > 0
    
    if model is not None and preprocessor is not None and len(df) > 0:
        try:
            sample = df.head(5)
            X = preprocessor.transform(sample)
            diag["feature_count"] = X.shape[1]
            diag["feature_shape_valid"] = (X.shape[1] == 53)
            preds = model.predict(X)
            diag["prediction_test"] = len(preds) == 5 and not np.isnan(preds).any()
        except Exception as e:
            diag["prediction_test"] = False
            diag["prediction_error"] = str(e)
    else:
        diag["feature_shape_valid"] = False
        diag["prediction_test"] = False
        
    return diag
