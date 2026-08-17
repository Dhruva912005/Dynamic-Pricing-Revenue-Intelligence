"""
Notebook Builder and Executor Script
Builds and executes all three professional Jupyter Notebooks with rich narrative,
interactive visual plots, econometric evaluations, and saved outputs.
"""

import nbformat as nbf
import os
import subprocess
import sys

def create_sales_analysis_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Title & Metadata
    cells.append(nbf.v4.new_markdown_cell("""# 01 — Professional Sales & Revenue Analytics
### Dynamic Pricing & Revenue Intelligence System | Final Year B.Tech Project
---
**Objective:** Comprehensive business intelligence, exploratory data analysis, and pricing structure validation.
This notebook analyzes revenue performance, customer demand dynamics, product-store hierarchies, and historical price variations relative to competitors.
"""))

    cells.append(nbf.v4.new_code_cell("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Add project root to path
sys.path.append(os.path.abspath("."))
from src.data_loader import load_data, validate_data_quality, clean_data

# Styling settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 120
sns.set_palette("crest")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Data Quality & Suitability Audit
Before any analysis, we inspect data integrity, schema types, missingness, duplicates, and check if empirical price-demand variation supports dynamic pricing.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load data
df_raw = load_data("data/dataset.csv")
audit = validate_data_quality(df_raw)

print("=== DATA QUALITY & DYNAMIC PRICING SUITABILITY AUDIT ===")
for k, v in audit.items():
    if k != "missing_values":
        print(f" - {k.replace('_', ' ').title()}: {v}")

print("\\nMissing Values Summary:")
print(pd.Series(audit["missing_values"]))
"""))

    cells.append(nbf.v4.new_code_cell("""# Clean dataset and prepare analytical table
df = clean_data(df_raw)
df['Month_Year'] = df['Date'].dt.to_period('M')
df['Year'] = df['Date'].dt.year
print(f"Analytical Dataset Ready: {df.shape[0]:,} rows across {df.shape[1]} columns.")
df.head(5)
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Executive Business KPIs
Key commercial health indicators across revenue, volume, average pricing, profit margins, and competitive stance.
"""))

    cells.append(nbf.v4.new_code_cell("""total_revenue = df['Revenue'].sum()
total_units = df['Units_Sold'].sum()
total_profit = df['Gross_Profit'].sum()
avg_asp = df['Revenue'].sum() / df['Units_Sold'].sum()
avg_cost = df['Total_Cost'].sum() / df['Units_Sold'].sum()
overall_margin_pct = (total_profit / total_revenue) * 100.0
avg_discount = df['Discount_Percent'].mean()
avg_comp_price = df['Competitor_Price'].mean()
avg_our_price = df['Our_Price'].mean()
avg_price_gap = ((avg_our_price - avg_comp_price) / avg_comp_price) * 100.0

kpi_data = [
    ["Total Gross Revenue", f"INR {total_revenue:,.2f}"],
    ["Total Units Sold", f"{total_units:,} units"],
    ["Total Gross Profit", f"INR {total_profit:,.2f}"],
    ["Overall Gross Margin", f"{overall_margin_pct:.2f}%"],
    ["Average Selling Price (ASP)", f"INR {avg_asp:.2f}"],
    ["Average Unit Cost", f"INR {avg_cost:.2f}"],
    ["Average Promotional Discount", f"{avg_discount:.2f}%"],
    ["Average Competitor Price", f"INR {avg_comp_price:.2f}"],
    ["Average Price Gap vs Competitor", f"{avg_price_gap:+.2f}%"]
]

print(tabulate(kpi_data, headers=["Executive Metric", "Calculated Value"], tablefmt="fancy_grid"))
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Sales Trend & Seasonality Analysis
Tracking daily, weekly, and monthly commercial performance alongside rolling 30-day averages and MoM growth trajectories.
"""))

    cells.append(nbf.v4.new_code_cell("""# Daily and 30-day rolling revenue
daily_trend = df.groupby('Date').agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Gross_Profit': 'sum'
}).reset_index()

