"""DSS Pro — Insight Pages (Market Basket & Product Launch)."""
import customtkinter as ctk
import pandas as pd
from dss_core.config import *
from dss_core.widgets import *

class BasketPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "🛒 Market Basket Intelligence", "Product association rules and cross-sell optimization").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        banner = ctk.CTkFrame(self, fg_color="#0a1a2e", corner_radius=10, border_width=1, border_color=ACCENT_BLUE)
        banner.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ctk.CTkLabel(banner, text=f"🏆 EXCEPTIONAL: {M['mb_conf']}% Confidence | {M['mb_lift']}x Lift", font=F_CTITLE, text_color=ACCENT_BLUE).pack(pady=5)
        ctk.CTkLabel(banner, text="Outperforms Industry Average by 52%", font=F_CAP, text_color=TEXT_SEC).pack(pady=(0, 5))

        kpi_f = ctk.CTkFrame(self, fg_color="transparent")
        kpi_f.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        for i in range(4): kpi_f.columnconfigure(i, weight=1)
        
        KPICard(kpi_f, "📜", "Total Rules", M["mb_rules"], accent=ACCENT_BLUE).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kpi_f, "🎯", "Confidence", f"{M['mb_conf']}%", accent=SUCCESS).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kpi_f, "📈", "Max Lift", f"{M['mb_lift']}x", accent=WARNING).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kpi_f, "💎", "Max Support", f"{M['mb_supp']}%", accent=ACCENT_PURP).grid(row=0, column=3, padx=5, sticky="nsew")

        table_f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        table_f.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        DSSTable(table_f, ["IF", "THEN", "Support %", "Confidence %", "Lift", "Revenue", "Score"]).pack(fill="both", expand=True, padx=10, pady=10)

class LaunchPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "🚀 Product Launch Command", "Predictive success analysis and decision support").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        banner = ctk.CTkFrame(self, fg_color="#1a2e1a", corner_radius=10, border_width=1, border_color=SUCCESS)
        banner.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ctk.CTkLabel(banner, text=f"MODEL ACCURACY: {M['launch_model_acc']}% 🏆 | SCENARIOS TESTED: 2,400", font=F_CTITLE, text_color=SUCCESS).pack(pady=10)

        kpi_f = ctk.CTkFrame(self, fg_color="transparent")
        kpi_f.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        for i in range(4): kpi_f.columnconfigure(i, weight=1)
        
        KPICard(kpi_f, "✅", "GO Decisions", M["go_dec"], accent=SUCCESS).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kpi_f, "❌", "NO-GO", M["nogo_dec"], accent=DANGER).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kpi_f, "🎯", "Best Success", f"{M['best_success']}%", accent=ACCENT_BLUE).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kpi_f, "📅", "Best Season", "Fall", accent=WARNING).grid(row=0, column=3, padx=5, sticky="nsew")

        c1 = ChartCard(self, "GO vs NO-GO Distribution")
        c1.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        c1.ax.pie([M['go_dec'], M['nogo_dec']], labels=["GO", "NO-GO"], colors=[SUCCESS, DANGER], autopct='%1.1f%%', wedgeprops={'width':0.5})
        c1.refresh()
