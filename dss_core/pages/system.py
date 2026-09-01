"""DSS Pro — System Pages (Complete Metrics, Reports, Recommendations, Settings)."""
import customtkinter as ctk
import pandas as pd
from dss_core.config import *
from dss_core.widgets import *

class MetricsDetailPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📊 Complete Metrics Display", "All project results in organized detail").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        M = METRICS
        sections = [
            ("🤖 Model Accuracies", [
                ("E-Commerce Churn", f"{M['ecom_churn_acc']}%", "✅ Best"),
                ("Marketing Model", f"{M['mkt_churn_acc']}%", "✅ Best"),
                ("Bank Churn", f"{M['bank_churn_acc']}%", "✅ Good"),
                ("Telco Churn", f"{M['telco_churn_acc']}%", "✅ Good"),
                ("Product Launch", f"{M['launch_model_acc']}%", "✅ Best"),
            ]),
            ("🛒 Market Basket Results", [
                ("Total Rules", M["mb_total_rules"], "N/A"),
                ("Max Confidence", f"{M['mb_max_confidence']}%", "✅✅ Exceptional"),
                ("Max Lift", f"{M['mb_max_lift']}x", "✅✅ Exceptional"),
                ("Max Support", f"{M['mb_max_support']}%", "✅✅ Exceptional"),
            ]),
            ("💰 Revenue & ROI", [
                ("E-Com Revenue", fmt_money(M["ecom_revenue"]), "✅ Good"),
                ("Mkt Rev After", fmt_money(M["mkt_revenue_after"]), "✅✅ Excellent"),
                ("Revenue Growth", f"+{M['revenue_growth_pct']}%", "✅✅ +383.6%"),
                ("Overall ROI", f"+{M['roi_after']}%", "✅✅ Excellent"),
            ])
        ]
        
        for i, (title, rows) in enumerate(sections):
            f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
            f.grid(row=i+1, column=0, sticky="ew", padx=20, pady=10)
            ctk.CTkLabel(f, text=title, font=FONT_SUBTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=10)
            tbl = DSSTable(f, ["Metric", "Value", "Rating"])
            tbl.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            tbl.load(rows)

class ReportsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📄 Report Generator", "Auto-generate professional BI reports").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        opts = ["Executive Summary", "Full Analytics Report", "Model Performance Report", "Marketing ROI Detail"]
        f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        f.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(f, text="Select Report Type", font=FONT_SUBTITLE).pack(pady=10)
        for opt in opts:
            ctk.CTkButton(f, text=f"Generate {opt}", fg_color=ACCENT_PURPLE).pack(pady=5, padx=50, fill="x")
        
        ctk.CTkFrame(f, fg_color=BORDER, height=1).pack(fill="x", pady=20, padx=20)
        ctk.CTkLabel(f, text="Export Formats", font=FONT_LABEL).pack()
        btn_f = ctk.CTkFrame(f, fg_color="transparent")
        btn_f.pack(pady=10)
        for fmt in ["CSV", "HTML", "PDF", "Excel"]:
            ctk.CTkButton(btn_f, text=fmt, width=80, fg_color=SUCCESS).pack(side="left", padx=5)

class RecommendationsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "💡 Business Recommendations", "AI-driven priority actions from data analysis").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Priority Cards
        recs = [
            ("High", "Retention", "Launch immediate retention campaign for high-risk churn segment ($2.4M at risk)."),
            ("High", "Marketing", "Shift 25% budget from Offline to Social Media for Amman/VIP segment."),
            ("Medium", "Pricing", "Increase price by 5% in Electronics category - elasticity is low."),
            ("Low", "Inventory", "Restock Home Appliances category - reorder point reached."),
        ]
        
        for i, (pri, area, txt) in enumerate(recs):
            color = DANGER if pri=="High" else (WARNING if pri=="Medium" else SUCCESS)
            f = ctk.CTkFrame(self, fg_color=BG_CARD, border_width=1, border_color=color, corner_radius=15)
            f.grid(row=i+1, column=0, sticky="ew", padx=20, pady=5)
            
            hdr = ctk.CTkFrame(f, fg_color="transparent")
            hdr.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(hdr, text=f"{pri} Priority", font=FONT_BADGE, text_color=color).pack(side="left")
            ctk.CTkLabel(hdr, text=area, font=FONT_SUBTITLE, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
            
            ctk.CTkLabel(f, text=txt, font=FONT_BODY, text_color=TEXT_SECONDARY, wraplength=1000).pack(anchor="w", padx=15, pady=(0, 15))

class SettingsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "⚙️ Settings", "Configuration and system preferences").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        f.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(f, text="App Theme", font=FONT_SUBTITLE).pack(anchor="w", padx=15, pady=10)
        ctk.CTkOptionMenu(f, values=["Dark", "Light", "System"], fg_color=ACCENT_PURPLE).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkLabel(f, text="Data Path", font=FONT_SUBTITLE).pack(anchor="w", padx=15, pady=(20, 10))
        ctk.CTkEntry(f, placeholder_text="C:/Users/user/DSS_Project/data", width=400, fg_color=BG_CARD2).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkLabel(f, text=f"DSS Pro v{APP_VERSION} | © 2026", font=FONT_CAPTION, text_color=TEXT_MUTED).pack(pady=40)