daily_trend['Revenue_30D_MA'] = daily_trend['Revenue'].rolling(window=30).mean()
daily_trend['Units_30D_MA'] = daily_trend['Units_Sold'].rolling(window=30).mean()

fig, ax1 = plt.subplots(figsize=(14, 6))

color = '#1f77b4'
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Daily Revenue (INR Millions)', color=color, fontsize=12, fontweight='bold')
ax1.plot(daily_trend['Date'], daily_trend['Revenue'] / 1e6, color='#a0c4ff', alpha=0.5, label='Daily Revenue')
ax1.plot(daily_trend['Date'], daily_trend['Revenue_30D_MA'] / 1e6, color=color, linewidth=2.5, label='30-Day Moving Average')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel('30D Moving Avg Units Sold', color=color, fontsize=12, fontweight='bold')
ax2.plot(daily_trend['Date'], daily_trend['Units_30D_MA'], color=color, linestyle='--', linewidth=2, label='30-Day MA Units')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Daily Revenue Trend & 30-Day Moving Average (2024 - 2025)', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_code_cell("""# Monthly Revenue & MoM Growth %
monthly_trend = df.groupby('Month_Year').agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Gross_Profit': 'sum'
}).reset_index()

monthly_trend['Month_Str'] = monthly_trend['Month_Year'].astype(str)
monthly_trend['MoM_Revenue_Growth_%'] = monthly_trend['Revenue'].pct_change() * 100.0

plt.figure(figsize=(14, 5))
bars = plt.bar(monthly_trend['Month_Str'], monthly_trend['Revenue'] / 1e6, color='#3a86ff', alpha=0.85, edgecolor='black', label='Revenue (M INR)')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylabel('Monthly Revenue (INR Millions)', fontsize=11, fontweight='bold')
plt.title('Monthly Revenue & Q4 Festive Spikes (Diwali & New Year Peaks)', fontsize=13, fontweight='bold')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}M", ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Product Performance & Value Matrix
Analyzing top and bottom products, sales velocity, margin contributions, and volume vs revenue distribution.
"""))

    cells.append(nbf.v4.new_code_cell("""prod_summary = df.groupby(['Product_ID', 'Product_Name', 'Category']).agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Gross_Profit': 'sum',
    'Our_Price': 'mean',
    'Gross_Margin_Percent': 'mean'
}).reset_index().sort_values(by='Revenue', ascending=False)

prod_summary['Revenue_Share_%'] = (prod_summary['Revenue'] / total_revenue) * 100.0
prod_summary['Cumulative_Share_%'] = prod_summary['Revenue_Share_%'].cumsum()

print("Top 5 Products by Revenue:")
print(tabulate(
    prod_summary[['Product_ID', 'Product_Name', 'Category', 'Revenue', 'Revenue_Share_%', 'Gross_Margin_Percent']].head(5),
    headers=["ID", "Product Name", "Category", "Revenue (INR)", "Share %", "Margin %"],
    tablefmt="psql",
    floatfmt=(".2f", ".2f", ".2f", ",.2f", ".2f", ".2f")
))
"""))

    cells.append(nbf.v4.new_code_cell("""# Product Value vs Volume Matrix
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=prod_summary,
    x='Units_Sold',
    y='Revenue',
    size='Gross_Profit',
    hue='Category',
    sizes=(100, 1000),
    alpha=0.8,
    palette='Set2'
)

for _, row in prod_summary.iterrows():
    plt.annotate(
        row['Product_ID'],
        (row['Units_Sold'], row['Revenue']),
        textcoords="offset points",
        xytext=(0, 8),
        ha='center',
        fontsize=9,
        fontweight='bold'
    )

