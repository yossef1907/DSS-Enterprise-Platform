import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { ML_MODELS, CHURN_DATA, MARKET_BASKET, PRODUCT_LAUNCH, PROJECT_METRICS } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtNum } from "@/lib/dss-utils";
import { BarChart3, Brain, Zap, Award, CheckCircle2, Activity } from "lucide-react";
import {
  ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { motion } from "framer-motion";
import { Gauge } from "@/components/dss/Gauge";

const radarData = ML_MODELS.map((m) => ({ module: m.name.split(" ")[0], score: m.accuracy, accuracy: m.accuracy }));
const avgAcc = ML_MODELS.reduce((s, m) => s + m.accuracy, 0) / ML_MODELS.length;
const production = ML_MODELS.filter(m => m.rating === "Exceptional" || m.rating === "Excellent").length;

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Models in Production" value={<CountUp to={production} />} icon={<CheckCircle2 className="h-4 w-4" />} accent="success" delay={0} />
        <StatCard label="Overall Score" value={<CountUp to={PROJECT_METRICS.overallScore} suffix="%" decimals={1} />} icon={<Award className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Avg ML Accuracy" value={<CountUp to={avgAcc} suffix="%" decimals={2} />} icon={<Brain className="h-4 w-4" />} accent="primary" delay={0.1} />
        <StatCard label="MB Rules" value={<CountUp to={MARKET_BASKET.totalRules} />} sublabel="Discovered" icon={<BarChart3 className="h-4 w-4" />} accent="success" delay={0.15} />
        <StatCard label="Total Rows" value={<CountUp to={PROJECT_METRICS.totalRows} compact />} icon={<Zap className="h-4 w-4" />} accent="primary" delay={0.2} />
        <StatCard label="Models Total" value={<CountUp to={ML_MODELS.length} />} icon={<Activity className="h-4 w-4" />} accent="gold" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="ML Accuracy Radar" subtitle="Accuracy per model — outer ring = 100%" delay={0.1}>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke={chartTheme.grid} />
              <PolarAngleAxis dataKey="module" tick={labelStyle} />
              <Radar name="Accuracy" dataKey="accuracy" stroke="oklch(0.78 0.18 195)" fill="oklch(0.78 0.18 195)" fillOpacity={0.22} strokeWidth={2} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "Accuracy"]} />
            </RadarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Churn Dataset Overview" subtitle="Churn rate & model accuracy per domain" delay={0.15}>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={CHURN_DATA}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="dataset" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number, name) => [`${v}%`, name === "churnRate" ? "Churn Rate" : "Accuracy"]} />
              <Bar dataKey="churnRate" name="churnRate" radius={[4, 4, 0, 0]} fill="oklch(0.66 0.24 25)" />
              <Bar dataKey="accuracy" name="accuracy" radius={[4, 4, 0, 0]} fill="oklch(0.78 0.2 150)" opacity={0.7} />
            </BarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      {/* Summary cards */}
      <Panel title="Platform Analytics Summary" subtitle="Key metrics across all modules" delay={0.3}>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {[
            { label: "Basket Rules", val: `${MARKET_BASKET.totalRules}`, sub: "Apriori mined", color: "var(--gradient-primary)" },
            { label: "Best Lift", val: `${MARKET_BASKET.maxLift}x`, sub: "vs 3.5x industry avg", color: "var(--gradient-gold)" },
            { label: "GO Scenarios", val: `${PRODUCT_LAUNCH.goDecisions}`, sub: `of ${PRODUCT_LAUNCH.totalScenarios} tested`, color: "var(--gradient-success)" },
            { label: "Best Success", val: `${PRODUCT_LAUNCH.bestSuccess}%`, sub: "Product launch peak", color: "var(--gradient-success)" },
            { label: "Total Datasets", val: `${PROJECT_METRICS.totalDatasets}`, sub: `${PROJECT_METRICS.realDatasets} real`, color: "var(--gradient-primary)" },
            { label: "DB Tables", val: `${PROJECT_METRICS.databaseTables}`, sub: `${PROJECT_METRICS.databaseSizeMB}MB`, color: "var(--gradient-gold)" },
            { label: "Exceptional Models", val: `${ML_MODELS.filter(m => m.rating === "Exceptional").length}`, sub: "99%+ accuracy", color: "var(--gradient-success)" },
            { label: "Platform Rating", val: PROJECT_METRICS.rating, sub: PROJECT_METRICS.industry, color: "var(--gradient-gold)" },
          ].map((item, i) => (
            <motion.div key={item.label} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.35 + i * 0.05 }}
              className="relative overflow-hidden rounded-xl border p-3 text-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: item.color }} />
              <div className="text-[10px] text-muted-foreground uppercase tracking-wider">{item.label}</div>
              <div className="mt-1.5 text-xl font-bold text-gradient">{item.val}</div>
              <div className="mt-0.5 text-[10px] text-muted-foreground">{item.sub}</div>
            </motion.div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
