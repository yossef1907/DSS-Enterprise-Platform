"""DSS Pro — Central Configuration v3.0"""
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = r"C:\Users\user\DSS_Project"
DATA_CLEAN = os.path.join(BASE_DIR, "data", "clean")
EXPORTS    = os.path.join(BASE_DIR, "exports")
POWERBI    = os.path.join(EXPORTS,  "powerbi")
LOGS_DIR   = os.path.join(BASE_DIR, "logs")
LOG_FILE   = os.path.join(LOGS_DIR, "app.log")

os.makedirs(LOGS_DIR, exist_ok=True)

POWERBI_FILES = {
    "ecommerce":         "ecommerce_powerbi.csv",
    "customer_segments": "customer_segments_powerbi.csv",
    "churn":             "churn_powerbi.csv",
    "forecast":          "forecast_powerbi.csv",
    "monthly_kpi":       "monthly_kpi_powerbi.csv",
    "roi":               "roi_powerbi.csv",
    "roi_region":        "roi_region_powerbi.csv",
    "top_products":      "top_products_powerbi.csv",
    "top_customers":     "top_customers_powerbi.csv",
    "market_basket":     "market_basket_powerbi_v2.csv",
    "product_launch":    "product_launch_powerbi.csv",
    "recommendations":   "recommendations_powerbi.csv",
    "marketing_summary": "marketing_summary_v2_powerbi.csv",
    "best_combos":       "best_combinations_v2_powerbi.csv",
    "final_metrics":     "final_metrics_powerbi.csv",
    "ecommerce_churn":   "ecommerce_churn_powerbi.csv",
    "marketing_model":   "marketing_model_powerbi.csv",
    "marketing_opt":     "marketing_optimization_powerbi.csv",
}

ADDITIONAL_FILES = {
    "product_launch": os.path.join(EXPORTS, "product_launch_simulation_v2.csv"),
    "cust_features":  os.path.join(EXPORTS, "customer_features.csv"),
    "mkt_features":   os.path.join(EXPORTS, "marketing_features.csv"),
    "best_combos":    os.path.join(EXPORTS, "best_combinations_v2.csv"),
    "eco_clean":      os.path.join(DATA_CLEAN, "ecommerce_clean.csv"),
}

# ── EXACT Project Metrics ─────────────────────────────────────────────────────
METRICS = {
    "ecom_churn_acc": 99.00,
    "mkt_churn_acc":  99.76,
    "bank_churn_acc": 86.32,
    "bank_logloss":   0.3235,
    "telco_churn_acc":85.80,
    "telco_logloss":  0.3321,
    "launch_model_acc": 99.00,
    "overall_score":  94.6,

    "mb_rules": 722,
    "mb_conf": 91.6,
    "mb_lift": 7.59,
    "mb_supp": 14.1,

    "roi_before": -41.1,
    "roi_after": 184.97,
    "best_roi": 421.18,
    "top15_roi": 272.77,
    "pos_combos": 682,
    "best_channel": "Social Media",
    "best_segment": "VIP",
    "best_season": "Q4",
    "best_region": "Amman",
    "best_cat": "Electronics",

    "rev_ecom": 26694597.16,
    "orders_ecom": 22049,
    "aov_ecom": 1210.69,
    "rev_mkt": 1715290018.00,
    "budget_mkt": 601914523.46,
    "growth_rev": 383.6,

    "churn_ecom": 16.8,
    "churn_telco": 26.5,
    "churn_hr": 16.1,
    "churn_bank": 20.0,

    "fc_m1": 1922152,
    "fc_m6": 2015454,
    "fc_growth": 18660,

    "go_dec": 670,
    "nogo_dec": 1730,
    "best_success": 99.51,
}

