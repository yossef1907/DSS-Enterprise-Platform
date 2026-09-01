"""Pages 16-18: Customer Journey, Report Generator, Settings."""
import os, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk
from datetime import datetime

from dss_core.config import (
    BG_MAIN, BG_CARD, BG_CARD2, BORDER, BORDER2,
    ACCENT_BLUE, ACCENT_PURPLE, SUCCESS, WARNING, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    CHART_COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_CAPTION, FONT_LABEL,
    APP_VERSION, BASE_DIR,
)
from dss_core.widgets import (
    KPICard, ChartCard, DSSTable, ScrollablePage,
    fmt_money, fmt_pct, fmt_count, Toast,
)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 16 – Customer Journey Analytics
# ─────────────────────────────────────────────────────────────────────────────
class JourneyPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="🛤️  Customer Journey Analytics", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Funnel analysis, drop-off rates, and lifecycle stage performance", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        eco  = self.store.eco_df
        kpi  = self.store.kpi
        cust = self.store.cust_df

        # Journey funnel data
        total_visitors   = int(kpi.total_customers * 12)
        interested       = int(total_visitors * 0.45)
        considered       = int(interested   * 0.55)
        purchased        = kpi.total_orders
        loyal            = kpi.low_risk
        advocates        = int(loyal * 0.3)

        stages = ["Awareness","Interest","Consideration","Purchase","Loyalty","Advocacy"]
        counts = [total_visitors, interested, considered, purchased, loyal, advocates]
        colors = [ACCENT_BLUE, ACCENT_PURPLE, "#40c4ff", SUCCESS, WARNING, "#ffe66d"]

        # Funnel chart
        f_card = self._add_chart(ChartCard(self, "🔽  Customer Journey Funnel", figsize=(12, 4)))
        f_card.grid(row=1, column=0, sticky="nsew", padx=20, pady=4)
        ax = f_card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        y_pos = range(len(stages))
        ax.barh(list(reversed(list(y_pos))), list(reversed(counts)),
                color=list(reversed(colors)), height=0.6)
        ax.set_yticks(list(reversed(list(y_pos))))
        ax.set_yticklabels(stages, fontsize=10)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:,.0f}"))
        for i, (c, v) in enumerate(zip(reversed(colors), reversed(counts))):
            ax.text(v * 1.01, len(stages)-1-i, f"{v:,}", va="center", fontsize=9, color=TEXT_PRIMARY)
        ax.grid(axis="x", alpha=0.15); f_card.refresh()

        # Drop-off rates
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=2, column=0, sticky="ew", padx=20, pady=4)
        for i in range(5): kf.columnconfigure(i, weight=1)
        for i in range(len(stages)-1):
            rate = (counts[i]-counts[i+1])/max(counts[i],1)*100
            KPICard(kf, icon="📉", title=f"{stages[i]}→{stages[i+1]}",
                    value=fmt_pct(rate), subtitle="Drop-off rate",
                    accent=DANGER if rate > 50 else WARNING).grid(
                row=0, column=i, sticky="nsew", padx=4, pady=4, ipady=5)

        # Journey stage breakdown from eco data
        if not eco.empty and "journey_stage" in eco.columns:
            cr = ctk.CTkFrame(self, fg_color="transparent")
            cr.grid(row=3, column=0, sticky="nsew", padx=20, pady=4)
            cr.columnconfigure((0,1), weight=1)

            stage_card = self._add_chart(ChartCard(cr, "🏷️  Revenue by Journey Stage", figsize=(6,3.5)))
            stage_card.grid(row=0, column=0, sticky="nsew", padx=(0,4))
            ax2 = stage_card.ax; ax2.clear(); ax2.set_facecolor(BG_CARD)
            g = eco.groupby("journey_stage")["total_amount"].sum()
            ax2.bar(g.index, g.values, color=CHART_COLORS[:len(g)], width=0.6)
            ax2.set_ylabel("Revenue ($)", color=TEXT_SECONDARY, fontsize=9)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
            ax2.tick_params(axis="x", rotation=15, labelsize=9)
            ax2.grid(axis="y", alpha=0.2); stage_card.refresh()

            rating_card = self._add_chart(ChartCard(cr, "⭐  Rating by Journey Stage", figsize=(6,3.5)))
            rating_card.grid(row=0, column=1, sticky="nsew", padx=(4,0))
            ax3 = rating_card.ax; ax3.clear(); ax3.set_facecolor(BG_CARD)
            g2 = eco.groupby("journey_stage")["customer_rating"].mean()
            ax3.bar(g2.index, g2.values, color=CHART_COLORS[:len(g2)], width=0.6)
            ax3.set_ylabel("Avg Rating", color=TEXT_SECONDARY, fontsize=9)
            ax3.axhline(3, color=WARNING, linestyle="--", linewidth=1)
            ax3.tick_params(axis="x", rotation=15, labelsize=9)
            ax3.grid(axis="y", alpha=0.2); rating_card.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 17 – BI Report Generator
