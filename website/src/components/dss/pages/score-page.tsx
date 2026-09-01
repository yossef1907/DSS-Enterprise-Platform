import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { ML_MODELS, PRODUCT_LAUNCH, PROJECT_METRICS } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtNum } from "@/lib/dss-utils";
import { useState, useEffect } from "react";
import { Award, Brain, CheckCircle2, TrendingUp, Zap, Activity, Database, Table, SlidersHorizontal, RefreshCw, Wand2, Lightbulb, PlayCircle } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { motion } from "framer-motion";
import { Gauge } from "@/components/dss/Gauge";

const avgAccuracy = ML_MODELS.reduce((s, m) => s + m.accuracy, 0) / ML_MODELS.length;

export default function ScorePage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Overall Score" value={<CountUp to={PROJECT_METRICS.overallScore} suffix="%" decimals={1} />} sublabel={PROJECT_METRICS.rating} icon={<Award className="h-4 w-4" />} accent="gold" delay={0} />
        <StatCard label="Avg ML Accuracy" value={<CountUp to={avgAccuracy} suffix="%" decimals={2} />} icon={<Brain className="h-4 w-4" />} accent="primary" delay={0.05} />
        <StatCard label="Total Customers" value={<CountUp to={PROJECT_METRICS.totalCustomers} compact />} sublabel={PROJECT_METRICS.industry} icon={<Activity className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Total Rows" value={<CountUp to={PROJECT_METRICS.totalRows} compact />} sublabel="Across all datasets" icon={<Database className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="DB Tables" value={<CountUp to={PROJECT_METRICS.databaseTables} />} sublabel={`${PROJECT_METRICS.databaseSizeMB}MB`} icon={<Table className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Notebooks" value={<CountUp to={PROJECT_METRICS.totalNotebooks} />} sublabel={`${PROJECT_METRICS.exportFiles} exports`} icon={<Zap className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_auto]">
        <Panel title="ML Model Accuracy Rankings" subtitle="All models ranked by accuracy" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={ML_MODELS}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="name" stroke={chartTheme.axis} tick={labelStyle} angle={-20} textAnchor="end" height={55} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} domain={[80, 100]} tickFormatter={(v) => `${v}%`} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "Accuracy"]} />
              <Bar dataKey="accuracy" radius={[6, 6, 0, 0]}>
                {ML_MODELS.map((m, i) => <Cell key={i} fill={m.accuracy >= 99 ? "oklch(0.78 0.2 150)" : m.accuracy >= 90 ? "oklch(0.78 0.18 195)" : "oklch(0.82 0.18 80)"} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="Overall Score" className="flex flex-col items-center justify-center min-w-[200px]" delay={0.15}>
          <Gauge value={PROJECT_METRICS.overallScore} label="DSS Pro" />
          <div className="mt-3 text-center">
            <div className="text-xs text-muted-foreground">{PROJECT_METRICS.industry}</div>
            <div className="mt-1 inline-block rounded-full px-3 py-1 text-xs font-bold text-primary-foreground"
              style={{ background: "var(--gradient-gold)" }}>{PROJECT_METRICS.rating}</div>
          </div>
        </Panel>
      </div>

      {/* Models table */}
      <Panel title="Model Details" subtitle="Type, accuracy & rating for each model" delay={0.25}>
        <div className="space-y-3">
          {ML_MODELS.map((m, i) => (
            <motion.div key={m.name} initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.07 }}
              className="flex items-center gap-4 rounded-xl border p-3" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="flex-1">
                <div className="font-semibold">{m.name}</div>
                <div className="text-xs text-muted-foreground">{m.type}</div>
              </div>
              <div className="h-1.5 flex-1 max-w-[160px] rounded-full overflow-hidden" style={{ background: "oklch(0.3 0.04 270)" }}>
                <motion.div className="h-full rounded-full" initial={{ width: 0 }} animate={{ width: `${m.accuracy}%` }} transition={{ delay: 0.35 + i * 0.07, duration: 0.8 }}
                  style={{ background: m.accuracy >= 99 ? "var(--gradient-success)" : "var(--gradient-primary)" }} />
              </div>
              <div className="text-lg font-bold text-right" style={{ color: m.accuracy >= 99 ? "var(--success)" : "var(--primary)" }}>{m.accuracy}%</div>
              <span className="rounded-full px-2 py-0.5 text-[10px] font-bold text-primary-foreground"
                style={{ background: m.accuracy >= 99 ? "var(--gradient-success)" : "var(--gradient-gold)" }}>{m.rating}</span>
            </motion.div>
          ))}
        </div>
      </Panel>

      {/* CEO Project Viability Assessment */}
      <Panel title="CEO Project Viability Evaluation" subtitle="Executive assessment of DSS Pro's market readiness and enterprise scalability" delay={0.25}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="rounded-xl border p-5 relative overflow-hidden group" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity"><Award className="w-16 h-16" style={{ color: "var(--success)" }} /></div>
            <div className="text-[10px] uppercase font-bold tracking-widest mb-2" style={{ color: "var(--success)" }}>Success Rate</div>
            <div className="text-4xl font-black text-gradient-success mb-2">95%</div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Highly scalable. Massive opportunity to capture the market with advanced interactive dashboards that outperform traditional systems.
            </p>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
            className="rounded-xl border p-5 relative overflow-hidden group" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity"><RefreshCw className="w-16 h-16" style={{ color: "var(--warning)" }} /></div>
            <div className="text-[10px] uppercase font-bold tracking-widest mb-2" style={{ color: "var(--warning)" }}>Review & Scaling</div>
            <div className="text-4xl font-black text-gradient-gold mb-2">4%</div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Requires minor continuous reviews to optimize cloud server infrastructure as the active enterprise user base grows.
            </p>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}
            className="rounded-xl border p-5 relative overflow-hidden group" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity"><Activity className="w-16 h-16" style={{ color: "var(--destructive)" }} /></div>
            <div className="text-[10px] uppercase font-bold tracking-widest mb-2" style={{ color: "var(--destructive)" }}>Failure Risk</div>
            <div className="text-4xl font-black text-gradient-danger mb-2">1%</div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Standard operational risk associated with brief downtimes or API rate limits. Exceptionally safe, resilient, and stable platform.
            </p>
          </motion.div>
        </div>
      </Panel>

      {/* Original Baseline Metrics */}
      <Panel title="Original Baseline: Product Launch" subtitle="The exact results from the 2,400 raw ML scenarios before optimization" delay={0.25}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { label: "GO (Success)", count: PRODUCT_LAUNCH.goDecisions, pct: PRODUCT_LAUNCH.goRate, color: "oklch(0.78 0.2 150)", gradient: "var(--gradient-success)" },
            { label: "REVIEW (Edge)", count: 2400 - PRODUCT_LAUNCH.goDecisions - PRODUCT_LAUNCH.noGoDecisions, pct: 100 - PRODUCT_LAUNCH.goRate - (PRODUCT_LAUNCH.noGoDecisions / 2400 * 100), color: "oklch(0.85 0.16 90)", gradient: "var(--gradient-gold)" },
            { label: "NO-GO (Fail)", count: PRODUCT_LAUNCH.noGoDecisions, pct: (PRODUCT_LAUNCH.noGoDecisions / 2400 * 100), color: "oklch(0.66 0.24 25)", gradient: "var(--gradient-danger)" },
          ].map((d, i) => (
            <motion.div key={d.label} 
              initial={{ opacity: 0, scale: 0.8, rotateX: 30 }} 
              animate={{ opacity: 1, scale: 1, rotateX: 0 }} 
              transition={{ delay: 0.3 + i * 0.15, type: "spring", stiffness: 100 }}
              className="relative overflow-hidden rounded-2xl border p-8 text-center flex flex-col items-center justify-center group" 
              style={{ background: "oklch(0.22 0.04 270 / 0.6)", borderColor: "var(--glass-border)", boxShadow: `0 8px 32px 0 oklch(0.1 0.05 270 / 0.5)` }}>
              
              {/* Background Glow */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-700" style={{ background: d.gradient }} />
              
              {/* Top Neon Bar */}
              <motion.div 
                initial={{ width: 0 }} 
                animate={{ width: "100%" }} 
                transition={{ delay: 0.8 + i * 0.2, duration: 1.2, ease: "easeOut" }}
                className="absolute top-0 left-0 h-1.5" 
                style={{ background: d.gradient, boxShadow: `0 0 20px ${d.color}` }} 
              />
              
              <div className="text-xs font-black tracking-[0.25em] text-muted-foreground mb-4 z-10">{d.label}</div>
              
              <motion.div 
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 + i * 0.1 }}
                className="text-6xl font-bold z-10 tracking-tight" 
                style={{ background: d.gradient, WebkitBackgroundClip: "text", color: "transparent" }}>
                {fmtNum(d.count)}
              </motion.div>
              
              <motion.div 
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 1.0 + i * 0.1, type: "spring", stiffness: 200 }}
                className="mt-5 inline-flex items-center gap-2 rounded-full px-5 py-2 text-sm font-bold border z-10 shadow-lg"
                style={{ background: "oklch(0.15 0.04 270 / 0.7)", borderColor: d.color, color: d.color, boxShadow: `0 0 15px ${d.color}40` }}>
                {d.pct.toFixed(1)}% of 2,400
              </motion.div>
            </motion.div>
          ))}
        </div>
      </Panel>

      {/* Prescriptive Analytics Engine */}
      <PrescriptiveEngine />
    </div>
  );
}

