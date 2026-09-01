"""DSS Pro — Report & System Pages."""
import customtkinter as ctk
from dss_core.config import *
from dss_core.widgets import *

class MetricsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📋 All Project Metrics", "Comprehensive performance index of all analytical models").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        M = METRICS
        sections = [
            ("🤖 Model Accuracies", [
                ["E-Commerce Churn", f"{M['ecom_churn_acc']}%", "99.00%", "✅ Best"],
                ["Marketing Model", f"{M['mkt_churn_acc']}%", "99.76%", "✅ Best"],
                ["Bank Churn", f"{M['bank_churn_acc']}%", "86.32%", "✅ Good"],
                ["Telco Churn", f"{M['telco_churn_acc']}%", "85.80%", "✅ Good"],
                ["Product Launch", f"{M['launch_model_acc']}%", "99.00%", "✅ Best"],
            ]),
            ("💰 Revenue & ROI", [
                ["E-Com Revenue", fmt_money(M["rev_ecom"]), "+12.4%", "✅ Good"],
                ["Marketing Rev", fmt_money(M["rev_mkt"]), "+383.6%", "✅ Excellent"],
                ["Overall ROI", f"+{M['roi_after']}%", "+226.1%", "✅ Excellent"],
                ["Growth", f"+{M['growth_rev']}%", "N/A", "✅ Excellent"],
            ]),
            ("🛒 Market Basket", [
                ["Total Rules", M["mb_rules"], "N/A", "✅ Strong"],
                ["Confidence", f"{M['mb_conf']}%", "+15.2%", "✅ Exceptional"],
                ["Lift", f"{M['mb_lift']}x", "N/A", "✅ Exceptional"],
            ])
        ]
        
        for i, (title, rows) in enumerate(sections):
            f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
            f.grid(row=i+1, column=0, sticky="ew", padx=20, pady=10)
            ctk.CTkLabel(f, text=title, font=F_CTITLE, text_color=ACCENT_BLUE).pack(anchor="w", padx=15, pady=10)
            tbl = DSSTable(f, ["Metric", "Value", "Improvement", "Rating"])
            tbl.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            tbl.load(rows)

class ReportPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📄 Report Generator", "Generate and export enterprise BI reports").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        f.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(f, text="Select Report Type", font=F_CTITLE).pack(pady=15)
        for opt in ["Executive Summary", "Financial Performance", "Model Accuracy Report", "Customer Churn Detail"]:
            ctk.CTkButton(f, text=f"Generate {opt}", fg_color=ACCENT_PURP, width=400, height=40).pack(pady=5)
            
        ctk.CTkFrame(f, fg_color=BORDER, height=1).pack(fill="x", pady=20, padx=50)
        ctk.CTkLabel(f, text="Export Format", font=F_BODY).pack()
        btn_f = ctk.CTkFrame(f, fg_color="transparent")
        btn_f.pack(pady=10)
        for fmt in ["CSV", "Excel", "HTML", "Print"]:
            ctk.CTkButton(btn_f, text=fmt, width=100, fg_color=SUCCESS).pack(side="left", padx=5)

class SettingsPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "⚙️ Settings", "Application configuration and user preferences").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        f = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER)
        f.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(f, text="Application Theme", font=F_CTITLE).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkOptionMenu(f, values=["Dark", "Light", "System"], fg_color=ACCENT_PURP).pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(f, text="Alert Thresholds", font=F_CTITLE).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkSlider(f, from_=0, to=100, fg_color=BG_CARD2, button_color=ACCENT_BLUE).pack(anchor="w", padx=20, pady=5, fill="x")
        
        ctk.CTkLabel(f, text="DSS Pro v1.0 | Enterprise Edition", font=F_CAP, text_color=TEXT_SEC).pack(pady=40)

class ScenarioPage(ScrollablePage):
    def build(self):
        self.columnconfigure(0, weight=1)
        SectionHeader(self, "📊 Scenario Builder", "Create and compare complex business scenarios").grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        kf = ctk.CTkFrame(self, fg_color="transparent")
        kf.grid(row=1, column=0, sticky="ew", padx=15)
        for i in range(3): kf.columnconfigure(i, weight=1)
        
        KPICard(kf, "⚖️", "Base Case", "$2.1M", accent=ACCENT_BLUE).grid(row=0, column=0, padx=5, sticky="nsew")
        KPICard(kf, "📉", "Pessimistic", "$1.8M", accent=DANGER).grid(row=0, column=1, padx=5, sticky="nsew")
        KPICard(kf, "📈", "Optimistic", "$3.2M", accent=SUCCESS).grid(row=0, column=2, padx=5, sticky="nsew")

        self._add_chart(ChartCard(self, "Scenario Comparison")).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
