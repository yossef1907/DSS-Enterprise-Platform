import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { CLV_SEGMENTS, CUSTOMER_SEGMENTS_RFM, PROJECT_METRICS } from "@/data/dss";
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { DollarSign, TrendingUp, Users, Target, Award, Activity } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { motion } from "framer-motion";

export default function CLVPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Platinum CLV" value={<CountUp to={CLV_SEGMENTS[0].avgCLV} prefix="$" compact />} sublabel={`${fmtNum(CLV_SEGMENTS[0].customers)} customers`} icon={<Award className="h-4 w-4" />} accent="gold" delay={0} />
        <StatCard label="Total Portfolio" value={<CountUp to={PROJECT_METRICS.totalCLV} prefix="$" compact />} sublabel="All tiers" icon={<DollarSign className="h-4 w-4" />} accent="primary" delay={0.05} />
        <StatCard label="Avg CLV" value={<CountUp to={PROJECT_METRICS.avgCLV} prefix="$" decimals={2} />} sublabel="Platform-wide" icon={<Target className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Median CLV" value={<CountUp to={PROJECT_METRICS.medianCLV} prefix="$" decimals={2} />} icon={<Activity className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Total Customers" value={<CountUp to={PROJECT_METRICS.totalCustomers} compact />} icon={<Users className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Gold CLV" value={<CountUp to={CLV_SEGMENTS[1].avgCLV} prefix="$" compact />} sublabel={`${fmtNum(CLV_SEGMENTS[1].customers)} customers`} icon={<TrendingUp className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Avg CLV by Tier" subtitle="Average customer lifetime value" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={CLV_SEGMENTS}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="segment" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}K`} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtCurrency(v, { compact: true }), "Avg CLV"]} />
              <Bar dataKey="avgCLV" radius={[6, 6, 0, 0]}>
                {CLV_SEGMENTS.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Portfolio Value by Tier" subtitle="Total CLV contribution" delay={0.15}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={CLV_SEGMENTS} layout="vertical">
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `$${(v / 1e9).toFixed(2)}B`} />
              <YAxis type="category" dataKey="segment" stroke={chartTheme.axis} tick={labelStyle} width={65} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtCurrency(v, { compact: true }), "Portfolio"]} />
              <Bar dataKey="totalCLV" radius={[0, 6, 6, 0]}>
                {CLV_SEGMENTS.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      <Panel title="CLV Tier Analysis" subtitle="Detailed breakdown across 4 CLV tiers" delay={0.25}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--glass-border)" }}>
                {["Tier", "Customers", "Avg CLV", "Portfolio Value", "Portfolio Share", "Priority"].map((h) => (
                  <th key={h} className="px-4 py-2.5 text-left text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {CLV_SEGMENTS.map((row, i) => {
                const share = (row.totalCLV / PROJECT_METRICS.totalCLV * 100).toFixed(1);
                const priorities = ["VIP", "High", "Medium", "Low"];
                const priorColors = ["var(--gradient-gold)", "var(--gradient-success)", "var(--gradient-primary)", "var(--gradient-danger)"];
                return (
                  <motion.tr key={row.segment} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 + i * 0.07 }}
                    className="border-b hover:bg-white/[0.03]" style={{ borderColor: "var(--glass-border)" }}>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-2.5 w-2.5 rounded-full" style={{ background: row.color }} />
                        <span className="font-semibold">{row.segment}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">{fmtNum(row.customers)}</td>
                    <td className="px-4 py-3 font-bold text-gradient">{fmtCurrency(row.avgCLV, { compact: true })}</td>
                    <td className="px-4 py-3 font-bold">{fmtCurrency(row.totalCLV, { compact: true })}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-20 rounded-full overflow-hidden" style={{ background: "oklch(0.3 0.04 270)" }}>
                          <div className="h-full rounded-full" style={{ width: `${share}%`, background: row.color }} />
                        </div>
                        <span>{share}%</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className="rounded-full px-2 py-0.5 text-[10px] font-bold text-primary-foreground" style={{ background: priorColors[i] }}>{priorities[i]}</span>
                    </td>
                  </motion.tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Panel>

      {/* RFM */}
      <Panel title="RFM Analysis — Top Segments" subtitle="Champions · Loyal · Potential · At Risk" delay={0.35}>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {CUSTOMER_SEGMENTS_RFM.map((seg, i) => {
            const colors = ["oklch(0.78 0.18 195)", "oklch(0.78 0.2 150)", "oklch(0.82 0.18 80)", "oklch(0.66 0.24 25)"];
            return (
              <motion.div key={seg.segment} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 + i * 0.08 }}
                className="relative overflow-hidden rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
                <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: colors[i] }} />
                <div className="text-xs font-semibold text-muted-foreground">{seg.segment}</div>
                <div className="mt-2 text-xl font-bold">{fmtNum(seg.count)}</div>
                <div className="mt-1 text-sm font-bold text-gradient">{fmtCurrency(seg.avgCLV, { compact: true })}</div>
                <div className="mt-1 text-[11px] text-muted-foreground">RFM Score: {seg.rfmScore}/15</div>
              </motion.div>
            );
          })}
        </div>
      </Panel>
    </div>
  );
}
