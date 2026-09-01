import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { SALES_FORECAST } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { TrendingUp, BarChart3, Target, Zap, Activity, Calendar } from "lucide-react";
import {
  ResponsiveContainer, ComposedChart, Area, Line, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip,
} from "recharts";
import { motion } from "framer-motion";

const growth6m = ((METRICS.fc_m6 - METRICS.fc_m1) / METRICS.fc_m1 * 100);
const lastActual = SALES_FORECAST.find(d => d.actual && !SALES_FORECAST[SALES_FORECAST.indexOf(d) + 1]?.actual);
const firstForecast = SALES_FORECAST.find(d => d.forecast !== null);

export default function ForecastPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="M1 Forecast" value={<CountUp to={METRICS.fc_m1} prefix="$" compact />} icon={<Calendar className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="M6 Forecast" value={<CountUp to={METRICS.fc_m6} prefix="$" compact />} icon={<TrendingUp className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Monthly Growth" value={<CountUp to={METRICS.fc_growth} prefix="$" compact />} sublabel="Per month avg" icon={<Zap className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="6-Month Growth" value={<CountUp to={growth6m} suffix="%" decimals={2} />} icon={<BarChart3 className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Revenue Growth" value={<CountUp to={METRICS.growth_rev} suffix="%" decimals={1} />} sublabel="Historical" icon={<Activity className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Data Points" value={<CountUp to={SALES_FORECAST.length} />} sublabel="Actual + forecast" icon={<Target className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <Panel title="Sales Forecast · Actual vs Projected" subtitle="6 months actual + 6 months forecast with confidence bands" delay={0.1}>
        <ResponsiveContainer width="100%" height={320}>
          <ComposedChart data={SALES_FORECAST}>
            <defs>
              <linearGradient id="actualGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="oklch(0.78 0.18 195)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="oklch(0.78 0.18 195)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="fcGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="oklch(0.7 0.22 320)" stopOpacity={0.25} />
                <stop offset="95%" stopColor="oklch(0.7 0.22 320)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke={chartTheme.grid} />
            <XAxis dataKey="month" stroke={chartTheme.axis} tick={labelStyle} />
            <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `$${(v / 1e6).toFixed(1)}M`} domain={["auto", "auto"]} />
            <Tooltip contentStyle={tooltipStyle}
              formatter={(v: number | null, name: string) => [v ? fmtCurrency(v, { compact: true }) : "–", name === "actual" ? "Actual" : "Forecast"]} />
            <Area type="monotone" dataKey="actual" stroke="oklch(0.78 0.18 195)" strokeWidth={2.5} fill="url(#actualGrad)" connectNulls={false} name="actual" />
            <Area type="monotone" dataKey="forecast" stroke="oklch(0.7 0.22 320)" strokeWidth={2.5} fill="url(#fcGrad)" connectNulls={false} strokeDasharray="6 3" name="forecast" />
          </ComposedChart>
        </ResponsiveContainer>
      </Panel>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {[
          { label: "Pessimistic", value: METRICS.fc_m6 * 0.85, desc: "-15% confidence lower bound", color: "var(--gradient-danger)" },
          { label: "Base Case", value: METRICS.fc_m6, desc: "Model forecast center line", color: "var(--gradient-primary)" },
          { label: "Optimistic", value: METRICS.fc_m6 * 1.20, desc: "+20% seasonal upside", color: "var(--gradient-success)" },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 + i * 0.1 }}
            className="relative overflow-hidden rounded-xl p-5 text-center" style={{ background: "oklch(0.22 0.04 270 / 0.5)", border: "1px solid var(--glass-border)" }}>
            <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: s.color }} />
            <div className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">{s.label}</div>
            <div className="mt-3 text-3xl font-bold">{fmtCurrency(s.value, { compact: true })}</div>
            <div className="mt-1 text-xs text-muted-foreground">{s.desc}</div>
          </motion.div>
        ))}
      </div>

      <Panel title="Forecast Detail Table" subtitle="Month-by-month actual and projected revenue" delay={0.4}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--glass-border)" }}>
                {["Month", "Actual", "Forecast", "Type", "vs Prev"].map((h) => (
                  <th key={h} className="px-4 py-2.5 text-left text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {SALES_FORECAST.map((row, i) => {
                const prev = SALES_FORECAST[i - 1];
                const prevVal = prev ? (prev.actual ?? prev.forecast) : null;
                const thisVal = row.actual ?? row.forecast;
                const vsPrev = prevVal && thisVal ? ((thisVal - prevVal) / prevVal * 100) : null;
                return (
                  <tr key={row.month} className="border-b hover:bg-white/[0.03]" style={{ borderColor: "var(--glass-border)" }}>
                    <td className="px-4 py-2.5 font-semibold">{row.month}</td>
                    <td className="px-4 py-2.5">{row.actual ? fmtCurrency(row.actual, { compact: true }) : "—"}</td>
                    <td className="px-4 py-2.5">{row.forecast ? fmtCurrency(row.forecast, { compact: true }) : "—"}</td>
                    <td className="px-4 py-2.5">
                      <span className="rounded-full px-2 py-0.5 text-[10px] font-bold text-primary-foreground"
                        style={{ background: row.actual ? "var(--gradient-success)" : "var(--gradient-primary)" }}>
                        {row.actual ? "Actual" : "Forecast"}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 font-semibold" style={{ color: vsPrev === null ? undefined : vsPrev >= 0 ? "var(--success)" : "var(--destructive)" }}>
                      {vsPrev === null ? "—" : `${vsPrev >= 0 ? "+" : ""}${vsPrev.toFixed(1)}%`}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}