# ── Colors — Premium Modern Palette ───────────────────────────────────────────
BG_MAIN     = "#0f0f1a"       # Deep navy背景
BG_SIDEBAR  = "#0a0a12"       # Sidebar darker
BG_CARD     = "#1e1e32"       # Card base
BG_CARD2    = "#16162a"       # Secondary card
BORDER      = "#2d2d4a"       # Subtle border
BORDER2     = "#3a3a5a"       # Lighter border

ACCENT_BLUE = "#00d4ff"       # Electric blue
ACCENT_PURP = "#8b5cf6"       # Modern purple
ACCENT_GOLD = "#fbbf24"       # Amber/gold
SUCCESS     = "#10b981"       # Emerald green
WARNING     = "#f59e0b"       # Warm amber
DANGER      = "#ef4444"       # Vibrant red

TEXT_PRI    = "#f8fafc"       # Near white
TEXT_SEC    = "#94a3b8"       # Cool gray
TEXT_MUTED  = "#64748b"       # Muted gray

CHART_COLORS = ['#00d4ff', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
                '#06b6d4', '#6366f1', '#14b8a6', '#f97316', '#ec4899']

# Compatibility Aliases
TEXT_PRIMARY   = TEXT_PRI
TEXT_SECONDARY = TEXT_SEC
ACCENT_PURPLE  = ACCENT_PURP

# ── Typography — Modern, Clean Hierarchy ─────────────────────────────────────
F_HERO   = ("Segoe UI", 30, "bold")   # Main title
F_TITLE  = ("Segoe UI", 22, "bold")   # Section titles
F_KPI    = ("Segoe UI", 38, "bold")   # Large KPI values
F_CTITLE = ("Segoe UI", 15, "bold")   # Card titles
F_BODY   = ("Segoe UI", 13)           # Body text
F_CAP    = ("Segoe UI", 11)           # Captions/labels
F_NAV    = ("Segoe UI", 12)           # Navigation
F_BADGE  = ("Segoe UI", 10, "bold")   # Badges/labels

# Font Aliases
FONT_TITLE     = F_TITLE
FONT_SUBTITLE  = F_CTITLE
FONT_BODY      = F_BODY
FONT_CAPTION   = F_CAP
FONT_LABEL     = F_BODY

# ── Navigation Structure ──────────────────────────────────────────────────────
NAV_CONFIG = [
    ("OVERVIEW", [
        ("⬡", "Executive Hub", "overview")
    ]),
    ("ANALYTICS", [
        ("📊", "Sales", "sales"),
        ("👥", "Customers", "customers"),
        ("⚠️", "Churn Risk", "churn")
    ]),
    ("AI INSIGHTS", [
        ("🛒", "Market Basket", "basket"),
        ("🚀", "Product Launch", "launch")
    ]),
    ("PLANNING", [
        ("📈", "Forecasting", "forecast"),
        ("📣", "Campaign Planner", "planner")
    ]),
    ("INTELLIGENCE", [
        ("💡", "Smart Pricing", "pricing"),
        ("🔬", "A/B Testing", "abtest"),
        ("📦", "Inventory", "inventory")
    ]),
    ("TOOLS", [
        ("🧪", "Product Tester", "tester"),
        ("📊", "Scenario Builder", "scenarios"),
        ("🔍", "Product Analyzer", "product_analyzer")
    ]),
    ("REPORTS", [
        ("📋", "All Metrics", "metrics"),
        ("📄", "Report Generator", "reports")
    ]),
    ("SYSTEM", [
        ("⚙️", "Settings", "settings")
    ])
]

APP_TITLE = "DSS Pro — Decision Support System v1.0"
APP_SIZE  = (1600, 1000)

# ── Compatibility Aliases ─────────────────────────────────────────────────────
TEXT_PRIMARY   = TEXT_PRI
TEXT_SECONDARY = TEXT_SEC
ACCENT_PURPLE  = ACCENT_PURP
FONT_TITLE     = F_TITLE
FONT_SUBTITLE  = F_CTITLE
FONT_BODY      = F_BODY
FONT_CAPTION   = F_CAP
FONT_LABEL     = F_BODY

