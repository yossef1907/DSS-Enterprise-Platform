"""DSS Pro — Intelligence Pages (A/B Test, Inventory, Alerts, Competitor, Journey)."""
import customtkinter as ctk
import pandas as pd
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSCalc

class ABTestPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "⚖️ A/B Testing Simulator", "Compare strategies with statistical significance").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        main_f = ctk.CTkFrame(self, fg_color="transparent")
        main_f.grid(row=1, column=0, sticky="nsew", padx=20)
        main_f.columnconfigure((0,1), weight=1)
        
        for i, opt in enumerate(["Option A", "Option B"]):
            f = ctk.CTkFrame(main_f, fg_color=BG_CARD, corner_radius=15, border_width=2, border_color=ACCENT_BLUE if i==0 else WARNING)
            f.grid(row=0, column=i, sticky="nsew", padx=5)
            ctk.CTkLabel(f, text=opt, font=FONT_SUBTITLE).pack(pady=10)
            ctk.CTkEntry(f, placeholder_text="Price", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
            ctk.CTkEntry(f, placeholder_text="Discount", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")

        ctk.CTkButton(self, text="⚡ Run Significance Test", fg_color=ACCENT_PURPLE).grid(row=2, column=0, pady=20)
        
        res = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        res.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(res, text="🏆 Option B Wins! (+12.4% Lift | 99% Sig.)", font=FONT_SUBTITLE, text_color=SUCCESS).pack(pady=20)

class InventoryPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📦 Inventory & Demand Planning", "Stock level optimization and reorder analytics").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📦", "Reorder Point", "450 Units", "Threshold", WARNING).grid(row=0, column=0, padx=5)
        KPICard(kf, "🛡️", "Safety Stock", "120 Units", "Buffer", ACCENT_BLUE).grid(row=0, column=1, padx=5)
        KPICard(kf, "🔄", "EOQ", "850 Units", "Optimal Order", SUCCESS).grid(row=0, column=2, padx=5)
        KPICard(kf, "📅", "Supply Days", "18 Days", "Remaining", SUCCESS).grid(row=0, column=3, padx=5)

        self._add_chart(ChartCard(self, "Stock Level Projection", figsize=(10, 4))).grid(row=2, column=0, padx=20, pady=10)

class AlertsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "🚨 KPI Alert Center", "Automated business monitoring and risk detection").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Display alerts from store
        alerts_f = ctk.CTkFrame(self, fg_color="transparent")
        alerts_f.grid(row=1, column=0, sticky="nsew", padx=20)
        
        for a in self.store.alerts:
            AlertCard(alerts_f, a).pack(fill="x", pady=5)

class CompetitorPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "🗺️ Competitor Analysis", "Market positioning and price benchmarking").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(3): kf.columnconfigure(i, weight=1)
        KPICard(kf, "🎯", "Market Index", "104.2%", "vs Benchmark", ACCENT_BLUE).grid(row=0, column=0, padx=5)
        KPICard(kf, "📊", "Price Gap", "+$12.50", "Premium Position", WARNING).grid(row=0, column=1, padx=5)
        KPICard(kf, "📈", "Share", "12.4%", "Estimated", SUCCESS).grid(row=0, column=2, padx=5)

        self._add_chart(ChartCard(self, "Market Price Distribution", figsize=(10, 4))).grid(row=2, column=0, padx=20, pady=10)

class JourneyPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "🛤️ Customer Journey Analytics", "Lifecycle funnel and drop-off analysis").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self._add_chart(ChartCard(self, "Customer Lifecycle Funnel", figsize=(10, 4))).grid(row=1, column=0, padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): kf.columnconfigure(i, weight=1)
        KPICard(kf, "🚪", "Entry Conv.", "42.1%", "Awareness", ACCENT_BLUE).grid(row=0, column=0, padx=5)
        KPICard(kf, "🛒", "Purchase Conv.", "18.5%", "Interest", SUCCESS).grid(row=0, column=1, padx=5)
        KPICard(kf, "💎", "Loyalty Rate", "12.2%", "Retention", ACCENT_PURPLE).grid(row=0, column=2, padx=5)
        KPICard(kf, "📉", "Drop-off", "65.4%", "Awareness→Interest", DANGER).grid(row=0, column=3, padx=5)
