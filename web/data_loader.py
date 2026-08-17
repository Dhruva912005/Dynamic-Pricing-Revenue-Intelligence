"""
Data loading and caching module for Streamlit Web Application.
Uses relative file paths for cloud-ready deployment.
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

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

@st.cache_resource(show_spinner=False)
def load_ml_pipeline():
    """
    Loads serialized XGBoost model, preprocessing pipeline, and elasticity table.
    """
    model_path = os.path.join("models", "demand_model.pkl")
    pipe_path = os.path.join("models", "preprocessing_pipeline.pkl")
    el_path = os.path.join("models", "elasticity_model.pkl")
    
    model = joblib.load(model_path) if os.path.exists(model_path) else None
    preprocessor = joblib.load(pipe_path) if os.path.exists(pipe_path) else None
    elasticity_df = joblib.load(el_path) if os.path.exists(el_path) else None
    
    return model, preprocessor, elasticity_df
