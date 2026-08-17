# Power BI DAX Measures Library
## Project: Dynamic Pricing & Retail Revenue Intelligence System

> **Implementation Note**: In Power BI Desktop, create a dedicated disconnected table named `_Measures` to store all calculated measures in organized display folders.

---

## 1. Core Financial & Volume KPIs (Pages 1, 2)

### `Total Revenue`
```dax
Total Revenue = 
SUM('Fact_DailySales'[Revenue])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

### `Total Units Sold`
```dax
Total Units Sold = 
SUM('Fact_DailySales'[Units_Sold])
```
- **Format**: Whole Number (`#,##0`)
- **Display Folder**: `01_Core_Financials`

### `Total Cost of Goods Sold`
```dax
Total COGS = 
SUM('Fact_DailySales'[Total_Cost])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

### `Gross Profit`
```dax
Gross Profit = 
[Total Revenue] - [Total COGS]
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

### `Gross Margin %`
```dax
Gross Margin % = 
DIVIDE([Gross Profit], [Total Revenue], 0)
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `01_Core_Financials`

### `Average Selling Price (ASP)`
```dax
Average Selling Price = 
DIVIDE([Total Revenue], [Total Units Sold], 0)
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

### `Average Revenue per Product`
```dax
Average Revenue per Product = 
DIVIDE([Total Revenue], DISTINCTCOUNT('Fact_DailySales'[Product_ID]), 0)
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

### `Average Revenue per Store`
```dax
Average Revenue per Store = 
DIVIDE([Total Revenue], DISTINCTCOUNT('Fact_DailySales'[Store_ID]), 0)
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `01_Core_Financials`

---

## 2. Competitive Pricing & Elasticity KPIs (Page 3)

### `Average Our Price`
```dax
Average Our Price = 
AVERAGE('Fact_DailySales'[Our_Price])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `02_Pricing_Intelligence`

### `Average Competitor Price`
```dax
Average Competitor Price = 
AVERAGE('Fact_DailySales'[Competitor_Price])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `02_Pricing_Intelligence`

### `Price Gap (Absolute)`
```dax
Price Gap Absolute = 
[Average Our Price] - [Average Competitor Price]
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `02_Pricing_Intelligence`

### `Price Premium %`
```dax
Price Premium % = 
DIVIDE([Average Our Price] - [Average Competitor Price], [Average Competitor Price], 0)
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `02_Pricing_Intelligence`

### `Average Discount %`
```dax
Average Discount % = 
AVERAGE('Fact_DailySales'[Discount_Percent]) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `02_Pricing_Intelligence`

### `Pricing Position Classification`
```dax
Pricing Position = 
SWITCH(
    TRUE(),
    [Price Premium %] > 0.02, "Premium (> +2% vs Competitor)",
    [Price Premium %] < -0.02, "Discounted (< -2% vs Competitor)",
    "Parity (±2% vs Competitor)"
)
```
- **Format**: Text
- **Display Folder**: `02_Pricing_Intelligence`

### `Own-Price Elasticity Display`
```dax
Selected Own Elasticity = 
IF(
    HASONEVALUE('Dim_Product'[Product_ID]),
    SELECTEDVALUE('Dim_Product'[Own_Price_Elasticity]),
    AVERAGEX(VALUES('Dim_Product'[Product_ID]), 'Dim_Product'[Own_Price_Elasticity])
)
```
- **Format**: Decimal (`0.00`)
- **Display Folder**: `02_Pricing_Intelligence`

---

## 3. Demand Forecasting & Model Performance (Page 4)

### `XGBoost MAE`
```dax
XGBoost MAE = 
CALCULATE(MAX('Model_Evaluation_Metrics'[MAE]), 'Model_Evaluation_Metrics'[Model] = "XGBoost Regressor (Tuned)")
```
- **Format**: Decimal (`0.000`)
- **Display Folder**: `03_Model_Evaluation`

### `XGBoost RMSE`
```dax
XGBoost RMSE = 
CALCULATE(MAX('Model_Evaluation_Metrics'[RMSE]), 'Model_Evaluation_Metrics'[Model] = "XGBoost Regressor (Tuned)")
```
- **Format**: Decimal (`0.000`)
- **Display Folder**: `03_Model_Evaluation`

### `XGBoost R²`
```dax
XGBoost R2 = 
CALCULATE(MAX('Model_Evaluation_Metrics'[R2]), 'Model_Evaluation_Metrics'[Model] = "XGBoost Regressor (Tuned)")
```
- **Format**: Decimal (`0.0000`)
- **Display Folder**: `03_Model_Evaluation`

### `XGBoost WAPE %`
```dax
XGBoost WAPE % = 
CALCULATE(MAX('Model_Evaluation_Metrics'[WAPE_%]), 'Model_Evaluation_Metrics'[Model] = "XGBoost Regressor (Tuned)") / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `03_Model_Evaluation`

