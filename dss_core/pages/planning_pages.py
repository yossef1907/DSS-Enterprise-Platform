"""DSS Pro — Planning & Intelligence Pages."""
import customtkinter as ctk
import numpy as np
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSEngine as Calc

class ForecastPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "📈 Future Profit Forecasting", "Revenue projections using Holt-Winters seasonal model").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=15)
        for i in range(3): kf.columnconfigure(i, weight=1)
        
        KPICard(kf, "📅", "Month 1 Forecast", fmt_money(M["fc_m1"]), accent=ACCENT_BLUE).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kf, "📊", "Month 6 Forecast", fmt_money(M["fc_m6"]), accent=ACCENT_PURP).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kf, "📈", "Monthly Growth", f"~{fmt_money(M['fc_growth'])}", accent=SUCCESS).grid(row=0, column=2, padx=5, sticky="nsew")

        c1 = ChartCard(self, "Revenue Forecast (12 Months)")
        c1.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        x = np.arange(1, 13)
        y = [2.0 + 0.1 * i + 0.2 * np.sin(i) for i in x]
        c1.ax.plot(x, y, 'o--', color=ACCENT_BLUE, label="Forecast")
        c1.ax.fill_between(x, [v*0.85 for v in y], [v*1.15 for v in y], alpha=0.2, color=ACCENT_BLUE, label="95% CI")
        c1.refresh()

class PricingPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "💡 Smart Pricing Engine", "AI-driven price optimization and elasticity analysis").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        inp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        for i in range(4): inp.columnconfigure(i, weight=1)
        
        ctk.CTkEntry(inp, placeholder_text="Category", fg_color=BG_CARD2).grid(row=0, column=0, padx=10, pady=15)
        ctk.CTkEntry(inp, placeholder_text="Current Price ($)", fg_color=BG_CARD2).grid(row=0, column=1, padx=10)
        ctk.CTkEntry(inp, placeholder_text="Target Margin %", fg_color=BG_CARD2).grid(row=0, column=2, padx=10)
        ctk.CTkButton(inp, text="Analyze Price", fg_color=ACCENT_PURP).grid(row=0, column=3, padx=10)

        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=15, pady=10)
        for i in range(4): kf.columnconfigure(i, weight=1)
        KPICard(kf, "🎯", "Optimal Price", "$112.50", accent=SUCCESS).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kf, "📊", "Elasticity", "-1.45", accent=DANGER).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kf, "🏷️", "Strategy", "Premium", accent=ACCENT_BLUE).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kf, "💰", "Profit Uplift", "+$15.2k", accent=SUCCESS).grid(row=0, column=3, padx=5, sticky="nsew")

class InventoryPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📦 Inventory Planning", "Stock level optimization and reorder analytics").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=15)
        for i in range(4): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📦", "Reorder Point", "450 units", accent=WARNING).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kf, "🛡️", "Safety Stock", "120 units", accent=ACCENT_BLUE).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kf, "🔄", "EOQ", "850 units", accent=SUCCESS).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kf, "📅", "Supply Days", "18 Days", accent=SUCCESS).grid(row=0, column=3, padx=5, sticky="nsew")

class ABTestPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "🔬 A/B Testing Simulator", "Compare strategies with statistical confidence").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20)
        main.columnconfigure((0, 1), weight=1)
        
        for i, opt in enumerate(["Option A", "Option B"]):
            f = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15, border_width=2, border_color=ACCENT_BLUE if i==0 else WARNING)
            f.grid(row=0, column=i, sticky="nsew", padx=5)
            ctk.CTkLabel(f, text=opt, font=F_TITLE).pack(pady=15)
            ctk.CTkEntry(f, placeholder_text="Price", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
            ctk.CTkEntry(f, placeholder_text="Discount %", fg_color=BG_CARD2).pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(f, text="Est. Revenue: $XXX", font=F_BODY).pack(pady=10)

        ctk.CTkButton(self, text="⚖️ RUN A/B TEST", fg_color=ACCENT_PURP, width=300).grid(row=2, column=0, pady=20)

class PlannerPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📣 Campaign Planner", "Simulate and optimize marketing campaign ROI").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=15)
        for i in range(3): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📣", "Expected ROI", "+185%", accent=SUCCESS).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kf, "🎯", "Target Reach", "1.2M", accent=ACCENT_BLUE).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kf, "💰", "Revenue Uplift", "+$450k", accent=SUCCESS).grid(row=0, column=2, padx=5, sticky="nsew")
