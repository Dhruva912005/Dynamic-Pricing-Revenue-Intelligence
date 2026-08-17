# Power BI Dashboard Specification & Visual Design Architecture
## Project: Dynamic Pricing & Retail Revenue Intelligence System

---

## 1. Global Design System & Layout Framework

### Canvas & Theme Standard
- **Canvas Aspect Ratio**: 16:9 widescreen ($1920 \times 1080$ px or standard $1280 \times 720$ px)
- **Background**: Soft Off-White (`#F8FAFC`) with pure white card containers (`#FFFFFF`)
- **Visual Containers**: Subtle border (`#E2E8F0`), $6\text{px}$ corner radius, gentle $4\text{px}$ shadow
- **Typography**: Segoe UI Semibold (Titles & Callouts), Segoe UI Regular (Labels & Tooltips)
- **Global Header**:
  - **Banner Height**: $65\text{px}$ top bar (`#0F172A` Dark Navy)
  - **System Title**: **DYNAMIC PRICING & REVENUE INTELLIGENCE SYSTEM** (White, $16\text{pt}$ Bold)
  - **Navigation Bar**: 6 Pill Button Tabs on top-right:
    `[1. Executive Overview]` `[2. Sales Performance]` `[3. Pricing Intelligence]` `[4. Demand Forecast]` `[5. Dynamic Pricing]` `[6. What-If Simulator]`
- **Global Footer (Mandatory Disclosure)**:
  `"Dataset: Synthetic econometrically calibrated retail panel data developed for pricing simulation and model validation."` ($9\text{pt}$ Charcoal `#64748B`)

---

## 2. PAGE 1 — EXECUTIVE OVERVIEW

### Header
- **Title**: `Executive Overview`
- **Subtitle**: `Retail sales, pricing and revenue performance at a glance`

### Global Slicer Bar (Top, Y: 75px - 135px)
- **Slicers**: `Date Range` (Between slider), `Category` (Dropdown), `Product` (Dropdown), `Store` (Dropdown), `Region` (Tile/Button)

### KPI Cards Row (Y: 145px - 235px, 6 Rounded Cards)
1. **Total Revenue**: `[Total Revenue]` (Currency INR, e.g. `INR 6.18 Cr`)
2. **Total Units Sold**: `[Total Units Sold]` (Integer, e.g. `5.17M Units`)
3. **Gross Profit**: `[Gross Profit]` (Currency INR, e.g. `INR 2.47 Cr`)
4. **Gross Margin %**: `[Gross Margin %]` (Percentage, e.g. `39.97%`)
5. **Avg Selling Price**: `[Average Selling Price]` (Currency, e.g. `INR 1,196.20`)
6. **Competitor Price Gap %**: `[Price Premium %]` (Color-coded: Green if negative/discounted, Amber if $>+2\%$)

### Visual Grid (Y: 250px - 660px)

```
+----------------------------------------------------+--------------------------------+
| Visual 1: 2-Year Daily Revenue Trend (Line Chart)  | Visual 3: Revenue by Category  |
| X: Dim_Date[Date]                                  | Y: Dim_Product[Category]       |
| Y: [Total Revenue]                                 | X: [Total Revenue] (Clustered) |
+----------------------------------------------------+--------------------------------+
| Visual 2: Daily Sales Volume Trend (Area/Line)     | Visual 4: Revenue by Region    |
| X: Dim_Date[Date]                                  | Y: Dim_Store[Region]           |
| Y: [Total Units Sold]                              | X: [Total Revenue]             |
+----------------------------------------------------+--------------------------------+
| Visual 5: Top 10 Revenue Generating Products (Horizontal Bar Chart)                 |
| Y: Dim_Product[Product_Name] (Top 10 Filter by [Total Revenue])                     |
| X: [Total Revenue], Data Label: [Gross Margin %]                                    |
+-------------------------------------------------------------------------------------+
```

### Dynamic Business Insights Panel (Bottom Container)
- **Dynamic KPI Card**: Sourced from actual measures:
  - *Top Category*: Electronics ($38.4\%$ total revenue contribution).
  - *Best-Selling SKU*: `PROD_02` (Smart Fitness Watch — INR 1.54 Cr total revenue).
  - *Competitive Position*: Portfolio average is priced at a **$2.06\%$ discount** relative to benchmark competitor prices.

