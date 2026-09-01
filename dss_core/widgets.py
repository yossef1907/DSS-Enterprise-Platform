"""DSS Pro — Premium UI Components v3.0."""
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time, threading

from dss_core.config import (
    BG_MAIN, BG_CARD, BORDER, ACCENT_BLUE, SUCCESS, WARNING, DANGER,
    TEXT_PRI, TEXT_SEC, F_TITLE, F_BODY, F_CAP, F_CTITLE, F_KPI, CHART_COLORS
)

def apply_mpl_style():
    """Apply premium dark theme to matplotlib charts."""
    plt.rcParams.update({
        "figure.facecolor": "#1e1e32",
        "axes.facecolor":   "#1e1e32",
        "axes.edgecolor":   "#2d2d4a",
        "axes.labelcolor":  "#94a3b8",
        "xtick.color":      "#94a3b8",
        "ytick.color":      "#94a3b8",
        "grid.color":       "#2d2d4a",
        "grid.alpha":       0.15,
        "text.color":       "#f8fafc",
        "axes.spines.top":  False,
        "axes.spines.right":False,
        "font.size":        9,
        "axes.titlesize":   11,
        "axes.labelsize":   9,
        "legend.fontsize":  8,
        "xtick.labelsize":  8,
        "ytick.labelsize":  8,
    })

def fmt_money(v): return f"${v:,.2f}"
def fmt_pct(v, decimals=2): return f"{v:+.{decimals}f}%" if v != 0 else f"{v:.{decimals}f}%"
def fmt_count(v): return f"{v:,}"

class Toast:
    @staticmethod
    def show(master, message, color=ACCENT_BLUE):
        toast = ctk.CTkToplevel(master)
        toast.wm_overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(fg_color=color)
        
        # Position at bottom right
        sw, sh = master.winfo_screenwidth(), master.winfo_screenheight()
        toast.geometry(f"+{sw-350}+{sh-150}")
        
        ctk.CTkLabel(toast, text=message, font=F_BODY, text_color=TEXT_PRI).pack(padx=20, pady=15)
        
        def fade():
            for i in range(10, 0, -1):
                try: toast.attributes("-alpha", i/10); time.sleep(0.05)
                except: break
            try: toast.destroy()
            except: pass
            
        threading.Thread(target=lambda: (time.sleep(2), fade()), daemon=True).start()

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text: return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = ctk.CTkLabel(tw, text=self.text, font=F_CAP, fg_color="#33334d", text_color="#fff", corner_radius=5)
        label.pack(padx=5, pady=2)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw: tw.destroy()

class KPICard(ctk.CTkFrame):
    def __init__(self, master, icon, title, value, trend=None, accent=ACCENT_BLUE, tooltip=None, **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=12, border_width=1, border_color=BORDER, **kwargs)
        
        # Left Accent Border
        self.accent_line = ctk.CTkFrame(self, fg_color=accent, width=4, corner_radius=0)
        self.accent_line.pack(side="left", fill="y", padx=(1, 0), pady=1)
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Header: Icon & Title
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=icon, font=("Segoe UI Emoji", 18)).pack(side="left")
        ctk.CTkLabel(header, text=title, font=F_CTITLE, text_color=TEXT_SEC).pack(side="left", padx=10)
        
        # Value
        ctk.CTkLabel(content, text=str(value), font=F_KPI, text_color=TEXT_PRI).pack(anchor="w", pady=(10, 5))
        
        # Trend
        if trend is not None:
            t_color = SUCCESS if trend >= 0 else DANGER
            t_icon = "▲" if trend >= 0 else "▼"
            ctk.CTkLabel(content, text=f"{t_icon} {abs(trend):.1f}%", font=("Segoe UI", 12, "bold"), text_color=t_color).pack(anchor="w")
            
        if tooltip:
            Tooltip(self, tooltip)

class ChartCard(ctk.CTkFrame):
    def __init__(self, master, title, figsize=(7, 4), **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER, **kwargs)
        
        ctk.CTkLabel(self, text=title, font=F_CTITLE, text_color=TEXT_PRI).pack(anchor="w", padx=15, pady=(15, 5))
        
        apply_mpl_style()
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.canvas_widget.configure(bg="#1a1a2e", highlightthickness=0)

    def refresh(self):
        self.fig.tight_layout()
        self.canvas.draw()

class DSSTable(ctk.CTkFrame):
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columns = columns
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#2a2a4a", corner_radius=5)
        self.header_frame.pack(fill="x", pady=(0, 5))
        
        for i, col in enumerate(columns):
            self.header_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(self.header_frame, text=col, font=F_CTITLE, text_color=TEXT_PRI).grid(row=0, column=i, padx=10, pady=8, sticky="w")
            
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

    def load(self, data_rows):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for r_idx, row in enumerate(data_rows):
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=BG_CARD if r_idx % 2 == 0 else "transparent", corner_radius=5)
            row_frame.pack(fill="x", pady=1)
            for c_idx, val in enumerate(row):
                row_frame.columnconfigure(c_idx, weight=1)
                ctk.CTkLabel(row_frame, text=str(val), font=F_BODY, text_color=TEXT_SEC).grid(row=0, column=c_idx, padx=10, pady=5, sticky="w")

class GaugeWidget(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=15, border_width=1, border_color=BORDER, **kwargs)
        ctk.CTkLabel(self, text=title, font=F_CTITLE, text_color=TEXT_PRI).pack(pady=(10, 0))
        
        self.fig, self.ax = plt.subplots(figsize=(3, 2), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)
        self.canvas_widget.configure(bg="#1a1a2e", highlightthickness=0)
        
    def set_value(self, val, color=SUCCESS):
        self.ax.clear()
        self.ax.set_facecolor("#1a1a2e")
        theta = np.linspace(np.pi, 0, 100)
        self.ax.plot(np.cos(theta), np.sin(theta), color="#2a2a4a", linewidth=12)
        progress = val / 100
        theta_val = np.linspace(np.pi, np.pi - progress * np.pi, 100)
        self.ax.plot(np.cos(theta_val), np.sin(theta_val), color=color, linewidth=12)
        self.ax.text(0, 0.2, f"{val:.1f}%", ha='center', va='center', fontsize=22, fontweight='bold', color=TEXT_PRI)
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-0.2, 1.2)
        self.ax.axis('off')
        self.canvas.draw()

class SectionHeader(ctk.CTkFrame):
    def __init__(self, master, title, subtitle=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=title, font=F_TITLE, text_color=TEXT_PRI).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(self, text=subtitle, font=F_BODY, text_color=TEXT_SEC).pack(anchor="w")
        ctk.CTkFrame(self, fg_color=BORDER, height=1).pack(fill="x", pady=(5, 15))

class ScrollablePage(ctk.CTkScrollableFrame):
    def __init__(self, master, store, **kwargs):
        super().__init__(master, fg_color=BG_MAIN, **kwargs)
        self.store = store
        self._charts = []

    def _add_chart(self, chart):
        self._charts.append(chart)
        return chart

    def build(self):
        pass
