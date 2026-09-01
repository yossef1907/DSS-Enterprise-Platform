"""DSS Pro — Dynamic Product Tester Page."""
import customtkinter as ctk
import numpy as np
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSEngine as Calc

class TesterPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        # ── LEFT PANEL: Inputs ──────────────────────────────────────────────
        self.left = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self._build_inputs()
        
        # ── RIGHT PANEL: Results ─────────────────────────────────────────────
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self._build_placeholder()

    def _build_inputs(self):
        p = self.left
        # Section A
        ctk.CTkLabel(p, text="📦 Product Info", font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.name_ent = ctk.CTkEntry(p, placeholder_text="Product Name", fg_color=BG_CARD2)
        self.name_ent.pack(fill="x", padx=15, pady=2)
        self.cat_drop = ctk.CTkComboBox(p, values=["Electronics", "Home & Garden", "Clothing", "Home Appliances"], fg_color=BG_CARD2)
        self.cat_drop.pack(fill="x", padx=15, pady=2)
        
        # Section B
        ctk.CTkLabel(p, text="💰 Pricing Strategy", font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.price_ent = ctk.CTkEntry(p, placeholder_text="Unit Price ($)", fg_color=BG_CARD2)
        self.price_ent.insert(0, "99.99")
        self.price_ent.pack(fill="x", padx=15, pady=2)
        
        self.disc_lbl = ctk.CTkLabel(p, text="Discount: 10%", font=F_CAP)
        self.disc_lbl.pack(anchor="w", padx=15)
        self.disc_sl = ctk.CTkSlider(p, from_=0, to=70, number_of_steps=70, command=self._update_calcs)
        self.disc_sl.set(10)
        self.disc_sl.pack(fill="x", padx=15, pady=2)
        
        # Section C
        ctk.CTkLabel(p, text="📣 Marketing", font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.budget_ent = ctk.CTkEntry(p, placeholder_text="Budget ($)", fg_color=BG_CARD2)
        self.budget_ent.insert(0, "5000")
        self.budget_ent.pack(fill="x", padx=15, pady=2)
        
        # Section D
        ctk.CTkLabel(p, text="🎯 Target Market", font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.qty_ent = ctk.CTkEntry(p, placeholder_text="Expected Quantity", fg_color=BG_CARD2)
        self.qty_ent.insert(0, "1000")
        self.qty_ent.pack(fill="x", padx=15, pady=2)
        
        # Buttons
        ctk.CTkButton(p, text="🚀 ANALYZE PRODUCT", fg_color=SUCCESS, font=F_CTITLE, command=self._run_analysis).pack(fill="x", padx=15, pady=(20, 5))
        ctk.CTkButton(p, text="📊 RUN ALL 2,400 SCENARIOS", fg_color=ACCENT_PURP, command=self._run_batch).pack(fill="x", padx=15, pady=5)

    def _build_placeholder(self):
        for w in self.right.winfo_children(): w.destroy()
        ctk.CTkLabel(self.right, text="👈 Configure product and click Analyze", font=F_TITLE, text_color=TEXT_SEC).pack(expand=True)

    def _update_calcs(self, _=None):
        disc = int(self.disc_sl.get())
        self.disc_lbl.configure(text=f"Discount: {disc}%")

    def _run_analysis(self):
        for w in self.right.winfo_children(): w.destroy()
        
        # Get inputs
        try:
            price = float(self.price_ent.get())
            disc = self.disc_sl.get()
            budget = float(self.budget_ent.get())
            qty = int(self.qty_ent.get())
        except: return
        
        # Calcs
        rev = Calc.expected_revenue(price, disc, qty)
        cost = budget # Simplified
        profit = rev - cost
        margin = Calc.profit_margin(profit, rev)
        roi = Calc.roi(rev, cost)
        be_units = Calc.break_even_units(cost, price * (1 - disc/100), 0)
        
        # Dummy prob for demo
        prob = np.random.uniform(30, 99)
        
        # 1. Verdict Banner
        v_color = SUCCESS if prob > 70 else (WARNING if prob > 40 else DANGER)
        v_text = "✅ GO FOR LAUNCH" if prob > 70 else ("⚠️ REVIEW NEEDED" if prob > 40 else "❌ DO NOT LAUNCH")
        banner = ctk.CTkFrame(self.right, fg_color=v_color, corner_radius=10)
        banner.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(banner, text=v_text, font=F_TITLE, text_color=TEXT_PRI).pack(pady=10)
        
        # 2. Gauge & KPIs
        top = ctk.CTkFrame(self.right, fg_color="transparent")
        top.pack(fill="x")
        
        gauge = GaugeWidget(top, "Success Probability", width=250)
        gauge.pack(side="left", padx=(0, 10))
        gauge.set_value(prob, color=v_color)
        
        kf = ctk.CTkFrame(top, fg_color="transparent")
        kf.pack(side="left", fill="both", expand=True)
        kf.columnconfigure((0,1), weight=1)
        
        KPICard(kf, "💰", "Exp. Revenue", fmt_money(rev), accent=SUCCESS).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "📈", "ROI", f"{roi:.1f}%", accent=WARNING).grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "📊", "Margin", f"{margin:.1f}%", accent=ACCENT_BLUE).grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "🔄", "Break Even", f"{int(be_units)} units", accent=ACCENT_PURP).grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        # 3. Sensitivity Chart
        c1 = ChartCard(self.right, "Sensitivity: Success vs Discount")
        c1.pack(fill="x", pady=10)
        x = np.linspace(0, 70, 20)
        y = 99 - (x - 50)**2 / 50 # Example curve peaking at 50%
        c1.ax.plot(x, y, color=ACCENT_BLUE, linewidth=3)
        c1.ax.scatter([disc], [99 - (disc - 50)**2 / 50], color=DANGER, s=100, zorder=5)
        c1.refresh()

    def _run_batch(self):
        # In real app, loop all combos and show top 5
        self._run_analysis()
        res = ctk.CTkFrame(self.right, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        res.pack(fill="x", pady=10)
        ctk.CTkLabel(res, text="🏆 TOP 5 SCENARIOS FOUND", font=F_CTITLE, text_color=ACCENT_BLUE).pack(pady=10)
        tbl = DSSTable(res, ["Rank", "Discount", "Season", "Region", "Score", "Verdict"])
        tbl.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tbl.load([
            ["1", "50%", "Fall", "Amman", "99.5%", "✅ GO"],
            ["2", "40%", "Fall", "Kuwait", "95.2%", "✅ GO"],
            ["3", "60%", "Fall", "Dubai", "91.8%", "✅ GO"],
        ])