---

## 3. PAGE 2 — SALES & PRODUCT PERFORMANCE

### Header
- **Title**: `Sales & Product Performance`
- **Subtitle**: `Product, category, store and regional performance analysis`

### KPI Cards Row
1. **Total Revenue**: `[Total Revenue]`
2. **Total Units Sold**: `[Total Units Sold]`
3. **Avg Revenue / Product**: `[Average Revenue per Product]` (e.g. `INR 30.89 Lakhs`)
4. **Avg Revenue / Store**: `[Average Revenue per Store]` (e.g. `INR 1.54 Cr`)

### Visual Grid
1. **Top 10 Products by Revenue**: Horizontal Bar Chart (`Dim_Product[Product_Name]` vs `[Total Revenue]`).
2. **Top 10 Products by Units Sold**: Horizontal Bar Chart (`Dim_Product[Product_Name]` vs `[Total Units Sold]`).
3. **Revenue by Category**: Donut Chart (`Category` vs `[Total Revenue]`).
4. **Volume Share by Category**: 100% Stacked Bar Chart (`Category` vs `[Total Units Sold]`).
5. **Revenue by Store**: Clustered Column Chart (`Store_Name` vs `[Total Revenue]`, sorted by performance).
6. **BCG-Style Product Segmentation Scatter Matrix**:
   - **X-Axis**: `[Total Units Sold]` (Volume Dimension)
   - **Y-Axis**: `[Total Revenue]` (Value Dimension)
   - **Bubble Size**: `[Gross Profit]`
   - **Legend**: `Dim_Product[Category]`
   - **Details / Tooltips**: `Dim_Product[Product_Name]`, `[Gross Margin %]`, `[Average Selling Price]`
   - **Quadrant Lines**: Constant lines at Median Volume and Median Revenue:
     - **Top-Right (Stars)**: High Volume / High Value (e.g. `PROD_02 Smart Watch`, `PROD_01 Headphones`).
     - **Bottom-Right (Cash Cows)**: High Volume / Low Value (e.g. `PROD_05 Basmati Rice`, `PROD_11 T-Shirt`).
     - **Top-Left (Question Marks)**: Low Volume / High Value (e.g. `PROD_13 Air Fryer`).
     - **Bottom-Left (Dogs)**: Low Volume / Low Value (e.g. `PROD_20 Sunscreen Gel`).

---

## 4. PAGE 3 — PRICING INTELLIGENCE

### Header
- **Title**: `Pricing Intelligence`
- **Subtitle**: `Competitive pricing, discount behavior and price-demand relationships`

### KPI Cards Row
1. **Avg Our Price**: `[Average Our Price]`
2. **Avg Competitor Price**: `[Average Competitor Price]`
3. **Avg Price Gap (INR)**: `[Price Gap Absolute]`
4. **Avg Price Premium %**: `[Price Premium %]`
5. **Avg Promotional Discount**: `[Average Discount %]`

### Visual Grid
1. **Our Price vs Competitor Price Comparison**:
   - **Visual**: Clustered Bar Chart.
   - **Y-Axis**: `Dim_Product[Product_Name]`.
   - **X-Axis**: `[Average Our Price]` (Navy `#1E3A8A`) and `[Average Competitor Price]` (Grey `#94A3B8`).
2. **Price vs Demand Empirical Curve (Scatter Plot)**:
   - **X-Axis**: `Fact_DailySales[Our_Price]`.
   - **Y-Axis**: `Fact_DailySales[Units_Sold]`.
   - **Legend**: `Dim_Product[Category]`.
   - **Trend Line**: Linear / Polynomial fit demonstrating clear downward slope.
3. **Discount Sensitivity vs Demand Volume**:
   - **X-Axis**: `Fact_DailySales[Discount_Percent]` (0%, 5%, 10%, 15%, 20%, 25%).
   - **Y-Axis**: `[Total Units Sold]`.
   - **Visual**: Clustered Column with Line for Average Daily Demand.