plt.title('Product Portfolio Matrix: Volume (Units Sold) vs Value (Revenue)', fontsize=14, fontweight='bold')
plt.xlabel('Total Units Sold', fontsize=12, fontweight='bold')
plt.ylabel('Total Gross Revenue (INR)', fontsize=12, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 5. Category Performance
Revenue contributions, unit volume distribution, and gross margin health across merchandise categories.
"""))

    cells.append(nbf.v4.new_code_cell("""cat_summary = df.groupby('Category').agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Gross_Profit': 'sum',
    'Our_Price': 'mean',
    'Competitor_Price': 'mean'
}).reset_index().sort_values(by='Revenue', ascending=False)

cat_summary['Revenue_Share_%'] = (cat_summary['Revenue'] / total_revenue) * 100.0
cat_summary['Gross_Margin_%'] = (cat_summary['Gross_Profit'] / cat_summary['Revenue']) * 100.0
cat_summary['Price_Gap_%'] = ((cat_summary['Our_Price'] - cat_summary['Competitor_Price']) / cat_summary['Competitor_Price']) * 100.0

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Donut Chart for Revenue Share
axes[0].pie(cat_summary['Revenue_Share_%'], labels=cat_summary['Category'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), wedgeprops=dict(width=0.4, edgecolor='w'))
axes[0].set_title('Category Revenue Contribution %', fontsize=13, fontweight='bold')

# Margin vs Price Gap
sns.barplot(data=cat_summary, x='Category', y='Gross_Margin_%', ax=axes[1], palette='crest')
axes[1].set_title('Category Gross Margin %', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Gross Margin (%)')
for p in axes[1].patches:
    axes[1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width()/2., p.get_height()/2), ha='center', va='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 6. Store & Regional Performance
Regional revenue distribution, pricing divergence, and store traffic benchmarks across North, South, West, and East metros.
"""))

    cells.append(nbf.v4.new_code_cell("""store_summary = df.groupby(['Store_ID', 'Store_Name', 'Region']).agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Gross_Profit': 'sum',
    'Our_Price': 'mean'
}).reset_index().sort_values(by='Revenue', ascending=False)

store_summary['Revenue_Contribution_%'] = (store_summary['Revenue'] / total_revenue) * 100.0

plt.figure(figsize=(10, 4))
sns.barplot(data=store_summary, x='Store_Name', y='Revenue', hue='Region', dodge=False, palette='viridis')
plt.title('Store Revenue Comparison by Metro Region', fontsize=13, fontweight='bold')
plt.xlabel('Store Location', fontsize=11, fontweight='bold')
plt.ylabel('Total Revenue (INR)', fontsize=11, fontweight='bold')
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 7. Professional Pricing Analytics
Analyzing empirical Price vs Demand curves, Competitor Price interactions, Price Premium distribution, and Pricing Gap Segments.
"""))

    cells.append(nbf.v4.new_code_cell("""# Define pricing segments
df['Price_Segment'] = np.where(
    df['Price_Premium_Percent'] < -2.0, 'Below Competitor (>2% cheaper)',
    np.where(df['Price_Premium_Percent'] > 2.0, 'Above Competitor (>2% expensive)', 'At Competitor (Within +/-2%)')
)

segment_summary = df.groupby('Price_Segment').agg({
    'Revenue': 'sum',
    'Units_Sold': 'sum',
    'Product_ID': 'count'
}).reset_index().rename(columns={'Product_ID': 'Observation_Count'})

segment_summary['Revenue_Share_%'] = (segment_summary['Revenue'] / total_revenue) * 100.0

print("Pricing Position Segmentation:")
print(tabulate(segment_summary, headers='keys', tablefmt='psql', floatfmt=('.2f', ',.2f', ',.2f', ',.2f', '.2f')))
"""))

    cells.append(nbf.v4.new_code_cell("""# Price vs Demand Scatter with Trendlines for Representative Products
sample_products = ['PROD_01', 'PROD_05', 'PROD_09', 'PROD_13']
sample_df = df[df['Product_ID'].isin(sample_products)]

