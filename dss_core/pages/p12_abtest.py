"""Pages 12-15: A/B Testing, Inventory, Alerts Center, Competitor Analysis."""
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
)
from dss_core.widgets import (
    KPICard, ChartCard, DSSTable, GaugeWidget, AlertCard,
    ScrollablePage, fmt_money, fmt_pct, fmt_count,
)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 12 – A/B Testing Simulator
# ─────────────────────────────────────────────────────────────────────────────
class ABTestPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="⚖️  A/B Testing Simulator", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Compare two strategies with statistical significance analysis", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20, pady=4)
        main.columnconfigure((0,1,2), weight=1)

        # Option A
        pa = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15, border_width=2, border_color=ACCENT_BLUE)
        pa.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        ctk.CTkLabel(pa, text="Option A", font=("Segoe UI",18,"bold"), text_color=ACCENT_BLUE).pack(pady=(12,4))
        self._a = self._option_form(pa)

        # Run button
        mid = ctk.CTkFrame(main, fg_color="transparent")
        mid.grid(row=0, column=1, sticky="nsew", padx=4)
        ctk.CTkLabel(mid, text="VS", font=("Segoe UI",30,"bold"), text_color=BORDER2).pack(expand=True)
        ctk.CTkButton(mid, text="⚡\nRun\nTest", font=FONT_SUBTITLE, fg_color=ACCENT_PURPLE,
                      hover_color="#5b21b6", width=80, height=80, command=self._run_ab).pack()

        # Option B
        pb = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15, border_width=2, border_color=WARNING)
        pb.grid(row=0, column=2, sticky="nsew", padx=(4,0))
        ctk.CTkLabel(pb, text="Option B", font=("Segoe UI",18,"bold"), text_color=WARNING).pack(pady=(12,4))
        self._b = self._option_form(pb)

        # Results
        self._ab_res = ctk.CTkFrame(self, fg_color="transparent")
        self._ab_res.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._ab_res.columnconfigure(0, weight=1)

    def _option_form(self, parent):
        d = {}
        fields = [("Price ($)","price","99.99"), ("Discount %","disc","10"),
                  ("Budget ($)","budget","5000"), ("Season","season",None),
                  ("Category","cat",None)]
        cats = sorted(self.store.eco_df["product_category"].unique().tolist()) if not self.store.eco_df.empty and "product_category" in self.store.eco_df.columns else ["Electronics"]
        for label, key, default in fields:
            ctk.CTkLabel(parent, text=label, font=FONT_CAPTION, text_color=TEXT_SECONDARY).pack(anchor="w", padx=12, pady=(6,1))
            if key == "season":
                w = ctk.CTkComboBox(parent, values=["Spring","Summer","Autumn","Winter"], fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
            elif key == "cat":
                w = ctk.CTkComboBox(parent, values=cats, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
            else:
                w = ctk.CTkEntry(parent, fg_color=BG_CARD2, border_color=BORDER2)
                if default: w.insert(0, default)
            w.pack(fill="x", padx=12, pady=(0,4))
            d[key] = w
        return d

    def _get_vals(self, form):
        try:
            price  = float(form["price"].get())
            disc   = float(form["disc"].get())
            budget = float(form["budget"].get())
        except: price, disc, budget = 99.99, 10, 5000
        season = form["season"].get()
        cat    = form["cat"].get()
        return price, disc, budget, season, cat

    def _run_ab(self):
        for w in self._ab_res.winfo_children(): w.destroy()
        self._ab_res.columnconfigure((0,1), weight=1)

        pa, pb = self._get_vals(self._a), self._get_vals(self._b)
        kpi = self.store.kpi

        def calc(price, disc, budget):
            fp  = price * (1 - disc/100)
            qty = max(int(budget / max(fp, 1) * 5), 1)
            rev = fp * qty
            roi = (rev - budget) / max(budget,1) * 100
            return rev, roi, qty

        rev_a, roi_a, qty_a = calc(*pa[:3])
        rev_b, roi_b, qty_b = calc(*pb[:3])
        lift = (rev_b - rev_a) / max(rev_a,1) * 100
        winner = "A" if rev_a >= rev_b else "B"
        winner_color = ACCENT_BLUE if winner == "A" else WARNING

        # Banner
        banner = ctk.CTkFrame(self._ab_res, fg_color=winner_color, corner_radius=12)
        banner.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)
        ctk.CTkLabel(banner, text=f"🏆  Option {winner} Wins!  |  Revenue Lift: {lift:+.1f}%",
                     font=("Segoe UI",18,"bold"), text_color=TEXT_PRIMARY).pack(pady=12)

        # Compare bars
        comp_card = self._add_chart(ChartCard(self._ab_res, "📊  Head-to-Head Comparison", figsize=(8,3.5)))
        comp_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=4)
        ax = comp_card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        metrics = ["Revenue","ROI %","Budget"]
        vals_a  = [rev_a, roi_a, pa[2]]
        vals_b  = [rev_b, roi_b, pb[2]]
        x = np.arange(len(metrics)); w = 0.35
        ax.bar(x-w/2, vals_a, w, label="Option A", color=ACCENT_BLUE, alpha=0.85)
        ax.bar(x+w/2, vals_b, w, label="Option B", color=WARNING,     alpha=0.85)
        ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=10)
        ax.legend(fontsize=9, facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(axis="y", alpha=0.2); comp_card.refresh()

        # KPIs
        kf = ctk.CTkFrame(self._ab_res, fg_color="transparent")
        kf.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)
        for i in range(4): kf.columnconfigure(i, weight=1)
        for i,(icon,title,val,acc) in enumerate([
            ("💰","Revenue A",   fmt_money(rev_a), ACCENT_BLUE),
            ("💰","Revenue B",   fmt_money(rev_b), WARNING),
            ("📈","ROI A",       fmt_pct(roi_a),   ACCENT_BLUE),
            ("📈","ROI B",       fmt_pct(roi_b),   WARNING),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, pady=3, ipady=5)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 13 – Inventory & Demand Planning
# ─────────────────────────────────────────────────────────────────────────────
class InventoryPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="📦  Inventory & Demand Planning", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Demand forecasting, reorder points, and safety stock optimization", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        inp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        inp.columnconfigure((0,1,2,3), weight=1)

        cats = sorted(self.store.eco_df["product_category"].unique().tolist()) if not self.store.eco_df.empty and "product_category" in self.store.eco_df.columns else ["All"]
        for col, (label, attr, default, is_combo) in enumerate({
            "Category":         ("_inv_cat",   cats,  True),
            "Current Stock":    ("_inv_stock", "1000", False),
            "Lead Time (days)": ("_inv_lead",  "7",    False),
        }.items()):
            ctk.CTkLabel(inp, text=col, font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=list({
                "Category":"_inv_cat","Current Stock":"_inv_stock","Lead Time (days)":"_inv_lead"
            }.keys()).index(col), padx=12, pady=(12,2), sticky="w")
            if is_combo:
                w = ctk.CTkComboBox(inp, values=attr, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
            else:
                w = ctk.CTkEntry(inp, fg_color=BG_CARD2, border_color=BORDER2)
                w.insert(0, default)
            setattr(self, attr, w)
            w.grid(row=1, column=list({
                "Category":"_inv_cat","Current Stock":"_inv_stock","Lead Time (days)":"_inv_lead"
            }.keys()).index(col), padx=12, pady=(0,12), sticky="ew")
        ctk.CTkButton(inp, text="📊  Calculate", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_inv).grid(row=1, column=3, padx=12, pady=(0,12), sticky="ew")

        self._inv_res = ctk.CTkFrame(self, fg_color="transparent")
        self._inv_res.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._inv_res.columnconfigure(0, weight=1)

        # Always show inventory table from pre-exported data
        inv_df = pd.read_csv(self.store.powerbi.get("monthly_kpi","") if False else "") if False else pd.DataFrame()
        try:
            import os
            from dss_core.config import POWERBI_DIR
            inv_path = os.path.join(POWERBI_DIR, "inventory_powerbi.csv")
            if os.path.exists(inv_path):
                inv_df = pd.read_csv(inv_path)
        except: pass

        if not inv_df.empty:
            tbl_f = ctk.CTkFrame(self._inv_res, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER)
            tbl_f.grid(row=0, column=0, sticky="nsew", pady=4)
            ctk.CTkLabel(tbl_f, text="📋  Inventory Summary", font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
            cols = list(inv_df.columns)[:7]
            tbl = DSSTable(tbl_f, columns=cols)
            tbl.pack(fill="both", expand=True, padx=10, pady=(0,10))
            rows = [tuple(str(inv_df[c].iloc[i]) for c in cols) for i in range(min(50, len(inv_df)))]
            tbl.load(rows)

    def _run_inv(self):
        for w in list(self._inv_res.winfo_children())[1:]: w.destroy()
        cat  = self._inv_cat.get()
        try: stock = float(self._inv_stock.get())
        except: stock = 1000
        try: lead  = float(self._inv_lead.get())
        except: lead = 7

        eco = self.store.eco_df
        cat_df = eco[eco["product_category"]==cat] if not eco.empty and "product_category" in eco.columns else eco
        daily  = cat_df["quantity"].sum() / 365 if not cat_df.empty and "quantity" in cat_df.columns else 10
        std_d  = cat_df["quantity"].std()  / 7  if not cat_df.empty and "quantity" in cat_df.columns else 3
        safety = std_d * 1.65 * (lead ** 0.5)
        reorder= daily * lead + safety
        eoq    = (2 * daily * 365 * 50 / 0.2) ** 0.5
        dos    = stock / max(daily, 0.01)

        kf = ctk.CTkFrame(self._inv_res, fg_color="transparent")
        kf.grid(row=99, column=0, sticky="ew", pady=4)
        for i in range(4): kf.columnconfigure(i, weight=1)
        for i,(icon,title,val,acc) in enumerate([
            ("📦","Reorder Point",  f"{reorder:.0f} units", WARNING),
            ("🛡️","Safety Stock",   f"{safety:.0f} units",  ACCENT_BLUE),
            ("🔄","EOQ",            f"{eoq:.0f} units",      SUCCESS),
            ("📅","Days of Supply", f"{dos:.0f} days",       DANGER if dos < 14 else SUCCESS),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, ipady=6)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 14 – KPI Alert Center
# ─────────────────────────────────────────────────────────────────────────────
class AlertsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="🚨  Real-Time KPI Alert Center", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Auto-generated alerts based on live metric thresholds", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        # Filter bar
        fb = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER)
        fb.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        fb.columnconfigure(2, weight=1)
        ctk.CTkLabel(fb, text="Filter:", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=0, padx=12, pady=10)
        self._alert_filter = ctk.CTkComboBox(fb, values=["All","CRITICAL","WARNING","INFO"],
                                              fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE,
                                              command=self._filter_alerts)
        self._alert_filter.grid(row=0, column=1, padx=8, pady=10)

        # Alerts list
        self._alerts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._alerts_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=4)
        self._alerts_frame.columnconfigure(0, weight=1)
        self._show_alerts("All")

        # KPI summary
        kpi = self.store.kpi
        sum_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        sum_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(4,20))
        ctk.CTkLabel(sum_frame, text="📊  Current KPI Status", font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        metrics = [
            ("Revenue Growth",  f"{kpi.revenue_growth:.1f}%",   kpi.revenue_growth >= 0),
            ("Churn Rate",      f"{kpi.churn_rate:.1f}%",       kpi.churn_rate < 45),
            ("Overall ROI",     f"{kpi.overall_roi:.1f}%",      kpi.overall_roi >= 100),
            ("Avg Rating",      f"{kpi.avg_rating:.2f}/5",      kpi.avg_rating >= 3),
            ("High Risk Cust.", fmt_count(kpi.high_risk),       kpi.high_risk < 100),
        ]
        gf = ctk.CTkFrame(sum_frame, fg_color="transparent")
        gf.pack(fill="x", padx=10, pady=(0,10))
        for i in range(5): gf.columnconfigure(i, weight=1)
        for i,(label, val, ok) in enumerate(metrics):
            f = ctk.CTkFrame(gf, fg_color=BG_CARD2, corner_radius=8)
            f.grid(row=0, column=i, sticky="nsew", padx=3, pady=3)
            ctk.CTkLabel(f, text="✅" if ok else "⚠️", font=("Segoe UI Emoji",18)).pack(pady=(8,2))
            ctk.CTkLabel(f, text=val, font=FONT_SUBTITLE, text_color=SUCCESS if ok else WARNING).pack()
            ctk.CTkLabel(f, text=label, font=FONT_CAPTION, text_color=TEXT_MUTED).pack(pady=(0,8))

    def _filter_alerts(self, val):
        for w in self._alerts_frame.winfo_children(): w.destroy()
        self._show_alerts(val)

    def _show_alerts(self, severity="All"):
        alerts = self.store.alerts
        if severity != "All":
            alerts = [a for a in alerts if a.get("severity","") == severity]
        for i, a in enumerate(alerts):
            AlertCard(self._alerts_frame, a).grid(row=i, column=0, sticky="ew", padx=4, pady=4)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 15 – Competitor & Market Analysis
# ─────────────────────────────────────────────────────────────────────────────
class CompetitorPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="🗺️  Competitor & Market Analysis", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Market positioning, price benchmarking, and competitive intelligence", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        inp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        inp.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        inp.columnconfigure((0,1,2,3), weight=1)

        cats = sorted(self.store.eco_df["product_category"].unique().tolist()) if not self.store.eco_df.empty and "product_category" in self.store.eco_df.columns else ["Electronics"]
        ctk.CTkLabel(inp, text="Category", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=0, padx=12, pady=(12,2), sticky="w")
        self._comp_cat = ctk.CTkComboBox(inp, values=cats, fg_color=BG_CARD2, border_color=BORDER2, button_color=ACCENT_PURPLE)
        self._comp_cat.grid(row=1, column=0, padx=12, pady=(0,12), sticky="ew")

        ctk.CTkLabel(inp, text="Your Price ($)", font=FONT_LABEL, text_color=TEXT_SECONDARY).grid(row=0, column=1, padx=12, pady=(12,2), sticky="w")
        self._comp_price = ctk.CTkEntry(inp, fg_color=BG_CARD2, border_color=BORDER2)
        self._comp_price.grid(row=1, column=1, padx=12, pady=(0,12), sticky="ew")
        self._comp_price.insert(0,"99.99")

        ctk.CTkButton(inp, text="🔍  Analyze", fg_color=ACCENT_PURPLE, hover_color="#5b21b6",
                      command=self._run_comp).grid(row=1, column=3, padx=12, pady=(0,12), sticky="ew")

        self._comp_res = ctk.CTkFrame(self, fg_color="transparent")
        self._comp_res.grid(row=2, column=0, sticky="nsew", padx=20, pady=(4,20))
        self._comp_res.columnconfigure((0,1), weight=1)

    def _run_comp(self):
        for w in self._comp_res.winfo_children(): w.destroy()
        self._comp_res.columnconfigure((0,1), weight=1)

        cat = self._comp_cat.get()
        try: your_price = float(self._comp_price.get())
        except: your_price = 99.99

        eco = self.store.eco_df
        cat_df = eco[eco["product_category"]==cat] if not eco.empty and "product_category" in eco.columns else pd.DataFrame()

        if cat_df.empty or "unit_price" not in cat_df.columns:
            ctk.CTkLabel(self._comp_res, text="No data for selected category", font=FONT_BODY, text_color=TEXT_MUTED).grid(row=0, column=0, columnspan=2, pady=40)
            return

        prices = cat_df["unit_price"]
        mkt_avg= prices.mean()
        q25, q75 = prices.quantile(0.25), prices.quantile(0.75)
        position = "Premium" if your_price > q75 else ("Economy" if your_price < q25 else "Competitive")
        pct_diff = (your_price - mkt_avg) / max(mkt_avg,1) * 100

        kf = ctk.CTkFrame(self._comp_res, fg_color="transparent")
        kf.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)
        for i in range(4): kf.columnconfigure(i, weight=1)
        for i,(icon,title,val,acc) in enumerate([
            ("🎯","Your Price",     fmt_money(your_price), ACCENT_BLUE),
            ("📊","Market Average", fmt_money(mkt_avg),    ACCENT_PURPLE),
            ("📈","Price Diff",     fmt_pct(pct_diff),     SUCCESS if pct_diff < 20 else WARNING),
            ("🏷️","Position",       position,              SUCCESS if position=="Competitive" else WARNING),
        ]):
            KPICard(kf, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, ipady=6)

        # Price histogram
        hist_card = self._add_chart(ChartCard(self._comp_res, "📊  Market Price Distribution", figsize=(6,4)))
        hist_card.grid(row=1, column=0, sticky="nsew", padx=(0,4), pady=4)
        ax = hist_card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        ax.hist(prices.dropna(), bins=30, color=ACCENT_PURPLE, alpha=0.7, edgecolor=BG_CARD)
        ax.axvline(your_price, color=ACCENT_BLUE, linewidth=2.5, linestyle="--", label=f"Your Price ${your_price:.0f}")
        ax.axvline(mkt_avg,    color=WARNING,      linewidth=1.5, linestyle=":", label=f"Market Avg ${mkt_avg:.0f}")
        ax.set_xlabel("Price ($)", color=TEXT_SECONDARY, fontsize=9)
        ax.set_ylabel("Count",     color=TEXT_SECONDARY, fontsize=9)
        ax.legend(fontsize=8, facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); hist_card.refresh()

        # Revenue by price bucket
        rev_card = self._add_chart(ChartCard(self._comp_res, "💰  Revenue by Price Range", figsize=(6,4)))
        rev_card.grid(row=1, column=1, sticky="nsew", padx=(4,0), pady=4)
        ax2 = rev_card.ax; ax2.clear(); ax2.set_facecolor(BG_CARD)
        if "total_amount" in cat_df.columns:
            cat_df2 = cat_df.copy()
            cat_df2["price_bin"] = pd.cut(cat_df2["unit_price"], bins=8)
            g = cat_df2.groupby("price_bin")["total_amount"].sum()
            ax2.bar(range(len(g)), g.values, color=CHART_COLORS[:len(g)], width=0.7)
            ax2.set_xticks(range(len(g)))
            ax2.set_xticklabels([str(x).replace("(","").replace("]","").split(",")[0][:5] for x in g.index], rotation=30, fontsize=7)
            ax2.set_ylabel("Revenue", color=TEXT_SECONDARY, fontsize=9)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
        ax2.grid(axis="y", alpha=0.2); rev_card.refresh()
