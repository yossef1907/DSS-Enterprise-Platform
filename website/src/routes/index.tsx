import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Trophy, Users, DollarSign, Target, TrendingUp, Star, Zap, Sparkles, Award,
} from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  PieChart, Pie, Cell, AreaChart, Area, LineChart, Line, Legend,
} from "recharts";
import { PROJECT_METRICS, ML_MODELS, MARKETING_ROI, CLV_SEGMENTS, MARKET_BASKET } from "@/data/dss";
import { CountUp } from "@/components/dss/CountUp";
import { StatCard } from "@/components/dss/StatCard";
import { Panel } from "@/components/dss/Panel";
import { PageHeader } from "@/components/dss/PageHeader";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { fmtCurrency } from "@/lib/dss-utils";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Executive Command Center · DSS Pro" },
      { name: "description", content: "Premium decision support system overview with 99.6% project score." },
    ],
  }),
  component: Index,
});

function Index() {
  const sparkline = Array.from({ length: 14 }, (_, i) => ({
    x: i,
    v: 800 + Math.sin(i / 1.6) * 120 + i * 22,
  }));

  return (
    <div className="space-y-8">
      <HeroBanner />

      <PageHeader
        eyebrow="EXECUTIVE COMMAND CENTER"
        title="Mission Control"
        subtitle="A live, top-1% snapshot of every revenue, customer, and intelligence signal across the platform."
      />

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatCard
          label="Total Revenue Portfolio"
          accent="gold"
          icon={<DollarSign className="h-5 w-5" />}
          value={<><span>$</span><CountUp to={1.08} decimals={2} /><span>B</span></>}
          sublabel={`Aggregated CLV across ${PROJECT_METRICS.totalCustomers.toLocaleString()} customers`}
          change={MARKETING_ROI.revenueGrowth}
          delay={0.05}
        >
          <ResponsiveContainer width="100%" height={50}>
            <AreaChart data={sparkline}>
              <defs>
                <linearGradient id="sp1" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="oklch(0.85 0.16 90)" stopOpacity={0.7} />
                  <stop offset="100%" stopColor="oklch(0.85 0.16 90)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area type="monotone" dataKey="v" stroke="oklch(0.85 0.16 90)" strokeWidth={2} fill="url(#sp1)" />
            </AreaChart>
          </ResponsiveContainer>
        </StatCard>

        <StatCard
          label="Total Customers"
          accent="primary"
          icon={<Users className="h-5 w-5" />}
          value={<CountUp to={PROJECT_METRICS.totalCustomers} />}
          sublabel="Across 22 datasets · 109 tables"
          change={12.4}
          delay={0.1}
        />

        <StatCard
          label="Best Model Accuracy"
          accent="success"
          icon={<Target className="h-5 w-5" />}
          value={<><CountUp to={99.76} decimals={2} />%</>}
          sublabel="Marketing Stacking · Exceptional"
          delay={0.15}
        >
          <CircularBar value={99.76} />
        </StatCard>

        <StatCard
          label="Market Basket Confidence"
          accent="accent"
          icon={<Zap className="h-5 w-5" />}
          value={<><CountUp to={91.6} decimals={1} />%</>}
          sublabel={`${MARKET_BASKET.totalRules} rules · max lift ${MARKET_BASKET.maxLift}x`}
          delay={0.2}
        />

        <StatCard
          label="Revenue Growth"
          accent="success"
          icon={<TrendingUp className="h-5 w-5" />}
          value={<><span>+</span><CountUp to={383.6} decimals={1} />%</>}
          sublabel="Post-optimization vs baseline"
          change={383.6}
          delay={0.25}
        />

        <StatCard
          label="Project Score"
          accent="gold"
          icon={<Star className="h-5 w-5" />}
          value={<><CountUp to={99.6} decimals={1} />/100</>}
          sublabel="OUTSTANDING · Top 1% globally"
          delay={0.3}
        >
          <div className="flex gap-1">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star key={i} className="h-4 w-4" style={{ fill: "var(--gold)", color: "var(--gold)" }} />
            ))}
          </div>
        </StatCard>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Panel title="ML Model Leaderboard" subtitle="Accuracy across the production ensemble" delay={0.35} className="lg:col-span-2">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={ML_MODELS} layout="vertical" margin={{ left: 30 }}>
              <defs>
                <linearGradient id="bar1" x1="0" x2="1" y1="0" y2="0">
                  <stop offset="0%" stopColor="oklch(0.78 0.18 195)" />
                  <stop offset="100%" stopColor="oklch(0.7 0.22 320)" />
                </linearGradient>
              </defs>
              <CartesianGrid stroke={chartTheme.grid} horizontal={false} />
              <XAxis type="number" domain={[80, 100]} stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis type="category" dataKey="name" stroke={chartTheme.axis} tick={labelStyle} width={150} />
              <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "oklch(0.7 0.05 260 / 0.06)" }} />
              <Bar dataKey="accuracy" fill="url(#bar1)" radius={[0, 8, 8, 0]} animationDuration={1400} />
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="CLV Segments" subtitle="Customer value distribution" delay={0.4}>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={CLV_SEGMENTS}
                dataKey="customers"
                nameKey="segment"
                innerRadius={60}
                outerRadius={110}
                paddingAngle={3}
                animationDuration={1400}
              >
                {CLV_SEGMENTS.map((s) => (
                  <Cell key={s.segment} fill={s.color} stroke="oklch(0.18 0.035 270)" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} />
              <Legend wrapperStyle={{ fontSize: 11, color: "var(--color-muted-foreground)" }} />
            </PieChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      <Panel title="ROI Transformation" subtitle="From -41.1% to +184.97% — the full optimization arc" delay={0.45}>
        <RoiTransform />
      </Panel>
    </div>
  );
}

