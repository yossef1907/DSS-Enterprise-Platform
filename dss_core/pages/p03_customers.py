"""Pages 3 & 4 – Customer Intelligence 360 and Churn Risk Command Center."""
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
    KPICard, ChartCard, SectionHeader, DSSTable, GaugeWidget,
    AlertCard, ScrollablePage, apply_mpl_style,
    fmt_money, fmt_pct, fmt_count,
)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 – Customer Intelligence 360
# ─────────────────────────────────────────────────────────────────────────────
class CustomersPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        kpi  = self.store.kpi
        cust = self.store.cust_df
        seg  = self.store.powerbi.get("customer_segments", pd.DataFrame())

        # ── Header ─────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        ctk.CTkLabel(hdr, text="👥 Customer Intelligence 360",
                     font=FONT_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(hdr, text="360° customer view — Segmentation, RFM scores, and lifetime value",
                     font=FONT_BODY, text_color=TEXT_SEC).pack(anchor="w")

        # ── KPI Strip ───────────────────────────────────────────────────────────
        ks = ctk.CTkFrame(self, fg_color="transparent")
        ks.grid(row=1, column=0, sticky="ew", padx=20, pady=6)
        for i in range(5): ks.columnconfigure(i, weight=1)
        kpis = [
            ("👥", "Total Customers", fmt_count(kpi.total_customers), ACCENT_BLUE),
            ("🔁", "Return Rate",     fmt_pct(kpi.returning_rate),    SUCCESS),
            ("⭐", "Avg Rating",      f"{kpi.avg_rating:.2f}/5",      WARNING),
            ("💎", "Avg CLV",         fmt_money(kpi.avg_clv),         ACCENT_PURP),
            ("🚚", "Avg Delivery",    f"{kpi.avg_delivery:.1f} days", ACCENT_BLUE),
        ]
        for i, (icon, title, val, acc) in enumerate(kpis):
            KPICard(ks, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=6, pady=6, ipady=7)

        # ── Main Content: 3-column ─────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        main.columnconfigure((0,1,2), weight=1)

        # ── Left: Segment Overview ─────────────────────────────────────────────
        seg_frame = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=15,
                                 border_width=1, border_color=BORDER)
        seg_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=6)
        ctk.CTkLabel(seg_frame, text="📊  Segment Overview",
                     font=FONT_SUBTITLE, text_color=TEXT_PRI).pack(anchor="w", padx=15, pady=(12, 8))

        if not cust.empty and "segment" in cust.columns:
            for seg_name, color in [("Champions",ACCENT_BLUE),("Loyal",SUCCESS),
                                     ("At Risk",WARNING),("Hibernating",DANGER)]:
                grp = cust[cust["segment"]==seg_name] if "segment" in cust.columns else pd.DataFrame()
                count = len(grp)
                avg_m = grp["monetary"].mean() if not grp.empty and "monetary" in grp.columns else 0
                f = ctk.CTkFrame(seg_frame, fg_color=BG_CARD2, corner_radius=8)
                f.pack(fill="x", padx=12, pady=4)
                # Header row
                h = ctk.CTkFrame(f, fg_color="transparent")
                h.pack(fill="x", padx=8, pady=(6, 2))
                ctk.CTkLabel(h, text=f"  {seg_name}", font=FONT_BODY,
                            text_color=color).pack(side="left")
                ctk.CTkLabel(h, text=f"{count:,} customers", font=FONT_BODY,
                            text_color=TEXT_SEC).pack(side="right")
                # Stats row
                s = ctk.CTkFrame(f, fg_color="transparent")
                s.pack(fill="x", padx=8, pady=(0, 6))
                ctk.CTkLabel(s, text=f"  Avg: {fmt_money(avg_m)}",
                            font=FONT_CAP, text_color=TEXT_MUTED).pack(side="left")
                f.columnconfigure(1, weight=1)
        else:
            ctk.CTkLabel(seg_frame, text="No segment data yet",
                         font=F_BODY, text_color=TEXT_MUTED).pack(padx=14, pady=30)

        # ── Center: RFM Scatter ─────────────────────────────────────────────────
        rfm_card = self._add_chart(ChartCard(main, "🔢  RFM Distribution", figsize=(5.5,5)))
        rfm_card.grid(row=0, column=1, sticky="nsew", padx=8, pady=6)
        self._draw_rfm(rfm_card, cust)

        # ── Right: Segment Revenue Donut ───────────────────────────────────────
        seg_rev = self._add_chart(ChartCard(main, "💰  Segment Revenue Share", figsize=(5.5,5)))
        seg_rev.grid(row=0, column=2, sticky="nsew", padx=(8,0), pady=6)
        self._draw_seg_revenue(seg_rev, cust)

        # ── Top Customers Table ─────────────────────────────────────────────────
        tc_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                                border_width=1, border_color=BORDER)
        tc_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(12, 20))
        ctk.CTkLabel(tc_frame, text="🏆  Top Customers by Revenue",
                     font=FONT_SUBTITLE, text_color=TEXT_PRI).pack(
            anchor="w", padx=15, pady=(12, 8))

        tc_df = self.store.powerbi.get("top_customers", pd.DataFrame())
        cols  = ["customer_id","total_orders","total_spent","avg_order_value","last_purchase"]
        cols  = [c for c in cols if c in tc_df.columns]
        if cols:
            tbl   = DSSTable(tc_frame, columns=cols)
            tbl.pack(fill="both", expand=True, padx=15, pady=(0, 12))
            if not tc_df.empty:
                rows = [tuple(str(tc_df[c].iloc[i]) for c in cols) for i in range(len(tc_df))]
                tbl.load(rows)

    def _draw_rfm(self, card, cust):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not cust.empty and all(c in cust.columns for c in ["recency","monetary"]):
            seg_col = "segment" if "segment" in cust.columns else None
            seg_map = {}
            if seg_col:
                unique_segs = cust[seg_col].unique()
                seg_map = {s: CHART_COLORS[i % len(CHART_COLORS)]
                           for i, s in enumerate(unique_segs)}
                colors = cust[seg_col].map(seg_map)
            else:
                colors = ACCENT_BLUE
            ax.scatter(cust["recency"], cust["monetary"],
                       c=colors, alpha=0.5, s=15, edgecolors="none")
            ax.set_xlabel("Recency (days)", color=TEXT_SECONDARY, fontsize=9)
            ax.set_ylabel("Monetary Value", color=TEXT_SECONDARY, fontsize=9)
            if seg_col:
                handles = [plt.Line2D([0],[0],marker="o",color="w",
                           markerfacecolor=c,markersize=8,label=s)
                           for s,c in seg_map.items()]
                ax.legend(handles=handles, fontsize=7, loc="upper right",
                          facecolor=BG_CARD2, labelcolor=TEXT_PRIMARY)
        ax.grid(alpha=0.15); card.refresh()

    def _draw_seg_revenue(self, card, cust):
        ax = card.ax; ax.clear()
        if not cust.empty and "segment" in cust.columns and "monetary" in cust.columns:
            g = cust.groupby("segment")["monetary"].sum()
            ax.pie(g.values, labels=g.index, autopct="%1.1f%%",
                   colors=CHART_COLORS[:len(g)], startangle=90,
                   wedgeprops={"width":0.6,"edgecolor":BG_CARD,"linewidth":2})
        card.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 – Churn Risk Command Center
