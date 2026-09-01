"""DSS Pro — Analytics Pages (Sales, Customers, Churn)."""
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSCalc

class SalesPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📊 Sales Intelligence", "Deep dive into e-commerce revenue and order trends").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        M = METRICS
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): kf.columnconfigure(i, weight=1)
        
        KPICard(kf, "💰", "Total Revenue", fmt_money(M["ecom_revenue"]), "Historical Total", ACCENT_BLUE).grid(row=0, column=0, padx=5)
        KPICard(kf, "📦", "Total Orders", fmt_count(M["ecom_orders"]), "Validated Orders", ACCENT_PURPLE).grid(row=0, column=1, padx=5)
        KPICard(kf, "🛒", "AOV", fmt_money(M["ecom_aov"]), "Avg Order Value", SUCCESS).grid(row=0, column=2, padx=5)
        KPICard(kf, "📊", "Growth", fmt_pct(M["revenue_growth_pct"]), "Monthly Trend", WARNING).grid(row=0, column=3, padx=5)

        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        charts.columnconfigure((0,1), weight=1)
        
        self._add_chart(ChartCard(charts, "Monthly Revenue")).grid(row=0, column=0, padx=5)
        self._add_chart(ChartCard(charts, "Category Distribution")).grid(row=0, column=1, padx=5)

class CustomersPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "👥 Customer Intelligence 360", "Comprehensive view of your customer base").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        main_f = ctk.CTkFrame(self, fg_color="transparent")
        main_f.grid(row=1, column=0, sticky="nsew", padx=20)
        main_f.columnconfigure(0, weight=1)
        main_f.columnconfigure(1, weight=2)
        
        # Left: Search/Filters
        left = ctk.CTkFrame(main_f, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        ctk.CTkLabel(left, text="🔍 Search Customer", font=FONT_SUBTITLE).pack(pady=10)
        ctk.CTkEntry(left, placeholder_text="Enter Customer ID...", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(left, text="Search Profile", fg_color=ACCENT_PURPLE).pack(pady=10)
        
        # Right: Overview
        right = ctk.CTkFrame(main_f, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")
        
        kf = ctk.CTkFrame(right, fg_color="transparent")
        kf.pack(fill="x", pady=5)
        for i in range(2): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📈", "Avg CLV", fmt_money(1210.69 * 4.5), "Estimated Lifetime", SUCCESS).grid(row=0, column=0, padx=5)
        KPICard(kf, "🛡️", "Retention", "83.2%", "Current Rate", ACCENT_BLUE).grid(row=0, column=1, padx=5)
        
        self._add_chart(ChartCard(right, "RFM Scatter: Recency vs Monetary", figsize=(6,3))).pack(fill="both", expand=True, pady=10)

class ChurnPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "🔄 Churn Risk Command Center", "Predictive churn analytics and risk mitigation").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        alert = ctk.CTkFrame(self, fg_color="#3e1a1a", corner_radius=10, border_width=1, border_color=DANGER)
        alert.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ctk.CTkLabel(alert, text="⚠️ HIGH RISK CUSTOMERS DETECTED — IMMEDIATE ACTION REQUIRED", font=FONT_SUBTITLE, text_color=DANGER).pack(pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): kf.columnconfigure(i, weight=1)
        
        models = [
            ("E-Com", M["ecom_churn_acc"]),
            ("Marketing", M["mkt_churn_acc"]),
            ("Bank", M["bank_churn_acc"]),
            ("Telco", M["telco_churn_acc"])
        ]
        for i, (name, acc) in enumerate(models):
            KPICard(kf, "🤖", f"{name} Accuracy", fmt_pct(acc), "Stacking Model", SUCCESS if acc > 90 else WARNING).grid(row=0, column=i, padx=5)

        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        charts.columnconfigure(0, weight=1)
        charts.columnconfigure(1, weight=1)
        
        gauge = GaugeWidget(charts, "Overall Churn Risk")
        gauge.grid(row=0, column=0, padx=5, sticky="nsew")
        gauge.set_value(M["churn_ecom"])
        
        self._add_chart(ChartCard(charts, "Revenue at Risk by Segment")).grid(row=0, column=1, padx=5, sticky="nsew")