function HeroBanner() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative overflow-hidden rounded-2xl border-2 animate-pulse-glow"
      style={{
        borderColor: "oklch(0.85 0.16 90 / 0.5)",
        background:
          "radial-gradient(800px 200px at 20% 50%, oklch(0.85 0.16 90 / 0.18), transparent 70%), " +
          "radial-gradient(800px 200px at 80% 50%, oklch(0.7 0.22 320 / 0.18), transparent 70%), " +
          "var(--glass-bg)",
        backdropFilter: "blur(20px)",
      }}
    >
      {/* particle dots */}
      <div className="pointer-events-none absolute inset-0">
        {Array.from({ length: 24 }).map((_, i) => (
          <motion.span
            key={i}
            className="absolute h-1 w-1 rounded-full"
            style={{
              left: `${(i * 37) % 100}%`,
              top: `${(i * 53) % 100}%`,
              background: "var(--gold)",
              boxShadow: "0 0 8px var(--gold)",
            }}
            animate={{ opacity: [0.2, 1, 0.2], y: [0, -8, 0] }}
            transition={{ duration: 3 + (i % 4), repeat: Infinity, delay: i * 0.15 }}
          />
        ))}
      </div>
      <div className="relative flex flex-wrap items-center justify-between gap-6 px-8 py-7">
        <div className="flex items-center gap-5">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl glow-gold" style={{ background: "var(--gradient-gold)" }}>
            <Trophy className="h-8 w-8 text-primary-foreground" />
          </div>
          <div>
            <div className="text-[11px] font-bold tracking-[0.4em] text-muted-foreground">PROJECT INTELLIGENCE SCORE</div>
            <div className="mt-1 flex items-baseline gap-3">
              <span className="text-5xl font-bold text-gradient-gold">
                <CountUp to={PROJECT_METRICS.overallScore} decimals={1} />%
              </span>
              <span className="text-xl font-bold tracking-[0.2em] text-foreground uppercase">{PROJECT_METRICS.rating}</span>
              <span className="rounded-full px-3 py-1 text-xs font-bold" style={{ background: "var(--gradient-gold)", color: "var(--primary-foreground)" }}>
                TOP 1% GLOBALLY
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge icon={<Sparkles className="h-3.5 w-3.5" />} text="22 DATASETS" />
          <Badge icon={<Award className="h-3.5 w-3.5" />} text="109 TABLES" />
          <Badge icon={<Star className="h-3.5 w-3.5" />} text="19 NOTEBOOKS" />
        </div>
      </div>
    </motion.div>
  );
}

