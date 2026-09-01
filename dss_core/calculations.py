"""DSS Pro — Core Calculations Engine v1.0."""
import pandas as pd
import numpy as np

class DSSEngine:
    
    # ── REVENUE ──────────────────────────────────────
    @staticmethod
    def total_revenue(df, col='total_amount'):
        return df[col].sum() if col in df.columns else 0
    
    @staticmethod
    def revenue_growth(current, previous):
        if previous == 0: return 0
        return round((current - previous) / previous * 100, 2)
    
    @staticmethod
    def aov(revenue, orders):
        return round(revenue / orders, 2) if orders > 0 else 0
    
    @staticmethod
    def basket_size(quantity, orders):
        return round(quantity / orders, 2) if orders > 0 else 0
    
    @staticmethod
    def revenue_per_day(revenue, days):
        return round(revenue / days, 2) if days > 0 else 0
    
    @staticmethod
    def monthly_revenue(df, date_col, amount_col):
        if df.empty: return pd.Series()
        temp = df.copy()
        temp[date_col] = pd.to_datetime(temp[date_col])
        return temp.groupby(temp[date_col].dt.to_period('M'))[amount_col].sum()
    
    # ── CUSTOMER ─────────────────────────────────────
    @staticmethod
    def clv(aov, frequency, months=12):
        return round(aov * frequency * months, 2)
    
    @staticmethod
    def churn_rate(churned, total):
        return round(churned/total*100, 2) if total > 0 else 0
    
    @staticmethod
    def retention_rate(churned, total):
        return round(100 - DSSEngine.churn_rate(churned,total),2)
    
    @staticmethod
    def revenue_at_risk(high_risk_count, avg_clv):
        return round(high_risk_count * avg_clv, 2)
    
    @staticmethod
    def cac(budget, new_customers):
        return round(budget/new_customers,2) if new_customers>0 else 0
    
    @staticmethod
    def repeat_rate(returning, total):
        return round(returning/total*100,2) if total > 0 else 0
    
    @staticmethod
    def rfm_score(r, f, m):
        return int(r) + int(f) + int(m)
    
    @staticmethod
    def segment_health(clv, retention, churn_risk):
        return round(clv * retention / (churn_risk+1), 2)
    
    # ── MARKETING ────────────────────────────────────
    @staticmethod
    def roi(revenue, cost):
        return round((revenue-cost)/cost*100,2) if cost > 0 else 0
    
    @staticmethod
    def roas(revenue, ad_spend):
        return round(revenue/ad_spend,2) if ad_spend > 0 else 0
    
    @staticmethod
    def cpa(budget, conversions):
        return round(budget/conversions,2) if conversions > 0 else 0
    
    @staticmethod
    def cpm(cost, impressions):
        return round(cost/impressions*1000,2) if impressions>0 else 0
    
    @staticmethod
    def ctr(clicks, impressions):
        return round(clicks/impressions*100,2) if impressions>0 else 0
    
    @staticmethod
    def conversion_rate(conversions, visitors):
        return round(conversions/visitors*100,2) if visitors>0 else 0
    
    @staticmethod
    def campaign_roi(revenue, budget):
        return round((revenue-budget)/budget*100,2) if budget>0 else 0
    
    @staticmethod
    def optimal_budget_weight(channel_roi, total_roi):
        return round(channel_roi/total_roi,4) if total_roi>0 else 0
    
    @staticmethod
    def expected_campaign_revenue(budget, roi_pct):
        return round(budget * (1 + roi_pct/100), 2)
    
    @staticmethod
    def marketing_efficiency(revenue, budget, days):
        if budget==0 or days==0: return 0
        return round(revenue/(budget*days)*1000, 4)
    
    # ── PRODUCT ──────────────────────────────────────
    @staticmethod
    def gross_profit(revenue, cost):
        return round(revenue - cost, 2)
    
    @staticmethod
    def profit_margin(profit, revenue):
        return round(profit/revenue*100,2) if revenue > 0 else 0
    
    @staticmethod
    def break_even_units(fixed_cost, price, variable_cost):
        contrib = price - variable_cost
        return round(fixed_cost/contrib,0) if contrib > 0 else 0
    
    @staticmethod
    def break_even_revenue(fixed_cost, margin_pct):
        return round(fixed_cost/(margin_pct/100),2) if margin_pct>0 else 0
    
    @staticmethod
    def payback_months(investment, monthly_profit):
        return round(investment/monthly_profit,1) if monthly_profit>0 else 0
    
    @staticmethod
    def price_elasticity(demand_chg_pct, price_chg_pct):
        return round(demand_chg_pct/price_chg_pct,4) if price_chg_pct!=0 else 0
    
    @staticmethod
    def optimal_price(cost, target_margin_pct):
        return round(cost/(1-target_margin_pct/100),2)
    
    @staticmethod
    def expected_revenue(price, discount_pct, quantity):
        return round(price*(1-discount_pct/100)*quantity, 2)
    
    @staticmethod
    def marketing_cost(budget, ad_spend_pct):
        return round(budget*(ad_spend_pct/100), 2)
    
    @staticmethod
    def product_success_score(ml_prob, margin_score, market_score):
        return round(ml_prob*0.4 + margin_score*0.3 + market_score*0.3, 4)
    
    @staticmethod
    def discount_revenue_impact(price, disc_pct, quantity):
        original = price * quantity
        discounted = price*(1-disc_pct/100)*quantity
        return round(original - discounted, 2)
    
    # ── FORECASTING ──────────────────────────────────
    @staticmethod
    def monthly_growth_rate(series):
        if len(series) < 2 or series.iloc[0] == 0: return 0
        return round((series.iloc[-1]-series.iloc[0]) / series.iloc[0] / len(series) * 100, 4)
    
    @staticmethod
    def compound_forecast(base, monthly_rate_pct, months):
        return round(base*(1+monthly_rate_pct/100)**months, 2)
    
    @staticmethod
    def forecast_upper(value, confidence_pct=15):
        return round(value*(1+confidence_pct/100), 2)
    
    @staticmethod
    def forecast_lower(value, confidence_pct=15):
        return round(value*(1-confidence_pct/100), 2)
    
    @staticmethod
    def cumulative_profit(monthly_profits):
        return [round(sum(monthly_profits[:i+1]),2) for i in range(len(monthly_profits))]
    
    @staticmethod
    def forecast_accuracy(actual, predicted):
        if actual == 0: return 0
        return round((1-abs(actual-predicted)/actual)*100, 2)
    
    # ── INVENTORY ────────────────────────────────────
    @staticmethod
    def reorder_point(avg_daily, lead_time, safety_stock):
        return round(avg_daily * lead_time + safety_stock, 0)
    
    @staticmethod
    def safety_stock(std_demand, lead_time, z=1.65):
        return round(z * std_demand * (lead_time**0.5), 0)
    
    @staticmethod
    def eoq(annual_demand, order_cost, holding_cost):
        if holding_cost == 0: return 0
        return round((2*annual_demand*order_cost/holding_cost)**0.5, 0)
    
    @staticmethod
    def days_of_supply(stock, avg_daily):
        return round(stock/avg_daily, 1) if avg_daily > 0 else 0
    
    @staticmethod
    def stockout_risk_pct(stock, reorder_point):
        if reorder_point == 0: return 0
        return round(max(0, (reorder_point-stock)/reorder_point*100), 2)
    
    # ── MARKET BASKET ────────────────────────────────
    @staticmethod
    def lift(confidence, exp_confidence):
        return round(confidence/exp_confidence,4) if exp_confidence>0 else 0
    
    @staticmethod
    def bundle_revenue(support, avg_order, total_customers):
        return round(support * avg_order * total_customers, 2)
    
    @staticmethod
    def opportunity_score(lift, confidence, support):
        return round(lift * confidence * support * 100, 4)
    
    # ── SCENARIO ─────────────────────────────────────
    @staticmethod
    def scenario_revenue(base, growth_pct):
        return round(base*(1+growth_pct/100), 2)
    
    @staticmethod
    def pessimistic(base, rate, months):
        return DSSEngine.compound_forecast(base, rate-10, months)
    
    @staticmethod
    def base_case(base, rate, months):
        return DSSEngine.compound_forecast(base, rate, months)
    
    @staticmethod
    def optimistic(base, rate, months):
        return DSSEngine.compound_forecast(base, rate+20, months)
    
    @staticmethod
    def ab_lift(rev_b, rev_a):
        return round((rev_b-rev_a)/rev_a*100,2) if rev_a>0 else 0
    
    @staticmethod
    def ab_winner(rev_a, profit_a, rev_b, profit_b):
        return "A" if profit_a > profit_b else "B"

DSSCalc = DSSEngine
