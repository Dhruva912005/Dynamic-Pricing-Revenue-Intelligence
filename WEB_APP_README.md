# Dynamic Pricing & Revenue Intelligence System — Web Application

An enterprise-grade **Retail Revenue Intelligence & Dynamic Pricing Decision Support Platform** built with **Streamlit**, **Plotly**, **XGBoost**, and **Scikit-Learn**.

---

## 1. Overview & Capabilities

This web application operationalizes econometrically calibrated demand forecasting, competitive intelligence, and business-constrained dynamic price optimization into an interactive, decision-support interface.

### Key Functional Pages
1. **Executive Overview**: High-level sales performance, revenue trends, margin health, and dynamic business insights.
2. **Sales Analytics**: Top 10 product value/volume rankings, store comparisons, and an interactive BCG-style product segmentation matrix.
3. **Demand Forecast**: Holdout test evaluation ($R^2 = 0.9223$, $\text{WAPE} = 10.66\%$), actual vs predicted trajectory curves, and model explainability.
4. **Pricing Intelligence**: Competitor parity benchmarking, empirical price-demand scatter, and log-log elasticity analysis.
5. **Dynamic Pricing (Decision Hub)**: AI-driven price recommendations, current vs recommended comparison cards, revenue/demand sensitivity curves, and natural language commercial rationalizations.
6. **What-If Simulator**: Interactive $-15\%$ to $+15\%$ price slider, dual sensitivity curves, and a 5-point operational guardrail compliance panel.
7. **Model Performance**: Benchmark matrix comparing Naive Baseline, 7-Day MA, Random Forest, and Tuned XGBoost.
8. **About Project**: Complete system architecture, technology stack, and econometric methodology.

---

## 2. Quick Start / Running Locally

### Step 1: Install Dependencies
Ensure you are in the project root directory:
```bash
pip install -r requirements-web.txt
```

### Step 2: Launch the Web Application
```bash
streamlit run app.py
```

### Step 3: Access in Browser
The application will automatically open in your default browser at:
```
http://localhost:8501
```

---

## 3. Technology Stack

- **Frontend & Web Framework**: Streamlit Cloud Architecture
- **Interactive Visualization**: Plotly Express & Plotly Graph Objects
- **Data Engineering**: Pandas Panel Series, NumPy
- **Machine Learning Engine**: XGBoost Regressor (Tuned), Scikit-Learn
- **Econometric Modeling**: Statsmodels (OLS Multiplicative Log-Log Formulation)
- **Serialization**: Joblib

---

## 4. Production Guardrails & Business Constraints

Every dynamic pricing recommendation is bounded by 5 commercial guardrails:
1. **Maximum Price Increase**: Hard ceiling capped at $+10.0\%$ to avoid customer churn.
2. **Maximum Price Decrease**: Floor capped at $-10.0\%$ to prevent margin erosion.
3. **Competitor Price Ceiling**: Maximum price premium capped at $\le +5.0\%$ over benchmark competitor.
4. **Minimum Expected Demand**: Predicted daily volume must satisfy $\ge 5\text{ units}$.
5. **Wholesale Cost Floor**: Selling price can never fall below wholesale procurement cost (`Unit_Cost`).

---

## 5. Deployment to Streamlit Community Cloud

1. Push your repository to GitHub.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New App"** and select your repository and branch.
4. Set the main file path to:
   ```
   app.py
   ```
5. Deploy! All required configurations (`.streamlit/config.toml` and `requirements-web.txt`) are pre-packaged.

---

## 6. Dataset Disclosure
> **Dataset Disclosure**: Synthetic econometrically calibrated retail panel data developed for pricing simulation and model validation.
