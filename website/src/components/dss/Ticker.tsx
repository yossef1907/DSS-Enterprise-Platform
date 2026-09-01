import { PROJECT_METRICS, MARKETING_ROI, MARKET_BASKET } from "@/data/dss";
import { fmtCurrency, fmtNum, fmtPct } from "@/lib/dss-utils";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";

export function Ticker() {
  const items = [
    { label: "Portfolio CLV", value: fmtCurrency(PROJECT_METRICS.totalCLV, { compact: true }), up: true },
    { label: "Customers", value: fmtNum(PROJECT_METRICS.totalCustomers), up: true },
    { label: "Avg CLV", value: fmtCurrency(PROJECT_METRICS.avgCLV), up: true },
    { label: "ROI After", value: fmtPct(MARKETING_ROI.afterROI), up: true },
    { label: "Best Combo ROI", value: fmtPct(MARKETING_ROI.bestComboROI), up: true },
    { label: "Revenue Growth", value: "+" + fmtPct(MARKETING_ROI.revenueGrowth), up: true },
    { label: "Basket Rules", value: fmtNum(MARKET_BASKET.totalRules), up: true },
    { label: "Max Lift", value: MARKET_BASKET.maxLift.toFixed(2) + "x", up: true },
    { label: "DB Tables", value: fmtNum(PROJECT_METRICS.databaseTables), up: false },
    { label: "Total Rows", value: fmtNum(PROJECT_METRICS.totalRows), up: true },
  ];
  const seq = [...items, ...items];
  return (
    <div className="sticky bottom-0 border-t glass overflow-hidden" style={{ borderColor: "var(--glass-border)" }}>
      <div className="flex items-center gap-2 px-4 py-2 text-xs">
        <span className="flex items-center gap-1.5 font-bold tracking-wider text-primary shrink-0">
          <Activity className="h-3.5 w-3.5 animate-pulse" /> LIVE
        </span>
        <div className="flex-1 overflow-hidden">
          <div className="flex animate-ticker whitespace-nowrap">
            {seq.map((it, i) => (
              <span key={i} className="mx-6 inline-flex items-center gap-2">
                <span className="text-muted-foreground">{it.label}</span>
                <span className="font-bold text-foreground">{it.value}</span>
                {it.up ? (
                  <TrendingUp className="h-3 w-3" style={{ color: "var(--success)" }} />
                ) : (
                  <TrendingDown className="h-3 w-3 text-muted-foreground" />
                )}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}