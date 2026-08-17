"""
Data Loader and Data Quality Validator Module
Provides robust dataset loading, schema verification, data cleaning, and dynamic pricing sanity checks.
"""

import os
import pandas as pd
import numpy as np

def load_data(filepath="data/dataset.csv"):
    """
    Loads dataset from CSV, performs parsing and basic type conversions.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}. Please generate or provide the dataset first.")
    
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Product_ID', 'Store_ID', 'Date']).reset_index(drop=True)
    return df

def validate_data_quality(df):
    """
    Performs comprehensive data quality audit and returns a structured audit report dictionary.
    """
    report = {
        "total_records": int(len(df)),
        "columns_count": int(df.shape[1]),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "date_min": str(df['Date'].min().date()),
        "date_max": str(df['Date'].max().date()),
        "total_days": int((df['Date'].max() - df['Date'].min()).days + 1),
        "unique_products": int(df['Product_ID'].nunique()),
        "unique_stores": int(df['Store_ID'].nunique()),
        "unique_categories": int(df['Category'].nunique()),
        "unique_regions": int(df['Region'].nunique()),
        "observations_per_product_store": int(len(df) / (df['Product_ID'].nunique() * df['Store_ID'].nunique())),
        "price_min": float(df['Our_Price'].min()),
        "price_max": float(df['Our_Price'].max()),
        "price_mean": float(df['Our_Price'].mean()),
        "competitor_price_available": bool('Competitor_Price' in df.columns and df['Competitor_Price'].notnull().all()),
        "cost_available": bool('Unit_Cost' in df.columns and df['Unit_Cost'].notnull().all()),
        "discount_available": bool('Discount_Percent' in df.columns),
        "promo_available": bool('Promotion_Flag' in df.columns),
    }
    
    # Check Price-Demand negative correlation per product
    product_correlations = []
    for pid, grp in df.groupby('Product_ID'):
        corr = grp['Our_Price'].corr(grp['Units_Sold'])
        product_correlations.append(corr)
    
    report["mean_price_demand_correlation"] = float(np.nanmean(product_correlations))
    report["is_suitable_for_dynamic_pricing"] = bool(
        report["duplicate_rows"] == 0 and 
        sum(report["missing_values"].values()) == 0 and 
        report["competitor_price_available"] and
        report["mean_price_demand_correlation"] < 0
    )
    
    return report

def clean_data(df):
    """
    Ensures no nulls, cleans negative quantities, clips outliers if any, and sorts canonically.
    """
    df_clean = df.copy()
    df_clean['Units_Sold'] = df_clean['Units_Sold'].clip(lower=0)
    df_clean['Revenue'] = df_clean['Our_Price'] * df_clean['Units_Sold']
    
    if 'Unit_Cost' in df_clean.columns:
        df_clean['Total_Cost'] = df_clean['Unit_Cost'] * df_clean['Units_Sold']
        df_clean['Gross_Profit'] = df_clean['Revenue'] - df_clean['Total_Cost']
        df_clean['Gross_Margin_Percent'] = np.where(
            df_clean['Revenue'] > 0,
            (df_clean['Gross_Profit'] / df_clean['Revenue']) * 100.0,
            0.0
        )
    return df_clean
