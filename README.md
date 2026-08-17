# Dynamic Pricing & Revenue Intelligence System

> **AI-Powered Retail Revenue Intelligence & Econometric Price Optimization System**  
> *End-to-End Enterprise Solution: Sales Analytics → Demand Forecasting → Price Elasticity → Pricing Optimization → Revenue & Profit Impact*

---

## 1. Business Problem

Modern retail and e-commerce enterprises face critical daily pricing decisions:
- **What price to charge:** Balancing competitive positioning against unit margin profitability.
- **How demand changes:** Understanding price sensitivity (own-price and cross-price elasticity) across products and categories.
- **How competitors affect pricing:** Responding dynamically to competitor price shifts without initiating self-destructive price wars.
- **How pricing impacts revenue and profit:** Identifying optimal price points that maximize business gross profit and top-line revenue under real-world commercial constraints.

This project delivers an end-to-end AI-driven pricing and revenue intelligence system that replaces static markdowns and crude heuristics with empirical machine learning, econometrics, and automated scenario simulation.

---

## 2. End-to-End Analytics & Optimization Pipeline

```
┌────────────────────────────────────────────────────────┐
│                   1. SALES ANALYTICS                   │
│ (Historical Panel Data, ASP, Category Mix, Margin Health)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                  2. DEMAND FORECASTING                 │
│ (Leakage-Free XGBoost / RF Regressor, 89.34% Accuracy) │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   3. PRICE ELASTICITY                  │
│ (Econometric Log-Log Own & Cross Elasticity Estimation) │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                 4. PRICING OPTIMIZATION                │
│ (Commercial Scoring: Profit, Revenue & Competitor Risk)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               5. REVENUE & PROFIT IMPACT               │
│ (What-If Simulator, Power BI Suite, Streamlit Web App) │
└────────────────────────────────────────────────────────┘
```

---

## 3. Core Features

- **Sales Analytics:** Comprehensive historical sales, revenue, volume, and gross margin diagnostics across 20 products and 4 metropolitan stores.
- **Demand Forecasting:** Supervised machine learning engine with zero data leakage (chronological train/validation/test splits, lag features, and rolling statistics).
- **Pricing Intelligence:** Real-time tracking of internal vs. competitor pricing, price gap percentages, and promotion penetration.
- **Dynamic Pricing Recommendation:** Multi-factor scoring engine evaluating profit lift (+50%), revenue lift (+20%), demand volume (+10%), and competitor risk penalty (-20%) with explicit decision states (`✓ RECOMMENDED`, `⚠ HOLD CURRENT PRICE`, `⚠ CONTROLLED PREMIUM`).
- **What-If Pricing Simulator:** Interactive scenario modeling allowing pricing managers to adjust price modifiers ($-15\%$ to $+15\%$) and instantly project unit demand, revenue, and gross profit.
- **Competitor Price Analysis:** Cross-elasticity modeling and dynamic premium monitoring to maintain strategic competitiveness.
- **Price Elasticity Modeling:** Statistically calibrated downward-sloping log-log regression curves across grocery, electronics, apparel, and home categories.
- **Revenue & Profit Impact Assessment:** Transparent trade-off analysis showing expected revenue lift, profit gains, and volume shifts.
- **Power BI Executive Dashboard:** 6-page enterprise BI suite (Executive Overview, Sales Performance, Pricing Intelligence, Forecast Accuracy, Pricing Directives, What-If Simulator).
- **Interactive Web Application:** Full-featured dark-mode Streamlit dashboard with rich glassmorphism visuals and Plotly interactive sensitivity curves.

---

## 4. Validated Model Performance

Models were evaluated on a completely unseen chronological holdout test set with strict zero-leakage enforcement:

| Model | MAE (Units) | RMSE (Units) | $R^2$ Score | WAPE % | Forecast Accuracy % |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Baseline (Lag 1)** | 26.53 | 36.42 | 0.4410 | 25.16% | 74.84% |
| **7-Day Moving Average** | 21.88 | 29.56 | 0.5820 | 20.75% | 79.25% |
| **Random Forest Regressor** | 12.18 | 16.94 | 0.8520 | 11.56% | 88.44% |
| **Tuned XGBoost Regressor** | **11.24** | **15.82** | **0.9223** | **10.66%** | **89.34%** |

