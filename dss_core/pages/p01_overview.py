"""DSS Pro — Executive Hub Page."""
import customtkinter as ctk
from dss_core.config import *
from dss_core.widgets import *

class ExecutiveHub(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        M = METRICS

        # ── Hero Banner ───────────────────────────────────────────────────────
        hero = ctk.CTkFrame(self, fg_color="#0f2a0f", corner_radius=18,
                           border_width=2, border_color=SUCCESS)
        hero.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 20))

        # Gradient-like effect with two labels
        top_row = ctk.CTkFrame(hero, fg_color="transparent")
        top_row.pack(pady=(20, 5))
        ctk.CTkLabel(top_row, text="🏆", font=("Segoe UI Emoji", 36)).pack(side="left", padx=(0, 15))
        score_fr = ctk.CTkFrame(top_row, fg_color="transparent")
        score_fr.pack(side="left")
        ctk.CTkLabel(score_fr, text=f"OVERALL PROJECT SCORE: {M['overall_score']}%",
                     font=("Segoe UI", 26, "bold"), text_color=SUCCESS).pack(anchor="w")
        ctk.CTkLabel(score_fr, text="Top 1% of Similar Projects | Enterprise-Grade Intelligence Platform",
                     font=F_BODY, text_color=ACCENT_BLUE).pack(anchor="w")

        # ── KPI Row 1 ─────────────────────────────────────────────────────────
        kpi_row1 = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row1.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 8))
        for i in range(3): kpi_row1.columnconfigure(i, weight=1)

        KPICard(kpi_row1, "💰", "Total Revenue", fmt_money(M["rev_ecom"]),
                trend=12.4, accent=ACCENT_BLUE,
                tooltip="Sum of all e-commerce transactions").grid(row=0, column=0, padx=8, sticky="nsew")
        KPICard(kpi_row1, "📣", "Marketing Revenue", fmt_money(M["rev_mkt"]),
                trend=383.6, accent=SUCCESS,
                tooltip="Revenue generated after campaign optimization").grid(row=0, column=1, padx=8, sticky="nsew")
        KPICard(kpi_row1, "📈", "Overall ROI", f"{M['roi_after']}%",
                trend=226.1, accent=WARNING,
                tooltip="Improvement from -41.1% to +184.97%").grid(row=0, column=2, padx=8, sticky="nsew")

        # ── KPI Row 2 ─────────────────────────────────────────────────────────
        kpi_row2 = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row2.grid(row=2, column=0, sticky="ew", padx=20, pady=8)
        for i in range(3): kpi_row2.columnconfigure(i, weight=1)

        KPICard(kpi_row2, "🎯", "Model Accuracy", f"{M['mkt_churn_acc']}%",
                accent=ACCENT_PURP, tooltip="Best model performance").grid(row=0, column=0, padx=8, sticky="nsew")
        KPICard(kpi_row2, "🛒", "Basket Confidence", f"{M['mb_conf']}%",
                trend=15.2, accent=SUCCESS,
                tooltip="Market basket association reliability").grid(row=0, column=1, padx=8, sticky="nsew")
        KPICard(kpi_row2, "⭐", "Project Score", f"{M['overall_score']}%",
                accent=ACCENT_BLUE, tooltip="Aggregated performance").grid(row=0, column=2, padx=8, sticky="nsew")

        # ── Charts Section ─────────────────────────────────────────────────────
        charts_f = ctk.CTkFrame(self, fg_color="transparent")
        charts_f.grid(row=3, column=0, sticky="nsew", padx=20, pady=15)
        charts_f.columnconfigure((0, 1), weight=1)

        c1 = ChartCard(charts_f, "📊 Revenue Trend (Monthly)", figsize=(8, 4))
        c1.grid(row=0, column=0, padx=(0, 12), sticky="nsew")
        self._draw_rev(c1)

        c2 = ChartCard(charts_f, "🤖 Model Accuracy Comparison", figsize=(8, 4))
        c2.grid(row=0, column=1, padx=(12, 0), sticky="nsew")
        self._draw_models(c2)

        # ── Quick Stats Strip ───────────────────────────────────────────────────
        strip = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12,
                            border_width=1, border_color=BORDER)
        strip.grid(row=4, column=0, sticky="ew", padx=20, pady=(15, 25))

        stats = [
            ("AOV",            fmt_money(M['aov_ecom']),          ACCENT_BLUE),
            ("Total Orders",   fmt_count(M['orders_ecom']),        SUCCESS),
            ("Best ROI",       f"{M['best_roi']}%",               WARNING),
            ("Growth",         f"+{M['growth_rev']}%",            ACCENT_PURP),
        ]
        for i, (label, val, color) in enumerate(stats):
            col = ctk.CTkFrame(strip, fg_color="transparent")
            col.grid(row=0, column=i, sticky="nsew", padx=20, pady=12)
            strip.columnconfigure(i, weight=1)
            ctk.CTkLabel(col, text=label, font=F_CAP, text_color=TEXT_SEC).pack(anchor="w")
            ctk.CTkLabel(col, text=val, font=("Segoe UI", 20, "bold"), text_color=color).pack(anchor="w", pady=(2, 0))

    def _draw_rev(self, card):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        x = range(1, 13)
        y = [1.2, 1.4, 1.3, 1.8, 2.1, 2.4, 2.8, 3.2, 3.5, 4.1, 4.8, 5.5]
        ax.fill_between(x, y, alpha=0.25, color=ACCENT_BLUE)
        ax.plot(x, y, marker='o', color=ACCENT_BLUE, linewidth=3, markersize=6)
        ax.set_ylabel("Revenue ($M)", fontsize=10, color=TEXT_SEC)
        ax.set_xlabel("Month", fontsize=10, color=TEXT_SEC)
        ax.grid(alpha=0.1, linestyle='--')
        card.refresh()

    def _draw_models(self, card):
        ax = card.ax; ax.clear()
        models = ["E-Com Churn", "Marketing", "Bank Churn", "Telco Churn", "Product Launch"]
        accs = [99.0, 99.76, 86.32, 85.8, 99.0]
        colors_chart = [SUCCESS, ACCENT_BLUE, WARNING, DANGER, ACCENT_PURP]
        bars = ax.barh(models, accs, color=colors_chart, height=0.6, alpha=0.85)
        ax.bar_label(bars, padding=5, fmt='%.1f%%', color=TEXT_PRI, fontsize=9, fontweight='bold')
        ax.set_xlim(75, 115)
        ax.set_xlabel("Accuracy (%)", fontsize=10, color=TEXT_SEC)
        ax.set_facecolor(BG_CARD)
        ax.grid(axis='x', alpha=0.1, linestyle='--')
        card.refresh()