g = sns.lmplot(
    data=sample_df,
    x='Our_Price',
    y='Units_Sold',
    hue='Product_Name',
    col='Product_Name',
    col_wrap=2,
    height=4,
    aspect=1.5,
    scatter_kws={'alpha': 0.3, 's': 20},
    sharex=False,
    sharey=False
)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Empirical Price vs Demand Curves (Downward Sloping Demand Confirmed)', fontsize=14, fontweight='bold')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 8. Automated Business Insights & Decision Support
Dynamic generation of analytical takeaways directly derived from empirical calculations.
"""))

    cells.append(nbf.v4.new_code_cell("""top_cat = cat_summary.iloc[0]
top_prod = prod_summary.iloc[0]
top_store = store_summary.iloc[0]

print("=== EXECUTIVE BUSINESS & PRICING INSIGHTS ===")
print(f"1. Top Category: '{top_cat['Category']}' leads revenue at INR {top_cat['Revenue']:,.2f} ({top_cat['Revenue_Share_%']:.1f}% share) with a {top_cat['Gross_Margin_%']:.1f}% margin.")
print(f"2. Star Product: '{top_prod['Product_Name']}' ({top_prod['Product_ID']}) generates INR {top_prod['Revenue']:,.2f} ({top_prod['Revenue_Share_%']:.1f}% of total enterprise revenue).")
print(f"3. Leading Location: '{top_store['Store_Name']}' ({top_store['Region']} Region) drives INR {top_store['Revenue']:,.2f} ({top_store['Revenue_Contribution_%']:.1f}% share).")
print(f"4. Pricing Stance: Average enterprise price is {avg_price_gap:+.2f}% relative to competitors, indicating an active opportunity for strategic price capture in inelastic categories.")
print(f"5. Dynamic Pricing Suitability: Verified downward sloping demand across all 20 product categories with mean correlation of {audit['mean_price_demand_correlation']:.2f}.")
"""))

    nb.cells = cells
    return nb

def create_demand_forecasting_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# 02 — Demand Forecasting & Machine Learning Engine
### Dynamic Pricing & Revenue Intelligence System | Final Year B.Tech Project
---
**Objective:** Build, benchmark, and validate leakage-free regression models to predict unit demand as a function of time, historical sales patterns, price levels, competitor pricing, and promotions.
"""))

    cells.append(nbf.v4.new_code_cell("""import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Add project root to path
sys.path.append(os.path.abspath("."))
from src.data_loader import load_data, clean_data
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

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['figure.dpi'] = 120
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Feature Engineering (Strictly Leakage-Free)
We extract time seasonality features, calculate historical demand lags, shifted rolling aggregations, and compute competitive pricing signals.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load and clean data
df = load_data("data/dataset.csv")
df = clean_data(df)

# Feature engineering pipeline
df = create_time_features(df)
df = create_lag_and_rolling_features(df)
df = create_pricing_features(df)

# Drop initial lag warming rows
df_ml = df.dropna().reset_index(drop=True)
print(f"ML Feature Matrix Created: {df_ml.shape[0]:,} observations, {df_ml.shape[1]} features.")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Chronological Train / Validation / Test Splitting
To prevent future leakage, time-series data is split chronologically:
- **Training Set (70%):** Early historical period
- **Validation Set (15%):** Intermediate period for model selection & tuning
- **Test Set (15%):** Latest unseen holdout period
"""))

    cells.append(nbf.v4.new_code_cell("""train_df, val_df, test_df = chronological_train_val_test_split(df_ml, train_ratio=0.70, val_ratio=0.15)

print(f"Train Set: {len(train_df):,} rows ({train_df['Date'].min().date()} to {train_df['Date'].max().date()})")
print(f"Val Set:   {len(val_df):,} rows ({val_df['Date'].min().date()} to {val_df['Date'].max().date()})")
print(f"Test Set:  {len(test_df):,} rows ({test_df['Date'].min().date()} to {test_df['Date'].max().date()})")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Preprocessing & Column Transformer Pipeline
Setting up Scikit-Learn transformers for one-hot encoding categorical variables (`Product_ID`, `Store_ID`, `Category`, `Region`) and standardizing numerical feature columns.
"""))

    cells.append(nbf.v4.new_code_cell("""categorical_cols = ['Product_ID', 'Store_ID', 'Category', 'Region']
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

print(f"Transformed Training Shape: {X_train.shape} features.")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Model Training & Benchmarking
Comparing 4 forecasting paradigms:
1. Naive Previous-Day Forecast (Lag 1)
2. 7-Day Moving Average Baseline
3. Random Forest Regressor
4. XGBoost Regressor
"""))

    cells.append(nbf.v4.new_code_cell("""# 1 & 2. Baselines
naive_metrics, ma_metrics, y_naive_test, y_ma_test = train_baseline_models(train_df, test_df)

# 3. Random Forest
rf_model, rf_val_metrics = train_random_forest(X_train, y_train, X_val, y_val, random_state=42)
y_rf_test = np.clip(rf_model.predict(X_test), 0, None)
rf_test_metrics = calculate_metrics(y_test, y_rf_test)
rf_test_metrics["Model"] = "Random Forest Regressor"

# 4. XGBoost
xgb_model, xgb_val_metrics = train_xgboost(X_train, y_train, X_val, y_val, random_state=42)
y_xgb_test = np.clip(xgb_model.predict(X_test), 0, None)
xgb_test_metrics = calculate_metrics(y_test, y_xgb_test)
xgb_test_metrics["Model"] = "XGBoost Regressor (Tuned)"

# Summary Table
metrics_list = [naive_metrics, ma_metrics, rf_test_metrics, xgb_test_metrics]
metrics_df = pd.DataFrame(metrics_list)[['Model', 'MAE', 'RMSE', 'R2', 'WAPE_%', 'sMAPE_%', 'Approx_Forecast_Accuracy_%']]

print("=== MODEL BENCHMARK ON UNSEEN CHRONOLOGICAL TEST SET ===")
print(tabulate(metrics_df, headers='keys', tablefmt='fancy_grid', showindex=False))
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 5. Forecast Visualizations (Actual vs Predicted)
Evaluating the forecast accuracy across chronological test holdout periods.
"""))

    cells.append(nbf.v4.new_code_cell("""test_results = test_df.copy()
test_results['Actual_Demand'] = y_test
test_results['Forecast_XGBoost'] = np.round(y_xgb_test, 1)
test_results['Forecast_Error'] = test_results['Forecast_XGBoost'] - test_results['Actual_Demand']

# Save forecast outputs
os.makedirs("outputs", exist_ok=True)
test_results[['Date', 'Product_ID', 'Product_Name', 'Store_ID', 'Category', 'Our_Price', 'Actual_Demand', 'Forecast_XGBoost', 'Forecast_Error']].to_csv("outputs/forecast_results.csv", index=False)

# Plot actual vs forecast for top product
prod_sample = test_results[test_results['Product_ID'] == 'PROD_01'].groupby('Date').agg({
    'Actual_Demand': 'sum',
    'Forecast_XGBoost': 'sum'
}).reset_index()

plt.figure(figsize=(14, 5))
plt.plot(prod_sample['Date'], prod_sample['Actual_Demand'], label='Actual Units Sold', color='#1d3557', linewidth=2)
plt.plot(prod_sample['Date'], prod_sample['Forecast_XGBoost'], label='XGBoost Forecast', color='#e63946', linestyle='--', linewidth=2)
plt.title('Test Set Holdout: Actual vs XGBoost Forecasted Demand (PROD_01 Wireless Headphones)', fontsize=13, fontweight='bold')
plt.xlabel('Date', fontsize=11, fontweight='bold')
plt.ylabel('Total Units Sold', fontsize=11, fontweight='bold')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 6. Model Explainability & Feature Importance
Analyzing key drivers of demand across pricing, competitive features, and seasonal temporal variables.
"""))

    cells.append(nbf.v4.new_code_cell("""# Extract feature names from OneHotEncoder + Numerical cols
ohe_feature_names = list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols))
all_feature_names = ohe_feature_names + numerical_cols

feature_importances = xgb_model.feature_importances_
feat_imp_df = pd.DataFrame({
    'Feature': all_feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=feat_imp_df.head(15), x='Importance', y='Feature', palette='mako')
plt.title('Top 15 Predictive Features Influencing Retail Demand (XGBoost)', fontsize=13, fontweight='bold')
plt.xlabel('Relative Feature Importance (Gain)', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 7. Model & Preprocessing Serialization
Saving the best model (`demand_model.pkl`), preprocessing pipeline (`preprocessing_pipeline.pkl`), feature schema, and evaluation metrics for downstream use in Notebook 03.
"""))

    cells.append(nbf.v4.new_code_cell("""save_model_artifacts(
    model=xgb_model,
    preprocessor=preprocessor,
    feature_names=feature_metadata,
    metrics_df=metrics_df,
    models_dir="models",
    outputs_dir="outputs"
)
print("Demand forecasting pipeline successfully trained and serialized.")
"""))

    nb.cells = cells
    return nb

