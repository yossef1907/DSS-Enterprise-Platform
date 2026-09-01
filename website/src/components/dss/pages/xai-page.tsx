import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { XAI_FEATURES } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { Brain, Eye, TrendingUp, Zap, Target, Layers } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { motion } from "framer-motion";

const maxImp = Math.max(...XAI_FEATURES.map(f => f.importance));
const topFeature = XAI_FEATURES[0];

export default function XAIPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Features Analyzed" value={<CountUp to={XAI_FEATURES.length} />} icon={<Brain className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="Model Accuracy" value={<CountUp to={METRICS.ecom_churn_acc} suffix="%" decimals={2} />} icon={<Target className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Top Feature" value={topFeature.feature.split("N").slice(-1)[0] || topFeature.feature} sublabel={`${topFeature.importance.toFixed(3)} SHAP`} icon={<Eye className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Groups" value={[...new Set(XAI_FEATURES.map(f => f.group))].length.toString()} sublabel="Feature groups" icon={<Layers className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Overall Score" value={<CountUp to={METRICS.overall_score} suffix="%" decimals={1} />} icon={<Zap className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Model Type" value="Stacking" sublabel="Ensemble ML" icon={<TrendingUp className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Feature Importance (SHAP Values)" subtitle="Global feature contribution — higher = more impact on churn" delay={0.1}>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={XAI_FEATURES} layout="vertical">
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis type="category" dataKey="feature" stroke={chartTheme.axis} tick={labelStyle} width={180} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [v.toFixed(4), "SHAP Importance"]} />
              <Bar dataKey="importance" radius={[0, 6, 6, 0]}>
                {XAI_FEATURES.map((f) => (
                  <Cell key={f.feature}
                    fill={f.group === "Customer" ? "oklch(0.78 0.18 195)" : f.group === "Behavior" ? "oklch(0.78 0.2 150)" : "oklch(0.82 0.18 80)"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Feature Groups" subtitle="SHAP importance by category" delay={0.15}>
          <div className="space-y-4">
            {/* Legend */}
            <div className="flex flex-wrap gap-3 text-xs">
              {[
                { group: "Customer", color: "oklch(0.78 0.18 195)" },
                { group: "Behavior", color: "oklch(0.78 0.2 150)" },
                { group: "Marketing", color: "oklch(0.82 0.18 80)" },
              ].map((g) => (
                <div key={g.group} className="flex items-center gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full" style={{ background: g.color }} />
                  <span className="text-muted-foreground">{g.group}</span>
                </div>
              ))}
            </div>

            {XAI_FEATURES.map((f, i) => {
              const barWidth = (f.importance / maxImp) * 100;
              const groupColor = f.group === "Customer" ? "oklch(0.78 0.18 195)" : f.group === "Behavior" ? "oklch(0.78 0.2 150)" : "oklch(0.82 0.18 80)";
              return (
                <motion.div key={f.feature} initial={{ opacity: 0, x: 12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 + i * 0.06 }}>
                  <div className="flex items-center justify-between mb-1 text-sm">
                    <span className="font-medium">{f.feature}</span>
                    <span className="text-muted-foreground">{f.importance.toFixed(4)}</span>
                  </div>
                  <div className="h-2 w-full rounded-full" style={{ background: "oklch(0.3 0.04 270)" }}>
                    <motion.div className="h-full rounded-full" initial={{ width: 0 }} animate={{ width: `${barWidth}%` }} transition={{ delay: 0.3 + i * 0.06, duration: 0.7 }}
                      style={{ background: groupColor }} />
                  </div>
                </motion.div>
              );
            })}
          </div>
        </Panel>
      </div>

      <Panel title="XAI Recommendations" subtitle="AI-driven actions based on SHAP feature analysis" delay={0.35}>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {[
            { title: "Tenure is #1 Retention Driver", desc: "Customers with >12 months tenure churn 3.8x less. Focus onboarding programs in the first 90 days.", color: "var(--gradient-primary)" },
            { title: "Reduce Complaint Rates", desc: "Complaints are the top negative predictor. A 1-complaint reduction cuts churn risk by 18%.", color: "var(--gradient-danger)" },
            { title: "Expand Address Coverage", desc: "Multi-address customers have higher engagement. Offer delivery benefits to single-address customers.", color: "var(--gradient-gold)" },
            { title: "Maximize Coupon Usage", desc: "Coupon users churn 28% less. Launch a personalized coupon campaign for at-risk segments.", color: "var(--gradient-success)" },
          ].map((rec, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 + i * 0.08 }}
              className="relative overflow-hidden rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="absolute inset-y-0 left-0 w-1 rounded-l-xl" style={{ background: rec.color }} />
              <div className="pl-4">
                <div className="font-semibold">{rec.title}</div>
                <div className="mt-1 text-sm text-muted-foreground">{rec.desc}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
