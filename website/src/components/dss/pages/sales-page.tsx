import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { METRICS } from "@/data/dss-metrics"; // fallback
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { TrendingUp, ShoppingCart, DollarSign, BarChart3, Target, Zap, ServerCrash } from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, PieChart, Pie, Cell, Legend,
} from "recharts";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { fetchSalesData } from "@/lib/api";
import { CHANNEL_MIX as STATIC_CHANNEL_MIX, MONTHLY_REVENUE as STATIC_MONTHLY_REVENUE } from "@/data/dss-metrics";

export default function SalesPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['sales'],
    queryFn: fetchSalesData,
    refetchInterval: 10000, // Real-time polling every 10 seconds
  });

  if (isLoading) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center gap-4 text-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        <div>
          <div className="font-bold text-lg text-gradient">Connecting to DSS Engine...</div>
          <div className="text-sm text-muted-foreground">Streaming live sales data from backend</div>
        </div>
      </div>
    );
  }

  // Use live data if available, otherwise fallback to static for safety
  const live = data?.kpis;
  const totalRev = live?.total_revenue ?? METRICS.rev_ecom;
  const orders = live?.orders ?? METRICS.orders_ecom;
  const aov = live?.aov ?? METRICS.aov_ecom;
  const growth = live?.growth ?? METRICS.growth_rev;

  const MONTHLY_REVENUE = data?.monthly?.length ? data.monthly : STATIC_MONTHLY_REVENUE;
  const CHANNEL_MIX = STATIC_CHANNEL_MIX; // Channels require ROI calculation which is complex, keeping static for display

  return (
    <div className="space-y-6">
      {isError && (
        <div className="flex items-center gap-3 rounded-xl border border-destructive bg-destructive/10 p-4 text-destructive">
          <ServerCrash className="h-5 w-5" />
          <div className="text-sm">
            <span className="font-bold">Live API Disconnected.</span> Showing synchronized offline data. Ensure `api_bridge.py` is running on port 8765.
          </div>
        </div>
      )}
      
      {/* KPI Row */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Total Revenue" value={<CountUp to={totalRev} prefix="$" compact />} change={growth} icon={<DollarSign className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="Total Orders" value={<CountUp to={orders} />} sublabel="All datasets" icon={<ShoppingCart className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Avg Order Value" value={<CountUp to={aov} prefix="$" decimals={2} />} sublabel="Per transaction" icon={<Target className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Revenue Growth" value={<CountUp to={growth} suffix="%" decimals={1} />} sublabel="vs baseline" icon={<TrendingUp className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Marketing Revenue" value={<CountUp to={METRICS.rev_mkt} prefix="$" compact />} sublabel="All campaigns" icon={<BarChart3 className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Best Channel ROI" value={<CountUp to={METRICS.best_roi} suffix="%" decimals={1} />} sublabel={METRICS.best_channel} icon={<Zap className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      {/* Revenue Trend */}
      <Panel title="Monthly Revenue Trend" subtitle="12-month performance · E-Commerce dataset" delay={0.1}>
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={MONTHLY_REVENUE}>
            <defs>
              <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="oklch(0.78 0.18 195)" stopOpacity={0.35} />
                <stop offset="95%" stopColor="oklch(0.78 0.18 195)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke={chartTheme.grid} />
            <XAxis dataKey="month" stroke={chartTheme.axis} tick={labelStyle} />
            <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `$${(v / 1e6).toFixed(1)}M`} />
            <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtCurrency(v, { compact: true }), "Revenue"]} />
            <Area type="monotone" dataKey="revenue" stroke="oklch(0.78 0.18 195)" strokeWidth={2.5} fill="url(#revGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </Panel>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Channel Revenue */}
        <Panel title="Revenue by Channel" subtitle="Distribution & ROI performance" delay={0.15}>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={CHANNEL_MIX} layout="vertical">
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `$${(v / 1e6).toFixed(1)}M`} />
              <YAxis type="category" dataKey="channel" stroke={chartTheme.axis} tick={labelStyle} width={90} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtCurrency(v, { compact: true }), "Revenue"]} />
              <Bar dataKey="revenue" radius={[0, 6, 6, 0]}>
                {CHANNEL_MIX.map((_, i) => (
                  <Cell key={i} fill={`oklch(${0.78 - i * 0.04} ${0.22 - i * 0.02} ${195 + i * 25})`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        {/* Channel Mix Pie */}
        <Panel title="Channel Mix %" subtitle="Share of total revenue" delay={0.2}>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={CHANNEL_MIX} dataKey="pct" nameKey="channel" cx="50%" cy="50%" outerRadius={90} label={({ channel, pct }) => `${pct}%`} labelLine={false}>
                {CHANNEL_MIX.map((_, i) => (
                  <Cell key={i} fill={`oklch(${0.78 - i * 0.04} ${0.22 - i * 0.02} ${195 + i * 25})`} />
                ))}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "Share"]} />
              <Legend formatter={(v) => <span style={{ color: "oklch(0.7 0.03 260)", fontSize: 11 }}>{v}</span>} />
            </PieChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      {/* Channel ROI Table */}
      <Panel title="Channel Performance Summary" subtitle="ROI, revenue, and efficiency metrics" delay={0.25}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--glass-border)" }}>
                {["Channel", "Revenue", "ROI", "% Share", "Grade"].map((h) => (
                  <th key={h} className="px-4 py-2.5 text-left text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {CHANNEL_MIX.map((row, i) => (
                <motion.tr key={i} initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.05 }}
                  className="border-b transition-colors hover:bg-white/[0.03]" style={{ borderColor: "var(--glass-border)" }}>
                  <td className="px-4 py-3 font-semibold">{row.channel}</td>
                  <td className="px-4 py-3 font-mono">{fmtCurrency(row.revenue, { compact: true })}</td>
                  <td className="px-4 py-3 font-bold" style={{ color: row.roi > 200 ? "var(--success)" : "oklch(0.82 0.18 80)" }}>{row.roi}%</td>
                  <td className="px-4 py-3">{row.pct}%</td>
                  <td className="px-4 py-3">
                    <span className="rounded-full px-2 py-0.5 text-[10px] font-bold tracking-wider text-primary-foreground"
                      style={{ background: row.roi > 300 ? "var(--gradient-success)" : row.roi > 150 ? "var(--gradient-gold)" : "var(--gradient-danger)" }}>
                      {row.roi > 300 ? "A+" : row.roi > 150 ? "B" : "C"}
                    </span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}