### `Approximate Forecast Accuracy %`
```dax
Approx Forecast Accuracy % = 
CALCULATE(MAX('Model_Evaluation_Metrics'[Approx_Forecast_Accuracy_%]), 'Model_Evaluation_Metrics'[Model] = "XGBoost Regressor (Tuned)") / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `03_Model_Evaluation`

---

## 4. Dynamic Pricing & Recommendation Engine (Page 5)

### `Selected Current Price`
```dax
Current Price = 
SELECTEDVALUE('Pricing_Recommendations'[Current_Price], AVERAGE('Pricing_Recommendations'[Current_Price]))
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Selected Competitor Price`
```dax
Competitor Price = 
SELECTEDVALUE('Pricing_Recommendations'[Competitor_Price], AVERAGE('Pricing_Recommendations'[Competitor_Price]))
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Selected Recommended Price`
```dax
Recommended Price = 
SELECTEDVALUE('Pricing_Recommendations'[Recommended_Price], AVERAGE('Pricing_Recommendations'[Recommended_Price]))
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Recommended Price Change %`
```dax
Rec Price Change % = 
SELECTEDVALUE('Pricing_Recommendations'[Price_Change_Percent], AVERAGE('Pricing_Recommendations'[Price_Change_Percent])) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Recommended Demand Change %`
```dax
Rec Demand Change % = 
SELECTEDVALUE('Pricing_Recommendations'[Demand_Change_Percent], AVERAGE('Pricing_Recommendations'[Demand_Change_Percent])) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Recommended Revenue Lift %`
```dax
Rec Revenue Lift % = 
SELECTEDVALUE('Pricing_Recommendations'[Revenue_Improvement_Percent], AVERAGE('Pricing_Recommendations'[Revenue_Improvement_Percent])) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Recommended Profit Lift %`
```dax
Rec Profit Lift % = 
SELECTEDVALUE('Pricing_Recommendations'[Profit_Lift_Percent], AVERAGE('Pricing_Recommendations'[Profit_Lift_Percent])) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Expected Revenue at Recommendation`
```dax
Rec Expected Revenue = 
SELECTEDVALUE('Pricing_Recommendations'[Recommended_Expected_Revenue], SUM('Pricing_Recommendations'[Recommended_Expected_Revenue]))
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Expected Profit at Recommendation`
```dax
Rec Expected Profit = 
SELECTEDVALUE('Pricing_Recommendations'[Recommended_Expected_Profit], SUM('Pricing_Recommendations'[Recommended_Expected_Profit]))
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Total Recommended Portfolio Revenue Lift (INR)`
```dax
Total Portfolio Revenue Lift INR = 
SUM('Pricing_Recommendations'[Recommended_Expected_Revenue]) - SUM('Pricing_Recommendations'[Current_Expected_Revenue])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Total Recommended Portfolio Profit Lift (INR)`
```dax
Total Portfolio Profit Lift INR = 
SUM('Pricing_Recommendations'[Recommended_Expected_Profit]) - SUM('Pricing_Recommendations'[Current_Expected_Profit])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `04_Pricing_Recommendations`

### `Dynamic Recommendation Explanation`
```dax
Dynamic Recommendation Text = 
VAR CurP = [Current Price]
VAR RecP = [Recommended Price]
VAR CompP = [Competitor Price]
VAR RevLift = [Rec Revenue Lift %]
VAR DemShift = [Rec Demand Change %]
VAR Conf = SELECTEDVALUE('Pricing_Recommendations'[Confidence_Level], "HIGH")
VAR Guard = SELECTEDVALUE('Pricing_Recommendations'[Guardrail_Status], "PASSED")
RETURN
IF(
    HASONEVALUE('Pricing_Recommendations'[Product_ID]) && HASONEVALUE('Pricing_Recommendations'[Store_ID]),
    IF(
        RecP > CurP,
        "RECOMMENDATION: Price increase from INR " & FORMAT(CurP, "#,##0.00") & " to INR " & FORMAT(RecP, "#,##0.00") & 
        " (+ " & FORMAT([Rec Price Change %], "0.0%") & ") captures margin while remaining within the competitor threshold (" & 
        FORMAT(CompP, "#,##0.00") & "). Expected revenue lift: +" & FORMAT(RevLift, "0.0%") & " with " & Conf & " confidence.",
        IF(
            RecP < CurP,
            "RECOMMENDATION: Strategic price markdown to INR " & FORMAT(RecP, "#,##0.00") & " (- " & 
            FORMAT(ABS([Rec Price Change %]), "0.0%") & ") stimulates demand volume by +" & FORMAT(DemShift, "0.0%") & 
            ", maximizing expected revenue lift to +" & FORMAT(RevLift, "0.0%") & " under " & Guard & " guardrails.",
            "RECOMMENDATION: Current price INR " & FORMAT(CurP, "#,##0.00") & " is already at the econometric optimal equilibrium point."
        )
    ),
    "Select a specific Product and Store from the slicers above to view individualized pricing rationalizations."
)
```
- **Format**: Text
- **Display Folder**: `04_Pricing_Recommendations`

