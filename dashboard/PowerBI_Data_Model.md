# Power BI Data Model Architecture & Schema Specification
## Project: Dynamic Pricing & Retail Revenue Intelligence System

---

## 1. Executive Summary & Modeling Strategy

The data model for the **Dynamic Pricing & Revenue Intelligence System** is engineered according to the **Kimball Dimensional Modeling Methodology (Star Schema)**. It connects the primary high-granularity transaction/daily panel log with dedicated dimensional tables, model evaluation benchmarks, pricing recommendations, and candidate simulation grids.

### Primary Architecture: Star Schema + Analytical Sidecars
- **Fact Table**: `Fact_DailySales` (sourced from `Dynamic_Pricing_Data_Enriched.csv` / daily panel)
- **Dimension Tables**: `Dim_Product`, `Dim_Store`, `Dim_Date`
- **Analytical Tables**:
  - `Pricing_Recommendations` (80 latest state recommendations with guardrails)
  - `Pricing_Simulation_Grid` (2,480 candidate price points for What-If scenario simulations)
  - `Model_Evaluation_Metrics` (Benchmark metrics across 4 models)
  - `Feature_Importance` (XGBoost explanatory feature weights)

---

## 2. Table Catalog & Data Dictionary

### Table 1: `Fact_DailySales` (Primary Fact Table)
- **Source File**: `dashboard/Dynamic_Pricing_Data_Enriched.csv`
- **Granularity**: Daily $\times$ Product $\times$ Store (58,480 rows)
- **Description**: Historical 2-year daily transaction log (2024-01-01 to 2025-12-31) containing pricing, volume, competitor actions, and cost structures.

| Column Name | Data Type | Format | Key Type | Description |
| :--- | :--- | :--- | :---: | :--- |
| `Date` | Date | `yyyy-MM-dd` | FK | Date of transaction |
| `Product_ID` | String / Text | Text | FK | Unique product identifier (`PROD_01` to `PROD_20`) |
| `Store_ID` | String / Text | Text | FK | Unique store identifier (`STORE_01` to `STORE_04`) |
| `Base_Price` | Decimal Number | Currency (`INR #,##0.00`) | Attribute | Catalog MSRP / reference anchor price |
| `Our_Price` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Effective daily selling price offered by our store |
| `Competitor_Price` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Local benchmark competitor selling price |
| `Discount_Percent` | Decimal Number | Percentage (`0.0%`) | Measure | Discount percentage applied from catalog price |
| `Promotion_Flag` | Whole Number | Boolean / Integer (`0` or `1`) | Attribute | Promotional campaign active indicator |
| `Unit_Cost` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Wholesale inventory cost per unit |
| `Inventory_Level` | Whole Number | Integer (`#,##0`) | Measure | Closing inventory stock available on that day |
| `Units_Sold` | Whole Number | Integer (`#,##0`) | Measure | Actual volume of units sold |
| `Revenue` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Total realized daily revenue (`Our_Price` $\times$ `Units_Sold`) |
| `Total_Cost` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Total realized cost of goods sold (`Unit_Cost` $\times$ `Units_Sold`) |
| `Gross_Profit` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Gross profit (`Revenue` - `Total_Cost`) |
| `Gross_Margin_Percent` | Decimal Number | Percentage (`0.0%`) | Measure | Gross profit margin percentage |
| `Price_Difference` | Decimal Number | Currency (`INR #,##0.00`) | Measure | Price variance vs competitor (`Our_Price` - `Competitor_Price`) |
| `Price_Ratio` | Decimal Number | Decimal (`0.0000`) | Measure | Price ratio vs competitor (`Our_Price` / `Competitor_Price`) |
| `Price_Premium_Percent` | Decimal Number | Percentage (`0.0%`) | Measure | Price premium % over competitor |
| `Demand_Lag_1` | Decimal Number | Decimal (`0.0`) | Feature | 1-day lagged sales volume |
| `Demand_Lag_7` | Decimal Number | Decimal (`0.0`) | Feature | 7-day lagged sales volume |
| `Demand_Rolling_Mean_7` | Decimal Number | Decimal (`0.0`) | Feature | 7-day trailing moving average demand |
| `Demand_Rolling_Mean_14`| Decimal Number | Decimal (`0.0`) | Feature | 14-day trailing moving average demand |
| `Demand_Rolling_Mean_28`| Decimal Number | Decimal (`0.0`) | Feature | 28-day trailing moving average demand |
| `Demand_Rolling_Std_7` | Decimal Number | Decimal (`0.0`) | Feature | 7-day trailing standard deviation |

