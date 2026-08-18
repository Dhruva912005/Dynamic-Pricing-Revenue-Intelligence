"""
Dynamic Pricing & Revenue Intelligence Optimizer Engine
Implements econometric log-log elasticity analysis, competitor-aware candidate grid simulation,
revenue/profit maximization under guardrails, confidence scoring, and what-if scenario simulations.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import statsmodels.api as sm

class DynamicPricingEngine:
    def __init__(self, model_path=None, pipeline_path=None, features_path="models/feature_columns.json"):
        """
        Initializes the dynamic pricing engine by loading ML artifacts.
        Supports native JSON models, pickle models, and robust preprocessor fallback.
        """
        json_path = os.path.join("models", "demand_model.json")
        default_model_path = model_path or (json_path if os.path.exists(json_path) else "models/demand_model.pkl")
        default_pipe_path = pipeline_path or "models/preprocessing_pipeline.pkl"
        
        if default_model_path.endswith(".json") and os.path.exists(default_model_path):
            import xgboost as xgb
            self.model = xgb.XGBRegressor()
            self.model.load_model(default_model_path)
        elif os.path.exists(default_model_path):
            self.model = joblib.load(default_model_path)
        else:
            raise FileNotFoundError(f"Demand model missing at {default_model_path}")
            
        try:
            if os.path.exists(default_pipe_path):
                self.preprocessor = joblib.load(default_pipe_path)
            else:
                raise FileNotFoundError()
        except Exception:
            from web.data_loader import reconstruct_preprocessor
            self.preprocessor = reconstruct_preprocessor()
        
        if os.path.exists(features_path):
            with open(features_path, "r") as f:
                self.feature_meta = json.load(f)
        else:
            self.feature_meta = {}

    @staticmethod
    def estimate_price_elasticity(df, min_obs=30):
        """
        Estimates empirical price elasticity using log-log OLS regression:
        ln(Units_Sold) = alpha + beta * ln(Our_Price) + gamma * ln(Competitor_Price) + epsilon
        Returns a DataFrame with product-level and category-level elasticity estimates.
        """
        elasticity_records = []
        
        for pid, grp in df.groupby('Product_ID'):
            # Filter non-zero demand and price
            sub = grp[(grp['Units_Sold'] > 0) & (grp['Our_Price'] > 0) & (grp['Competitor_Price'] > 0)].copy()
            
            if len(sub) < min_obs:
                continue
                
            y = np.log(sub['Units_Sold'])
            X = np.log(sub[['Our_Price', 'Competitor_Price']])
            X = sm.add_constant(X)
            
            try:
                ols_res = sm.OLS(y, X).fit()
                beta_own = ols_res.params.get('Our_Price', np.nan)
                p_val_own = ols_res.pvalues.get('Our_Price', np.nan)
                gamma_comp = ols_res.params.get('Competitor_Price', np.nan)
                r_squared = ols_res.rsquared
                
                # Interpretation
                if beta_own < -1.0:
                    interp = "Elastic (Highly Price-Sensitive)"
                elif -1.0 <= beta_own < 0:
                    interp = "Inelastic (Volume Resilient)"
                else:
                    interp = "Positive/Anomalous Response"
                    
                elasticity_records.append({
                    "Product_ID": pid,
                    "Product_Name": sub['Product_Name'].iloc[0],
                    "Category": sub['Category'].iloc[0],
                    "Observations": len(sub),
                    "Own_Price_Elasticity": round(float(beta_own), 3),
                    "Cross_Price_Elasticity": round(float(gamma_comp), 3),
                    "P_Value": round(float(p_val_own), 4),
                    "R_Squared": round(float(r_squared), 3),
                    "Elasticity_Category": interp
                })
            except Exception:
                continue
                
        elasticity_df = pd.DataFrame(elasticity_records)
        return elasticity_df

    def generate_price_candidates(self, current_price, competitor_price, 
                                   max_increase_pct=10.0, max_decrease_pct=10.0,
                                   max_competitor_premium_pct=5.0, step_pct=1.0):
        """
        Generates realistic candidate prices around current price and competitor price.
        """
        min_p = current_price * (1.0 - max_decrease_pct / 100.0)
        max_p = current_price * (1.0 + max_increase_pct / 100.0)
        
        # Step size
        step_val = max(1.0, current_price * (step_pct / 100.0))
        candidate_prices = np.arange(min_p, max_p + step_val, step_val)
        
        # Always include exact current price and competitor price (if within reasonable bounds)
        candidate_prices = np.unique(np.round(np.append(candidate_prices, [current_price, competitor_price]), 2))
        return candidate_prices

    def simulate_price_change(self, base_row_df, candidate_price, unit_cost=None,
                              min_expected_demand=5, max_competitor_premium_pct=5.0,
                              max_price_increase_pct=10.0, max_price_decrease_pct=10.0):
        """
        Simulates the demand, expected revenue, and profit for a specific candidate price on a given state row.
        """
        sim_df = base_row_df.copy()
        cur_price = float(sim_df['Our_Price'].iloc[0])
        comp_price = float(sim_df['Competitor_Price'].iloc[0])
        cost = unit_cost if unit_cost is not None else float(sim_df.get('Unit_Cost', pd.Series([0])).iloc[0])
        
        # Modify price and dependent competitive features
        sim_df['Our_Price'] = candidate_price
        sim_df['Price_Difference'] = candidate_price - comp_price
        sim_df['Price_Ratio'] = candidate_price / (comp_price + 1e-6)
        sim_df['Price_Premium_Percent'] = ((candidate_price - comp_price) / (comp_price + 1e-6)) * 100.0
        
        if 'Base_Price' in sim_df.columns:
            base_p = float(sim_df['Base_Price'].iloc[0])
            sim_df['Discount_From_Base'] = ((base_p - candidate_price) / (base_p + 1e-6)) * 100.0
        
        # Apply preprocessing pipeline
        X_trans = self.preprocessor.transform(sim_df)
        pred_demand = float(np.clip(self.model.predict(X_trans)[0], 0, None))
        
        # Expected Financials
        exp_revenue = round(candidate_price * pred_demand, 2)
        exp_cost = round(cost * pred_demand, 2)
        exp_profit = round(exp_revenue - exp_cost, 2) if cost > 0 else None
        
        # Metrics relative to current price
        price_change_pct = ((candidate_price - cur_price) / cur_price) * 100.0
        competitor_gap_pct = ((candidate_price - comp_price) / comp_price) * 100.0
        
        # Guardrail Validation
        violations = []
        if price_change_pct > max_price_increase_pct:
            violations.append(f"Exceeds max price increase limit (+{max_price_increase_pct}%)")
        if price_change_pct < -max_price_decrease_pct:
            violations.append(f"Exceeds max price decrease limit (-{max_price_decrease_pct}%)")
        if competitor_gap_pct > max_competitor_premium_pct:
            violations.append(f"Exceeds max competitor premium (+{max_competitor_premium_pct}%)")
        if pred_demand < min_expected_demand:
            violations.append(f"Predicted demand ({pred_demand:.1f}) below threshold ({min_expected_demand})")
        if cost > 0 and candidate_price < cost:
            violations.append("Candidate price below wholesale unit cost")
            
        guardrail_status = "PASSED" if len(violations) == 0 else f"VIOLATED: {'; '.join(violations)}"
        
        return {
            "Candidate_Price": round(candidate_price, 2),
            "Predicted_Demand": round(pred_demand, 2),
            "Expected_Revenue": exp_revenue,
            "Expected_Profit": exp_profit,
            "Price_Change_Percent": round(price_change_pct, 2),
            "Competitor_Gap_Percent": round(competitor_gap_pct, 2),
            "Guardrail_Status": guardrail_status,
            "Is_Feasible": len(violations) == 0
        }

    def compute_confidence_score(self, hist_prices, candidate_price, observations_count, r2_score=0.85):
        """
        Transparent confidence scoring based on historical price density, sample count, and model R2.
        """
        p_min, p_max = np.min(hist_prices), np.max(hist_prices)
        price_in_range = (candidate_price >= p_min * 0.95) and (candidate_price <= p_max * 1.05)
        
        score = 0
        reasons = []
        
        if observations_count >= 100:
            score += 2
            reasons.append("High historical observation density (>100)")
        elif observations_count >= 30:
            score += 1
            reasons.append("Moderate observation sample")
        else:
            reasons.append("Sparse historical sample (<30)")
            
        if price_in_range:
            score += 2
            reasons.append("Candidate price falls within observed empirical distribution")
        else:
            reasons.append("Candidate price requires extrapolation outside observed envelope")
            
        if r2_score >= 0.80:
            score += 2
            reasons.append(f"Demand model demonstrated high validation explanatory power (R²={r2_score:.2f})")
        else:
            score += 1
            
        if score >= 5:
            confidence = "HIGH"
        elif score >= 3:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
            
        return confidence, "; ".join(reasons)

    def optimize_price(self, base_row_df, hist_prices_series=None, unit_cost=None,
                       objective="MAX_REVENUE", max_increase_pct=10.0, 
                       max_decrease_pct=10.0, max_competitor_premium_pct=5.0):
        """
        Evaluates all candidate prices, enforces guardrails, and identifies the optimal price.
        """
        cur_price = float(base_row_df['Our_Price'].iloc[0])
        comp_price = float(base_row_df['Competitor_Price'].iloc[0])
        cost = unit_cost if unit_cost is not None else float(base_row_df.get('Unit_Cost', pd.Series([0])).iloc[0])
        
        candidates = self.generate_price_candidates(
            cur_price, comp_price,
            max_increase_pct=max_increase_pct,
            max_decrease_pct=max_decrease_pct,
            max_competitor_premium_pct=max_competitor_premium_pct
        )
        
        sim_results = []
        for cand in candidates:
            res = self.simulate_price_change(
                base_row_df, cand, unit_cost=cost,
                max_competitor_premium_pct=max_competitor_premium_pct,
                max_price_increase_pct=max_increase_pct,
                max_price_decrease_pct=max_decrease_pct
            )
            sim_results.append(res)
            
        sim_df = pd.DataFrame(sim_results)
        
        # Evaluate baseline at current price
        base_res = self.simulate_price_change(base_row_df, cur_price, unit_cost=cost)
        cur_demand = base_res['Predicted_Demand']
        cur_revenue = base_res['Expected_Revenue']
        cur_profit = base_res['Expected_Profit']
        
        # Filter feasible candidates
        feasible_df = sim_df[sim_df['Is_Feasible']].copy()
        
        if len(feasible_df) == 0:
            # Fallback to current price if all candidates violate constraints
            optimal_cand = cur_price
            opt_res = base_res
            opt_reason = "No candidate satisfied guardrails; preserving current price."
        else:
            if objective == "MAX_PROFIT" and cost > 0 and 'Expected_Profit' in feasible_df.columns:
                best_row = feasible_df.sort_values(by='Expected_Profit', ascending=False).iloc[0]
            else:
                best_row = feasible_df.sort_values(by='Expected_Revenue', ascending=False).iloc[0]
                
            optimal_cand = best_row['Candidate_Price']
            opt_res = best_row.to_dict()
            
            rev_diff_pct = ((opt_res['Expected_Revenue'] - cur_revenue) / (cur_revenue + 1e-6)) * 100.0
            
            if optimal_cand > cur_price:
                opt_reason = f"Price increase to INR {optimal_cand:.2f} captures margin while keeping competitor gap at {opt_res['Competitor_Gap_Percent']:.1f}%, yielding expected revenue lift of +{rev_diff_pct:.2f}%."
            elif optimal_cand < cur_price:
                opt_reason = f"Price reduction to INR {optimal_cand:.2f} stimulates demand volume ({opt_res['Predicted_Demand']} units), driving expected revenue lift of +{rev_diff_pct:.2f}%."
            else:
                opt_reason = f"Current price INR {cur_price:.2f} is already at the optimal balance point."
                
        # Confidence calculation
        hist_p = hist_prices_series.values if hist_prices_series is not None else np.array([cur_price])
        confidence_label, conf_details = self.compute_confidence_score(hist_p, optimal_cand, len(hist_p))
        
        rev_improvement_pct = ((opt_res['Expected_Revenue'] - cur_revenue) / (cur_revenue + 1e-6)) * 100.0
        demand_change_pct = ((opt_res['Predicted_Demand'] - cur_demand) / (cur_demand + 1e-6)) * 100.0
        
        recommendation = {
            "Product_ID": base_row_df['Product_ID'].iloc[0],
            "Product_Name": base_row_df['Product_Name'].iloc[0],
            "Category": base_row_df['Category'].iloc[0],
            "Store_ID": base_row_df['Store_ID'].iloc[0],
            "Store_Name": base_row_df['Store_Name'].iloc[0],
            "Current_Price": cur_price,
            "Competitor_Price": comp_price,
            "Recommended_Price": optimal_cand,
            "Price_Change_Percent": opt_res['Price_Change_Percent'],
            "Competitor_Gap_Percent": opt_res['Competitor_Gap_Percent'],
            "Current_Predicted_Demand": cur_demand,
            "Recommended_Predicted_Demand": opt_res['Predicted_Demand'],
            "Demand_Change_Percent": round(demand_change_pct, 2),
            "Current_Expected_Revenue": cur_revenue,
            "Recommended_Expected_Revenue": opt_res['Expected_Revenue'],
            "Revenue_Improvement_Percent": round(rev_improvement_pct, 2),
            "Unit_Cost": cost,
            "Current_Expected_Profit": cur_profit,
            "Recommended_Expected_Profit": opt_res.get('Expected_Profit'),
            "Confidence_Level": confidence_label,
            "Confidence_Rationale": conf_details,
            "Recommendation_Reason": opt_reason,
            "Simulation_Grid": sim_df
        }
        
        return recommendation
