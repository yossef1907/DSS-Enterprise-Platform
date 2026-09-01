"""Pages 5, 6, 7 – Market Basket, Campaign ROI, Product Launch."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import customtkinter as ctk

from dss_core.config import (
    BG_MAIN, BG_CARD, BG_CARD2, BORDER, BORDER2,
    ACCENT_BLUE, ACCENT_PURPLE, SUCCESS, WARNING, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    CHART_COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_CAPTION, FONT_LABEL,
)
from dss_core.widgets import (
    KPICard, ChartCard, DSSTable, GaugeWidget,
    ScrollablePage, fmt_money, fmt_pct, fmt_count,
)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 – Market Basket Intelligence
# ─────────────────────────────────────────────────────────────────────────────
class BasketPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        kpi = self.store.kpi
        mb  = self.store.powerbi.get("market_basket", pd.DataFrame())

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="🛒  Market Basket Intelligence",
                     font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Association rules, product bundles, and cross-sell opportunities",
                     font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        ks = ctk.CTkFrame(self, fg_color="transparent")
        ks.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        for i in range(5): ks.columnconfigure(i, weight=1)
        for i, (icon, title, val, acc) in enumerate([
            ("📏", "Total Rules",    fmt_count(kpi.total_rules),      ACCENT_BLUE),
            ("🎯", "Max Confidence", fmt_pct(kpi.max_confidence),      ACCENT_PURPLE),
            ("🚀", "Max Lift",       f"{kpi.max_lift:.2f}",            SUCCESS),
            ("📊", "Max Support",    fmt_pct(kpi.max_support),         WARNING),
            ("🛒", "Avg Basket",     f"{kpi.basket_size:.2f} items",   ACCENT_BLUE),
        ]):
            KPICard(ks, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, pady=4, ipady=6)

        # Charts
        cr = ctk.CTkFrame(self, fg_color="transparent")
        cr.grid(row=2, column=0, sticky="nsew", padx=20, pady=4)
        cr.columnconfigure((0,1), weight=1)

        top_card = self._add_chart(ChartCard(cr, "🏆  Top Rules by Lift", figsize=(7,4)))
        top_card.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        self._draw_top_rules(top_card, mb)

        sc_card = self._add_chart(ChartCard(cr, "🔵  Support vs Confidence", figsize=(6,4)))
        sc_card.grid(row=0, column=1, sticky="nsew", padx=(4,0))
        self._draw_scatter(sc_card, mb)

        # Rules table
        tbl_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                                  border_width=1, border_color=BORDER)
        tbl_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(4,20))
        ctk.CTkLabel(tbl_frame, text="📋  Association Rules",
                     font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        cols = ["antecedents_str","consequents_str","support","confidence","lift"]
        cols = [c for c in cols if c in mb.columns]
        tbl  = DSSTable(tbl_frame, columns=cols)
        tbl.pack(fill="both", expand=True, padx=10, pady=(0,10))
        if not mb.empty:
            top = mb.nlargest(100, "lift") if "lift" in mb.columns else mb.head(100)
            rows = [tuple(
                f"{top[c].iloc[i]:.4f}" if mb[c].dtype in [float,int]
                else str(top[c].iloc[i]) for c in cols
            ) for i in range(len(top))]
            tbl.load(rows)

    def _draw_top_rules(self, card, mb):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not mb.empty and "lift" in mb.columns:
            top = mb.nlargest(12,"lift")
            labels = [
                f"{str(row.get('antecedents_str',''))[:15]}→{str(row.get('consequents_str',''))[:12]}"
                for _, row in top.iterrows()
            ]
            ax.barh(range(len(top)), top["lift"].values,
                    color=CHART_COLORS[:len(top)], height=0.7)
            ax.set_yticks(range(len(top))); ax.set_yticklabels(labels, fontsize=8)
            ax.set_xlabel("Lift", color=TEXT_SECONDARY, fontsize=9)
            ax.axvline(1, color=BORDER2, linestyle="--", linewidth=1)
        ax.grid(axis="x", alpha=0.2); card.refresh()

    def _draw_scatter(self, card, mb):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not mb.empty and all(c in mb.columns for c in ["support","confidence","lift"]):
            sc = ax.scatter(mb["support"], mb["confidence"],
                            c=mb["lift"], cmap="plasma", s=30, alpha=0.7)
            card.fig.colorbar(sc, ax=ax, label="Lift", fraction=0.04)
            ax.set_xlabel("Support",    color=TEXT_SECONDARY, fontsize=9)
            ax.set_ylabel("Confidence", color=TEXT_SECONDARY, fontsize=9)
        ax.grid(alpha=0.15); card.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 – Campaign ROI Intelligence
# ─────────────────────────────────────────────────────────────────────────────
class CampaignPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        kpi  = self.store.kpi
        roi  = self.store.powerbi.get("roi",        pd.DataFrame())
        roreg= self.store.powerbi.get("roi_region", pd.DataFrame())
        mkt  = self.store.mkt_df

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="📣  Campaign ROI Intelligence",
                     font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="Marketing performance, channel ROI, and budget analysis",
                     font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        ks = ctk.CTkFrame(self, fg_color="transparent")
        ks.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        for i in range(6): ks.columnconfigure(i, weight=1)
        roas = (kpi.total_mkt_revenue / max(kpi.total_budget, 1))
        cpa  = (kpi.total_budget / max(kpi.total_orders, 1))
        for i,(icon,title,val,acc) in enumerate([
            ("💰","Total Budget",    fmt_money(kpi.total_budget),      ACCENT_BLUE),
            ("💵","Revenue",         fmt_money(kpi.total_mkt_revenue), SUCCESS),
            ("📈","Overall ROI",     fmt_pct(kpi.overall_roi),         WARNING),
            ("🏆","Best Channel",    str(kpi.best_channel),            ACCENT_PURPLE),
            ("📡","ROAS",            f"{roas:.2f}x",                   ACCENT_BLUE),
            ("🎯","CPA",             fmt_money(cpa),                   DANGER),
        ]):
            KPICard(ks, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, pady=4, ipady=6)

        cr = ctk.CTkFrame(self, fg_color="transparent")
        cr.grid(row=2, column=0, sticky="nsew", padx=20, pady=4)
        cr.columnconfigure((0,1), weight=1)

        rc = self._add_chart(ChartCard(cr, "📊  ROI by Channel", figsize=(7,4)))
        rc.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        self._draw_channel_roi(rc, roi)

        rrc = self._add_chart(ChartCard(cr, "🗺️  ROI by Region", figsize=(6,4)))
        rrc.grid(row=0, column=1, sticky="nsew", padx=(4,0))
        self._draw_region_roi(rrc, roreg)

        # Budget vs Revenue bubble chart
        bub = self._add_chart(ChartCard(self, "🫧  Channel Performance Matrix", figsize=(12,4)))
        bub.grid(row=3, column=0, sticky="nsew", padx=20, pady=4)
        self._draw_bubble(bub, roi)

        # ROI table
        tbl_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                                  border_width=1, border_color=BORDER)
        tbl_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(4,20))
        ctk.CTkLabel(tbl_frame, text="📋  Channel Details",
                     font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        cols = [c for c in ["sales_channel","total_budget","total_revenue","roi","profit","avg_conversion","total_orders"]
                if c in roi.columns]
        if cols:
            tbl = DSSTable(tbl_frame, columns=cols)
            tbl.pack(fill="both", expand=True, padx=10, pady=(0,10))
            rows = [tuple(
                f"${roi[c].iloc[i]:,.2f}" if c in ["total_budget","total_revenue","profit"]
                else (f"{roi[c].iloc[i]:.2f}%" if c in ["roi","avg_conversion"]
                      else str(roi[c].iloc[i]))
                for c in cols
            ) for i in range(len(roi))]
            tbl.load(rows)

    def _draw_channel_roi(self, card, roi):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not roi.empty and "sales_channel" in roi.columns and "roi" in roi.columns:
            colors = [SUCCESS if v > 0 else DANGER for v in roi["roi"]]
            ax.bar(roi["sales_channel"], roi["roi"], color=colors, width=0.6)
            ax.axhline(0, color=BORDER2, linewidth=1)
            ax.set_ylabel("ROI %", color=TEXT_SECONDARY, fontsize=9)
            ax.tick_params(axis="x", rotation=15, labelsize=9)
        ax.grid(axis="y", alpha=0.2); card.refresh()

    def _draw_region_roi(self, card, roreg):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not roreg.empty and "region" in roreg.columns and "roi" in roreg.columns:
            colors = CHART_COLORS[:len(roreg)]
            ax.bar(roreg["region"], roreg["roi"], color=colors, width=0.6)
            ax.set_ylabel("ROI %", color=TEXT_SECONDARY, fontsize=9)
            ax.tick_params(axis="x", rotation=15, labelsize=9)
        ax.grid(axis="y", alpha=0.2); card.refresh()

    def _draw_bubble(self, card, roi):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not roi.empty and all(c in roi.columns for c in ["total_budget","total_revenue"]):
            sizes  = roi.get("total_orders", pd.Series([100]*len(roi))) * 0.5
            colors = CHART_COLORS[:len(roi)]
            ax.scatter(roi["total_budget"], roi["total_revenue"],
                       s=sizes.clip(50,800), c=colors, alpha=0.85, edgecolors=BG_CARD, linewidth=2)
            for i, row in roi.iterrows():
                ax.annotate(str(row.get("sales_channel",""))[:10],
                            (row["total_budget"], row["total_revenue"]),
                            fontsize=8, color=TEXT_PRIMARY, ha="center", va="bottom")
            ax.set_xlabel("Budget ($)", color=TEXT_SECONDARY, fontsize=9)
            ax.set_ylabel("Revenue ($)", color=TEXT_SECONDARY, fontsize=9)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v/1e3:.0f}K"))
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v/1e6:.1f}M"))
        ax.grid(alpha=0.15); card.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 – Product Launch Command Center
# ─────────────────────────────────────────────────────────────────────────────
class ProductLaunchPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        pl = self.store.powerbi.get("product_launch", pd.DataFrame())
        if pl.empty:
            pl = self.store.sim_df

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,8))
        ctk.CTkLabel(hdr, text="🚀  Product Launch Command Center",
                     font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(hdr, text="GO / NO-GO decisions, success rates, and launch intelligence",
                     font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w")

        go_count   = len(pl[pl["decision"]=="GO"])   if not pl.empty and "decision" in pl.columns else 0
        nogo_count = len(pl[pl["decision"]=="NO-GO"]) if not pl.empty and "decision" in pl.columns else 0
        avg_succ   = pl["success_prob"].mean() if not pl.empty and "success_prob" in pl.columns else 0
        best_cat   = (pl.groupby("product_category")["success_prob"].mean().idxmax()
                     if not pl.empty and "product_category" in pl.columns and "success_prob" in pl.columns
                     else "N/A")
        best_seas  = (pl.groupby("season")["success_prob"].mean().idxmax()
                     if not pl.empty and "season" in pl.columns and "success_prob" in pl.columns
                     else "N/A")

        ks = ctk.CTkFrame(self, fg_color="transparent")
        ks.grid(row=1, column=0, sticky="ew", padx=20, pady=4)
        for i in range(5): ks.columnconfigure(i, weight=1)
        for i,(icon,title,val,acc) in enumerate([
            ("✅","Total GO",       fmt_count(go_count),   SUCCESS),
            ("❌","Total NO-GO",    fmt_count(nogo_count),  DANGER),
            ("📊","Avg Success",    fmt_pct(avg_succ),      ACCENT_BLUE),
            ("🏆","Best Category",  str(best_cat),          ACCENT_PURPLE),
            ("🗓️","Best Season",    str(best_seas),         WARNING),
        ]):
            KPICard(ks, icon=icon, title=title, value=val, accent=acc).grid(
                row=0, column=i, sticky="nsew", padx=4, pady=4, ipady=6)

        cr = ctk.CTkFrame(self, fg_color="transparent")
        cr.grid(row=2, column=0, sticky="nsew", padx=20, pady=4)
        cr.columnconfigure((0,1,2), weight=1)

        donut = self._add_chart(ChartCard(cr, "🍩  GO vs NO-GO", figsize=(5,4)))
        donut.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        self._draw_go_nogo(donut, go_count, nogo_count)

        cat_card = self._add_chart(ChartCard(cr, "📦  Success by Category", figsize=(6,4)))
        cat_card.grid(row=0, column=1, sticky="nsew", padx=4)
        self._draw_cat_success(cat_card, pl)

        seas_card = self._add_chart(ChartCard(cr, "🗓️  Success by Season", figsize=(5,4)))
        seas_card.grid(row=0, column=2, sticky="nsew", padx=(4,0))
        self._draw_season_success(seas_card, pl)

        # Heatmap
        hmap = self._add_chart(ChartCard(self, "🌡️  Category × Season Heatmap", figsize=(12,4)))
        hmap.grid(row=3, column=0, sticky="nsew", padx=20, pady=4)
        self._draw_heatmap(hmap, pl)

        # Table
        tbl_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15,
                                  border_width=1, border_color=BORDER)
        tbl_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(4,20))
        ctk.CTkLabel(tbl_frame, text="📋  All Simulations",
                     font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10,4))
        cols = [c for c in ["product_category","unit_price","discount_pct","season","city","success_prob","decision"]
                if not pl.empty and c in pl.columns]
        if cols:
            tbl = DSSTable(tbl_frame, columns=cols)
            tbl.pack(fill="both", expand=True, padx=10, pady=(0,10))
            rows = [tuple(str(pl[c].iloc[i]) for c in cols)
                    for i in range(min(200, len(pl)))]
            tbl.load(rows)

    def _draw_go_nogo(self, card, go, nogo):
        ax = card.ax; ax.clear()
        if go + nogo > 0:
            ax.pie([go, nogo], labels=["GO","NO-GO"],
                   colors=[SUCCESS, DANGER], autopct="%1.1f%%",
                   startangle=90, wedgeprops={"width":0.6,"edgecolor":BG_CARD,"linewidth":2})
        card.refresh()

    def _draw_cat_success(self, card, pl):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not pl.empty and "product_category" in pl.columns and "success_prob" in pl.columns:
            g = pl.groupby("product_category")["success_prob"].mean().sort_values(ascending=False)
            ax.barh(range(len(g)), g.values, color=CHART_COLORS[:len(g)], height=0.65)
            ax.set_yticks(range(len(g))); ax.set_yticklabels(g.index, fontsize=8)
            ax.set_xlabel("Avg Success %", color=TEXT_SECONDARY, fontsize=9)
        ax.grid(axis="x", alpha=0.2); card.refresh()

    def _draw_season_success(self, card, pl):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not pl.empty and "season" in pl.columns and "success_prob" in pl.columns:
            g = pl.groupby("season")["success_prob"].mean()
            ax.bar(g.index, g.values, color=CHART_COLORS[:len(g)], width=0.6)
            ax.set_ylabel("Avg Success %", color=TEXT_SECONDARY, fontsize=9)
            ax.tick_params(axis="x", rotation=15, labelsize=9)
        ax.grid(axis="y", alpha=0.2); card.refresh()

    def _draw_heatmap(self, card, pl):
        ax = card.ax; ax.clear(); ax.set_facecolor(BG_CARD)
        if not pl.empty and "product_category" in pl.columns and "season" in pl.columns:
            pivot = pl.pivot_table(values="success_prob", index="product_category",
                                    columns="season", aggfunc="mean", fill_value=0)
            import matplotlib.colors as mc
            cmap = mc.LinearSegmentedColormap.from_list("succ", [DANGER, WARNING, SUCCESS])
            im = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0, vmax=100)
            ax.set_yticks(range(len(pivot.index)))
            ax.set_yticklabels(pivot.index, fontsize=8)
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_xticklabels(pivot.columns, fontsize=9)
            card.fig.colorbar(im, ax=ax, fraction=0.03, label="Avg Success %")
        ax.grid(False); card.refresh()