---

### Table 2: `Dim_Product` (Product Dimension)
- **Source File**: `dashboard/Dim_Product.csv`
- **Granularity**: 1 row per unique Product (20 rows)

| Column Name | Data Type | Format | Key Type | Description |
| :--- | :--- | :--- | :---: | :--- |
| `Product_ID` | String / Text | Text | **PK** | Primary product key |
| `Product_Name` | String / Text | Text | Attribute | Standard catalog descriptive name |
| `Category` | String / Text | Text | Attribute | Product category (Electronics, Groceries, Apparel, etc.) |
| `Base_Price` | Decimal Number | Currency (`INR #,##0.00`) | Attribute | Baseline retail catalog price |
| `Unit_Cost` | Decimal Number | Currency (`INR #,##0.00`) | Attribute | Mean wholesale procurement cost |
| `Own_Price_Elasticity` | Decimal Number | Decimal (`0.00`) | Metric | Empirical log-log own-price elasticity coefficient ($\beta$) |
| `Cross_Price_Elasticity`| Decimal Number | Decimal (`0.00`) | Metric | Cross-price elasticity coefficient ($\gamma$) |
| `Elasticity_Category` | String / Text | Text | Attribute | Classification (Elastic, Inelastic, etc.) |
| `R_Squared` | Decimal Number | Decimal (`0.000`) | Metric | Econometric elasticity regression fit $R^2$ |

---

### Table 3: `Dim_Store` (Store Dimension)
- **Source File**: `dashboard/Dim_Store.csv`
- **Granularity**: 1 row per unique Store (4 rows)

| Column Name | Data Type | Format | Key Type | Description |
| :--- | :--- | :--- | :---: | :--- |
| `Store_ID` | String / Text | Text | **PK** | Primary store key |
| `Store_Name` | String / Text | Text | Attribute | Retail outlet name |
| `Region` | String / Text | Text | Attribute | Geographic territory (North, South, East, West) |

---

### Table 4: `Dim_Date` (Date Dimension)
- **Source File**: `dashboard/Dim_Date.csv`
- **Granularity**: 1 row per calendar day (731 rows: 2024-01-01 to 2025-12-31)

| Column Name | Data Type | Format | Key Type | Description |
| :--- | :--- | :--- | :---: | :--- |
| `Date` | Date | `yyyy-MM-dd` | **PK** | Primary date key (Mark as Date Table) |
| `Year` | Whole Number | Integer (`0000`) | Attribute | Calendar year (2024, 2025) |
| `Quarter` | String / Text | Text (`Q1`, `Q2`, etc.) | Attribute | Quarter label |
| `Quarter_Number` | Whole Number | Integer (`1-4`) | Sort Key | Numeric quarter |
| `Month_Number` | Whole Number | Integer (`1-12`) | Sort Key | Numeric month for sorting |
| `Month_Name` | String / Text | Text | Attribute | Full month name (Sort by `Month_Number`) |
| `Month_Short` | String / Text | Text | Attribute | 3-letter month (Sort by `Month_Number`) |
| `Week_Number` | Whole Number | Integer (`1-53`) | Attribute | ISO calendar week number |
| `Day_Of_Month` | Whole Number | Integer (`1-31`) | Attribute | Calendar day of month |
| `Day_Of_Week_Number`| Whole Number | Integer (`1-7`) | Sort Key | Numeric day of week (1=Mon, 7=Sun) |
| `Day_Name` | String / Text | Text | Attribute | Full day name (Sort by `Day_Of_Week_Number`)|
| `Is_Weekend` | Whole Number | Boolean (`0` or `1`)| Attribute | Weekend flag (Saturday/Sunday) |
| `Season_Name` | String / Text | Text | Attribute | Retail season (Festive Q4, Monsoon/Summer, etc.)|

---

### Table 5: `Pricing_Recommendations` (Optimized Decisions Sidecar)
- **Source File**: `dashboard/Pricing_Recommendations_Enriched.csv`
- **Granularity**: 1 row per latest Product $\times$ Store pair (80 rows)

