"""
Forecast service module for model evaluation, holdout test time-series curves,
and feature importance charts in Streamlit web app.
"""

import pandas as pd
import numpy as np

def filter_forecast_data(forecast_df, product_id=None, store_id=None, category=None, date_range=None):
    """
    Filters test forecast dataset by selected dimensions.
    """
    if forecast_df is None or len(forecast_df) == 0:
        return pd.DataFrame()
        
    df = forecast_df.copy()
    if product_id and product_id != "All Products":
        df = df[df["Product_ID"] == product_id]
    if store_id and store_id != "All Stores":
        df = df[df["Store_ID"] == store_id]
    if category and category != "All Categories":
        df = df[df["Category"] == category]
    if date_range and len(date_range) == 2:
        df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]
        
    # Aggregate daily demand if multiple products/stores are selected
    daily = df.groupby("Date").agg({
        "Actual_Demand": "sum",
        "Forecast_XGBoost": "sum"
    }).reset_index().sort_values("Date")
    
    return daily

def get_top_features(feat_imp_df, top_n=12):
    """
    Retrieves top N predictive drivers with readable names.
    """
    if feat_imp_df is None or len(feat_imp_df) == 0:
        return pd.DataFrame()
        
    df = feat_imp_df.head(top_n).copy()
    # Format readable labels
    name_map = {
        "Demand_Rolling_Mean_14": "14-Day Demand Rolling Mean",
        "Promotion_Flag": "Promotional Event Active",
        "Demand_Rolling_Mean_7": "7-Day Demand Rolling Mean",
        "Discount_Percent": "Discount Depth %",
        "Demand_Rolling_Mean_28": "28-Day Demand Rolling Mean",
        "DayOfWeek": "Day of Week (Weekend Effect)",
        "Demand_Lag_7": "7-Day Volume Lag",
        "Demand_Lag_1": "1-Day Volume Lag",
        "Demand_Lag_28": "28-Day Volume Lag",
        "Price_Ratio": "Price vs Competitor Ratio",
        "Our_Price": "Our Selling Price",
        "Competitor_Price": "Competitor Selling Price",
        "Month": "Calendar Month",
        "Season": "Retail Season (Festive/Monsoon)"
    }
    df["Feature_Label"] = df["Feature"].apply(lambda x: name_map.get(x, x.replace("_", " ")))
    return df
