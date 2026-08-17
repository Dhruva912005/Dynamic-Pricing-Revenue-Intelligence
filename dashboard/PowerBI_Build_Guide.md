# Power BI Desktop Step-by-Step Implementation & Build Guide
## Project: Dynamic Pricing & Retail Revenue Intelligence System

This guide provides a comprehensive step-by-step walkthrough for building the corporate-grade **Dynamic Pricing & Revenue Intelligence** dashboard in **Power BI Desktop** using the pre-packaged data and schema artifacts in the `dashboard/` directory.

---

## 1. Prerequisites & File Checklist

Ensure the following files are available in your project `dashboard/` folder:
1. `Dynamic_Pricing_Data_Enriched.csv` (Primary Fact Data)
2. `Dim_Product.csv` (Product Dimension + Elasticity)
3. `Dim_Store.csv` (Store Dimension)
4. `Dim_Date.csv` (Calendar Dimension)
5. `Pricing_Recommendations_Enriched.csv` (Optimized Recommendations)
6. `Pricing_Simulation_Grid.csv` (What-If 31-Point Simulation Grid)
7. `Model_Evaluation_Metrics.csv` (Model Benchmarks)
8. `Feature_Importance.csv` (XGBoost Gini Importance)
9. `PowerBI_Theme.json` (Corporate Dark Navy Theme)

---

## 2. Phase 1: Data Ingestion & Power Query Configuration

1. Launch **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV**.
3. Import the files one by one:
   - `Dynamic_Pricing_Data_Enriched.csv` $\rightarrow$ Rename query to `Fact_DailySales`
   - `Dim_Product.csv` $\rightarrow$ Rename query to `Dim_Product`
   - `Dim_Store.csv` $\rightarrow$ Rename query to `Dim_Store`
   - `Dim_Date.csv` $\rightarrow$ Rename query to `Dim_Date`
   - `Pricing_Recommendations_Enriched.csv` $\rightarrow$ Rename query to `Pricing_Recommendations`
   - `Pricing_Simulation_Grid.csv` $\rightarrow$ Rename query to `Pricing_Simulation_Grid`
   - `Model_Evaluation_Metrics.csv` $\rightarrow$ Rename query to `Model_Evaluation_Metrics`
   - `Feature_Importance.csv` $\rightarrow$ Rename query to `Feature_Importance`
4. **Data Type Verifications**:
   - `Fact_DailySales[Date]`: Set type to **Date** (`yyyy-MM-dd`).
   - `Dim_Date[Date]`: Set type to **Date** (`yyyy-MM-dd`).
   - `Fact_DailySales[Revenue]`, `Gross_Profit`, `Total_Cost`, `Our_Price`, `Competitor_Price`: Set type to **Fixed Decimal Number (Currency)**.
   - `Fact_DailySales[Units_Sold]`, `Inventory_Level`: Set type to **Whole Number**.
5. Click **Close & Apply**.

---

## 3. Phase 2: Theme Application & Date Table Marking

### Apply Theme
1. In the Power BI ribbon, go to **View** $\rightarrow$ **Themes dropdown** $\rightarrow$ **Browse for themes**.
2. Select `dashboard/PowerBI_Theme.json`.
3. The report canvas will immediately adopt the clean corporate styling, dark navy callout palette, positive emerald greens, and warning ambers.

### Mark as Date Table
1. In the **Fields / Data** pane, right-click `Dim_Date`.
2. Select **Mark as Date Table** $\rightarrow$ choose `Date` column $\rightarrow$ Click **OK**.
3. Sort `Dim_Date[Month_Name]` by `Dim_Date[Month_Number]`.
4. Sort `Dim_Date[Day_Name]` by `Dim_Date[Day_Of_Week_Number]`.

---

## 4. Phase 3: Data Model Relationships (Star Schema)

Switch to **Model View** in Power BI and establish the following relationships:

1. `Dim_Date[Date]` (1) $\xrightarrow{1:N}$ `Fact_DailySales[Date]` (*)
2. `Dim_Product[Product_ID]` (1) $\xrightarrow{1:N}$ `Fact_DailySales[Product_ID]` (*)
3. `Dim_Store[Store_ID]` (1) $\xrightarrow{1:N}$ `Fact_DailySales[Store_ID]` (*)
4. `Dim_Product[Product_ID]` (1) $\xrightarrow{1:N}$ `Pricing_Recommendations[Product_ID]` (*)
5. `Dim_Store[Store_ID]` (1) $\xrightarrow{1:N}$ `Pricing_Recommendations[Store_ID]` (*)
6. `Dim_Product[Product_ID]` (1) $\xrightarrow{1:N}$ `Pricing_Simulation_Grid[Product_ID]` (*)
7. `Dim_Store[Store_ID]` (1) $\xrightarrow{1:N}$ `Pricing_Simulation_Grid[Store_ID]` (*)