| Column Name | Data Type | Format | Description |
| :--- | :--- | :--- | :--- |
| `Product_ID` | String / Text | Text | Product key |
| `Product_Name` | String / Text | Text | Product descriptive title |
| `Category` | String / Text | Text | Category name |
| `Store_ID` | String / Text | Text | Store key |
| `Store_Name` | String / Text | Text | Store name |
| `Current_Price` | Decimal Number | Currency (`INR #,##0.00`) | Baseline current selling price |
| `Competitor_Price` | Decimal Number | Currency (`INR #,##0.00`) | Benchmark competitor price |
| `Recommended_Price` | Decimal Number | Currency (`INR #,##0.00`) | AI-optimized recommended price |
| `Price_Change_Percent`| Decimal Number | Percentage (`0.0%`) | Recommended price change % |
| `Competitor_Gap_Percent`| Decimal Number | Percentage (`0.0%`) | Competitor price premium at recommended price |
| `Current_Predicted_Demand` | Decimal Number | Decimal (`0.0`) | Model predicted demand at current price |
| `Recommended_Predicted_Demand` | Decimal Number | Decimal (`0.0`) | Model predicted demand at recommended price |
| `Demand_Change_Percent` | Decimal Number | Percentage (`0.0%`) | Expected demand volume shift % |
| `Current_Expected_Revenue` | Decimal Number | Currency (`INR #,##0.00`) | Baseline expected revenue |
| `Recommended_Expected_Revenue` | Decimal Number | Currency (`INR #,##0.00`) | Optimized expected revenue |
| `Revenue_Improvement_Percent` | Decimal Number | Percentage (`0.0%`) | Expected revenue lift % |
| `Unit_Cost` | Decimal Number | Currency (`INR #,##0.00`) | Unit cost of product |
| `Current_Expected_Profit` | Decimal Number | Currency (`INR #,##0.00`) | Baseline expected profit |
| `Recommended_Expected_Profit` | Decimal Number | Currency (`INR #,##0.00`) | Optimized expected profit |
| `Profit_Lift_Percent` | Decimal Number | Percentage (`0.0%`) | Expected profit lift % |
| `Confidence_Level` | String / Text | Text (`HIGH`, `MEDIUM`, `LOW`) | Recommendation confidence rating |
| `Confidence_Rationale` | String / Text | Text | Explanatory confidence reasoning |
| `Recommendation_Reason` | String / Text | Text | Natural language commercial rationalization |
| `Guardrail_Status` | String / Text | Text (`PASSED`, `VIOLATED`) | Overall compliance across all 4 guardrails |

---

### Table 6: `Pricing_Simulation_Grid` (What-If Simulation Engine Table)
- **Source File**: `dashboard/Pricing_Simulation_Grid.csv`
- **Granularity**: 31 candidate prices ($-15\%$ to $+15\%$) $\times$ 80 Product-Store pairs = 2,480 rows

| Column Name | Data Type | Format | Description |
| :--- | :--- | :--- | :--- |
| `Product_ID` | String / Text | Text | Product identifier |
| `Store_ID` | String / Text | Text | Store identifier |
| `Price_Adjustment_Percent` | Whole Number | Integer (`-15` to `+15`) | Candidate adjustment step (%) |
| `Candidate_Price` | Decimal Number | Currency (`INR #,##0.00`) | Simulated candidate price |
| `Predicted_Demand` | Decimal Number | Decimal (`0.0`) | Model predicted demand volume |
| `Expected_Revenue` | Decimal Number | Currency (`INR #,##0.00`) | Simulated expected revenue |
| `Expected_Profit` | Decimal Number | Currency (`INR #,##0.00`) | Simulated expected gross profit |
| `Competitor_Gap_Percent` | Decimal Number | Percentage (`0.0%`) | Gap vs competitor at candidate price |
| `Guardrail_Status` | String / Text | Text | Detailed pass/violation string |
| `Is_Feasible` | True / False | Boolean | True if all pricing guardrails are satisfied |

---

### Table 7: `Model_Evaluation_Metrics` (Model Benchmark Table)
- **Source File**: `dashboard/Model_Evaluation_Metrics.csv`
- **Granularity**: 1 row per algorithm (4 rows: Naive, 7-Day MA, Random Forest, XGBoost)

| Column Name | Data Type | Format | Description |
| :--- | :--- | :--- | :--- |
| `Model` | String / Text | Text | Model name |
| `MAE` | Decimal Number | Decimal (`0.000`) | Mean Absolute Error |
| `RMSE` | Decimal Number | Decimal (`0.000`) | Root Mean Squared Error |
| `R2` | Decimal Number | Decimal (`0.0000`) | Coefficient of Determination ($R^2$) |
| `WAPE_%` | Decimal Number | Percentage (`0.0%`) | Weighted Absolute Percentage Error |
| `sMAPE_%` | Decimal Number | Percentage (`0.0%`) | Symmetric Mean Absolute Percentage Error |
| `Approx_Forecast_Accuracy_%` | Decimal Number | Percentage (`0.0%`) | $100 - \text{WAPE}$ forecast accuracy |