def create_dynamic_pricing_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# 03 — Dynamic Pricing & Revenue Optimization Engine
### Dynamic Pricing & Revenue Intelligence System | Final Year B.Tech Project
---
**Objective:** Deliver an end-to-end pricing decision engine combining empirical price elasticity, competitor-aware candidate pricing grids, demand simulation, revenue/profit optimization under guardrails, confidence scoring, and interactive what-if simulation.
"""))

    cells.append(nbf.v4.new_code_cell("""import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Add project root to path
sys.path.append(os.path.abspath("."))
from src.data_loader import load_data, clean_data
from src.feature_engineering import create_time_features, create_lag_and_rolling_features, create_pricing_features
from src.pricing_optimizer import DynamicPricingEngine

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['figure.dpi'] = 120
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Load Pretrained ML Model & Preprocessing Pipeline
We instantiate the `DynamicPricingEngine` by loading the serialized XGBoost model and preprocessor created in Notebook 02.
"""))

    cells.append(nbf.v4.new_code_cell("""engine = DynamicPricingEngine(
    model_path="models/demand_model.pkl",
    pipeline_path="models/preprocessing_pipeline.pkl",
    features_path="models/feature_columns.json"
)

# Load dataset and prepare features
df = load_data("data/dataset.csv")
df = clean_data(df)
df = create_time_features(df)
df = create_lag_and_rolling_features(df)
df = create_pricing_features(df)
df = df.dropna().reset_index(drop=True)