4. **Empirical Price Elasticity Comparison Table**:
   - Columns: `Product Name`, `Category`, `Own-Price Elasticity (β)`, `Cross-Price Elasticity (γ)`, `Elasticity Classification`, `R²`.
   - **Explaining Callout**:
     - *Negative Own-Price Elasticity*: Higher price is associated with lower demand.
     - *Positive Cross-Price Elasticity*: Higher competitor price increases demand for our SKU.

---

## 5. PAGE 4 — DEMAND FORECAST & MODEL PERFORMANCE

### Header
- **Title**: `Demand Forecast & Model Performance`
- **Subtitle**: `XGBoost demand forecasting and model evaluation`

### Validated Model Metrics (Top KPI Cards)
1. **Selected Model**: `XGBoost Regressor (Tuned)`
2. **MAE**: `11.242`
3. **RMSE**: `16.077`
4. **R²**: `0.9223`
5. **WAPE**: `10.66%`
6. **Approx. Forecast Accuracy**: `89.34%` *(Explicitly labeled as Approx. Forecast Accuracy: $100 - \text{WAPE}$)*

### Visual Grid
1. **Actual vs XGBoost Forecast Demand (Test Partition Line Chart)**:
   - **Source**: `dashboard/Demand_Forecast_Test_Set.csv` (or test slice).
   - **X-Axis**: `Date`.
   - **Values**: `Actual Demand` (Dark Navy `#0F172A` solid) vs `XGBoost Forecast` (Vibrant Blue `#2563EB` dashed line).
   - **Slicers**: `Category`, `Product`, `Store`.
2. **Benchmark Model Comparison Matrix (Table / Clustered Bar)**:
   - Compares:
     - `Naive Baseline (Lag 1)`: MAE = 26.528, $R^2 = 0.5318$, WAPE = 25.16%
     - `7-Day Moving Average`: MAE = 21.878, $R^2 = 0.6923$, WAPE = 20.75%
     - `Random Forest Regressor`: MAE = 12.184, $R^2 = 0.9068$, WAPE = 11.56%
     - `XGBoost Regressor (Champion)`: MAE = 11.242, $R^2 = 0.9223$, WAPE = 10.66%
3. **XGBoost Feature Importance (Horizontal Bar Chart)**:
   - **Source**: `dashboard/Feature_Importance.csv`.
   - **Y-Axis**: `Feature` (Top 10: `Demand_Rolling_Mean_14`, `Promotion_Flag`, `Demand_Rolling_Mean_7`, `Discount_Percent`, `Demand_Rolling_Mean_28`, `DayOfWeek`).
   - **X-Axis**: `Importance_Percent`.

---

## 6. PAGE 5 — DYNAMIC PRICING RECOMMENDATIONS *(Core Business Page)*

### Header
- **Title**: `Dynamic Pricing Recommendations`
- **Subtitle**: `AI-driven price recommendations based on demand, competition and business constraints`

### Top Filter Slicers
- `Product Slicer` (Single-select dropdown), `Store Slicer` (Single-select dropdown), `Category Slicer`.

### Current vs Recommended KPI Row
| Metric | Current Baseline | AI Recommendation | Impact / Delta |
| :--- | :---: | :---: | :---: |
| **Price** | `[Current Price]` | `[Recommended Price]` | `[Rec Price Change %]` (Color-coded) |
| **Competitor Gap** | `[Competitor Gap Base]` | `[Competitor Gap Rec]` | Safe ($\le +5.0\%$) |
| **Predicted Demand** | `[Current Pred Demand]` | `[Rec Pred Demand]` | `[Rec Demand Change %]` |
| **Expected Revenue** | `[Current Exp Revenue]` | `[Rec Expected Revenue]`| `[Rec Revenue Lift %]` (Green badge) |
| **Expected Profit** | `[Current Exp Profit]` | `[Rec Expected Profit]` | `[Rec Profit Lift %]` (Green badge) |

### Visual Grid
1. **Price vs Expected Revenue Simulation Curve**:
   - **X-Axis**: `Pricing_Simulation_Grid[Candidate_Price]`.
   - **Y-Axis**: `Pricing_Simulation_Grid[Expected_Revenue]`.
   - **Visual**: Line Chart with a marker indicating the **Optimal Recommended Price**.
