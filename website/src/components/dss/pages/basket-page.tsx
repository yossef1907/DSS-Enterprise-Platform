import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { MARKET_BASKET } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { ShoppingCart, TrendingUp, Zap, Target, Link, Award } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell, ZAxis,
} from "recharts";
import { motion } from "framer-motion";

const rules = MARKET_BASKET.topBundles.map((r) => ({
  antecedent: r.antecedent,
  consequent: r.consequent,
  confidence: r.confidence,
  lift: r.lift,
  support: r.support,
  revenue: Math.round(r.lift * r.confidence * 8000),
}));

export default function BasketPage() {
  const topRevenue = rules.reduce((s, r) => s + r.revenue, 0);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Association Rules" value={<CountUp to={METRICS.mb_rules} />} sublabel="Discovered rules" icon={<Link className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="Top Confidence" value={<CountUp to={MARKET_BASKET.maxConfidence} suffix="%" decimals={1} />} sublabel="Best rule" icon={<Target className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Best Lift" value={<CountUp to={MARKET_BASKET.maxLift} decimals={2} />} sublabel={`Industry avg: ${MARKET_BASKET.industryAvgLift}x`} icon={<Zap className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Max Support" value={<CountUp to={MARKET_BASKET.maxSupport} suffix="%" decimals={1} />} sublabel={`Industry avg: ${MARKET_BASKET.industryAvgSupport}%`} icon={<ShoppingCart className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Bundle Revenue" value={<CountUp to={topRevenue} prefix="$" compact />} sublabel="Top rules opportunity" icon={<TrendingUp className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Algorithm" value={MARKET_BASKET.algorithm} sublabel="Association mining" icon={<Award className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Lift by Rule" subtitle="Top association rule lift scores (higher = stronger)" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={rules} layout="vertical">
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" stroke={chartTheme.axis} tick={labelStyle} domain={[0, 8]} />
              <YAxis type="category" dataKey="antecedent" stroke={chartTheme.axis} tick={{ ...labelStyle, fontSize: 9 }} width={170} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v.toFixed(2)}x`, "Lift"]} />
              <Bar dataKey="lift" radius={[0, 6, 6, 0]}>
                {rules.map((_, i) => <Cell key={i} fill={`oklch(${0.78 - i * 0.03} ${0.20 - i * 0.01} ${195 + i * 22})`} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Confidence vs Support Scatter" subtitle="Rule quality map — size = revenue opportunity" delay={0.15}>
          <ResponsiveContainer width="100%" height={260}>
            <ScatterChart>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="support" name="Support" stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} label={{ value: "Support %", position: "insideBottom", fill: "oklch(0.7 0.03 260)", fontSize: 10, offset: -5 }} />
              <YAxis dataKey="confidence" name="Confidence" stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} label={{ value: "Confidence %", angle: -90, position: "insideLeft", fill: "oklch(0.7 0.03 260)", fontSize: 10 }} />
              <ZAxis dataKey="lift" range={[60, 250]} name="Lift" />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number, name) => [`${typeof v === "number" ? v.toFixed(2) : v}`, name]} />
              <Scatter data={rules} fill="oklch(0.78 0.18 195)" />
            </ScatterChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      <Panel title="Top Association Rules — Ranked by Lift" subtitle="Real Apriori-mined rules from product data" delay={0.25}>
        <div className="space-y-3">
          {rules.map((rule, i) => (
            <motion.div key={i} initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.07 }}
              className="rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="flex items-start gap-3">
                <div className="text-xl shrink-0">{["🥇","🥈","🥉","4️⃣","5️⃣"][i]}</div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold truncate">{rule.antecedent}</div>
                  <div className="mt-0.5 text-xs text-muted-foreground truncate">→ {rule.consequent}</div>
                </div>
                <div className="flex gap-4 shrink-0 text-center">
                  <div>
                    <div className="text-[10px] text-muted-foreground">Confidence</div>
                    <div className="font-bold" style={{ color: "var(--success)" }}>{rule.confidence}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-muted-foreground">Lift</div>
                    <div className="font-bold text-gradient">{rule.lift}x</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-muted-foreground">Support</div>
                    <div className="font-bold">{rule.support}%</div>
                  </div>
                  <span className="self-center rounded-full px-2 py-0.5 text-[10px] font-bold text-primary-foreground"
                    style={{ background: rule.lift > 6 ? "var(--gradient-success)" : "var(--gradient-gold)" }}>
                    {rule.lift > 6 ? "HOT" : "STRONG"}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* vs Industry */}
        <div className="mt-4 grid grid-cols-3 gap-3 border-t pt-4" style={{ borderColor: "var(--glass-border)" }}>
          {[
            { label: "Our Confidence", our: MARKET_BASKET.maxConfidence, ind: MARKET_BASKET.industryAvgConfidence, unit: "%" },
            { label: "Our Lift", our: MARKET_BASKET.maxLift, ind: MARKET_BASKET.industryAvgLift, unit: "x" },
            { label: "Our Support", our: MARKET_BASKET.maxSupport, ind: MARKET_BASKET.industryAvgSupport, unit: "%" },
          ].map((m) => (
            <div key={m.label} className="rounded-xl border p-3 text-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="text-[10px] text-muted-foreground uppercase tracking-wider">{m.label}</div>
              <div className="mt-1 text-2xl font-bold text-gradient">{m.our}{m.unit}</div>
              <div className="text-[11px]" style={{ color: "var(--success)" }}>
                {((m.our / m.ind - 1) * 100).toFixed(0)}% above industry avg
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