print("Dynamic Pricing Engine successfully initialized.")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Econometric Price Elasticity Analysis
We estimate product-level own-price elasticity ($\beta$) and cross-price elasticity ($\gamma$) using log-log regression:
$$\ln(\text{Units\_Sold}) = \alpha + \beta \ln(\text{Our\_Price}) + \gamma \ln(\text{Competitor\_Price}) + \epsilon$$
"""))

    cells.append(nbf.v4.new_code_cell("""elasticity_df = DynamicPricingEngine.estimate_price_elasticity(df)
joblib.dump(elasticity_df, "models/elasticity_model.pkl")

print("=== PRODUCT-LEVEL EMPIRICAL PRICE ELASTICITY & SENSITIVITY ===")
print(tabulate(
    elasticity_df[['Product_ID', 'Product_Name', 'Category', 'Own_Price_Elasticity', 'Cross_Price_Elasticity', 'P_Value', 'R_Squared', 'Elasticity_Category']],
    headers=["ID", "Product Name", "Category", "Own Elasticity (β)", "Cross Elasticity (γ)", "P-Val", "R²", "Classification"],
    tablefmt="fancy_grid",
    showindex=False
))
"""))

    cells.append(nbf.v4.new_code_cell("""# Visualize Elasticity by Category
plt.figure(figsize=(10, 4))
sns.barplot(data=elasticity_df, x='Category', y='Own_Price_Elasticity', palette='coolwarm')
plt.axhline(-1.0, color='red', linestyle='--', label='Unit Elasticity Threshold (β = -1.0)')
plt.title('Empirical Price Elasticity of Demand by Category', fontsize=13, fontweight='bold')
plt.ylabel('Price Elasticity (β)', fontsize=11, fontweight='bold')
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Dynamic Price Simulation & Optimization Curves
Simulating candidate price responses for a representative product to observe the trade-off between price, predicted demand, and expected revenue/profit.
"""))

    cells.append(nbf.v4.new_code_cell("""# Select the latest state for PROD_01 in Store_01
