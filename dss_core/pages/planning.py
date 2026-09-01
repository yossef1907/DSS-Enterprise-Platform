"""DSS Pro — Planning Pages (Pricing, Forecasting, Campaign Planner)."""
import customtkinter as ctk
import pandas as pd
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSCalc

class PricingPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "💰 Smart Pricing Engine", "AI-driven price optimization and margin analysis").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        inp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): inp.columnconfigure(i, weight=1)
        
        ctk.CTkEntry(inp, placeholder_text="Category", fg_color=BG_CARD2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(inp, placeholder_text="Current Price ($)", fg_color=BG_CARD2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkEntry(inp, placeholder_text="Target Margin %", fg_color=BG_CARD2).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(inp, text="Analyze Pricing", fg_color=ACCENT_PURPLE).grid(row=0, column=3, padx=10, pady=10)

        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        for i in range(4): kf.columnconfigure(i, weight=1)
        KPICard(kf, "🎯", "Optimal Price", "$112.50", "Max profit point", SUCCESS).grid(row=0, column=0, padx=5)
        KPICard(kf, "📊", "Elasticity", "-1.45", "High sensitivity", DANGER).grid(row=0, column=1, padx=5)
        KPICard(kf, "🏷️", "Strategy", "Premium", "vs Market Avg", ACCENT_BLUE).grid(row=0, column=2, padx=5)
        KPICard(kf, "💰", "Profit Uplift", "+$15.2k", "at Opt Price", SUCCESS).grid(row=0, column=3, padx=5)

class ForecastPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "📈 Future Profit Forecasting", "Revenue projections using Holt-Winters model").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(3): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📅", "Month 1 Forecast", fmt_money(M["forecast_m1"]), "Holt-Winters", ACCENT_BLUE).grid(row=0, column=0, padx=5)
        KPICard(kf, "📊", "Month 6 Forecast", fmt_money(M["forecast_m6"]), "Projected", ACCENT_PURPLE).grid(row=0, column=1, padx=5)
        KPICard(kf, "📈", "Monthly Growth", fmt_money(M["forecast_monthly_growth"]), "Estimated", SUCCESS).grid(row=0, column=2, padx=5)

        self._add_chart(ChartCard(self, "Revenue Forecast with Confidence Band", figsize=(10, 4))).grid(row=2, column=0, padx=20, pady=10)

class PlannerPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📋 Marketing Campaign Planner", "Simulate and optimize upcoming marketing campaigns").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        main_f = ctk.CTkFrame(self, fg_color="transparent")
        main_f.grid(row=1, column=0, sticky="nsew", padx=20)
        main_f.columnconfigure(0, weight=1)
        main_f.columnconfigure(1, weight=1)
        
        inp = ctk.CTkFrame(main_f, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(inp, text="Campaign Details", font=FONT_SUBTITLE).pack(pady=10)
        ctk.CTkEntry(inp, placeholder_text="Campaign Name", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
        ctk.CTkEntry(inp, placeholder_text="Budget ($)", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(inp, text="Generate Plan", fg_color=ACCENT_PURPLE).pack(pady=20)
        
        res = ctk.CTkFrame(main_f, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        res.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(res, text="Expected Results", font=FONT_SUBTITLE).pack(pady=10)
        self._add_chart(ChartCard(res, "Budget Allocation", figsize=(4, 3))).pack(padx=10, pady=10)
