"""
Dynamic Pricing Dataset Generator
Generates an industry-grade, econometrically grounded retail panel dataset
with authentic price elasticity, cross-price competitor effects, holiday seasonality,
cost structures, and operational inventory constraints.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_retail_dataset(start_date="2024-01-01", end_date="2025-12-31", random_seed=42):
    np.random.seed(random_seed)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(dates)
    
    products = [
        # Electronics (Highly Elastic: -1.4 to -2.1)
        {"id": "PROD_01", "name": "Wireless Noise-Canceling Headphones", "category": "Electronics", "base_price": 2999.0, "cost": 1750.0, "base_demand": 45, "elasticity": -1.85, "cross_elasticity": 0.55},
        {"id": "PROD_02", "name": "Smart Fitness Watch", "category": "Electronics", "base_price": 4499.0, "cost": 2600.0, "base_demand": 30, "elasticity": -2.05, "cross_elasticity": 0.65},
        {"id": "PROD_03", "name": "Portable Bluetooth Speaker", "category": "Electronics", "base_price": 1499.0, "cost": 850.0, "base_demand": 60, "elasticity": -1.65, "cross_elasticity": 0.45},
        {"id": "PROD_04", "name": "Fast-Charging 20000mAh Power Bank", "category": "Electronics", "base_price": 999.0, "cost": 550.0, "base_demand": 80, "elasticity": -1.45, "cross_elasticity": 0.40},
        
        # Groceries & Staples (Inelastic: -0.45 to -0.75)
        {"id": "PROD_05", "name": "Organic Basmati Rice 5kg", "category": "Groceries", "base_price": 450.0, "cost": 330.0, "base_demand": 120, "elasticity": -0.50, "cross_elasticity": 0.20},
        {"id": "PROD_06", "name": "Extra Virgin Olive Oil 1L", "category": "Groceries", "base_price": 850.0, "cost": 620.0, "base_demand": 50, "elasticity": -0.65, "cross_elasticity": 0.25},
        {"id": "PROD_07", "name": "Premium Arabica Coffee Beans 500g", "category": "Groceries", "base_price": 599.0, "cost": 410.0, "base_demand": 70, "elasticity": -0.75, "cross_elasticity": 0.30},
        {"id": "PROD_08", "name": "Almond & Oat Milk 1L Pack of 3", "category": "Groceries", "base_price": 380.0, "cost": 270.0, "base_demand": 90, "elasticity": -0.55, "cross_elasticity": 0.22},
        
        # Apparel & Footwear (Moderately Elastic: -1.2 to -1.55)
        {"id": "PROD_09", "name": "Breathable Running Shoes", "category": "Apparel", "base_price": 2499.0, "cost": 1350.0, "base_demand": 40, "elasticity": -1.55, "cross_elasticity": 0.50},
        {"id": "PROD_10", "name": "Classic Denim Jacket", "category": "Apparel", "base_price": 1999.0, "cost": 1100.0, "base_demand": 35, "elasticity": -1.40, "cross_elasticity": 0.42},
        {"id": "PROD_11", "name": "Organic Cotton Crew-Neck T-Shirt", "category": "Apparel", "base_price": 699.0, "cost": 340.0, "base_demand": 110, "elasticity": -1.25, "cross_elasticity": 0.35},
        {"id": "PROD_12", "name": "High-Waist Performance Yoga Pants", "category": "Apparel", "base_price": 1299.0, "cost": 720.0, "base_demand": 55, "elasticity": -1.35, "cross_elasticity": 0.45},
        
        # Home & Kitchen (Moderately Elastic: -1.3 to -1.7)
        {"id": "PROD_13", "name": "Digital Touchscreen Air Fryer 4.5L", "category": "Home & Kitchen", "base_price": 3999.0, "cost": 2300.0, "base_demand": 25, "elasticity": -1.70, "cross_elasticity": 0.60},
        {"id": "PROD_14", "name": "High-Speed Smoothie Blender 900W", "category": "Home & Kitchen", "base_price": 2199.0, "cost": 1250.0, "base_demand": 40, "elasticity": -1.50, "cross_elasticity": 0.48},
        {"id": "PROD_15", "name": "Non-Stick Ceramic Cookware Set 3pc", "category": "Home & Kitchen", "base_price": 2799.0, "cost": 1600.0, "base_demand": 30, "elasticity": -1.45, "cross_elasticity": 0.44},
        {"id": "PROD_16", "name": "Stainless Steel Electric Kettle 1.8L", "category": "Home & Kitchen", "base_price": 899.0, "cost": 490.0, "base_demand": 75, "elasticity": -1.30, "cross_elasticity": 0.38},
        
        # Health & Personal Care (Inelastic to Moderate: -0.6 to -1.1)
        {"id": "PROD_17", "name": "Whey Isolate Protein Powder 1kg", "category": "Health & Care", "base_price": 2899.0, "cost": 1950.0, "base_demand": 45, "elasticity": -0.85, "cross_elasticity": 0.35},
        {"id": "PROD_18", "name": "Daily Multivitamin & Mineral 60s", "category": "Health & Care", "base_price": 499.0, "cost": 280.0, "base_demand": 100, "elasticity": -0.60, "cross_elasticity": 0.20},
        {"id": "PROD_19", "name": "Vitamin C Radiance Face Serum 30ml", "category": "Health & Care", "base_price": 649.0, "cost": 330.0, "base_demand": 65, "elasticity": -1.05, "cross_elasticity": 0.40},
        {"id": "PROD_20", "name": "Broad-Spectrum Sunscreen Gel SPF50", "category": "Health & Care", "base_price": 420.0, "cost": 220.0, "base_demand": 85, "elasticity": -0.70, "cross_elasticity": 0.28},
    ]
    
    stores = [
        {"id": "STORE_01", "name": "Delhi Flagship Metro", "region": "North", "store_factor": 1.25},
        {"id": "STORE_02", "name": "Bengaluru Tech Park Store", "region": "South", "store_factor": 1.15},
        {"id": "STORE_03", "name": "Mumbai High Street Mall", "region": "West", "store_factor": 1.30},
        {"id": "STORE_04", "name": "Kolkata City Center", "region": "East", "store_factor": 0.90},
    ]
    
    records = []
    
    for prod in products:
        p_id = prod["id"]
        p_name = prod["name"]
        cat = prod["category"]
        base_p = prod["base_price"]
        cost = prod["cost"]
        base_q = prod["base_demand"]
        own_el = prod["elasticity"]
        cross_el = prod["cross_elasticity"]
        
        # Monthly cost fluctuation (inflation / supply chain drift)
        cost_series = cost * (1.0 + 0.04 * np.sin(np.linspace(0, 4*np.pi, n_days)) + np.random.normal(0, 0.01, n_days))
        
        for store in stores:
            s_id = store["id"]
            s_name = store["name"]
            region = store["region"]
            s_factor = store["store_factor"]
            
            # Competitor pricing dynamic: fluctuating around base price with periodic strategic cuts/increases
            comp_drift = np.sin(np.linspace(0, 8*np.pi, n_days) + np.random.uniform(0, 2*np.pi)) * 0.06
            comp_noise = np.random.normal(0, 0.025, n_days)
            competitor_price = np.round(base_p * (1.0 + comp_drift + comp_noise), 2)
            
            # Our pricing strategy: dynamic promotions, weekend markdowns, competitor matching
            discount_pcts = np.zeros(n_days)
            promo_flags = np.zeros(n_days, dtype=int)
            
            for d_idx, dt in enumerate(dates):
                # Weekend discount probability
                is_weekend = dt.weekday() >= 5
                # Holiday seasons (Oct-Nov Diwali, Late Dec New Year, July Monsoon Sale)
                is_festive = (dt.month in [10, 11] and dt.day in [10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25]) or \
                             (dt.month == 12 and dt.day >= 20) or (dt.month == 7 and dt.day <= 10)
                
                promo_prob = 0.35 if is_festive else (0.20 if is_weekend else 0.08)
                if np.random.rand() < promo_prob:
                    promo_flags[d_idx] = 1
                    discount_pcts[d_idx] = np.random.choice([5.0, 10.0, 15.0, 20.0, 25.0], p=[0.35, 0.30, 0.20, 0.10, 0.05])
                else:
                    # Occasional everyday price adjustment (0% to 5% variance)
                    discount_pcts[d_idx] = np.random.choice([0.0, 2.0, 4.0], p=[0.80, 0.12, 0.08])
            
            our_price = np.round(base_p * (1.0 - discount_pcts / 100.0), 2)
            
            # Ensure price never below cost + 5% floor
            min_price_floor = np.round(cost_series * 1.05, 2)
            our_price = np.maximum(our_price, min_price_floor)
            
            for d_idx, dt in enumerate(dates):
                cur_our_p = our_price[d_idx]
                cur_comp_p = competitor_price[d_idx]
                cur_cost = np.round(cost_series[d_idx], 2)
                cur_disc = discount_pcts[d_idx]
                cur_promo = promo_flags[d_idx]
                
                # Seasonality & Calendar multiplier
                day_of_week = dt.weekday()
                dow_mult = 1.25 if day_of_week in [5, 6] else (1.10 if day_of_week == 4 else 0.95)
                
                month = dt.month
                month_mult = 1.30 if month in [10, 11, 12] else (1.15 if month in [6, 7] else 0.95)
                
                # Econometric Demand Calculation (Log-Log Form)
                # ln(Q) = ln(base_Q * s_factor * dow * month) + beta * ln(Our_P / Base_P) + gamma * ln(Comp_P / Base_P) + delta * Promo + noise
                log_base = np.log(base_q * s_factor * dow_mult * month_mult)
                price_ratio_own = cur_our_p / base_p
                price_ratio_comp = cur_comp_p / base_p
                
                elasticity_impact = own_el * np.log(price_ratio_own)
                cross_elasticity_impact = cross_el * np.log(price_ratio_comp)
                promo_impact = 0.25 * cur_promo
                
                noise = np.random.normal(0, 0.12)
                
                expected_log_q = log_base + elasticity_impact + cross_elasticity_impact + promo_impact + noise
                q_simulated = np.exp(expected_log_q)
                
                # Inventory capacity & availability
                base_inv = base_q * s_factor * 8
                inv_noise = np.random.normal(0, 0.15)
                inventory = int(np.clip(base_inv * (1 + inv_noise), 20, 2000))
                
                units_sold = int(np.clip(np.round(q_simulated), 0, inventory))
                
                revenue = np.round(cur_our_p * units_sold, 2)
                total_cost = np.round(cur_cost * units_sold, 2)
                profit = np.round(revenue - total_cost, 2)
                margin_pct = np.round((profit / revenue * 100.0) if revenue > 0 else 0.0, 2)
                
                price_diff = np.round(cur_our_p - cur_comp_p, 2)
                price_ratio = np.round(cur_our_p / cur_comp_p, 4)
                price_premium_pct = np.round(((cur_our_p - cur_comp_p) / cur_comp_p) * 100.0, 2)
                
                records.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Product_ID": p_id,
                    "Product_Name": p_name,
                    "Category": cat,
                    "Store_ID": s_id,
                    "Store_Name": s_name,
                    "Region": region,
                    "Base_Price": base_p,
                    "Our_Price": cur_our_p,
                    "Competitor_Price": cur_comp_p,
                    "Discount_Percent": cur_disc,
                    "Promotion_Flag": cur_promo,
                    "Unit_Cost": cur_cost,
                    "Inventory_Level": inventory,
                    "Units_Sold": units_sold,
                    "Revenue": revenue,
                    "Total_Cost": total_cost,
                    "Gross_Profit": profit,
                    "Gross_Margin_Percent": margin_pct,
                    "Price_Difference": price_diff,
                    "Price_Ratio": price_ratio,
                    "Price_Premium_Percent": price_premium_pct
                })
                
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    print("Generating industry-grade retail dynamic pricing dataset...")
    df = generate_retail_dataset()
    output_path = "data/dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created at '{output_path}'.")
    print(f"Shape: {df.shape}")
    print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Products: {df['Product_ID'].nunique()}, Stores: {df['Store_ID'].nunique()}, Categories: {df['Category'].nunique()}")
    print(f"Total Revenue: INR {df['Revenue'].sum():,.2f}")
    print(f"Total Units Sold: {df['Units_Sold'].sum():,}")