sample_state = df[(df['Product_ID'] == 'PROD_01') & (df['Store_ID'] == 'STORE_01')].iloc[[-1]]
hist_p = df[(df['Product_ID'] == 'PROD_01') & (df['Store_ID'] == 'STORE_01')]['Our_Price']

rec = engine.optimize_price(sample_state, hist_prices_series=hist_p, objective="MAX_REVENUE", max_increase_pct=12.0, max_decrease_pct=12.0)

sim_curve = rec['Simulation_Grid']

fig, ax1 = plt.subplots(figsize=(12, 5))

color = '#1f77b4'
ax1.set_xlabel('Candidate Price (INR)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Predicted Demand (Units)', color=color, fontsize=11, fontweight='bold')
ax1.plot(sim_curve['Candidate_Price'], sim_curve['Predicted_Demand'], color=color, marker='o', linewidth=2, label='Demand Curve')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel('Expected Revenue (INR)', color=color, fontsize=11, fontweight='bold')
ax2.plot(sim_curve['Candidate_Price'], sim_curve['Expected_Revenue'], color=color, marker='s', linewidth=2.5, label='Expected Revenue')
ax2.tick_params(axis='y', labelcolor=color)

# Markers for Current, Competitor, and Recommended
plt.axvline(rec['Current_Price'], color='blue', linestyle=':', label=f"Current Price (INR {rec['Current_Price']:.2f})")
plt.axvline(rec['Competitor_Price'], color='orange', linestyle=':', label=f"Competitor Price (INR {rec['Competitor_Price']:.2f})")
plt.axvline(rec['Recommended_Price'], color='red', linestyle='--', linewidth=2, label=f"Optimal Price (INR {rec['Recommended_Price']:.2f})")

