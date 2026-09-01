"""DSS Pro — AI Insights Pages (Market Basket, Marketing ROI, Product Launch)."""
import customtkinter as ctk
import pandas as pd
from dss_core.config import *
from dss_core.widgets import *

class BasketPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS

        # ── Header ─────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        ctk.CTkLabel(hdr, text="🛒 Market Basket Intelligence",
                     font=FONT_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(hdr, text="AI-powered product associations — Cross-sell & bundle opportunities",
                     font=F_BODY, text_color=TEXT_SEC).pack(anchor="w")

        # ── Performance Banner ─────────────────────────────────────────────────
        banner = ctk.CTkFrame(self, fg_color="#0a1a2e", corner_radius=12,
                             border_width=1, border_color=ACCENT_BLUE)
        banner.grid(row=1, column=0, sticky="ew", padx=20, pady=6)
        ctk.CTkLabel(banner, text=f"🏆 EXCEPTIONAL RESULTS — Confidence: {M['mb_conf']}% | Lift: {M['mb_lift']}x",
                     font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(pady=8)
        ctk.CTkLabel(banner, text="Industry Average: Confidence 40–60% | Lift 2–5x",
                     font=FONT_CAPTION, text_color=TEXT_SEC).pack(pady=(0, 8))

        # ── KPI Cards ───────────────────────────────────────────────────────────
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        for i in range(4): kf.columnconfigure(i, weight=1)

        KPICard(kf, "📜", "Total Rules",      M["mb_rules"],  accent=ACCENT_BLUE).grid(row=0, column=0, padx=6, sticky="nsew")
        KPICard(kf, "🎯", "Max Confidence",   f"{M['mb_conf']}%", accent=SUCCESS).grid(row=0, column=1, padx=6, sticky="nsew")
        KPICard(kf, "📈", "Max Lift",         f"{M['mb_lift']}x", accent=WARNING).grid(row=0, column=2, padx=6, sticky="nsew")
        KPICard(kf, "💎", "Max Support",      f"{M['mb_supp']}%", accent=ACCENT_PURP).grid(row=0, column=3, padx=6, sticky="nsew")

        # ── Association Rules Table ────────────────────────────────────────────
        table_f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                               border_width=1, border_color=BORDER)
        table_f.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(table_f, text="🔍 Top Association Rules — Revenue Opportunities",
                     font=FONT_SUBTITLE, text_color=TEXT_PRI).pack(pady=12)
        DSSTable(table_f, ["IF (Antecedent)", "THEN (Consequent)", "Support %",
                           "Confidence %", "Lift", "Opportunity $", "Score"]).pack(
            fill="both", expand=True, padx=15, pady=(0, 12))

class ROIPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS
        SectionHeader(self, "📣 Marketing ROI Intelligence", "Channel optimization and performance uplift").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        banner = ctk.CTkFrame(self, fg_color="#1a2e1a", corner_radius=10, border_width=1, border_color=SUCCESS)
        banner.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ctk.CTkLabel(banner, text=f"ROI IMPROVEMENT: {M['roi_before']}% → +{M['roi_after']}% | Revenue: +{M['revenue_growth_pct']}%", font=FONT_SUBTITLE, text_color=SUCCESS).pack(pady=10)

        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        for i in range(3): kf.columnconfigure(i, weight=1)
        KPICard(kf, "📈", "Overall ROI", fmt_pct(M["roi_after"]), f"vs {M['roi_before']}%", SUCCESS).grid(row=0, column=0, padx=5)
        KPICard(kf, "🥇", "Best Combo", fmt_pct(M["best_combo_roi"]), M["best_channel"], ACCENT_GOLD).grid(row=0, column=1, padx=5)
        KPICard(kf, "💰", "Revenue After", fmt_money(M["mkt_revenue_after"]), "Optimized", ACCENT_BLUE).grid(row=0, column=2, padx=5)

        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        charts.columnconfigure((0,1), weight=1)
        self._add_chart(ChartCard(charts, "ROI Before vs After")).grid(row=0, column=0, padx=5)
        self._add_chart(ChartCard(charts, "Top Channels ROI")).grid(row=0, column=1, padx=5)

class LaunchHubPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS

        # ── Header ─────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        ctk.CTkLabel(hdr, text="🚀 Product Launch Command Center",
                     font=FONT_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Predictive go/no-go analysis — 2,400 scenarios simulated",
                     font=F_BODY, text_color=TEXT_SEC).pack(anchor="w")

        # ── KPI Grid ────────────────────────────────────────────────────────────
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        for i in range(4): kf.columnconfigure(i, weight=1)

        KPICard(kf, "✅", "GO Decisions",    M["go_dec"],  accent=SUCCESS).grid(row=0, column=0, padx=6, sticky="nsew")
        KPICard(kf, "❌", "NO-GO Decisions", M["nogo_dec"], accent=DANGER).grid(row=0, column=1, padx=6, sticky="nsew")
        KPICard(kf, "🎯", "Best Success",   f"{M['best_success']}%", accent=ACCENT_BLUE).grid(row=0, column=2, padx=6, sticky="nsew")
        KPICard(kf, "🤖", "Model Accuracy", f"{M['launch_model_acc']}%", accent=WARNING).grid(row=0, column=3, padx=6, sticky="nsew")

        # ── Charts ──────────────────────────────────────────────────────────────
        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        charts.columnconfigure((0,1), weight=1)

        # GO vs NO-GO Distribution
        c1 = ChartCard(charts, "✅ GO vs ❌ NO-GO Distribution", figsize=(6,4))
        c1.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ax = c1.ax
        ax.pie([M['go_dec'], M['nogo_dec']], labels=["GO", "NO-GO"],
               colors=[SUCCESS, DANGER], autopct='%1.1f%%', startangle=90,
               wedgeprops={'width':0.55, 'edgecolor': BG_CARD, 'linewidth':2})
        ax.set_facecolor(BG_CARD)
        c1.refresh()

        # Success by Category
        c2 = ChartCard(charts, "🎯 Success Rate by Product Category", figsize=(7,4))
        c2.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ax2 = c2.ax
        categories = ["Electronics", "Home & Garden", "Clothing", "Appliances", "Sports"]
        success_rates = [98.2, 94.5, 89.1, 91.7, 95.3]
        colors_bar = [SUCCESS if s >= 95 else WARNING if s >= 90 else ACCENT_BLUE for s in success_rates]
        bars = ax2.barh(categories[::-1], success_rates[::-1], color=colors_bar[::-1], height=0.6, alpha=0.85)
        ax2.set_xlim(85, 100)
        ax2.set_xlabel("Success Probability (%)", fontsize=9)
        ax2.bar_label(bars, padding=3, fmt='%.1f%%', fontsize=8)
        ax2.set_facecolor(BG_CARD)
        ax2.grid(axis='x', alpha=0.1, linestyle='--')
        c2.refresh()
