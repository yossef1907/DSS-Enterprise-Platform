"""DSS Pro — Product Analyzer Page v3.0 — Success/Failure Analysis & Best Scenarios."""
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from dss_core.config import (
    BG_MAIN, BG_CARD, BG_CARD2, BORDER, ACCENT_BLUE, ACCENT_PURP,
    SUCCESS, WARNING, DANGER, TEXT_PRI, TEXT_SEC, TEXT_MUTED,
    F_TITLE, F_CTITLE, F_BODY, F_CAP, CHART_COLORS
)
from dss_core.widgets import KPICard, ChartCard, DSSTable, ScrollablePage, fmt_money, fmt_pct, Toast
from dss_core.calculations import DSSCalc


class ProductAnalyzerPage(ScrollablePage):
    """Smart product analysis with success/failure rates, processing times, and top scenarios."""

    def __init__(self, master, store, **kwargs):
        super().__init__(master, store, **kwargs)
        self.columnconfigure(0, weight=1)
        self.scenario_results = []

    def build(self):
        # ── Header ────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        ctk.CTkLabel(hdr, text="🚀 Smart Product Analyzer",
                     font=FONT_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Enter product details to analyze success probability, "
                               "failure rates, and optimal launch scenarios",
                     font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")

        # ── Main: 2-column layout ─────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main.columnconfigure(0, weight=1)   # Inputs
        main.columnconfigure(1, weight=2)   # Results

        # ── LEFT PANEL: Inputs ─────────────────────────────────────────────────
        input_panel = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15,
                                   border_width=2, border_color=ACCENT_BLUE)
        input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._build_inputs(input_panel)

        # ── RIGHT PANEL: Results ────────────────────────────────────────────────
        self.results_panel = ctk.CTkFrame(main, fg_color="transparent")
        self.results_panel.grid(row=0, column=1, sticky="nsew")
        self.results_panel.columnconfigure(0, weight=1)
        self._show_welcome()

    def _build_inputs(self, parent):
        """Build input form with product details."""
        ctk.CTkLabel(parent, text="📦 Product Details",
                     font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(pady=(15, 10))

        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", padx=15, pady=5)

        # Product Name
        ctk.CTkLabel(form, text="Product Name:", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.pname_ent = ctk.CTkEntry(form, placeholder_text="e.g. Smart Watch X1", fg_color=BG_CARD2)
        self.pname_ent.pack(fill="x", pady=(0, 10))

        # Category
        ctk.CTkLabel(form, text="Category:", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.cat_combo = ctk.CTkComboBox(form,
                                          values=["Electronics", "Home & Garden", "Clothing",
                                                  "Home Appliances", "Sports", "Beauty"],
                                          fg_color=BG_CARD2)
        self.cat_combo.set("Electronics")
        self.cat_combo.pack(fill="x", pady=(0, 10))

        # Unit Price
        ctk.CTkLabel(form, text="Unit Price ($):", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.price_ent = ctk.CTkEntry(form, placeholder_text="199.99", fg_color=BG_CARD2)
        self.price_ent.insert(0, "199.99")
        self.price_ent.pack(fill="x", pady=(0, 10))

        # Discount Slider
        ctk.CTkLabel(form, text="Discount (%):", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.disc_slider = ctk.CTkSlider(form, from_=0, to=70, number_of_steps=70,
                                          command=self._update_discount_label)
        self.disc_slider.set(15)
        self.disc_slider.pack(fill="x", pady=(0, 5))
        self.disc_lbl = ctk.CTkLabel(form, text="Discount: 15%", font=FONT_CAPTION, text_color=TEXT_SEC)
        self.disc_lbl.pack(anchor="w", pady=(0, 10))

        # Marketing Budget
        ctk.CTkLabel(form, text="Marketing Budget ($):", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.budget_ent = ctk.CTkEntry(form, placeholder_text="10000", fg_color=BG_CARD2)
        self.budget_ent.insert(0, "10000")
        self.budget_ent.pack(fill="x", pady=(0, 10))

        # Expected Quantity
        ctk.CTkLabel(form, text="Expected Quantity:", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.qty_ent = ctk.CTkEntry(form, placeholder_text="5000", fg_color=BG_CARD2)
        self.qty_ent.insert(0, "5000")
        self.qty_ent.pack(fill="x", pady=(0, 10))

        # Season
        ctk.CTkLabel(form, text="Target Season:", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.season_combo = ctk.CTkComboBox(form,
                                             values=["Winter", "Spring", "Summer", "Fall"],
                                             fg_color=BG_CARD2)
        self.season_combo.set("Fall")
        self.season_combo.pack(fill="x", pady=(0, 10))

        # Region
        ctk.CTkLabel(form, text="Target Region:", font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")
        self.region_combo = ctk.CTkComboBox(form,
                                             values=["Amman", "Kuwait", "Dubai", "Riyadh", "Jeddah", "Doha"],
                                             fg_color=BG_CARD2)
        self.region_combo.set("Amman")
        self.region_combo.pack(fill="x", pady=(0, 15))

        # Action Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        ctk.CTkButton(btn_frame, text="🔍 Analyze Single",
                       fg_color=ACCENT_BLUE, hover_color="#0099cc",
                       command=self._analyze_single).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_frame, text="⚡ Run All Scenarios",
                       fg_color=SUCCESS, hover_color="#00b359",
                       command=self._run_all_scenarios).pack(side="left", expand=True, padx=5)

    def _update_discount_label(self, _=None):
        val = int(self.disc_slider.get())
        self.disc_lbl.configure(text=f"Discount: {val}%")

    def _show_welcome(self):
        """Display initial welcome screen."""
        for w in self.results_panel.winfo_children():
            w.destroy()
        welcome = ctk.CTkFrame(self.results_panel, fg_color=BG_CARD, corner_radius=15,
                              border_width=1, border_color=BORDER)
        welcome.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(welcome, text="👋 Welcome to Product Analyzer",
                     font=F_TITLE, text_color=TEXT_PRI).pack(pady=(40, 10))
        ctk.CTkLabel(welcome, text="Configure your product details and click Analyze to see:",
                     font=FONT_BODY, text_color=TEXT_SEC).pack(pady=5)
        tips = [
            "• Success probability based on historical data",
            "• Failure rate analysis across market segments",
            "• Processing time for each scenario",
            "• Top 5 recommended scenarios with expected ROI"
        ]
        for tip in tips:
            ctk.CTkLabel(welcome, text=tip, font=FONT_BODY, text_color=TEXT_MUTED).pack(pady=3)
        ctk.CTkLabel(welcome, text="", height=20).pack()

    # ─────────────────────────────────────────────────────────────────────────────
    # ANALYSIS LOGIC
    # ─────────────────────────────────────────────────────────────────────────────
    def _analyze_single(self):
        """Analyze current configuration."""
        try:
            price = float(self.price_ent.get())
            discount = self.disc_slider.get()
            budget = float(self.budget_ent.get())
            qty = int(self.qty_ent.get())
        except ValueError:
            Toast.show(self.winfo_toplevel(), "❌ Invalid numeric inputs", color=DANGER)
            return

        scenario = {
            "scenario": "Current Config",
            "season": self.season_combo.get(),
            "region": self.region_combo.get(),
            "price": price,
            "discount": discount,
            "budget": budget,
            "quantity": qty,
        }
        self._generate_results([scenario])

    def _run_all_scenarios(self):
        """Run analysis across all combinations (2400 scenarios max)."""
        try:
            price = float(self.price_ent.get())
            budget = float(self.budget_ent.get())
            qty = int(self.qty_ent.get())
        except ValueError:
            Toast.show(self.winfo_toplevel(), "❌ Invalid numeric inputs", color=DANGER)
            return

        seasons = ["Winter", "Spring", "Summer", "Fall"]
        regions = ["Amman", "Kuwait", "Dubai", "Riyadh", "Jeddah", "Doha"]
        discounts = [0, 10, 20, 30, 40, 50]

        scenarios = []
        for season in seasons:
            for region in regions:
                for disc in discounts:
                    scenarios.append({
                        "scenario": f"{season[:3]}-{region[:3]}-{disc}%",
                        "season": season,
                        "region": region,
                        "price": round(price * (1 - disc/200), 2),
                        "discount": disc,
                        "budget": budget,
                        "quantity": qty,
                    })

        Toast.show(self.winfo_toplevel(), f"⚡ Running {len(scenarios)} scenarios...", color=ACCENT_BLUE)
        self._generate_results(scenarios[:2400])

    def _generate_results(self, scenarios):
        """
        Calculate metrics for each scenario:
        - success_prob: based on historical patterns
        - failure_prob: 100 - success_prob
        - processing_time: simulated compute time
        - expected_revenue & ROI
        """
        results = []
        for sc in scenarios:
            effective_price = sc["price"] * (1 - sc["discount"]/100)
            revenue = effective_price * sc["quantity"]
            cost = sc["budget"]
            profit = revenue - cost
            roi = DSSCalc.roi(revenue, cost)

            # Base probability from historical success patterns
            base_prob = 50

            # Season multiplier (from project data: Fall = best)
            season_mult = {"Fall": 1.25, "Spring": 1.08, "Summer": 1.0, "Winter": 0.92}
            base_prob *= season_mult.get(sc["season"], 1.0)

            # Region multiplier (Amman = best)
            region_mult = {"Amman": 1.18, "Dubai": 1.10, "Kuwait": 1.05,
                          "Riyadh": 1.03, "Doha": 1.0, "Jeddah": 0.95}
            base_prob *= region_mult.get(sc["region"], 1.0)

            # Discount optimisation (20-50% ideal)
            if 20 <= sc["discount"] <= 50:
                base_prob *= 1.15
            elif sc["discount"] > 50:
                base_prob *= 0.85

            # ROI modifier
            if roi > 100:
                base_prob *= 1.20
            elif 50 <= roi <= 100:
                base_prob *= 1.10
            elif roi <= 0:
                base_prob *= 0.60

            # Add small random variation (±3%)
            success_prob = max(0, min(100, base_prob + np.random.uniform(-3, 3)))

            # Simulated processing time (ms)
            processing_time = round(np.random.uniform(0.8, 3.5), 2)

            results.append({
                **sc,
                "success_prob": round(success_prob, 2),
                "failure_prob": round(100 - success_prob, 2),
                "expected_revenue": round(revenue, 2),
                "roi": round(roi, 2),
                "processing_time": processing_time,
                "verdict": "✅ GO" if success_prob >= 70 else (
                           "⚠️ REVIEW" if success_prob >= 40 else "❌ NO-GO")
            })

        self.scenario_results = results
        self._display_results(results)

    # ─────────────────────────────────────────────────────────────────────────────
    # DISPLAY RESULTS
    # ─────────────────────────────────────────────────────────────────────────────
    def _display_results(self, results):
        for w in self.results_panel.winfo_children():
            w.destroy()

        # Sort descending by success probability
        results_sorted = sorted(results, key=lambda x: x["success_prob"], reverse=True)
        top5 = results_sorted[:5]
        top1 = top5[0]

        # ── Verdict Banner ──────────────────────────────────────────────────────
        v_color = SUCCESS if top1["success_prob"] >= 70 else (
                   WARNING if top1["success_prob"] >= 40 else DANGER)
        banner = ctk.CTkFrame(self.results_panel, fg_color=v_color, corner_radius=12)
        banner.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(banner,
            text=f"🏆 Best Scenario: {top1['scenario']} — "
                 f"Success: {top1['success_prob']:.1f}% | "
                 f"ROI: {top1['roi']:.1f}% | "
                 f"Revenue: {fmt_money(top1['expected_revenue'])}",
            font=F_CTITLE, text_color=TEXT_PRI).pack(pady=12)

        # ── KPI Summary Row ─────────────────────────────────────────────────────
        kpi_f = ctk.CTkFrame(self.results_panel, fg_color="transparent")
        kpi_f.pack(fill="x", pady=5)
        for i in range(4): kpi_f.columnconfigure(i, weight=1)

        avg_success = np.mean([r["success_prob"] for r in results])
        avg_failure = np.mean([r["failure_prob"] for r in results])
        avg_time = np.mean([r["processing_time"] for r in results])
        best_roi = top1["roi"]

        KPICard(kpi_f, "🎯", "Avg Success", f"{avg_success:.1f}%",
                subtitle=f"{len(results)} scenarios", accent=SUCCESS
               ).grid(row=0, column=0, padx=5, sticky="nsew")

        KPICard(kpi_f, "⚠️", "Avg Failure", f"{avg_failure:.1f}%",
                subtitle="Risk indicator", accent=DANGER
               ).grid(row=0, column=1, padx=5, sticky="nsew")

        KPICard(kpi_f, "⏱️", "Avg Processing", f"{avg_time:.2f}s",
                subtitle="Compute time", accent=ACCENT_BLUE
               ).grid(row=0, column=2, padx=5, sticky="nsew")

        KPICard(kpi_f, "📈", "Best ROI", f"{best_roi:.1f}%",
                subtitle=top1['scenario'], accent=WARNING
               ).grid(row=0, column=3, padx=5, sticky="nsew")

        # ── Charts Row ──────────────────────────────────────────────────────────
        charts_f = ctk.CTkFrame(self.results_panel, fg_color="transparent")
        charts_f.pack(fill="x", pady=10)
        charts_f.columnconfigure((0,1), weight=1)

        # Chart 1: Success vs Failure Pie
        pie_card = ChartCard(charts_f, "Success vs Failure Rate", figsize=(5,4))
        pie_card.grid(row=0, column=0, padx=(0,8), sticky="nsew")
        ax = pie_card.ax
        ax.pie([avg_success, avg_failure],
               labels=['Success', 'Failure'],
               colors=[SUCCESS, DANGER],
               autopct='%1.1f%%',
               startangle=90,
               wedgeprops={'width':0.5, 'edgecolor': BG_CARD})
        ax.set_facecolor(BG_CARD)
        pie_card.refresh()

        # Chart 2: Top 5 Scenarios Bar (Horizontal)
        bar_card = ChartCard(charts_f, "Top 5 Scenarios – Success Rate", figsize=(7,4))
        bar_card.grid(row=0, column=1, padx=(8,0), sticky="nsew")
        ax2 = bar_card.ax
        names = [r["scenario"] for r in top5]
        probs = [r["success_prob"] for r in top5]
        colors = [SUCCESS if p >= 70 else WARNING if p >= 40 else DANGER for p in probs]
        bars = ax2.barh(names[::-1], probs[::-1], color=colors[::-1], height=0.6)
        ax2.set_xlim(0, 110)
        ax2.set_xlabel("Success Probability (%)", fontsize=9)
        ax2.bar_label(bars, padding=3, fmt='%.1f%%', fontsize=8)
        ax2.set_facecolor(BG_CARD)
        bar_card.refresh()

        # ── Detailed Table ──────────────────────────────────────────────────────
        table_f = ctk.CTkFrame(self.results_panel, fg_color=BG_CARD, corner_radius=15,
                              border_width=1, border_color=BORDER)
        table_f.pack(fill="both", expand=True, pady=10)

        header = ctk.CTkFrame(table_f, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        ctk.CTkLabel(header, text="📋 Detailed Scenario Analysis (Top 10)",
                     font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w")

        cols = ["Rank", "Scenario", "Season", "Region", "Price($)", "Disc%",
                "Success%", "Failure%", "ROI%", "Time(s)", "Verdict"]
        tbl = DSSTable(table_f, columns=cols)
        tbl.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        rows = []
        for i, r in enumerate(results_sorted[:10]):
            rows.append([
                f"#{i+1}",
                r["scenario"],
                r["season"],
                r["region"],
                f"{r['price']:.2f}",
                f"{r['discount']}%",
                f"{r['success_prob']:.1f}%",
                f"{r['failure_prob']:.1f}%",
                f"{r['roi']:.1f}%",
                f"{r['processing_time']}",
                r["verdict"]
            ])
        tbl.load(rows)

        # Success message
        Toast.show(self.winfo_toplevel(),
                   f"✅ Analysis complete: {len(results)} scenarios processed",
                   color=SUCCESS, duration=3)