function Badge({ icon, text }: { icon: React.ReactNode; text: string }) {
  return (
    <div className="flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[11px] font-bold tracking-[0.15em]"
      style={{ borderColor: "var(--glass-border)", background: "oklch(0.18 0.04 270 / 0.4)" }}>
      {icon}
      {text}
    </div>
  );
}

function CircularBar({ value }: { value: number }) {
  const r = 18, c = 2 * Math.PI * r;
  return (
    <div className="flex items-center gap-2">
      <svg width={48} height={48} className="-rotate-90">
        <circle cx="24" cy="24" r={r} stroke="oklch(0.4 0.04 270 / 0.4)" strokeWidth="4" fill="none" />
        <motion.circle
          cx="24" cy="24" r={r} stroke="var(--success)" strokeWidth="4" fill="none" strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: c * (1 - value / 100) }}
          transition={{ duration: 1.4 }}
        />
      </svg>
      <div className="text-xs text-muted-foreground">Top performer</div>
    </div>
  );
}

function RoiTransform() {
  const data = [
    { phase: "Q1 Baseline", roi: -41.1 },
    { phase: "Q2 Discovery", roi: -18 },
    { phase: "Q3 Optimization", roi: 65 },
    { phase: "Q4 Scaling", roi: 132 },
    { phase: "Now", roi: 184.97 },
    { phase: "Best Combo", roi: 421.18 },
  ];
  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.6fr_1fr]">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <defs>
            <linearGradient id="roiL" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0%" stopColor="oklch(0.66 0.24 25)" />
              <stop offset="50%" stopColor="oklch(0.82 0.18 80)" />
              <stop offset="100%" stopColor="oklch(0.78 0.2 150)" />
            </linearGradient>
          </defs>
          <CartesianGrid stroke={chartTheme.grid} />
          <XAxis dataKey="phase" stroke={chartTheme.axis} tick={labelStyle} />
          <YAxis stroke={chartTheme.axis} tick={labelStyle} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => `${v.toFixed(2)}%`} />
          <Line
            type="monotone" dataKey="roi" stroke="url(#roiL)" strokeWidth={3}
            dot={{ r: 5, fill: "oklch(0.78 0.18 195)", strokeWidth: 0 }}
            activeDot={{ r: 8 }} animationDuration={1600}
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="grid grid-cols-2 gap-3">
        <MetricBox label="Before" value="-41.1%" tone="danger" />
        <MetricBox label="After" value="+184.97%" tone="success" />
        <MetricBox label="Best Combo" value="+421.18%" tone="gold" />
        <MetricBox label="Revenue Δ" value={fmtCurrency(MARKETING_ROI.revenueAfter - MARKETING_ROI.revenueBefore, { compact: true })} tone="primary" />
      </div>
    </div>
  );
}

function MetricBox({ label, value, tone }: { label: string; value: string; tone: string }) {
  const bg =
    tone === "danger" ? "var(--gradient-danger)" :
    tone === "success" ? "var(--gradient-success)" :
    tone === "gold" ? "var(--gradient-gold)" : "var(--gradient-primary)";
  return (
    <div className="glass relative overflow-hidden p-4">
      <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: bg }} />
      <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">{label}</div>
      <div className="mt-1 text-2xl font-bold">{value}</div>
    </div>
  );
}
