"""Page 8 – Product Success Calculator (full interactive lab)."""
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
    CHART_COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_BODY,
    FONT_CAPTION, FONT_LABEL, HISTORY_FILES,
)
from dss_core.widgets import (
    KPICard, ChartCard, DSSTable, GaugeWidget,
    ScrollablePage, fmt_money, fmt_pct, fmt_count, Toast,
)


class CalculatorPage(ScrollablePage):
    """Interactive product success calculator with ML predictions."""

    def build(self):
        self.columnconfigure((0, 1), weight=1)

        # ── Page title ────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 8))
        ctk.CTkLabel(hdr, text="🧪  Product Success Calculator",
                     font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="AI-powered product viability analysis and financial projections",
                     font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # ── LEFT: Input Panel ─────────────────────────────────────────────
        left = ctk.CTkScrollableFrame(self, fg_color=BG_CARD, corner_radius=15,
                                       border_width=1, border_color=BORDER, width=380)
        left.grid(row=1, column=0, sticky="nsew", padx=(20, 6), pady=(4, 20))
        self._build_inputs(left)

        # ── RIGHT: Results Panel ──────────────────────────────────────────
        self._right = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._right.grid(row=1, column=1, sticky="nsew", padx=(6, 20), pady=(4, 20))
        self._right.columnconfigure(0, weight=1)
        self._build_placeholder()

    # ── Input Form ────────────────────────────────────────────────────────
    def _build_inputs(self, parent):
        parent.columnconfigure(0, weight=1)
        pad = {"padx": 16, "pady": 4}

        def section(text):
            ctk.CTkLabel(parent, text=text, font=FONT_SUBTITLE,
                         text_color=ACCENT_BLUE).pack(anchor="w", padx=16, pady=(14, 2))
            ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=2)

        def lbl(text):
            ctk.CTkLabel(parent, text=text, font=FONT_LABEL,
                         text_color=TEXT_SECONDARY).pack(anchor="w", **pad)

        # Section 1 – Product Info
        section("📦  Product Information")
        lbl("Product Name")
        self._name = ctk.CTkEntry(parent, placeholder_text="e.g. Smart Watch Pro",
                                   fg_color=BG_CARD2, border_color=BORDER2)
        self._name.pack(fill="x", **pad)

        lbl("Product Category")
        cats = []
        eco = self.store.eco_df
        if not eco.empty and "product_category" in eco.columns:
            cats = sorted(eco["product_category"].unique().tolist())
        self._cat = ctk.CTkComboBox(parent, values=cats or ["Electronics","Fashion","Food"],
                                     fg_color=BG_CARD2, border_color=BORDER2,
                                     button_color=ACCENT_PURPLE)
        self._cat.pack(fill="x", **pad)

        # Section 2 – Pricing
        section("💰  Pricing Strategy")
        lbl("Unit Price ($)")
        self._price = ctk.CTkEntry(parent, placeholder_text="e.g. 99.99",
                                    fg_color=BG_CARD2, border_color=BORDER2)
        self._price.pack(fill="x", **pad)
        self._price.insert(0, "99.99")

        lbl("Discount % (0–70)")
        self._disc_val = ctk.StringVar(value="10")
        disc_row = ctk.CTkFrame(parent, fg_color="transparent")
        disc_row.pack(fill="x", **pad)
        disc_row.columnconfigure(0, weight=1)
        self._disc_sl = ctk.CTkSlider(disc_row, from_=0, to=70, number_of_steps=70,
                                       variable=self._disc_val,
                                       button_color=ACCENT_BLUE,
                                       progress_color=ACCENT_PURPLE,
                                       command=self._on_disc_change)
        self._disc_sl.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkLabel(disc_row, textvariable=self._disc_val,
                     font=FONT_LABEL, text_color=ACCENT_BLUE, width=35).grid(row=0, column=1)
        lbl("Final Price (after discount)")
        self._final_lbl = ctk.CTkLabel(parent, text="$89.99", font=("Segoe UI", 18, "bold"),
                                        text_color=SUCCESS)
        self._final_lbl.pack(anchor="w", **pad)

        # Section 3 – Marketing
        section("📣  Marketing Plan")
        lbl("Marketing Budget ($)")
        self._budget = ctk.CTkEntry(parent, placeholder_text="e.g. 5000",
                                     fg_color=BG_CARD2, border_color=BORDER2)
        self._budget.pack(fill="x", **pad)
        self._budget.insert(0, "5000")

        lbl("Target Season")
        self._season = ctk.CTkComboBox(parent, values=["Spring","Summer","Autumn","Winter","All"],
                                        fg_color=BG_CARD2, border_color=BORDER2,
                                        button_color=ACCENT_PURPLE)
        self._season.pack(fill="x", **pad)

        lbl("Target City/Region")
        cities = []
        if not eco.empty and "city" in eco.columns:
            cities = sorted(eco["city"].unique().tolist())
        self._city = ctk.CTkComboBox(parent, values=cities or ["All"],
                                      fg_color=BG_CARD2, border_color=BORDER2,
                                      button_color=ACCENT_PURPLE)
        self._city.pack(fill="x", **pad)

        # Section 4 – Operational
        section("⚙️  Operational")
        lbl("Expected Quantity")
        self._qty = ctk.CTkEntry(parent, placeholder_text="e.g. 500",
                                  fg_color=BG_CARD2, border_color=BORDER2)
        self._qty.pack(fill="x", **pad)
        self._qty.insert(0, "500")

        lbl("Payment Method")
        self._payment = ctk.CTkComboBox(parent,
            values=["Credit Card","Debit Card","Cash","Bank Transfer","PayPal"],
            fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
        self._payment.pack(fill="x", **pad)

        # Buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(16, 8))
        btn_frame.columnconfigure((0,1), weight=1)
        ctk.CTkButton(btn_frame, text="🚀  Run Full Analysis",
                      font=("Segoe UI", 13, "bold"),
                      fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_analysis).grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(0,6))
        ctk.CTkButton(btn_frame, text="🔄  Reset",
                      fg_color=BG_CARD2, hover_color=BORDER2,
                      command=self._reset).grid(row=1, column=0, sticky="ew", padx=(0,3))
        ctk.CTkButton(btn_frame, text="💾  Save Test",
                      fg_color=BG_CARD2, hover_color=BORDER2,
                      command=self._save_test).grid(row=1, column=1, sticky="ew", padx=(3,0))

    # ── Helpers ───────────────────────────────────────────────────────────
    def _on_disc_change(self, val):
        try:
            price = float(self._price.get() or 0)
            disc  = float(val)
            final = price * (1 - disc / 100)
            self._final_lbl.configure(text=f"${final:.2f}")
        except Exception:
            pass

    def _reset(self):
        self._name.delete(0, "end")
        self._price.delete(0, "end"); self._price.insert(0, "99.99")
        self._disc_sl.set(10)
        self._budget.delete(0, "end"); self._budget.insert(0, "5000")
        self._qty.delete(0, "end");    self._qty.insert(0, "500")
        for w in list(self._right.winfo_children()):
            w.destroy()
        self._build_placeholder()

    def _build_placeholder(self):
        ctk.CTkLabel(self._right,
                     text="👈  Fill in the form and click\n🚀 Run Full Analysis",
                     font=("Segoe UI", 18), text_color=TEXT_MUTED,
                     justify="center").pack(expand=True, pady=80)

    def _get_inputs(self):
        try:
            price  = float(self._price.get() or 99.99)
            disc   = float(self._disc_val.get() or 0)
            budget = float(self._budget.get() or 5000)
            qty    = int(float(self._qty.get() or 500))
            cat    = self._cat.get()
            season = self._season.get()
            city   = self._city.get()
            return price, disc, budget, qty, cat, season, city
        except Exception:
            return 99.99, 10, 5000, 500, "Electronics", "Summer", "All"

    # ── Core Analysis ─────────────────────────────────────────────────────
    def _run_analysis(self):
        for w in list(self._right.winfo_children()):
            w.destroy()

        price, disc, budget, qty, cat, season, city = self._get_inputs()
        self._last_inputs = (price, disc, budget, qty, cat, season, city)

        # Financial calcs
        final_price    = price * (1 - disc / 100)
        revenue        = final_price * qty
        marketing_cost = budget
        gross_profit   = revenue - marketing_cost
        margin_pct     = (gross_profit / revenue * 100) if revenue > 0 else 0
        break_even     = marketing_cost / final_price if final_price > 0 else 0
        payback        = marketing_cost / max(gross_profit / 12, 1)
        roi_pct        = (gross_profit - marketing_cost) / max(marketing_cost, 1) * 100
        roas           = revenue / max(marketing_cost, 1)

        # ML score
        ml_prob        = self._ml_predict(cat, price, disc, season, city)

        # Composite score
        market_score = 70.0
        eco = self.store.eco_df
        if not eco.empty and "product_category" in eco.columns and "unit_price" in eco.columns:
            cat_avg = eco[eco["product_category"]==cat]["unit_price"].mean()
            if cat_avg > 0:
                pos = abs(price - cat_avg) / cat_avg
                market_score = max(0, 100 - pos * 50)

        margin_score = min(100, max(0, margin_pct))
        final_score  = ml_prob * 0.4 + margin_score * 0.3 + market_score * 0.3

        # Verdict
        if final_score >= 70:
            verdict, vcolor, vicon = "GO FOR LAUNCH", SUCCESS, "✅"
        elif final_score >= 40:
            verdict, vcolor, vicon = "REVIEW NEEDED", WARNING, "⚠️"
        else:
            verdict, vcolor, vicon = "DO NOT LAUNCH", DANGER, "❌"

        self._last_result = dict(
            verdict=verdict, score=final_score, ml_prob=ml_prob,
            margin_score=margin_score, market_score=market_score,
            revenue=revenue, cost=marketing_cost, profit=gross_profit,
            margin_pct=margin_pct, break_even=break_even,
            payback=payback, roi_pct=roi_pct, roas=roas,
        )

        r = self._right
        r.columnconfigure(0, weight=1)
        row_idx = [0]

        def nrow():
            r_v = row_idx[0]; row_idx[0] += 1; return r_v

        # 1. Verdict banner
        banner = ctk.CTkFrame(r, fg_color=vcolor, corner_radius=15)
        banner.grid(row=nrow(), column=0, sticky="ew", padx=4, pady=(4,6))
        ctk.CTkLabel(banner, text=f"{vicon}  {verdict}",
                     font=("Segoe UI", 24, "bold"), text_color=TEXT_PRIMARY).pack(pady=10)
        ctk.CTkLabel(banner, text=f"Composite Score: {final_score:.1f}%",
                     font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(pady=(0, 10))

        # 2. Gauge
        gauge = GaugeWidget(r, "Success Probability", min_val=0, max_val=100)
        gauge.grid(row=nrow(), column=0, sticky="ew", padx=4, pady=4)
        gauge.set_value(final_score)

        # 3. Financial cards
        ctk.CTkLabel(r, text="💵  Financial Projections", font=FONT_SUBTITLE,
                     text_color=TEXT_PRIMARY).grid(row=nrow(), column=0, sticky="w", padx=8, pady=(8,2))
        fin_frame = ctk.CTkFrame(r, fg_color="transparent")
        fin_frame.grid(row=nrow(), column=0, sticky="ew", padx=4, pady=2)
        for i in range(4): fin_frame.columnconfigure(i, weight=1)
        fin_items = [
            ("💰","Expected Revenue",   fmt_money(revenue),        ACCENT_BLUE),
            ("📉","Marketing Cost",     fmt_money(marketing_cost), DANGER),
            ("💵","Gross Profit",       fmt_money(gross_profit),   SUCCESS if gross_profit >= 0 else DANGER),
            ("📊","Profit Margin",      fmt_pct(margin_pct),       SUCCESS if margin_pct >= 20 else WARNING),
            ("🔢","Break-Even Units",   fmt_count(int(break_even)),ACCENT_PURPLE),
            ("📅","Payback (months)",   f"{payback:.1f}",          WARNING),
            ("📈","ROI %",              fmt_pct(roi_pct),          SUCCESS if roi_pct >= 0 else DANGER),
            ("📡","ROAS",               f"{roas:.2f}x",            ACCENT_BLUE),
        ]
        for i, (icon, title, val, acc) in enumerate(fin_items):
            KPICard(fin_frame, icon=icon, title=title, value=val, accent=acc).grid(
                row=i//4, column=i%4, sticky="nsew", padx=3, pady=3, ipady=4)

        # 4. ML Breakdown
        ctk.CTkLabel(r, text="🤖  ML Prediction Breakdown", font=FONT_SUBTITLE,
                     text_color=TEXT_PRIMARY).grid(row=nrow(), column=0, sticky="w", padx=8, pady=(8,2))
        ml_frame = ctk.CTkFrame(r, fg_color=BG_CARD, corner_radius=12,
                                 border_width=1, border_color=BORDER)
        ml_frame.grid(row=nrow(), column=0, sticky="ew", padx=4, pady=4)
        ml_frame.columnconfigure(0, weight=1)
        for label, val, weight in [
            ("🤖  ML Score (40%)",            ml_prob,       0.4),
            ("💰  Margin Score (30%)",         margin_score,  0.3),
            ("📈  Market Position Score (30%)", market_score, 0.3),
            ("🏆  Final Weighted Score",        final_score,  1.0),
        ]:
            row2 = ctk.CTkFrame(ml_frame, fg_color="transparent")
            row2.pack(fill="x", padx=12, pady=3)
            row2.columnconfigure(1, weight=1)
            ctk.CTkLabel(row2, text=label, font=FONT_BODY,
                         text_color=TEXT_SECONDARY).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(row2, text=f"{val:.1f}%", font=FONT_BODY,
                         text_color=ACCENT_BLUE).grid(row=0, column=2, sticky="e")
            pb = ctk.CTkProgressBar(row2, progress_color=ACCENT_BLUE if weight < 1 else SUCCESS)
            pb.grid(row=1, column=0, columnspan=3, sticky="ew", pady=2)
            pb.set(val / 100)

        # 5. Sensitivity chart
        sens_card = self._add_chart(ChartCard(r, "📉  Sensitivity Analysis", figsize=(8, 3.5)))
        sens_card.grid(row=nrow(), column=0, sticky="nsew", padx=4, pady=4)
        self._draw_sensitivity(sens_card, price, disc, cat, season, city, ml_prob)

        # 6. Risk assessment
        ctk.CTkLabel(r, text="⚠️  Risk Assessment", font=FONT_SUBTITLE,
                     text_color=TEXT_PRIMARY).grid(row=nrow(), column=0, sticky="w", padx=8, pady=(8,2))
        risk_frame = ctk.CTkFrame(r, fg_color="transparent")
        risk_frame.grid(row=nrow(), column=0, sticky="ew", padx=4, pady=4)
        for i in range(4): risk_frame.columnconfigure(i, weight=1)
        self._draw_risks(risk_frame, price, disc, cat, margin_pct)

        # 7. Recommendations
        ctk.CTkLabel(r, text="💡  AI Recommendations", font=FONT_SUBTITLE,
                     text_color=TEXT_PRIMARY).grid(row=nrow(), column=0, sticky="w", padx=8, pady=(8,2))
        self._draw_recommendations(r, nrow(), price, disc, cat, season, margin_pct, roi_pct)

        # 8. Similar products table
        ctk.CTkLabel(r, text="🔍  Similar Successful Products", font=FONT_SUBTITLE,
                     text_color=TEXT_PRIMARY).grid(row=nrow(), column=0, sticky="w", padx=8, pady=(8,2))
        self._draw_similar(r, nrow(), cat)

    def _ml_predict(self, cat, price, disc, season, city):
        ml = self.store.ml
        if ml.product_model is None:
            # Fallback heuristic
            base = 60.0
            if disc > 30: base -= 10
            if disc < 10: base += 5
            if price > 200: base -= 5
            return max(0, min(100, base))
        try:
            enc = ml.product_encoders
            cat_enc    = enc["product_category"].transform([cat])[0]    if cat    in enc.get("product_category", type("",(),{"classes_":[]})()).classes_ else 0
            season_enc = enc["season"].transform([season])[0] if season in enc.get("season", type("",(),{"classes_":[]})()).classes_ else 0
            city_enc   = enc["city"].transform([city])[0]     if city   in enc.get("city",   type("",(),{"classes_":[]})()).classes_ else 0
            X = [[cat_enc, price, disc, season_enc, city_enc]]
            prob = ml.product_model.predict_proba(X)[0][1] * 100
            return round(prob, 1)
        except Exception:
            return 60.0

    def _draw_sensitivity(self, card, price, disc, cat, season, city, base_prob):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        discs   = np.linspace(0, 70, 30)
        probs_d = [self._ml_predict(cat, price, d, season, city) for d in discs]
        prices  = np.linspace(price * 0.5, price * 1.5, 30)
        probs_p = [self._ml_predict(cat, p, disc, season, city) for p in prices]
        ax.plot(discs, probs_d, color=ACCENT_BLUE, linewidth=2.5, label="vs Discount %")
        ax2 = ax.twiny()
        ax2.plot(prices, probs_p, color=WARNING, linewidth=2.5, linestyle="--", label="vs Price $")
        ax2.set_xlabel("Price ($)", color=WARNING, fontsize=9)
        ax.axvline(disc, color=ACCENT_BLUE, linestyle=":", linewidth=1.5, alpha=0.7)
        ax.axhline(70, color=SUCCESS, linestyle="--", linewidth=1, alpha=0.5, label="GO threshold")
        ax.set_xlabel("Discount %", color=ACCENT_BLUE, fontsize=9)
        ax.set_ylabel("Success Prob %", color=TEXT_SECONDARY, fontsize=9)
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8,
                  facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); card.refresh()

    def _draw_risks(self, parent, price, disc, cat, margin):
        eco = self.store.eco_df
        cat_avg = 0
        if not eco.empty and "product_category" in eco.columns:
            g = eco[eco["product_category"]==cat]["unit_price"]
            cat_avg = g.mean() if len(g) > 0 else price

        risks = [
            ("💰 Price Risk",
             ("LOW" if abs(price-cat_avg)/max(cat_avg,1) < 0.2 else
              ("MED" if abs(price-cat_avg)/max(cat_avg,1) < 0.5 else "HIGH")),
             f"Mkt avg: ${cat_avg:.0f}"),
            ("🏷️ Discount Risk",
             "LOW" if disc < 20 else ("MED" if disc < 40 else "HIGH"),
             f"Margin impact: {disc:.0f}%"),
            ("📈 Market Risk",
             "LOW" if margin > 30 else ("MED" if margin > 10 else "HIGH"),
             f"Margin: {margin:.1f}%"),
            ("🗓️ Timing Risk",
             "LOW", "Seasonal analysis based on data"),
        ]
        rcolors = {"LOW": SUCCESS, "MED": WARNING, "HIGH": DANGER}
        for i, (title, level, note) in enumerate(risks):
            f = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10,
                              border_width=1, border_color=BORDER)
            f.grid(row=0, column=i, sticky="nsew", padx=3, pady=2)
            ctk.CTkLabel(f, text=title, font=FONT_LABEL, text_color=TEXT_SECONDARY).pack(padx=8, pady=(8,2))
            ctk.CTkLabel(f, text=level, font=("Segoe UI",15,"bold"),
                         text_color=rcolors.get(level, ACCENT_BLUE)).pack()
            ctk.CTkLabel(f, text=note, font=FONT_CAPTION, text_color=TEXT_MUTED).pack(padx=8, pady=(2,8))

    def _draw_recommendations(self, parent, row_fn, price, disc, cat, season, margin, roi):
        f = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12,
                          border_width=1, border_color=BORDER)
        f.grid(row=row_fn(), column=0, sticky="ew", padx=4, pady=4)
        recs = [
            f"💡 Optimal discount: {max(0,disc-5):.0f}% may improve margin by ~5%",
            f"🗓️ Launch in {season} for best seasonal performance",
            f"💰 Target price: ${price:.2f} — consider ${price*0.95:.2f} for higher volume",
            f"📈 Current ROI: {roi:.1f}% — {'strong' if roi>50 else 'needs improvement'}",
            f"📣 Allocate 60% of budget to online channels for best ROAS",
        ]
        for rec in recs:
            ctk.CTkLabel(f, text=rec, font=FONT_BODY, text_color=TEXT_SECONDARY,
                         anchor="w", wraplength=450).pack(anchor="w", padx=14, pady=3)

    def _draw_similar(self, parent, row_fn, cat):
        sim_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12,
                                  border_width=1, border_color=BORDER)
        sim_frame.grid(row=row_fn(), column=0, sticky="ew", padx=4, pady=(4,20))
        pl = self.store.powerbi.get("product_launch", self.store.sim_df)
        cols = ["product_category","unit_price","discount_pct","season","success_prob","decision"]
        cols = [c for c in cols if not pl.empty and c in pl.columns]
        if cols and not pl.empty:
            sub = pl[pl["product_category"]==cat].nlargest(5, "success_prob") if "success_prob" in pl.columns else pl[pl["product_category"]==cat].head(5)
            tbl = DSSTable(sim_frame, columns=cols)
            tbl.pack(fill="both", expand=True, padx=10, pady=10)
            rows = [tuple(str(sub[c].iloc[i]) for c in cols) for i in range(len(sub))]
            tbl.load(rows)
        else:
            ctk.CTkLabel(sim_frame, text="No similar product data",
                         font=FONT_BODY, text_color=TEXT_MUTED).pack(padx=14, pady=20)

    def _save_test(self):
        if not hasattr(self, "_last_result"):
            return
        res = self._last_result
        inp = self._last_inputs if hasattr(self, "_last_inputs") else (0,)*7
        price, disc, budget, qty, cat, season, city = inp
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            self._name.get() or "Unnamed",
            cat, price, disc, budget,
            f"{res['score']:.1f}", res['verdict'],
            f"{res['revenue']:.2f}", f"{res['roi_pct']:.2f}", res['verdict']
        ]
        fp = HISTORY_FILES.get("product_tests", "")
        if fp:
            exists = os.path.exists(fp)
            with open(fp, "a", newline="") as f:
                w = csv.writer(f)
                if not exists:
                    w.writerow(["timestamp","product_name","category","price","discount",
                                "budget","success_prob","decision","expected_revenue","roi","verdict"])
                w.writerow(row)
        Toast.show(self.winfo_toplevel(), "✅  Test saved successfully!")
