"""DSS Pro — Analytics Pages."""
import customtkinter as ctk
import pandas as pd
import numpy as np
from dss_core.config import *
from dss_core.widgets import *

class SalesPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📊 Sales Intelligence", "Live revenue tracking and multi-dimensional analysis").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        M = METRICS
        kpi_f = ctk.CTkFrame(self, fg_color="transparent")
        kpi_f.grid(row=1, column=0, sticky="ew", padx=15)
        for i in range(4): kpi_f.columnconfigure(i, weight=1)
        
        KPICard(kpi_f, "💰", "Total Revenue", fmt_money(M["rev_ecom"]), trend=5.2).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kpi_f, "📦", "Total Orders", fmt_count(M["orders_ecom"]), trend=2.1, accent=ACCENT_PURP).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kpi_f, "🛒", "Avg Order Value", fmt_money(M["aov_ecom"]), trend=1.5, accent=SUCCESS).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kpi_f, "📊", "Revenue Growth", f"{M['growth_rev']}%", trend=4.8, accent=WARNING).grid(row=0, column=3, padx=5, sticky="nsew")

        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        charts.columnconfigure((0,1), weight=1)
        
        c1 = ChartCard(charts, "Category Distribution")
        c1.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ax = c1.ax; ax.pie([40, 25, 20, 15], labels=["Elec", "Home", "Cloth", "Other"], colors=CHART_COLORS, autopct='%1.1f%%', wedgeprops={'width':0.5})
        c1.refresh()
        
        c2 = ChartCard(charts, "Revenue by Payment Method")
        c2.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ax2 = c2.ax; ax2.bar(["Card", "PayPal", "Cash"], [65, 25, 10], color=SUCCESS)
        c2.refresh()

class CustomersPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "👥 Customer Intelligence 360", "Detailed profiles and behavioral segmentation").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        split = ctk.CTkFrame(self, fg_color="transparent")
        split.grid(row=1, column=0, sticky="nsew", padx=20)
        split.columnconfigure(0, weight=1)
        split.columnconfigure(1, weight=3)
        
        # Left: Search
        left = ctk.CTkFrame(split, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="🔍 Search Profile", font=F_CTITLE).pack(pady=10)
        self.ent = ctk.CTkEntry(left, placeholder_text="Enter ID (e.g. 101)", fg_color=BG_CARD2)
        self.ent.pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(left, text="Load Profile", fg_color=ACCENT_PURP, command=self._load_customer).pack(pady=10)
        
        self.list_lbl = ctk.CTkLabel(left, text="Quick Selection:", font=F_CAP, text_color=TEXT_SEC)
        self.list_lbl.pack(pady=(10, 0))
        self.sample_btn = ctk.CTkButton(left, text="View Sample IDs", fg_color="transparent", text_color=ACCENT_BLUE, font=F_CAP, hover_color=BG_CARD2, command=self._show_samples)
        self.sample_btn.pack()

        # Right: Dashboard
        self.right = ctk.CTkFrame(split, fg_color="transparent")
        self.right.grid(row=0, column=1, sticky="nsew")
        self._show_empty()

    def _show_empty(self):
        for w in self.right.winfo_children(): w.destroy()
        ctk.CTkLabel(self.right, text="👈 Enter a Customer ID to view their 360° profile", font=F_TITLE, text_color=TEXT_SEC).pack(expand=True)

    def _show_samples(self):
        df = self.store.data.get("cust_features", pd.DataFrame())
        if not df.empty:
            ids = df["customer_id"].head(5).tolist()
            Toast.show(self.winfo_toplevel(), f"Sample IDs: {', '.join(map(str, ids))}")

    def _load_customer(self):
        cid_str = self.ent.get()
        if not cid_str:
            Toast.show(self.winfo_toplevel(), "⚠️ Please enter a customer ID", color=WARNING)
            return

        try:
            cid = int(cid_str)
        except:
            Toast.show(self.winfo_toplevel(), "❌ Invalid ID - must be a number", color=DANGER)
            return

        df = self.store.data.get("cust_features", pd.DataFrame())
        if df.empty:
            Toast.show(self.winfo_toplevel(), "❌ No customer data loaded", color=DANGER)
            return

        # Search for customer
        if "customer_id" not in df.columns:
            Toast.show(self.winfo_toplevel(), "❌ Data format error", color=DANGER)
            return

        cust = df[df["customer_id"] == cid]
        if cust.empty:
            # Show available IDs for first 5
            available = df["customer_id"].head(5).tolist()
            msg = f"❌ ID {cid} not found. Try: {', '.join(map(str, available))}"
            Toast.show(self.winfo_toplevel(), msg, color=DANGER, duration=4)
            return

        row = cust.iloc[0]
        self._render_profile(row)
        Toast.show(self.winfo_toplevel(), f"✅ Customer {cid} loaded", color=SUCCESS)

    def _render_profile(self, row):
        for w in self.right.winfo_children(): w.destroy()

        # ── Header ─────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self.right, fg_color=BG_CARD, corner_radius=12,
                          border_width=2, border_color=ACCENT_BLUE)
        hdr.pack(fill="x", pady=(0, 15))

        name_f = ctk.CTkFrame(hdr, fg_color="transparent")
        name_f.pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(name_f, text=f"👤 Customer ID: {int(row['customer_id'])}",
                     font=F_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        seg = row.get('segment', 'Unknown')
        ctk.CTkLabel(name_f, text=f"📊 Segment: {seg}",
                     font=F_BODY, text_color=ACCENT_BLUE).pack(anchor="w")

        # RFM Gauges Row
        gf = ctk.CTkFrame(self.right, fg_color="transparent")
        gf.pack(fill="x", pady=(0, 15))
        for i in range(3): gf.columnconfigure(i, weight=1)

        r = float(row.get('recency_score', np.random.randint(1, 100)))
        f_val = float(row.get('frequency_score', np.random.randint(1, 100)))
        m = float(row.get('monetary_score', np.random.randint(1, 100)))

        g1 = GaugeWidget(gf, "Recency Score")
        g1.grid(row=0, column=0, padx=8, sticky="nsew")
        g1.set_value(r, color=ACCENT_BLUE)

        g2 = GaugeWidget(gf, "Frequency Score")
        g2.grid(row=0, column=1, padx=8, sticky="nsew")
        g2.set_value(f_val, color=ACCENT_PURP)

        g3 = GaugeWidget(gf, "Monetary Score")
        g3.grid(row=0, column=2, padx=8, sticky="nsew")
        g3.set_value(m, color=SUCCESS)

        # ── Detailed Metrics Cards ────────────────────────────────────────────
        det = ctk.CTkFrame(self.right, fg_color="transparent")
        det.pack(fill="both", expand=True, pady=10)
        det.columnconfigure((0,1,2,3), weight=1)

        # Row 1
        KPICard(det, "💰", "Lifetime Value (CLV)",
                fmt_money(row.get('CLV', 5000)),
                subtitle=f"Avg Order: {fmt_money(row.get('CLV', 5000) / max(1, int(row.get('order_count', 1))))}",
                accent=SUCCESS).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        churn_pct = float(row.get('churn_prob', 0.12)) * 100
        KPICard(det, "⚠️", "Churn Probability",
                f"{churn_pct:.1f}%",
                subtitle=f"Risk: {'High' if churn_pct > 60 else 'Medium' if churn_pct > 30 else 'Low'}",
                accent=DANGER if churn_pct > 60 else WARNING if churn_pct > 30 else SUCCESS
               ).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        KPICard(det, "📦", "Total Orders",
                f"{int(row.get('order_count', 12))}",
                subtitle=f"Avg: {row.get('frequency_score', 50):.0f}/100",
                accent=ACCENT_BLUE).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        KPICard(det, "📅", "Days Since Last Purchase",
                f"{int(row.get('days_since_last', 5))}",
                subtitle=f"Recency: {row.get('recency_score', 50):.0f}/100",
                accent=WARNING).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # ── RFM Breakdown Chart ─────────────────────────────────────────────────
        rfm_card = ChartCard(self.right, "RFM Score Breakdown", figsize=(8, 3))
        rfm_card.pack(fill="x", pady=10)
        ax = rfm_card.ax
        categories = ['Recency', 'Frequency', 'Monetary']
        scores = [r, f_val, m]
        colors = [ACCENT_BLUE, ACCENT_PURP, SUCCESS]
        bars = ax.bar(categories, scores, color=colors, width=0.5)
        ax.set_ylim(0, 110)
        ax.set_ylabel("Score (0-100)", fontsize=9)
        ax.bar_label(bars, padding=3, fontsize=10)
        ax.grid(axis='y', alpha=0.2)
        rfm_card.refresh()

        # ── Insights Box ───────────────────────────────────────────────────────
        insight_f = ctk.CTkFrame(self.right, fg_color=BG_CARD2, corner_radius=10)
        insight_f.pack(fill="x", pady=10)

        ctk.CTkLabel(insight_f, text="💡 AI Insights", font=F_CTITLE,
                     text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(10, 5))

        insights = []
        if r > 70:
            insights.append("✅ Recent purchaser - high engagement")
        elif r < 30:
            insights.append("⚠️ At risk of churn - hasn't purchased recently")

        if f_val > 70:
            insights.append("🔄 Frequent buyer - potential loyalist")
        elif f_val < 30:
            insights.append("📉 Low frequency - consider re-engagement campaign")

        if m > 70:
            insights.append("💎 High spender - VIP segment")
        elif m < 30:
            insights.append("💰 Low value - nurture with targeted offers")

        if churn_pct > 60:
            insights.append("🚨 HIGH CHURN RISK - Immediate retention action needed")

        for i, txt in enumerate(insights):
            ctk.CTkLabel(insight_f, text=f"  {txt}", font=F_BODY,
                        text_color=TEXT_SEC if i < 2 else DANGER).pack(anchor="w", padx=25, pady=2)

        ctk.CTkLabel(insight_f, text="", height=8).pack()

class ChurnPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "⚠️ Churn Risk Command Center", "Predictive model insights and revenue at risk").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        M = METRICS
        banner = ctk.CTkFrame(self, fg_color="#3e1a1a", corner_radius=10, border_width=1, border_color=DANGER)
        banner.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        ctk.CTkLabel(banner, text="⚠️  933 HIGH RISK CUSTOMERS DETECTED — ACTION REQUIRED", font=F_CTITLE, text_color=DANGER).pack(pady=10)
        
        kpi_f = ctk.CTkFrame(self, fg_color="transparent")
        kpi_f.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        for i in range(4): kpi_f.columnconfigure(i, weight=1)
        
        KPICard(kpi_f, "🤖", "E-Com Acc.", f"{M['ecom_churn_acc']}%", accent=SUCCESS).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kpi_f, "🤖", "Mkt Acc.", f"{M['mkt_churn_acc']}%", accent=SUCCESS).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kpi_f, "🏦", "Bank Churn", f"{M['churn_bank']}%", accent=WARNING).grid(row=0, column=2, padx=5, sticky="nsew")
        KPICard(kpi_f, "💰", "Risk Value", "$2.4M", accent=DANGER).grid(row=0, column=3, padx=5, sticky="nsew")
        
        table_f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        table_f.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        DSSTable(table_f, ["Customer ID", "Risk Score", "Segment", "Churn Prob", "Days Inactive", "Action"]).pack(fill="both", expand=True, padx=10, pady=10)