# ─────────────────────────────────────────────────────────────────────────────
class ChurnPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        kpi   = self.store.kpi
        churn = self.store.powerbi.get("churn", pd.DataFrame())
        cust  = self.store.cust_df

        # ── Header ─────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        risk_count = kpi.high_risk
        ctk.CTkLabel(hdr,
            text=f"🔄  Churn Risk Command Center  –  {risk_count:,} High-Risk Customers",
            font=FONT_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Predictive churn model — Revenue at risk analysis",
                     font=F_BODY, text_color=TEXT_SEC).pack(anchor="w")

        # ── Alert Banner ───────────────────────────────────────────────────────
        if risk_count > 0:
            banner = ctk.CTkFrame(self, fg_color=DANGER, corner_radius=10)
            banner.grid(row=1, column=0, sticky="ew", padx=20, pady=6)
            ctk.CTkLabel(banner,
                text=f"🚨  {risk_count:,} HIGH-RISK CUSTOMERS — Immediate retention action required!",
                font=FONT_SUBTITLE, text_color=TEXT_PRI).pack(padx=15, pady=12)

        # ── KPI Strip ───────────────────────────────────────────────────────────
        ks = ctk.CTkFrame(self, fg_color="transparent")
        ks.grid(row=2, column=0, sticky="ew", padx=20, pady=8)
        for i in range(5): ks.columnconfigure(i, weight=1)
        kpis = [
            ("🔴", "High Risk",     fmt_count(kpi.high_risk),     DANGER),
            ("🟡", "Medium Risk",   fmt_count(kpi.medium_risk),   WARNING),
            ("🟢", "Low Risk",      fmt_count(kpi.low_risk),      SUCCESS),
            ("📉", "Churn Rate",    fmt_pct(kpi.churn_rate),      DANGER),
            ("💸", "Revenue at Risk",fmt_money(kpi.revenue_at_risk),WARNING),
        ]
        for i, (icon, title, val, acc) in enumerate(kpis):
            KPICard(ks, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=6, pady=6, ipady=7)

        # ── Charts Row ─────────────────────────────────────────────────────────
        cr = ctk.CTkFrame(self, fg_color="transparent")
        cr.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        cr.columnconfigure((0,1,2), weight=1)

        gauge = GaugeWidget(cr, "Churn Rate", width=200)
        gauge.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=6)
        gauge.set_value(kpi.churn_rate, color=DANGER)

        dist_card = self._add_chart(ChartCard(cr, "📊  Risk Distribution", figsize=(5,4)))
        dist_card.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        self._draw_risk_dist(dist_card, kpi)

        hist_card = self._add_chart(ChartCard(cr, "📈  Churn Score Histogram", figsize=(5,4)))
        hist_card.grid(row=0, column=2, sticky="nsew", padx=(6,0), pady=6)
        self._draw_churn_hist(hist_card, churn)

        # ── At-Risk Customers Table ────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                                 border_width=1, border_color=BORDER)
        tbl_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(12, 20))
        ctk.CTkLabel(tbl_frame, text="🚨  High-Risk Customers — Requires Immediate Action",
                     font=FONT_SUBTITLE, text_color=DANGER).pack(
            anchor="w", padx=15, pady=(12, 8))

        if not churn.empty and "churn_risk" in churn.columns:
            hi = churn[churn["churn_risk"]=="High"]
            cols = [c for c in ["customerID","churn_score","churn_risk","Churn","last_purchase"]
                    if c in hi.columns]
            if cols:
                tbl = DSSTable(tbl_frame, columns=cols)
                tbl.pack(fill="both", expand=True, padx=15, pady=(0, 12))
                rows = [tuple(str(hi[c].iloc[i]) for c in cols)
                        for i in range(min(200, len(hi)))]
                tbl.load(rows)
        elif not cust.empty and "rfm_score" in cust.columns:
            hi  = cust[cust["rfm_score"] < 30]  # lower = higher risk
            cols = [c for c in ["customer_id","rfm_score","segment","monetary","churn_prob"]
                    if c in hi.columns]
            if cols:
                tbl = DSSTable(tbl_frame, columns=cols)
                tbl.pack(fill="both", expand=True, padx=15, pady=(0, 12))
                rows = [tuple(str(hi[c].iloc[i]) for c in cols)
                        for i in range(min(200, len(hi)))]
                tbl.load(rows)
        else:
            ctk.CTkLabel(tbl_frame, text="No churn data available — Model not trained",
                         font=F_BODY, text_color=TEXT_MUTED).pack(padx=14, pady=30)

    def _draw_risk_dist(self, card, kpi):
        ax = card.ax; ax.clear()
        labels = ["High","Medium","Low"]
        vals   = [kpi.high_risk, kpi.medium_risk, kpi.low_risk]
        if sum(vals) > 0:
            ax.pie(vals, labels=labels, autopct="%1.1f%%",
                   colors=[DANGER, WARNING, SUCCESS], startangle=90,
                   wedgeprops={"width":0.6,"edgecolor":BG_CARD,"linewidth":2})
            ax.set_facecolor(BG_CARD)
        card.refresh()

    def _draw_churn_hist(self, card, churn):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not churn.empty and "churn_score" in churn.columns:
            ax.hist(churn["churn_score"].dropna(), bins=30,
                    color=ACCENT_PURP, alpha=0.75, edgecolor=BG_CARD, linewidth=0.5)
            ax.axvline(churn["churn_score"].mean(), color=WARNING,
                       linestyle="--", linewidth=2, label="Mean")
            ax.set_xlabel("Churn Score", fontsize=9, color=TEXT_SEC)
            ax.set_ylabel("Count", fontsize=9, color=TEXT_SEC)
            ax.legend(fontsize=8, facecolor=BG_CARD2, labelcolor=TEXT_PRI, framealpha=0.9)
            ax.grid(alpha=0.12, linestyle='--')
        else:
            ax.text(0.5,0.5,"No churn score data",ha="center",va="center",
                    color=TEXT_SEC, fontsize=10, transform=ax.transAxes)
        card.refresh()