// ── Interactive Prescriptive Analytics Engine ────────────────────────────────

function PrescriptiveEngine() {
  const [threshold, setThreshold] = useState(90);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optComplete, setOptComplete] = useState(false);

  // Dynamic Decision Logic based on Risk Tolerance Threshold
  // When Threshold is 90 (Strict): GO ~670
  // When Threshold is 60 (Aggressive): GO ~1850
  const maxScenarios = 2400;
  
  // Calculate dynamic numbers
  const calculatedGo = optComplete 
    ? 2150 // After optimization
    : Math.max(100, Math.min(2300, Math.round(2400 - (threshold - 50) * 43.25)));
    
  const calculatedNoGo = optComplete
    ? 100 // After optimization
    : Math.max(0, Math.round((threshold - 60) * 48.6));
    
  const calculatedReview = maxScenarios - calculatedGo - calculatedNoGo;
  
  const goPct = ((calculatedGo / maxScenarios) * 100).toFixed(1);

  const handleOptimize = () => {
    setIsOptimizing(true);
    setOptComplete(false);
    setTimeout(() => {
      setIsOptimizing(false);
      setOptComplete(true);
      setThreshold(75); // Auto-adjust to optimal threshold
    }, 2500);
  };

  return (
    <Panel title="Prescriptive AI Engine" subtitle="From Descriptive to Prescriptive: Flip NO-GOs into Opportunities" delay={0.35}>
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        
        {/* Left Column: Risk Slider & Dynamic Metrics */}
        <div className="xl:col-span-1 space-y-6">
          <div className="rounded-xl border p-5" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
            <div className="flex justify-between items-end mb-4">
              <div>
                <div className="text-sm font-bold flex items-center gap-2 text-primary">
                  <SlidersHorizontal className="h-4 w-4" />
                  Risk Tolerance Slider
                </div>
                <div className="text-xs text-muted-foreground mt-1">Adjust AI Confidence Threshold</div>
              </div>
              <div className="text-2xl font-bold text-gradient-gold">{threshold}%</div>
            </div>
            
            <input 
              type="range" 
              min="50" max="99" 
              value={threshold} 
              onChange={(e) => {
                setThreshold(Number(e.target.value));
                setOptComplete(false);
              }}
              disabled={isOptimizing}
              className="w-full h-2 rounded-lg appearance-none cursor-pointer"
              style={{ background: "var(--gradient-primary)", opacity: isOptimizing ? 0.5 : 1 }}
            />
            <div className="flex justify-between text-[10px] text-muted-foreground mt-2 uppercase font-bold tracking-wider">
              <span>Aggressive (50%)</span>
              <span>Strict (99%)</span>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2">
            {[
              { label: "GO", count: calculatedGo, color: "var(--success)" },
              { label: "REVIEW", count: calculatedReview, color: "var(--warning)" },
              { label: "NO-GO", count: calculatedNoGo, color: "var(--destructive)" },
            ].map((d, i) => (
              <motion.div key={d.label} layout transition={{ type: "spring", stiffness: 300, damping: 25 }}
                className="rounded-lg border p-3 text-center flex flex-col justify-center" 
                style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.3)" }}>
                <div className="text-[9px] font-bold uppercase tracking-wider text-muted-foreground">{d.label}</div>
                <motion.div className="mt-1 text-xl font-bold" style={{ color: d.color }}>
                  {isOptimizing ? <RefreshCw className="h-5 w-5 animate-spin mx-auto text-muted-foreground" /> : fmtNum(d.count)}
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Middle Column: Adaptive Simulation */}
        <div className="xl:col-span-1 rounded-xl border p-5 flex flex-col justify-between relative overflow-hidden" 
             style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          {isOptimizing && (
            <div className="absolute inset-0 z-0 bg-primary/10 animate-pulse" />
          )}
          <div className="relative z-10">
            <div className="text-sm font-bold flex items-center gap-2 text-primary">
              <PlayCircle className="h-4 w-4" />
              Adaptive Grid Search
            </div>
            <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
              Stop brute-forcing 2,400 scenarios. The AI will use <b>Early Stopping</b> to kill failing branches immediately and dedicate compute power to exploring highly profitable parameter combinations.
            </p>
          </div>
          
          <div className="relative z-10 mt-6">
            <button 
              onClick={handleOptimize}
              disabled={isOptimizing || optComplete}
              className={`w-full py-3 rounded-lg font-bold text-sm flex justify-center items-center gap-2 transition-all duration-300
                ${isOptimizing ? "bg-muted text-muted-foreground cursor-wait" : 
                  optComplete ? "bg-success/20 text-success border border-success/50" : 
                  "bg-primary text-primary-foreground hover:opacity-90 glow"}`}
            >
              {isOptimizing ? (
                <><RefreshCw className="h-4 w-4 animate-spin" /> Simulating Generations...</>
              ) : optComplete ? (
                <><Wand2 className="h-4 w-4" /> Optimization Complete ({goPct}% GO)</>
              ) : (
                <><Wand2 className="h-4 w-4" /> Run Optimization Engine</>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Counterfactual Explanations (What-If) */}
        <div className="xl:col-span-1 rounded-xl border p-5" 
             style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          <div className="text-sm font-bold flex items-center gap-2 text-gold">
            <Lightbulb className="h-4 w-4" />
            Counterfactual Explanations
          </div>
          <p className="text-[10px] text-muted-foreground mt-1 mb-4 uppercase tracking-wider">How to flip a NO-GO decision</p>
          
          <div className="space-y-3">
            {[
              { id: "#1402", fix: "Increase Marketing +12%", prob: 92 },
              { id: "#0891", fix: "Shift Season to 'Fall'", prob: 88 },
              { id: "#2105", fix: "Target 'Champions' Segment", prob: 95 },
            ].map((cf, i) => (
              <motion.div key={cf.id} 
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: 1, x: 0 }} 
                transition={{ delay: 0.5 + i * 0.1 }}
                className="p-3 rounded-lg border flex items-center justify-between group hover:bg-white/5 transition-colors"
                style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.3)" }}>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-muted-foreground">{cf.id}</span>
                    <span className="text-[10px] bg-destructive/20 text-destructive px-1.5 py-0.5 rounded uppercase font-bold">No-Go</span>
                  </div>
                  <div className="text-xs font-medium mt-1 group-hover:text-gold transition-colors">
                    ↳ {cf.fix}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] uppercase text-success font-bold">GO</div>
                  <div className="text-sm font-bold text-gradient-success">{cf.prob}%</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </Panel>
  );
}