---

### Table 8: `Feature_Importance` (XGBoost Explainability Table)
- **Source File**: `dashboard/Feature_Importance.csv`
- **Granularity**: 1 row per predictive feature (53 rows)

| Column Name | Data Type | Format | Description |
| :--- | :--- | :--- | :--- |
| `Feature` | String / Text | Text | Feature name in XGBoost model |
| `Importance` | Decimal Number | Decimal (`0.0000`) | XGBoost Gini gain feature weight |
| `Importance_Percent` | Decimal Number | Percentage (`0.0%`) | Relative importance contribution percentage |

---

## 3. Entity-Relationship Diagram (ERD)

```
       +-------------------+       +-------------------+
       |     Dim_Date      |       |    Dim_Product    |
       +-------------------+       +-------------------+
       | PK Date           |<--+   | PK Product_ID     |<---+
       |    Year           |   |   |    Product_Name   |    |
       |    Month_Name     |   |   |    Category       |    |
       |    Quarter        |   |   |    Base_Price     |    |
       |    Is_Weekend     |   |   |    Own_Elasticity |    |
       +-------------------+   |   +-------------------+    |
                               |                            |
                               | (1:N)                      | (1:N)
                     +---------+----------------------------+---------+
                     |                 Fact_DailySales                |
                     +------------------------------------------------+
                     | FK Date                                        |
                     | FK Product_ID                                  |
                     | FK Store_ID                                    |
                     |    Our_Price, Competitor_Price, Discount_Pct   |
                     |    Units_Sold, Revenue, Total_Cost             |
                     |    Gross_Profit, Gross_Margin_Percent          |
                     +------------------------------------------------+
                               | (N:1)
       +-------------------+   |
       |     Dim_Store     |   |
       +-------------------+   |
       | PK Store_ID       |<--+
       |    Store_Name     |
       |    Region         |
       +-------------------+

   ----------------------------------------------------------------------
   Analytical Sidecar Tables (Filtered via Slicers / Parameters)
   ----------------------------------------------------------------------
   +------------------------------------+   +------------------------------------+
   |     Pricing_Recommendations        |   |       Pricing_Simulation_Grid      |
   +------------------------------------+   +------------------------------------+
   | Product_ID, Store_ID               |   | Product_ID, Store_ID               |
   | Current_Price, Recommended_Price   |   | Price_Adjustment_Percent (-15..+15)|
   | Revenue_Lift_%, Profit_Lift_%      |   | Candidate_Price, Predicted_Demand  |
   | Confidence_Level, Guardrail_Status |   | Expected_Revenue, Expected_Profit  |
   +------------------------------------+   +------------------------------------+
                     ^                                         ^
                     | (1:N Product_ID / Store_ID)             | (1:N Product_ID / Store_ID)
                     +--------------------+--------------------+
                                          |
                     +--------------------+--------------------+
                     |      Model_Evaluation_Metrics / FeatImp |
                     +-----------------------------------------+
```

---

## 4. Relationship Definitions & Cardinality

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter | Active |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `Fact_DailySales` | `Date` | `Dim_Date` | `Date` | Many-to-One ($N:1$) | Single | **Yes** |
| `Fact_DailySales` | `Product_ID` | `Dim_Product` | `Product_ID` | Many-to-One ($N:1$) | Single | **Yes** |
| `Fact_DailySales` | `Store_ID` | `Dim_Store` | `Store_ID` | Many-to-One ($N:1$) | Single | **Yes** |
| `Pricing_Recommendations` | `Product_ID` | `Dim_Product` | `Product_ID` | Many-to-One ($N:1$) | Single | **Yes** |
| `Pricing_Recommendations` | `Store_ID` | `Dim_Store` | `Store_ID` | Many-to-One ($N:1$) | Single | **Yes** |
| `Pricing_Simulation_Grid` | `Product_ID` | `Dim_Product` | `Product_ID` | Many-to-One ($N:1$) | Single | **Yes** |
| `Pricing_Simulation_Grid` | `Store_ID` | `Dim_Store` | `Store_ID` | Many-to-One ($N:1$) | Single | **Yes** |