2. **Price vs Predicted Demand Curve**:
   - **X-Axis**: `Pricing_Simulation_Grid[Candidate_Price]`.
   - **Y-Axis**: `Pricing_Simulation_Grid[Predicted_Demand]`.
   - **Visual**: Line chart demonstrating the downward elasticity slope.
3. **Portfolio Pricing Recommendations Master Table**:
   - **Source**: `dashboard/Pricing_Recommendations_Enriched.csv`.
   - **Columns**: `Product Name`, `Store Name`, `Current Price`, `Competitor Price`, `Recommended Price`, `Price Change %`, `Predicted Demand`, `Demand Change %`, `Expected Revenue`, `Revenue Lift %`, `Expected Profit`, `Profit Lift %`, `Confidence Level`, `Guardrail Status`.
   - **Conditional Formatting**:
     - `Revenue Lift %` & `Profit Lift %`: Gradient (Green for positive, Red for negative).
     - `Guardrail Status`: Green pill (`PASSED`), Red pill (`VIOLATED`).
     - `Confidence Level`: Green (`HIGH`), Amber (`MEDIUM`), Red (`LOW`).
4. **Dynamic Natural Language Commercial Rationalization Box**:
   - Sourced from measure `[Dynamic Recommendation Text]`.
   - *Example*: `"RECOMMENDATION: Price increase from INR 2,999.00 to INR 3,268.91 (+9.0%) captures margin while keeping competitor gap at +0.3%. Expected revenue lift: +3.6% (INR 2.39L) with HIGH confidence under PASSED guardrails."*

---

## 7. PAGE 6 — WHAT-IF PRICING SIMULATOR

### Header
- **Title**: `What-If Pricing Simulator`
- **Subtitle**: `Simulate price changes before making an operational pricing decision`

### Interactive Parameter Slicer (Y: 140px - 200px)
- **What-If Slider**: `Price Adjustment %`
  - Range: $-15\%$ to $+15\%$
  - Step: $1\%$
  - Default: $0\%$

### Live Simulation KPI Comparison Cards
1. **Current Price**: `[Current Price]` (Baseline)
2. **Simulated Price**: `[Simulated Price]`
3. **Simulated Demand**: `[Simulated Demand]` (`[Demand Shift %]`)
4. **Simulated Expected Revenue**: `[Simulated Expected Revenue]` (`[Simulated Revenue Lift %]`)
5. **Simulated Expected Profit**: `[Simulated Expected Profit]` (`[Simulated Profit Lift %]`)
6. **Competitor Gap at Simulated Price**: `[Simulated Competitor Gap %]`

### Visual Grid
1. **Interactive Revenue & Profit Curve**:
   - **X-Axis**: `Pricing_Simulation_Grid[Candidate_Price]`.
   - **Y-Axis 1 (Line)**: `Expected_Revenue`.
   - **Y-Axis 2 (Line)**: `Expected_Profit`.
   - **Reference Line**: Vertical line linking to selected `[Simulated Price]`.
2. **Pricing Guardrails Compliance Matrix (5 Status Cards)**:
   - `Guardrail 1 (Max Increase +10%)`: `[Guardrail Price Increase Status]` (Green PASS / Red FAIL)
   - `Guardrail 2 (Max Decrease -10%)`: `[Guardrail Price Decrease Status]` (Green PASS / Red FAIL)
   - `Guardrail 3 (Competitor Gap <= +5%)`: `[Guardrail Competitor Gap Status]` (Green PASS / Red FAIL)
   - `Guardrail 4 (Minimum Demand >= 5)`: `[Guardrail Minimum Demand Status]` (Green PASS / Red FAIL)
   - `Guardrail 5 (Cost Floor)`: PASS (Price $\ge$ Unit Cost)
3. **Commercial Decision Verdict Banner**:
   - Displays `[Simulator Decision Badge]`:
     - **Green Banner**: `COMMERCIALLY ACCEPTABLE: Safe Margin Capture / Volume Markdown`.
     - **Red Banner**: `UNACCEPTABLE: Guardrail Boundary Violated (Action Blocked)`.