---

## 5. What-If Simulator DAX Measures (Page 6)

### `Selected Price Adjustment Parameter %`
```dax
WhatIf Price Adjustment % = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Price_Adjustment_Percent], 0) / 100.0
```
- **Format**: Percentage (`0.0%`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Proposed Price`
```dax
Simulated Price = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Candidate_Price], [Current Price])
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Predicted Demand`
```dax
Simulated Demand = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Predicted_Demand], 0)
```
- **Format**: Decimal (`0.0`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Expected Revenue`
```dax
Simulated Expected Revenue = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Expected_Revenue], 0)
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Expected Profit`
```dax
Simulated Expected Profit = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Expected_Profit], 0)
```
- **Format**: Currency (`INR #,##0.00`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Revenue Lift %`
```dax
Simulated Revenue Lift % = 
VAR BaseRev = SELECTEDVALUE('Pricing_Recommendations'[Current_Expected_Revenue], 0)
VAR SimRev = [Simulated Expected Revenue]
RETURN
DIVIDE(SimRev - BaseRev, BaseRev, 0)
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Profit Lift %`
```dax
Simulated Profit Lift % = 
VAR BaseProf = SELECTEDVALUE('Pricing_Recommendations'[Current_Expected_Profit], 0)
VAR SimProf = [Simulated Expected Profit]
RETURN
DIVIDE(SimProf - BaseProf, BaseProf, 0)
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `05_What_If_Simulator`

### `Simulated Competitor Gap %`
```dax
Simulated Competitor Gap % = 
SELECTEDVALUE('Pricing_Simulation_Grid'[Competitor_Gap_Percent], 0) / 100.0
```
- **Format**: Percentage (`0.00%`)
- **Display Folder**: `05_What_If_Simulator`

### `Guardrail 1 Status: Max Price Increase (+10%)`
```dax
Guardrail Price Increase Status = 
IF([WhatIf Price Adjustment %] <= 0.10, "PASS", "VIOLATION (+10% Limit Exceeded)")
```
- **Format**: Text
- **Display Folder**: `05_What_If_Simulator`

### `Guardrail 2 Status: Max Price Decrease (-10%)`
```dax
Guardrail Price Decrease Status = 
IF([WhatIf Price Adjustment %] >= -0.10, "PASS", "VIOLATION (-10% Limit Exceeded)")
```
- **Format**: Text
- **Display Folder**: `05_What_If_Simulator`

### `Guardrail 3 Status: Max Competitor Premium (+5%)`
```dax
Guardrail Competitor Gap Status = 
IF([Simulated Competitor Gap %] <= 0.05, "PASS", "VIOLATION (Exceeds +5% Competitor Gap)")
```
- **Format**: Text
- **Display Folder**: `05_What_If_Simulator`

### `Guardrail 4 Status: Minimum Demand (>= 5 units)`
```dax
Guardrail Minimum Demand Status = 
IF([Simulated Demand] >= 5, "PASS", "VIOLATION (Demand < 5 units)")
```
- **Format**: Text
- **Display Folder**: `05_What_If_Simulator`

### `Overall Simulator Commercial Decision Badge`
```dax
Simulator Decision Badge = 
VAR IsFeas = SELECTEDVALUE('Pricing_Simulation_Grid'[Is_Feasible], FALSE)
VAR PAdj = [WhatIf Price Adjustment %]
RETURN
IF(
    IsFeas,
    IF(PAdj > 0, "FEASIBLE: Strategic Price Increase", IF(PAdj < 0, "FEASIBLE: Strategic Volume Markdown", "BASELINE CURRENT PRICE")),
    "UNACCEPTABLE: Guardrail Boundary Violated"
)
```
- **Format**: Text
- **Display Folder**: `05_What_If_Simulator`

---

## 6. Dynamic Visual Formatting & Indicator Colors

### `Color: Revenue Lift Indicator`
```dax
Color Rev Lift = 
IF([Rec Revenue Lift %] > 0, "#10B981", IF([Rec Revenue Lift %] < 0, "#EF4444", "#64748B"))
```

### `Color: Guardrail Badge`
```dax
Color Guardrail Badge = 
IF(SELECTEDVALUE('Pricing_Recommendations'[Guardrail_Status]) = "PASSED", "#10B981", "#EF4444")
```

### `Color: Confidence Level Badge`
```dax
Color Confidence Badge = 
SWITCH(
    SELECTEDVALUE('Pricing_Recommendations'[Confidence_Level]),
    "HIGH", "#10B981",
    "MEDIUM", "#F59E0B",
    "LOW", "#EF4444",
    "#64748B"
)
```