- **XGBoost $R^2$ Score:** `0.9223`
- **Weighted Absolute Percentage Error (WAPE):** `10.66%`
- **Approximate Forecast Accuracy:** `89.34%`

---

## 5. Repository Structure

```
Dynamic-Pricing-Revenue-Intelligence/
│
├── 01_Sales_Analysis.ipynb               # Exploratory Sales, Category & Pricing Analytics
├── 02_Demand_Forecasting.ipynb            # ML Demand Forecasting & Leak-Free Feature Pipeline
├── 03_Dynamic_Pricing_Optimization.ipynb  # Econometric Elasticity & Price Optimization
│
├── app.py                                 # Streamlit Web Application
├── audit_pricing.py                       # Automated 5-Scenario Decision Logic Audit Harness
│
├── data/
│   └── dataset.csv                        # 58,480 Daily Panel Observations (20 SKUs × 4 Stores × 2 Yrs)
│
├── models/
│   ├── demand_model.pkl                   # Trained XGBoost Demand Regressor
│   ├── preprocessing_pipeline.pkl         # Scikit-Learn Feature Transformation Pipeline
│   ├── feature_columns.json               # Input Feature Schema Registry
│   └── elasticity_model.pkl               # Product & Category Elasticity Lookup Table
│
├── dashboard/
│   ├── Dynamic_Pricing_Data_Enriched.csv  # Consolidated Master Dataset for Power BI
│   ├── Pricing_Recommendations_Enriched.csv# Active Pricing Directives & Metrics
│   ├── Pricing_Simulation_Grid.csv        # Multi-Candidate Price Simulation Matrix
│   ├── PowerBI_Dashboard_Specification.md # Complete 6-Page BI Design & DAX Specs
│   ├── PowerBI_Theme.json                 # Custom Dark Enterprise Power BI Theme
│   └── README.md                          # Power BI Setup & Import Guide
│
├── outputs/
│   ├── model_metrics.csv                  # Multi-Model Benchmark Comparison Table
│   ├── forecast_results.csv               # Actual vs Predicted Test Set Holdout Values
│   └── pricing_recommendations.csv        # SKU-Level Optimized Pricing Directives
│
├── src/                                   # Core Backend Python Modules
│   ├── data_loader.py                     # Data Ingestion & Sanitization
│   ├── feature_engineering.py             # Lag, Rolling & Competitor Features
│   ├── modeling.py                        # Model Training & Cross-Validation
│   ├── pricing_optimizer.py               # Candidate Generation & Financial Simulation
│   └── execute_pipeline.py                # Automated End-to-End Pipeline Execution
│
├── web/                                   # Web App Components & Presentation Layer
│   ├── components.py                      # Glassmorphic KPI Cards & Hero HTML
│   ├── data_loader.py                     # Cached Web Data Ingestion
│   ├── pricing_service.py                 # Multi-Factor Commercial Scoring Engine
│   └── styles.py                          # Premium CSS & Dark-Mode Design System
│
├── .gitignore                             # Git Ignore Rules
├── requirements.txt                       # Python Core Dependencies
├── requirements-web.txt                   # Streamlit & UI Dependencies
└── README.md                              # Project Documentation
```

---

## 6. Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Dhruva912005/Dynamic-Pricing-Revenue-Intelligence.git
cd Dynamic-Pricing-Revenue-Intelligence
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-web.txt
```

### 3. Run the Web Application
```bash
streamlit run app.py
```

### 4. Execute the End-to-End Machine Learning Pipeline
```bash
python src/execute_pipeline.py
```

### 5. Run the Automated Pricing Audit
```bash
python audit_pricing.py
```

---

## 7. License & Attribution

Developed by **Dhruva** as a comprehensive capstone for Retail Intelligence, Dynamic Pricing, and Demand Forecasting.
Distributed under the MIT License.