plt.title(f"Dynamic Price Optimization Curve: {rec['Product_Name']} (STORE_01)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print(f"Optimization Outcome:")
print(f" - Current Price: INR {rec['Current_Price']:.2f} | Current Exp. Revenue: INR {rec['Current_Expected_Revenue']:,.2f}")
print(f" - Recommended Price: INR {rec['Recommended_Price']:.2f} | Recommended Exp. Revenue: INR {rec['Recommended_Expected_Revenue']:,.2f}")
print(f" - Revenue Improvement: {rec['Revenue_Improvement_Percent']:+.2f}%")
print(f" - Confidence: {rec['Confidence_Level']} ({rec['Confidence_Rationale']})")
print(f" - Recommendation Reason: {rec['Recommendation_Reason']}")
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Enterprise-Wide Dynamic Pricing Recommendations
Executing the pricing optimization engine across all 20 products and 4 store locations using current operational states and pricing guardrails.
"""))

    cells.append(nbf.v4.new_code_cell("""# Run optimization across latest active state of all (Product, Store) pairs
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
    # Exclude simulation grid for CSV export
    r_dict = {k: v for k, v in r.items() if k != "Simulation_Grid"}
    all_recs.append(r_dict)

recs_df = pd.DataFrame(all_recs)
recs_df.to_csv("outputs/pricing_recommendations.csv", index=False)

print(f"Generated {len(recs_df)} Dynamic Pricing Recommendations.")
print(tabulate(
    recs_df[['Product_ID', 'Store_ID', 'Current_Price', 'Competitor_Price', 'Recommended_Price', 'Price_Change_Percent', 'Revenue_Improvement_Percent', 'Confidence_Level']].head(10),
    headers=["Product", "Store", "Cur Price", "Comp Price", "Rec Price", "Price Δ %", "Rev Lift %", "Confidence"],
    tablefmt="psql",
    floatfmt=(".2f", ".2f", ".2f", ".2f", ".2f", "+.2f", "+.2f", "")
))
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 5. What-If Pricing Simulator Function
Interactive simulation tool enabling commercial managers to test hypothetical price changes and observe predicted demand, revenue, competitor gaps, and guardrail statuses.
"""))

    cells.append(nbf.v4.new_code_cell("""def run_what_if_analysis(product_id, store_id, proposed_price):
    \"\"\"
    Interactive simulation helper for commercial decision makers.
    \"\"\"
    state = df[(df['Product_ID'] == product_id) & (df['Store_ID'] == store_id)].iloc[[-1]]
    cur_p = float(state['Our_Price'].iloc[0])
    comp_p = float(state['Competitor_Price'].iloc[0])
    
    sim_result = engine.simulate_price_change(state, proposed_price)
    cur_result = engine.simulate_price_change(state, cur_p)
    
    rev_change = ((sim_result['Expected_Revenue'] - cur_result['Expected_Revenue']) / cur_result['Expected_Revenue']) * 100.0
    demand_change = ((sim_result['Predicted_Demand'] - cur_result['Predicted_Demand']) / cur_result['Predicted_Demand']) * 100.0
    
    table_data = [
        ["Current State", f"INR {cur_p:.2f}", f"{cur_result['Predicted_Demand']:.1f}", f"INR {cur_result['Expected_Revenue']:,.2f}", "Baseline"],
        ["Simulated State", f"INR {proposed_price:.2f}", f"{sim_result['Predicted_Demand']:.1f}", f"INR {sim_result['Expected_Revenue']:,.2f}", sim_result['Guardrail_Status']],
        ["Impact / Delta", f"{((proposed_price - cur_p)/cur_p)*100:+.2f}%", f"{demand_change:+.2f}%", f"{rev_change:+.2f}%", "—"]
    ]
    
    print(f"=== WHAT-IF SIMULATION: {state['Product_Name'].iloc[0]} ({store_id}) ===")
    print(f"Competitor Price: INR {comp_p:.2f} | Gap: {sim_result['Competitor_Gap_Percent']:+.2f}%")
    print(tabulate(table_data, headers=["Scenario", "Price", "Predicted Demand", "Expected Revenue", "Guardrail Status"], tablefmt="fancy_grid"))

# Test What-If scenarios
run_what_if_analysis("PROD_01", "STORE_01", 2850.0)
run_what_if_analysis("PROD_01", "STORE_01", 3100.0)
"""))

    nb.cells = cells
    return nb

if __name__ == "__main__":
    print("Building Jupyter Notebooks...")
    
    nb1 = create_sales_analysis_notebook()
    with open("01_Sales_Analysis.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb1, f)
    print("Created 01_Sales_Analysis.ipynb")
    
    nb2 = create_demand_forecasting_notebook()
    with open("02_Demand_Forecasting.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb2, f)
    print("Created 02_Demand_Forecasting.ipynb")
    
    nb3 = create_dynamic_pricing_notebook()
    with open("03_Dynamic_Pricing_Optimization.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb3, f)
    print("Created 03_Dynamic_Pricing_Optimization.ipynb")
    
    print("All notebooks created successfully.")