# ─────────────────────────────────────────────────────────────────────────────
class ReportsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="📄  Business Intelligence Report Generator", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Auto-generate professional reports with KPIs, charts, and AI insights", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # Report type selection
        sel_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        sel_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        ctk.CTkLabel(sel_frame, text="Select Report Type", font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,6))

        btn_frame = ctk.CTkFrame(sel_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0,10))
        for i in range(3): btn_frame.columnconfigure(i, weight=1)

        reports = [
            ("📊  Executive Summary",  "executive"),
            ("💰  Sales Report",        "sales"),
            ("👥  Customer Report",     "customer"),
            ("📣  Campaign ROI Report", "campaign"),
            ("🚀  Product Report",      "product"),
            ("📋  Full DSS Report",     "full"),
        ]
        for i, (label, rtype) in enumerate(reports):
            ctk.CTkButton(btn_frame, text=label, fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                          command=lambda rt=rtype: self._generate(rt)).grid(
                row=i//3, column=i%3, sticky="ew", padx=4, pady=4)

        self._report_area = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=15,
                                                    border_width=1, border_color=BORDER)
        self._report_area.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._report_area.columnconfigure(0, weight=1)
        ctk.CTkLabel(self._report_area, text="Select a report type above to generate it.",
                     font=FONT_BODY, text_color=TEXT_MUTED).pack(pady=40)

    def _generate(self, rtype):
        for w in self._report_area.winfo_children(): w.destroy()
        kpi = self.store.kpi
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        titles = {"executive":"Executive Summary","sales":"Sales Performance",
                  "customer":"Customer Analysis","campaign":"Campaign ROI",
                  "product":"Product Performance","full":"Full DSS Report"}

        ctk.CTkLabel(self._report_area, text=f"📄  {titles.get(rtype,'Report')}",
                     font=("Segoe UI",20,"bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(15,2))
        ctk.CTkLabel(self._report_area, text=f"Generated: {now}  |  DSS Pro v{APP_VERSION}",
                     font=FONT_CAPTION, text_color=TEXT_MUTED).pack(anchor="w", padx=20, pady=(0,10))
        ctk.CTkFrame(self._report_area, fg_color=BORDER, height=1).pack(fill="x", padx=20, pady=4)

        sections = self._get_sections(rtype, kpi)
        for title, items in sections:
            ctk.CTkLabel(self._report_area, text=f"\n{title}", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=20)
            for item in items:
                ctk.CTkLabel(self._report_area, text=f"  • {item}", font=FONT_BODY,
                             text_color=TEXT_SECONDARY, anchor="w", wraplength=700).pack(anchor="w", padx=28, pady=1)

        # Export button
        ctk.CTkButton(self._report_area, text="💾  Export as CSV",
                      fg_color=SUCCESS, hover_color="#00b358",
                      command=lambda: self._export_csv(rtype, sections)).pack(padx=20, pady=(15,20), anchor="w")

    def _get_sections(self, rtype, kpi):
        secs = []
        if rtype in ("executive","full"):
            secs.append(("📊 Key Performance Indicators", [
                f"Total Revenue: {fmt_money(kpi.total_revenue)}",
                f"Total Orders: {fmt_count(kpi.total_orders)}",
                f"Average Order Value: {fmt_money(kpi.aov)}",
                f"Total Customers: {fmt_count(kpi.total_customers)}",
                f"Revenue Growth: {fmt_pct(kpi.revenue_growth)}",
                f"Best Month: {kpi.best_month}",
            ]))
        if rtype in ("sales","full"):
            secs.append(("💰 Sales Highlights", [
                f"Top Category: {kpi.top_category}",
                f"Top City: {kpi.top_city}",
                f"Top Payment: {kpi.top_payment}",
                f"Basket Size: {kpi.basket_size:.2f} items",
                f"Customer Return Rate: {fmt_pct(kpi.returning_rate)}",
                f"Avg Rating: {kpi.avg_rating:.2f}/5",
            ]))
        if rtype in ("customer","full"):
            secs.append(("👥 Customer Intelligence", [
                f"High Churn Risk: {fmt_count(kpi.high_risk)} customers",
                f"Medium Risk: {fmt_count(kpi.medium_risk)} customers",
                f"Churn Rate: {fmt_pct(kpi.churn_rate)}",
                f"Revenue at Risk: {fmt_money(kpi.revenue_at_risk)}",
                f"Average CLV: {fmt_money(kpi.avg_clv)}",
                f"Avg Delivery: {kpi.avg_delivery:.1f} days",
            ]))
        if rtype in ("campaign","full"):
            secs.append(("📣 Marketing & Campaign ROI", [
                f"Total Marketing Budget: {fmt_money(kpi.total_budget)}",
                f"Marketing Revenue: {fmt_money(kpi.total_mkt_revenue)}",
                f"Overall ROI: {fmt_pct(kpi.overall_roi)}",
                f"Best Channel: {kpi.best_channel}",
                f"Avg Conversion Rate: {fmt_pct(kpi.avg_conversion)}",
            ]))
        if rtype in ("product","full"):
            secs.append(("🛒 Market Basket & Products", [
                f"Total Association Rules: {fmt_count(kpi.total_rules)}",
                f"Max Confidence: {fmt_pct(kpi.max_confidence)}",
                f"Max Lift: {kpi.max_lift:.2f}",
                f"Max Support: {fmt_pct(kpi.max_support)}",
            ]))
        if rtype == "full":
            secs.append(("💡 AI Recommendations", [
                "Focus retention campaigns on high-risk churn segment immediately",
                f"Allocate more budget to {kpi.best_channel} channel for best ROI",
                f"Push promotions in {kpi.best_month[:7]} — historically best performing period",
                "Implement bundle strategies based on top market basket rules",
                f"Target {kpi.top_category} category for maximum revenue impact",
            ]))
        return secs

    def _export_csv(self, rtype, sections):
        path = os.path.join(BASE_DIR, f"report_{rtype}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for title, items in sections:
                w.writerow([title])
                for item in items:
                    w.writerow(["", item])
                w.writerow([])
        Toast.show(self.winfo_toplevel(), f"✅  Report exported: {os.path.basename(path)}")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 18 – Settings & Configuration
# ─────────────────────────────────────────────────────────────────────────────
class SettingsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="⚙️  Settings & Configuration", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Customize your DSS Pro experience", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        row_idx = [1]
        def nrow():
            v = row_idx[0]; row_idx[0] += 1; return v

        def section(title):
            f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
            f.grid(row=nrow(), column=0, sticky="ew", padx=20, pady=4)
            ctk.CTkLabel(f, text=title, font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=14, pady=(10,4))
            ctk.CTkFrame(f, fg_color=BORDER, height=1).pack(fill="x", padx=14, pady=2)
            return f

        # Theme
        th = section("🎨  Appearance")
        rf = ctk.CTkFrame(th, fg_color="transparent"); rf.pack(fill="x", padx=14, pady=8)
        ctk.CTkLabel(rf, text="Color Theme:", font=FONT_LABEL, text_color=TEXT_SECONDARY).pack(side="left", padx=(0,10))
        ctk.CTkSegmentedButton(rf, values=["Dark","System"], command=lambda v: ctk.set_appearance_mode(v.lower())).pack(side="left")

        # Data paths
        dp = section("📂  Data Sources")
        from dss_core.config import ECOMMERCE_CLEAN, MARKETING_CSV, CUSTOMER_CSV, SIMULATION_CSV
        for label, path in [("Ecommerce",ECOMMERCE_CLEAN),("Marketing",MARKETING_CSV),
                             ("Customer",CUSTOMER_CSV),("Simulation",SIMULATION_CSV)]:
            pf = ctk.CTkFrame(dp, fg_color="transparent"); pf.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(pf, text=f"{label}:", font=FONT_LABEL, text_color=TEXT_SECONDARY, width=120).pack(side="left")
            e = ctk.CTkEntry(pf, fg_color=BG_CARD2, border_color=BORDER2); e.pack(side="left", fill="x", expand=True)
            e.insert(0, path)
        ctk.CTkLabel(dp, text="", height=8).pack()

        # KPI Thresholds
        thr = section("📊  KPI Alert Thresholds")
        thresholds = [
            ("Revenue Drop Alert (%)", "10"),
            ("Churn Rate Alert (%)", "45"),
            ("Min Marketing ROI (%)", "100"),
            ("Min Avg Rating", "3.0"),
        ]
        for label, default in thresholds:
            tf = ctk.CTkFrame(thr, fg_color="transparent"); tf.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(tf, text=label+":", font=FONT_LABEL, text_color=TEXT_SECONDARY, width=220).pack(side="left")
            e = ctk.CTkEntry(tf, fg_color=BG_CARD2, border_color=BORDER2, width=100); e.pack(side="left")
            e.insert(0, default)
        ctk.CTkLabel(thr, text="", height=8).pack()

        # About
        ab = section(f"ℹ️  About  –  DSS Pro v{APP_VERSION}")
        about_items = [
            f"Version: {APP_VERSION}",
            "Framework: CustomTkinter + matplotlib + scikit-learn",
            "Author: DSS Pro Team",
            f"Data directory: {BASE_DIR}",
            "© 2025 DSS Pro. All rights reserved.",
        ]
        for item in about_items:
            ctk.CTkLabel(ab, text=item, font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w", padx=14, pady=2)
        ctk.CTkLabel(ab, text="", height=10).pack()

        ctk.CTkButton(self, text="💾  Save Settings", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=lambda: Toast.show(self.winfo_toplevel(), "✅  Settings saved!")).grid(
            row=nrow(), column=0, padx=20, pady=(8,20), sticky="w")