*All cross-filter directions should be set to **Single**.*

---

## 5. Phase 4: Create DAX Measures Table

1. Go to **Home** $\rightarrow$ **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Copy and paste all measures from [dashboard/PowerBI_DAX_Measures.md](file:///c:/Users/LENOVO/Desktop/Project/dashboard/PowerBI_DAX_Measures.md) into this table.
4. Delete the default `Column1` to make `_Measures` a dedicated measures container.
5. Set appropriate display formatting:
   - Revenue / Profit / Cost measures: Currency (`₹ #,##0.00` or `$ #,##0.00`).
   - Margin / Lift / Elasticity measures: Percentage (`0.0%`) or Decimal (`0.00`).

---

## 6. Phase 5: Building the 6 Report Pages

### Master Header & Navigation (Apply to all 6 Pages)
1. Add a Dark Navy rectangle shape at the top ($X=0, Y=0, W=1920, H=65$, Color: `#0F172A`).
2. Add a Text Box: `"DYNAMIC PRICING & REVENUE INTELLIGENCE SYSTEM"` (Font: Segoe UI Bold, $16\text{pt}$, Color: White).
3. Insert 6 Navigation Buttons linking to each page:
   `[1. Executive Overview]` `[2. Sales Performance]` `[3. Pricing Intelligence]` `[4. Demand Forecast]` `[5. Dynamic Pricing]` `[6. What-If Simulator]`
4. Add a footer text box at the bottom ($Y=1050$):
   `"Dataset: Synthetic econometrically calibrated retail panel data developed for pricing simulation and model validation."` ($9\text{pt}$, `#64748B`).

---

### Page 1: Executive Overview
1. **Slicers**: Add dropdown slicers for `Dim_Date[Date]`, `Dim_Product[Category]`, `Dim_Store[Region]`.
2. **KPI Cards**: Place 6 Card visuals:
   - `[Total Revenue]`, `[Total Units Sold]`, `[Gross Profit]`, `[Gross Margin %]`, `[Average Selling Price]`, `[Price Premium %]`.
3. **Visual 1 (Revenue Trend)**: Line Chart $\rightarrow$ X: `Dim_Date[Date]`, Y: `[Total Revenue]`.
4. **Visual 2 (Volume Trend)**: Area Chart $\rightarrow$ X: `Dim_Date[Date]`, Y: `[Total Units Sold]`.
5. **Visual 3 (Category Performance)**: Clustered Bar Chart $\rightarrow$ Y: `Dim_Product[Category]`, X: `[Total Revenue]`.
6. **Visual 4 (Regional Revenue)**: Donut Chart $\rightarrow$ Legend: `Dim_Store[Region]`, Values: `[Total Revenue]`.
7. **Visual 5 (Top Products)**: Horizontal Bar Chart $\rightarrow$ Y: `Dim_Product[Product_Name]` (Top 10 filter by `[Total Revenue]`), X: `[Total Revenue]`.

---

### Page 2: Sales & Product Performance
1. **KPI Cards**: `[Total Revenue]`, `[Total Units Sold]`, `[Average Revenue per Product]`, `[Average Revenue per Store]`.
2. **Top 10 by Revenue**: Bar Chart (`Product_Name` vs `[Total Revenue]`).
3. **Top 10 by Volume**: Bar Chart (`Product_Name` vs `[Total Units Sold]`).
4. **BCG Product Matrix (Scatter Plot)**:
   - **X-Axis**: `[Total Units Sold]`
   - **Y-Axis**: `[Total Revenue]`
   - **Size**: `[Gross Profit]`
   - **Legend**: `Category`
   - **Tooltips**: `Product_Name`, `[Gross Margin %]`, `[Average Selling Price]`
   - Add horizontal/vertical median reference lines to form quadrants (Stars, Cash Cows, Question Marks, Dogs).

---

### Page 3: Pricing Intelligence
1. **KPI Cards**: `[Average Our Price]`, `[Average Competitor Price]`, `[Price Gap Absolute]`, `[Price Premium %]`, `[Average Discount %]`.
2. **Our Price vs Competitor Price**: Clustered Bar Chart $\rightarrow$ Y: `Product_Name`, X: `[Average Our Price]`, `[Average Competitor Price]`.
3. **Price vs Demand Empirical Scatter**: X: `Fact_DailySales[Our_Price]`, Y: `Fact_DailySales[Units_Sold]`, Legend: `Category`.
4. **Elasticity Analysis Table**: Table visual $\rightarrow$ Columns: `Product_Name`, `Category`, `Own_Price_Elasticity`, `Cross_Price_Elasticity`, `Elasticity_Category`, `R_Squared`.

---

### Page 4: Demand Forecast & Model Performance
1. **KPI Cards**:
   - `Selected Model: XGBoost Regressor (Tuned)`
   - `MAE: 11.242`
   - `RMSE: 16.077`
   - `R²: 0.9223`
   - `WAPE: 10.66%`
   - `Approx. Forecast Accuracy: 89.34%`
2. **Actual vs XGBoost Forecast Line Chart**:
   - X: `Date`, Lines: `Actual Demand` (Dark Navy `#0F172A`), `XGBoost Forecast` (Vibrant Blue `#2563EB`).
3. **Model Benchmark Comparison Table**:
   - Source: `Model_Evaluation_Metrics` $\rightarrow$ Columns: `Model`, `MAE`, `RMSE`, `R2`, `WAPE_%`, `Approx_Forecast_Accuracy_%`.
4. **Feature Importance Chart**:
   - Horizontal Bar Chart $\rightarrow$ Y: `Feature_Importance[Feature]` (Top 10), X: `Importance_Percent`.

---

### Page 5: Dynamic Pricing Recommendations *(Primary Decision Page)*
1. **Slicers**: `Dim_Product[Product_Name]` (Single Select), `Dim_Store[Store_Name]` (Single Select).
2. **Comparison KPI Cards**:
   - `Current Price` vs `Recommended Price` (`[Rec Price Change %]`)
   - `Current Exp Revenue` vs `Rec Expected Revenue` (`[Rec Revenue Lift %]`)
   - `Current Exp Profit` vs `Rec Expected Profit` (`[Rec Profit Lift %]`)
   - `Confidence Level` (Pill format) | `Guardrail Status` (`PASSED` badge)
3. **Price vs Expected Revenue Simulation Curve**:
   - Line Chart $\rightarrow$ X: `Pricing_Simulation_Grid[Candidate_Price]`, Y: `Expected_Revenue`. Highlight optimal point.
4. **Price vs Predicted Demand Curve**:
   - Line Chart $\rightarrow$ X: `Pricing_Simulation_Grid[Candidate_Price]`, Y: `Predicted_Demand`.
5. **Recommendations Master Table**:
   - Source: `Pricing_Recommendations` $\rightarrow$ Columns: `Product_Name`, `Store_Name`, `Current_Price`, `Competitor_Price`, `Recommended_Price`, `Price_Change_Percent`, `Revenue_Improvement_Percent`, `Profit_Lift_Percent`, `Confidence_Level`, `Guardrail_Status`.
   - Apply Conditional Formatting (Green for positive lift, Red for violation).
6. **Dynamic NLP Rationale Card**:
   - Single Card visual displaying measure `[Dynamic Recommendation Text]`.

---

### Page 6: What-If Pricing Simulator
1. **Interactive Slider Parameter**:
   - Insert Slicer $\rightarrow$ Field: `Pricing_Simulation_Grid[Price_Adjustment_Percent]` (Set visual style to **Single Slider** from $-15\%$ to $+15\%$).
2. **Dynamic Output Cards**:
   - `Current Price`: `[Current Price]`
   - `Simulated Price`: `[Simulated Price]`
   - `Simulated Demand`: `[Simulated Demand]`
   - `Simulated Revenue`: `[Simulated Expected Revenue]` (`[Simulated Revenue Lift %]`)
   - `Simulated Profit`: `[Simulated Expected Profit]` (`[Simulated Profit Lift %]`)
   - `Competitor Gap`: `[Simulated Competitor Gap %]`
3. **Interactive Simulation Curves**:
   - Line Chart $\rightarrow$ X: `Candidate_Price`, Y: `Expected_Revenue`, `Expected_Profit`.
4. **Guardrail Compliance Panel (5 Status Badges)**:
   - Place 5 mini KPI cards bound to:
     - `[Guardrail Price Increase Status]`
     - `[Guardrail Price Decrease Status]`
     - `[Guardrail Competitor Gap Status]`
     - `[Guardrail Minimum Demand Status]`
     - `Cost Floor (Price >= Unit Cost)`
5. **Commercial Feasibility Verdict Banner**:
   - Large Callout Card bound to `[Simulator Decision Badge]`.

---

## 7. Phase 6: Validation & Quality Checklist

Before finalizing your demonstration:
- [x] All 6 navigation tabs switch pages smoothly.
- [x] Slicers on Page 5 and Page 6 correctly filter simulation curves.
- [x] All currency figures format cleanly in INR (`₹ #,##0.00`).
- [x] Slicing by category shows dynamic elasticity adjustments.
- [x] Synthetic dataset disclosure footer is clearly legible across all pages.
- [x] Model accuracy on Page 4 is strictly labeled **"Approx. Forecast Accuracy (89.34%)"**.
