"""
Feature Engineering Module
Implements strictly leakage-free lag, rolling, time, and pricing features.
Includes reusable preprocessing pipeline compatible with dynamic price simulation.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def create_time_features(df):
    """
    Extracts rich calendar and seasonal features from Date.
    """
    df = df.copy()
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Quarter'] = df['Date'].dt.quarter
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
    df['Is_Weekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
    
    # Seasonality in retail context (1: Winter, 2: Spring, 3: Monsoon/Summer, 4: Festive/Q4)
    df['Season'] = df['Month'].apply(lambda m: 4 if m in [10, 11, 12] else (3 if m in [6, 7, 8, 9] else (2 if m in [3, 4, 5] else 1)))
    return df

def create_lag_and_rolling_features(df):
    """
    Generates historical demand lags and rolling averages strictly using .shift(1)
    to prevent target leakage. Computed per (Product_ID, Store_ID) panel.
    """
    df = df.copy()
    df = df.sort_values(by=['Product_ID', 'Store_ID', 'Date']).reset_index(drop=True)
    
    # Target lags
    for lag in [1, 7, 14, 28]:
        df[f'Demand_Lag_{lag}'] = df.groupby(['Product_ID', 'Store_ID'])['Units_Sold'].shift(lag)
        
    # Rolling means strictly shifted by 1 day
    for window in [7, 14, 28]:
        df[f'Demand_Rolling_Mean_{window}'] = (
            df.groupby(['Product_ID', 'Store_ID'])['Units_Sold']
            .shift(1)
            .rolling(window=window, min_periods=1)
            .mean()
        )
        
    df['Demand_Rolling_Std_7'] = (
        df.groupby(['Product_ID', 'Store_ID'])['Units_Sold']
        .shift(1)
        .rolling(window=7, min_periods=1)
        .std()
        .fillna(0)
    )
    
    return df

def create_pricing_features(df):
    """
    Generates competitive pricing signals and relative discount features.
    """
    df = df.copy()
    df['Price_Difference'] = df['Our_Price'] - df['Competitor_Price']
    df['Price_Ratio'] = df['Our_Price'] / (df['Competitor_Price'] + 1e-6)
    df['Price_Premium_Percent'] = ((df['Our_Price'] - df['Competitor_Price']) / (df['Competitor_Price'] + 1e-6)) * 100.0
    
    # Historical base price ratio
    if 'Base_Price' in df.columns:
        df['Discount_From_Base'] = ((df['Base_Price'] - df['Our_Price']) / (df['Base_Price'] + 1e-6)) * 100.0
    else:
        df['Discount_From_Base'] = df.get('Discount_Percent', 0.0)
        
    return df

def build_feature_pipeline(categorical_cols, numerical_cols):
    """
    Constructs a Scikit-Learn ColumnTransformer pipeline for categorical encoding and scaling.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ],
        remainder='drop'
    )
    return preprocessor
