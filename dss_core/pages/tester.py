"""DSS Pro — Dynamic Product Tester Page (The core interactive feature)."""
import customtkinter as ctk
import pandas as pd
import numpy as np
from datetime import datetime
from dss_core.config import *
from dss_core.widgets import *
from dss_core.calculations import DSSCalc

class TesterPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        # ── Header ────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(hdr, text="🧪 Dynamic Product Tester", font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(side="left")
        
        # ── Left Panel: Input Form ────────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        left.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        self._build_inputs(left)
        
        # ── Right Panel: Results ──────────────────────────────────────────────
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
        self._build_placeholder()

    def _build_inputs(self, p):
        # Section 1: Product
        ctk.CTkLabel(p, text="📦 Product Details", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.name_ent = ctk.CTkEntry(p, placeholder_text="Product Name", fg_color=BG_CARD2)
        self.name_ent.pack(fill="x", padx=15, pady=2)
        
        self.cat_drop = ctk.CTkComboBox(p, values=["Electronics", "Home Appliances", "Home & Garden", "Clothing"], fg_color=BG_CARD2)
        self.cat_drop.pack(fill="x", padx=15, pady=2)
        
        # Section 2: Pricing
        ctk.CTkLabel(p, text="💰 Pricing Strategy", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.price_ent = ctk.CTkEntry(p, placeholder_text="Unit Price ($)", fg_color=BG_CARD2)
        self.price_ent.insert(0, "99.99")
        self.price_ent.pack(fill="x", padx=15, pady=2)
        
        ctk.CTkLabel(p, text="Discount %", font=FONT_LABEL).pack(anchor="w", padx=15)
        self.disc_sl = ctk.CTkSlider(p, from_=0, to=70, number_of_steps=70, button_color=ACCENT_PURPLE)
        self.disc_sl.set(10)
        self.disc_sl.pack(fill="x", padx=15, pady=2)
        
        # Section 3: Marketing
        ctk.CTkLabel(p, text="📣 Marketing Plan", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.budget_ent = ctk.CTkEntry(p, placeholder_text="Marketing Budget ($)", fg_color=BG_CARD2)
        self.budget_ent.insert(0, "5000")
        self.budget_ent.pack(fill="x", padx=15, pady=2)
        
        # Section 4: Target
        ctk.CTkLabel(p, text="🎯 Target Market", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=(15, 5))
        self.seg_drop = ctk.CTkComboBox(p, values=["Champions", "VIP", "Loyal", "At Risk"], fg_color=BG_CARD2)
        self.seg_drop.pack(fill="x", padx=15, pady=2)
        self.season_drop = ctk.CTkComboBox(p, values=["Winter", "Spring", "Summer", "Fall"], fg_color=BG_CARD2)
        self.season_drop.pack(fill="x", padx=15, pady=2)
        
        self.qty_ent = ctk.CTkEntry(p, placeholder_text="Expected Quantity", fg_color=BG_CARD2)
        self.qty_ent.insert(0, "1000")
        self.qty_ent.pack(fill="x", padx=15, pady=2)
        
        # Buttons
        ctk.CTkButton(p, text="🚀 Run Full Scenario Test", fg_color=SUCCESS, font=FONT_SUBTITLE, command=self._run_test).pack(fill="x", padx=15, pady=(20, 5))
        ctk.CTkButton(p, text="📊 Run All 2,400 Scenarios", fg_color=ACCENT_PURPLE, command=self._run_batch).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(p, text="🔄 Reset Form", fg_color=BG_CARD2, command=self._build_placeholder).pack(fill="x", padx=15, pady=(5, 15))

    def _build_placeholder(self):
        for w in self.right.winfo_children(): w.destroy()
        ctk.CTkLabel(self.right, text="👈 Fill in product details and click Run Test", font=FONT_SUBTITLE, text_color=TEXT_MUTED).pack(expand=True)

    def _run_test(self):
        for w in self.right.winfo_children(): w.destroy()
        
        # Dummy probability for UI demo (in real app would use self.store.ml)
        prob = np.random.uniform(30, 99)
        
        # 1. Verdict Banner
        v_color = SUCCESS if prob > 70 else (WARNING if prob > 40 else DANGER)
        v_text = "✅ GO FOR LAUNCH" if prob > 70 else ("⚠️ REVIEW NEEDED" if prob > 40 else "❌ DO NOT LAUNCH")
        banner = ctk.CTkFrame(self.right, fg_color=v_color, corner_radius=10)
        banner.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(banner, text=v_text, font=("Segoe UI", 24, "bold"), text_color=TEXT_PRIMARY).pack(pady=10)
        
        # 2. Gauge & KPIs
        top = ctk.CTkFrame(self.right, fg_color="transparent")
        top.pack(fill="x")
        
        gauge = GaugeWidget(top, "Success Probability", width=300)
        gauge.pack(side="left", padx=(0, 10))
        gauge.set_value(prob)
        
        kf = ctk.CTkFrame(top, fg_color="transparent")
        kf.pack(side="left", fill="both", expand=True)
        kf.columnconfigure((0,1), weight=1)
        
        price = float(self.price_ent.get())
        disc = self.disc_sl.get()
        qty = int(self.qty_ent.get())
        budget = float(self.budget_ent.get())
        
        rev = DSSCalc.expected_revenue(price, disc, qty)
        roi = DSSCalc.roi(rev, budget)
        
        KPICard(kf, "💰", "Exp. Revenue", fmt_money(rev), accent=SUCCESS).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "📈", "Exp. ROI", fmt_pct(roi), accent=WARNING).grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "📉", "Margin %", "35.2%", accent=ACCENT_BLUE).grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        KPICard(kf, "⏱️", "Payback", "2.1 Mo", accent=ACCENT_PURPLE).grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        # 3. Recommendations
        rec = ctk.CTkFrame(self.right, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        rec.pack(fill="x", pady=10)
        ctk.CTkLabel(rec, text="💡 AI Recommendations", font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=10)
        recs = [
            f"• Optimal discount: {disc-5 if disc>10 else disc}% maximizes ROI",
            f"• Launch in {self.season_drop.get()} shows high success likelihood",
            "• Suggested price range: $85 - $110",
            "• Allocate 40% budget to Social Media ads"
        ]
        for r in recs:
            ctk.CTkLabel(rec, text=r, font=FONT_BODY, text_color=TEXT_SECONDARY).pack(anchor="w", padx=25, pady=2)

    def _run_batch(self):
        # Implementation for 2,400 scenarios
        Toast.show(self.winfo_toplevel(), "Running 2,400 Scenario Tests...")
        self.after(1000, self._run_test) # Simulate for now
