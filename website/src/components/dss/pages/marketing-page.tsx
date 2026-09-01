import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { MARKETING_ROI as MKT } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { TrendingUp, DollarSign, Target, Zap, Award, BarChart3 } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ReferenceLine, Legend
} from "recharts";
import { motion } from "framer-motion";

// Before vs After optimization comparison
const comparison = [
  { period: "Before Opt.", roi: MKT.beforeROI },
  { period: "After Opt.", roi: MKT.afterROI },
  { period: "Best Combo", roi: MKT.bestComboROI },
  { period: "Top 15 Avg", roi: MKT.avgTop15ROI },
];

const bySegment = MKT.bySegment;
const bestCombo = MKT.bestCombo;

export default function MarketingPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="ROI Before" value={<CountUp to={MKT.beforeROI} suffix="%" decimals={1} />} accent="danger" icon={<TrendingUp className="h-4 w-4" />} delay={0} />
        <StatCard label="ROI After Opt." value={<CountUp to={MKT.afterROI} suffix="%" decimals={2} />} accent="success" icon={<TrendingUp className="h-4 w-4" />} delay={0.05} />
        <StatCard label="Best Combo ROI" value={<CountUp to={MKT.bestComboROI} suffix="%" decimals={2} />} sublabel="Social · VIP · Q4 · Amman" accent="gold" icon={<Award className="h-4 w-4" />} delay={0.1} />
        <StatCard label="Rev Before" value={<CountUp to={MKT.revenueBefore} prefix="$" compact />} icon={<DollarSign className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Rev After" value={<CountUp to={MKT.revenueAfter} prefix="$" compact />} icon={<BarChart3 className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Revenue Growth" value={<CountUp to={MKT.revenueGrowth} suffix="%" decimals={1} />} sublabel="After optimization" icon={<Target className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="ROI Before vs After Optimization" subtitle="The impact of intelligent campaign allocation" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={comparison}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="period" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} />
              <ReferenceLine y={0} stroke="oklch(0.5 0.03 260)" strokeWidth={1.5} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "ROI"]} />
              <Bar dataKey="roi" radius={[6, 6, 0, 0]}>
                {comparison.map((d) => (
                  <Cell key={d.period} fill={d.roi < 0 ? "oklch(0.66 0.24 25)" : d.roi > 200 ? "oklch(0.78 0.2 150)" : d.roi > 100 ? "oklch(0.82 0.18 80)" : "oklch(0.78 0.18 195)"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="ROI by Channel (Pre-Optimization)" subtitle="Original performance by channel" delay={0.15}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={MKT.byChannel} layout="vertical">
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} />
              <YAxis type="category" dataKey="channel" stroke={chartTheme.axis} tick={labelStyle} width={90} />
              <ReferenceLine x={0} stroke="oklch(0.5 0.03 260)" />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "ROI"]} />
              <Bar dataKey="roi" radius={[0, 6, 6, 0]}>
                {MKT.byChannel.map((d) => <Cell key={d.channel} fill={d.roi < 0 ? "oklch(0.66 0.24 25)" : "oklch(0.78 0.2 150)"} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      {/* Best Combo Highlight */}
      <Panel title="🏆 Best Marketing Combination" subtitle={`Found via bootstrap CI (${fmtNum(MKT.bootstrapIterations)} iterations)`} delay={0.25}>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
          {[
            { label: "Channel", value: bestCombo.channel },
            { label: "Segment", value: bestCombo.segment },
            { label: "Season", value: bestCombo.season },
            { label: "Region", value: bestCombo.region },
            { label: "Category", value: bestCombo.category },
          ].map((item, i) => (
            <motion.div key={item.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 + i * 0.07 }}
              className="relative overflow-hidden rounded-xl border p-4 text-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
              <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: "var(--gradient-gold)" }} />
              <div className="text-[10px] text-muted-foreground uppercase tracking-wider">{item.label}</div>
              <div className="mt-2 text-lg font-bold text-gradient-gold">{item.value}</div>
            </motion.div>
          ))}
        </div>
        <div className="mt-4 rounded-xl border p-4 text-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
          <div className="text-sm text-muted-foreground">Best Combination ROI</div>
          <div className="mt-1 text-4xl font-bold text-gradient">{bestCombo.roi}%</div>
          <div className="mt-1 text-xs text-muted-foreground">Bootstrap CI: [{MKT.bootstrapCI[0]}%, {MKT.bootstrapCI[1]}%] — {MKT.roiAbove100} combos above 100% ROI</div>
        </div>
      </Panel>

      {/* By Segment */}
      {/* By Segment (Before vs After) */}
      <Panel title="ROI by Customer Segment" subtitle="Segment performance Before vs After Optimization" delay={0.35}>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={bySegment} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="segment" stroke={chartTheme.axis} tick={labelStyle} />
            <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} />
            <Tooltip
              contentStyle={tooltipStyle}
              cursor={{ fill: "oklch(0.5 0.05 270 / 0.1)" }}
              formatter={(value: number, name: string) => [
                `${value > 0 ? "+" : ""}${value}%`,
                name === "roi" ? "Before Optimization" : "After Optimization",
              ]}
            />
            <Legend wrapperStyle={{ paddingTop: "20px" }} />
            <ReferenceLine y={0} stroke="oklch(0.5 0.03 260)" strokeWidth={1.5} />
            <Bar
              dataKey="roi"
              name="Before Optimization"
              fill="oklch(0.66 0.24 25)" /* Danger/Red */
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            />
            <Bar
              dataKey="roiAfter"
              name="After Optimization"
              fill="oklch(0.78 0.2 150)" /* Success/Green */
              radius={[4, 4, 0, 0]}
              animationDuration={1500}
            />
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {bySegment.map((seg, i) => (
            <motion.div
              key={seg.segment}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1 }}
              className="relative overflow-hidden rounded-xl border p-4 glass hover:bg-white/5 transition-colors"
            >
              {/* Top Accent Line */}
              <div
                className="absolute inset-x-0 top-0 h-[2px]"
                style={{ background: "var(--gradient-primary)", opacity: 0.8 }}
              />
              
              <div className="text-sm font-bold text-center tracking-wide mb-3">{seg.segment}</div>
              
              <div className="flex justify-between items-center">
                <div className="flex flex-col items-center w-1/2">
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1">Before</span>
                  <span style={{ color: "oklch(0.66 0.24 25)" }} className="font-bold text-lg">
                    {seg.roi}%
                  </span>
                </div>
                
                <div className="h-8 w-px bg-border/50"></div>
                
                <div className="flex flex-col items-center w-1/2">
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1">After</span>
                  <span style={{ color: "oklch(0.78 0.2 150)" }} className="font-bold text-lg glow">
                    +{seg.roiAfter}%
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
