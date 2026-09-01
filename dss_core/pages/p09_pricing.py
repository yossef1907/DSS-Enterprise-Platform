"""Pages 9-11: Pricing Engine, Profit Forecasting, Campaign Planner."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk
from datetime import datetime
import os, csv

from dss_core.config import (
    BG_MAIN, BG_CARD, BG_CARD2, BORDER, BORDER2,
    ACCENT_BLUE, ACCENT_PURPLE, SUCCESS, WARNING, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    CHART_COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_CAPTION, FONT_LABEL,
    HISTORY_FILES,
)
from dss_core.widgets import (
    KPICard, ChartCard, DSSTable, ScrollablePage,
    fmt_money, fmt_pct, fmt_count, Toast,
)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9 – Smart Pricing Engine
# ─────────────────────────────────────────────────────────────────────────────
class PricingPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        eco = self.store.eco_df

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 8))
        ctk.CTkLabel(hdr, text="💰  Smart Pricing Engine", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Optimal price points, elasticity curves, and margin analysis", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # Input panel
        inp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        inp.columnconfigure((0,1,2,3,4), weight=1)

        cats = sorted(eco["product_category"].unique().tolist()) if not eco.empty and "product_category" in eco.columns else ["Electronics"]
        ctk.CTkLabel(inp, text="Category", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=0, padx=10, pady=(12,2), sticky="w")
        self._p_cat = ctk.CTkComboBox(inp, values=cats, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
        self._p_cat.grid(row=1, column=0, padx=10, pady=(0,12), sticky="ew")

        ctk.CTkLabel(inp, text="Current Price ($)", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=1, padx=10, pady=(12,2), sticky="w")
        self._p_price = ctk.CTkEntry(inp, placeholder_text="99.99", fg_color=BG_CARD2, border_color=BORDER2)
        self._p_price.grid(row=1, column=1, padx=10, pady=(0,12), sticky="ew")
        self._p_price.insert(0, "99.99")

        ctk.CTkLabel(inp, text="Target Margin %", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=2, padx=10, pady=(12,2), sticky="w")
        self._p_margin = ctk.CTkEntry(inp, placeholder_text="30", fg_color=BG_CARD2, border_color=BORDER2)
        self._p_margin.grid(row=1, column=2, padx=10, pady=(0,12), sticky="ew")
        self._p_margin.insert(0, "30")

        ctk.CTkButton(inp, text="⚡  Analyze Pricing", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_pricing).grid(row=1, column=3, padx=10, pady=(0,12), sticky="ew")

        # Results
        self._p_results = ctk.CTkFrame(self, fg_color="transparent")
        self._p_results.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._p_results.columnconfigure((0,1), weight=1)
        ctk.CTkLabel(self._p_results, text="Run analysis to see results", font=FONT_BODY,
                     text_color=TEXT_MUTED).grid(row=0, column=0, columnspan=2, pady=40)

    def _run_pricing(self):
        for w in self._p_results.winfo_children():
            w.destroy()
        self._p_results.columnconfigure((0,1), weight=1)

        cat   = self._p_cat.get()
        try: price = float(self._p_price.get())
        except: price = 99.99
        try: tgt_margin = float(self._p_margin.get())
        except: tgt_margin = 30.0

        eco = self.store.eco_df
        ml  = self.store.ml

        opt_price    = ml.optimal_prices.get(cat, price)
        elasticity   = ml.price_elasticity.get(cat, -0.5)
        cat_df       = eco[eco["product_category"] == cat] if not eco.empty and "product_category" in eco.columns else pd.DataFrame()
        cat_avg      = cat_df["unit_price"].mean() if not cat_df.empty and "unit_price" in cat_df.columns else price
        rec_min      = cat_avg * 0.9
        rec_max      = cat_avg * 1.15
        strategy     = "Premium" if price > cat_avg * 1.2 else ("Economy" if price < cat_avg * 0.8 else "Competitive")

        # KPI strip
        kf = ctk.CTkFrame(self._p_results, fg_color="transparent")
        kf.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)
        for i in range(4): kf.columnconfigure(i, weight=1)
        for i, (icon, title, val, acc) in enumerate([
            ("🎯", "Optimal Price",   fmt_money(opt_price),    SUCCESS),
            ("📊", "Market Average",  fmt_money(cat_avg),      ACCENT_BLUE),
            ("📉", "Elasticity",      f"{elasticity:.3f}",     WARNING),
            ("🏷️", "Strategy",        strategy,                ACCENT_PURPLE),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, ipady=6)

        # Elasticity curve
        el_card = self._add_chart(ChartCard(self._p_results, "📉  Price Elasticity Curve", figsize=(6, 3.8)))
        el_card.grid(row=1, column=0, sticky="nsew", padx=(0,4), pady=4)
        self._draw_elasticity(el_card, cat_df, price, opt_price)

        # Revenue curve
        rev_card = self._add_chart(ChartCard(self._p_results, "💰  Revenue vs Price", figsize=(6, 3.8)))
        rev_card.grid(row=1, column=1, sticky="nsew", padx=(4,0), pady=4)
        self._draw_revenue_curve(rev_card, cat_df, opt_price)

    def _draw_elasticity(self, card, cat_df, current, optimal):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not cat_df.empty and "unit_price" in cat_df.columns and "quantity" in cat_df.columns:
            g = cat_df.groupby("unit_price")["quantity"].mean().reset_index()
            ax.scatter(g["unit_price"], g["quantity"], color=ACCENT_PURPLE, s=20, alpha=0.6)
            ax.axvline(current, color=WARNING, linestyle="--", linewidth=1.5, label=f"Current ${current:.0f}")
            ax.axvline(optimal, color=SUCCESS, linestyle="--", linewidth=1.5, label=f"Optimal ${optimal:.0f}")
            ax.set_xlabel("Price ($)", color=TEXT_SECONDARY, fontsize=9)
            ax.set_ylabel("Avg Quantity", color=TEXT_SECONDARY, fontsize=9)
            ax.legend(fontsize=8, facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); card.refresh()

    def _draw_revenue_curve(self, card, cat_df, optimal):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not cat_df.empty and "unit_price" in cat_df.columns:
            g = cat_df.groupby("unit_price")["total_amount"].sum().reset_index()
            ax.plot(g["unit_price"], g["total_amount"], color=ACCENT_BLUE, linewidth=2.5)
            ax.axvline(optimal, color=SUCCESS, linestyle="--", linewidth=1.5, label=f"Optimal ${optimal:.0f}")
            ax.fill_between(g["unit_price"], g["total_amount"], alpha=0.15, color=ACCENT_BLUE)
            ax.set_xlabel("Price ($)", color=TEXT_SECONDARY, fontsize=9)
            ax.set_ylabel("Total Revenue", color=TEXT_SECONDARY, fontsize=9)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e3:.0f}K"))
            ax.legend(fontsize=8, facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); card.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 10 – Future Profit Forecasting
# ─────────────────────────────────────────────────────────────────────────────
class ForecastPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 8))
        ctk.CTkLabel(hdr, text="📈  Future Profit Forecasting", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Revenue projections, scenario analysis, and break-even timelines", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # Controls
        ctrl = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        ctrl.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        ctrl.columnconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(ctrl, text="Months", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=0, padx=12, pady=(12,2), sticky="w")
        self._f_months = ctk.CTkSlider(ctrl, from_=1, to=24, number_of_steps=23, button_color=ACCENT_BLUE, progress_color=ACCENT_PURPLE)
        self._f_months.set(12)
        self._f_months.grid(row=1, column=0, padx=12, pady=(0,12), sticky="ew")

        ctk.CTkLabel(ctrl, text="Growth Assumption %", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=1, padx=12, pady=(12,2), sticky="w")
        self._f_growth = ctk.CTkSlider(ctrl, from_=-20, to=50, number_of_steps=70, button_color=ACCENT_BLUE, progress_color=ACCENT_PURPLE)
        self._f_growth.set(5)
        self._f_growth.grid(row=1, column=1, padx=12, pady=(0,12), sticky="ew")

        ctk.CTkLabel(ctrl, text="Scenario", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=2, padx=12, pady=(12,2), sticky="w")
        self._f_scenario = ctk.CTkComboBox(ctrl, values=["Base","Optimistic","Pessimistic"],
                                            fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
        self._f_scenario.grid(row=1, column=2, padx=12, pady=(0,12), sticky="ew")

        ctk.CTkButton(ctrl, text="🔮  Generate Forecast", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_forecast).grid(row=1, column=3, padx=12, pady=(0,12), sticky="ew")

        self._f_results = ctk.CTkFrame(self, fg_color="transparent")
        self._f_results.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._f_results.columnconfigure(0, weight=1)

    def _run_forecast(self):
        for w in self._f_results.winfo_children():
            w.destroy()
        self._f_results.columnconfigure((0,1), weight=1)

        months    = int(self._f_months.get())
        growth    = self._f_growth.get() / 100
        scenario  = self._f_scenario.get()
        mult      = {"Base": 1.0, "Optimistic": 1.15, "Pessimistic": 0.85}.get(scenario, 1.0)
        kpi       = self.store.kpi
        ml        = self.store.ml
        mkpi      = self.store.powerbi.get("monthly_kpi", pd.DataFrame())

        hist_rev  = mkpi["total_revenue"].tolist() if not mkpi.empty and "total_revenue" in mkpi.columns else [kpi.total_revenue / 12] * 12
        base_val  = hist_rev[-1] if hist_rev else kpi.total_revenue / 12
        monthly_g = (hist_rev[-1] - hist_rev[0]) / max(hist_rev[0], 1) / max(len(hist_rev), 1) if len(hist_rev) > 1 else 0.01
        rate      = monthly_g + growth

        forecast  = [base_val * (1 + rate + growth) ** (i + 1) * mult for i in range(months)]
        upper     = [v * 1.15 for v in forecast]
        lower     = [v * 0.85 for v in forecast]

        next_m    = forecast[0]  if forecast else 0
        next_q    = sum(forecast[:3]) if len(forecast) >= 3 else sum(forecast)
        next_y    = sum(forecast[:12]) if len(forecast) >= 12 else sum(forecast)

        # KPI strip
        kf = ctk.CTkFrame(self._f_results, fg_color="transparent")
        kf.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)
        for i in range(4): kf.columnconfigure(i, weight=1)
        for i, (icon, title, val, acc) in enumerate([
            ("📅","Next Month",   fmt_money(next_m), ACCENT_BLUE),
            ("📊","Next Quarter", fmt_money(next_q), ACCENT_PURPLE),
            ("📈","Next Year",    fmt_money(next_y), SUCCESS),
            ("📉","Scenario",     scenario,          WARNING),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, ipady=6)

        # Forecast chart
        fc = self._add_chart(ChartCard(self._f_results, "🔮  Revenue Forecast", figsize=(12, 4)))
        fc.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=4)
        ax = fc.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        x_hist = range(len(hist_rev))
        ax.plot(x_hist, hist_rev, color=ACCENT_BLUE, linewidth=2.5, label="Historical")
        x_fore = range(len(hist_rev) - 1, len(hist_rev) + months)
        fore_plot = [hist_rev[-1]] + forecast
        up_plot   = [hist_rev[-1]] + upper
        lo_plot   = [hist_rev[-1]] + lower
        ax.plot(x_fore, fore_plot, color=SUCCESS, linewidth=2.5, linestyle="--", label=f"{scenario} Forecast")
        ax.fill_between(x_fore, lo_plot, up_plot, alpha=0.15, color=SUCCESS, label="Confidence Band")
        ax.axvline(len(hist_rev) - 1, color=BORDER2, linestyle=":", linewidth=1.5)
        ax.set_ylabel("Revenue ($)", color=TEXT_SECONDARY, fontsize=9)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))
        ax.legend(fontsize=9, facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); fc.refresh()

        # Month-by-month table
        tbl_frame = ctk.CTkFrame(self._f_results, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER)
        tbl_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(4, 20))
        ctk.CTkLabel(tbl_frame, text="📋  Monthly Projections", font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        tbl = DSSTable(tbl_frame, columns=["Month","Revenue","Upper","Lower","Growth%","Cumulative"])
        tbl.pack(fill="both", expand=True, padx=10, pady=(0,10))
        rows, cum = [], 0
        for i, (rev, up, lo) in enumerate(zip(forecast, upper, lower)):
            cum += rev
            grw = ((rev - base_val) / max(base_val, 1)) * 100
            rows.append((f"M+{i+1}", fmt_money(rev), fmt_money(up), fmt_money(lo), fmt_pct(grw, 1), fmt_money(cum)))
        tbl.load(rows)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 11 – Marketing Campaign Planner
# ─────────────────────────────────────────────────────────────────────────────
class PlannerPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 8))
        ctk.CTkLabel(hdr, text="📋  Marketing Campaign Planner", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Design campaigns, estimate reach, and optimize budget allocation", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # Two-column layout
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20, pady=4)
        main.columnconfigure((0,1), weight=1)

        # Left: inputs
        left = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,6), pady=2)
        left.columnconfigure(0, weight=1)
        self._build_planner_inputs(left)

        # Right: outputs
        self._plan_right = ctk.CTkScrollableFrame(main, fg_color="transparent")
        self._plan_right.grid(row=0, column=1, sticky="nsew", padx=(6,0), pady=2)
        self._plan_right.columnconfigure(0, weight=1)
        ctk.CTkLabel(self._plan_right, text="Plan a campaign to see projections",
                     font=FONT_BODY, text_color=TEXT_MUTED).pack(pady=60)

    def _build_planner_inputs(self, p):
        pad = {"padx": 16, "pady": 4}
        def lbl(t): ctk.CTkLabel(p, text=t, font=FONT_LABEL, text_color=TEXT_SECONDARY).pack(anchor="w", **pad)
        def sec(t):
            ctk.CTkLabel(p, text=t, font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=16, pady=(14,2))
            ctk.CTkFrame(p, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=2)

        sec("📋  Campaign Details")
        lbl("Campaign Name"); self._pl_name = ctk.CTkEntry(p, fg_color=BG_CARD2, border_color=BORDER2); self._pl_name.pack(fill="x", **pad)
        lbl("Budget ($)");    self._pl_budget = ctk.CTkEntry(p, fg_color=BG_CARD2, border_color=BORDER2); self._pl_budget.pack(fill="x", **pad); self._pl_budget.insert(0,"10000")
        lbl("Duration (weeks)"); self._pl_dur = ctk.CTkEntry(p, fg_color=BG_CARD2, border_color=BORDER2); self._pl_dur.pack(fill="x", **pad); self._pl_dur.insert(0,"4")

        sec("🎯  Targeting")
        segs = ["All","Champions","Loyal","At Risk","New","Regular"]
        lbl("Target Segment"); self._pl_seg = ctk.CTkComboBox(p, values=segs, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE); self._pl_seg.pack(fill="x", **pad)

        cats = ["All"] + (sorted(self.store.eco_df["product_category"].unique().tolist()) if not self.store.eco_df.empty and "product_category" in self.store.eco_df.columns else [])
        lbl("Product Category"); self._pl_cat = ctk.CTkComboBox(p, values=cats, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE); self._pl_cat.pack(fill="x", **pad)
        lbl("Discount Offer %"); self._pl_disc = ctk.CTkEntry(p, fg_color=BG_CARD2, border_color=BORDER2); self._pl_disc.pack(fill="x", **pad); self._pl_disc.insert(0,"15")

        ctk.CTkButton(p, text="📊  Generate Campaign Plan", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_plan).pack(fill="x", padx=16, pady=(16,16))

    def _run_plan(self):
        for w in self._plan_right.winfo_children(): w.destroy()
        self._plan_right.columnconfigure(0, weight=1)
        try:
            budget = float(self._pl_budget.get() or 10000)
            weeks  = float(self._pl_dur.get()    or 4)
            disc   = float(self._pl_disc.get()   or 15)
        except: budget, weeks, disc = 10000, 4, 15

        kpi = self.store.kpi
        mkt = self.store.mkt_df
        avg_conv = kpi.avg_conversion / 100 if kpi.avg_conversion else 0.03
        reach       = int(budget / 0.5)
        conversions = int(reach * avg_conv)
        revenue     = conversions * kpi.aov * (1 - disc / 100)
        roi         = (revenue - budget) / max(budget, 1) * 100

        kf = ctk.CTkFrame(self._plan_right, fg_color="transparent")
        kf.pack(fill="x", pady=4)
        for i in range(2): kf.columnconfigure(i, weight=1)
        for i, (icon, title, val, acc) in enumerate([
            ("👁️","Expected Reach",       fmt_count(reach),       ACCENT_BLUE),
            ("🎯","Expected Conversions", fmt_count(conversions), ACCENT_PURPLE),
            ("💰","Expected Revenue",     fmt_money(revenue),     SUCCESS),
            ("📈","Expected ROI",         fmt_pct(roi),           WARNING if roi >= 0 else DANGER),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=i//2, column=i%2, sticky="nsew", padx=4, pady=3, ipady=5)

        # Budget allocation chart
        alloc_card = self._add_chart(ChartCard(self._plan_right, "💰  Budget Allocation", figsize=(6, 3.5)))
        alloc_card.pack(fill="x", pady=4, padx=4)
        ax = alloc_card.ax; ax.clear()
        channels = ["Email","Social Media","Online Ads","Offline"]
        allocs   = [0.25, 0.35, 0.30, 0.10]
        ax.pie([a * budget for a in allocs], labels=channels, autopct="%1.0f%%",
               colors=CHART_COLORS, startangle=90,
               wedgeprops={"width": 0.55, "edgecolor": BG_CARD, "linewidth": 2})
        alloc_card.refresh()

        # Best channel recommendation
        rec_frame = ctk.CTkFrame(self._plan_right, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER)
        rec_frame.pack(fill="x", padx=4, pady=(4,20))
        ctk.CTkLabel(rec_frame, text="💡  Recommendations", font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        for txt in [
            f"🏆 Best channel: {kpi.best_channel} (based on historical ROI)",
            f"📣 Allocate 35% to Social Media for max reach at ${budget*0.35:,.0f}",
            f"🎯 Target {self._pl_seg.get()} segment for highest conversion rate",
            f"📅 Run for {weeks:.0f} weeks with {disc:.0f}% discount offer",
        ]:
            ctk.CTkLabel(rec_frame, text=txt, font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w").pack(anchor="w", padx=14, pady=3)
        ctk.CTkLabel(rec_frame, text="", height=8).pack()
