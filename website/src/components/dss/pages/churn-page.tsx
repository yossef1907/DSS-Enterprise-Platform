import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { CHURN_DATASETS, CHURN_TREND, CUSTOMER_SEGMENTS, METRICS } from "@/data/dss-metrics";
import { fmtNum } from "@/lib/dss-utils";
import { AlertTriangle, ShieldCheck, Brain, TrendingDown, Activity } from "lucide-react";
import {
  ResponsiveContainer, LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell, ReferenceLine,
} from "recharts";
import { motion } from "framer-motion";

const avgChurn = (METRICS.churn_ecom + METRICS.churn_telco + METRICS.churn_bank + METRICS.churn_hr) / 4;
const atRisk = CHURN_DATASETS.reduce((s, d) => s + d.at_risk, 0);

export default function ChurnPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Avg Churn Rate" value={<CountUp to={avgChurn} suffix="%" decimals={1} />} sublabel="4 datasets" icon={<TrendingDown className="h-4 w-4" />} accent="danger" delay={0} />
        <StatCard label="Total At-Risk" value={<CountUp to={atRisk} />} sublabel="Customers flagged" icon={<AlertTriangle className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Ecom ML Accuracy" value={<CountUp to={METRICS.ecom_churn_acc} suffix="%" decimals={2} />} icon={<Brain className="h-4 w-4" />} accent="primary" delay={0.1} />
        <StatCard label="Mkt Accuracy" value={<CountUp to={METRICS.mkt_churn_acc} suffix="%" decimals={2} />} icon={<Brain className="h-4 w-4" />} accent="success" delay={0.15} />
        <StatCard label="Retention Rate" value={<CountUp to={100 - METRICS.churn_ecom} suffix="%" decimals={1} />} sublabel="E-Commerce" icon={<ShieldCheck className="h-4 w-4" />} accent="success" delay={0.2} />
        <StatCard label="Revenue at Risk" value={<CountUp to={atRisk * METRICS.aov_ecom} prefix="$" compact />} icon={<Activity className="h-4 w-4" />} accent="danger" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Monthly Churn Rate Trend" subtitle="12-month risk evolution" delay={0.1}>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={CHURN_TREND}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="month" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} domain={[12, 20]} />
              <ReferenceLine y={16.8} stroke="oklch(0.66 0.24 25)" strokeDasharray="4 4" />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, "Churn Rate"]} />
              <Line type="monotone" dataKey="rate" stroke="oklch(0.66 0.24 25)" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="At-Risk Customers by Month" subtitle="High churn-probability count" delay={0.15}>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={CHURN_TREND}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="month" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtNum(v), "At-Risk"]} />
              <Bar dataKey="high_risk" radius={[4, 4, 0, 0]}>
                {CHURN_TREND.map((d, i) => (
                  <Cell key={i} fill={d.rate > 17 ? "oklch(0.66 0.24 25)" : "oklch(0.82 0.18 80)"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      <Panel title="Churn by Dataset · ML Performance" subtitle="Accuracy vs churn rate" delay={0.2}>
        <div className="space-y-3">
          {CHURN_DATASETS.map((d, i) => (
            <motion.div key={d.dataset} initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.25 + i * 0.07 }}
              className="grid grid-cols-[1fr_auto_auto_auto] items-center gap-4 rounded-xl border p-3"
              style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="flex items-center gap-3">
                <div className="h-3 w-3 rounded-full shrink-0" style={{ background: d.color }} />
                <span className="text-sm font-semibold">{d.dataset}</span>
              </div>
              <div className="text-xs text-muted-foreground text-right">{fmtNum(d.at_risk)} at-risk</div>
              <div className="text-xs text-muted-foreground text-right">{d.accuracy}% acc</div>
              <div className="text-lg font-bold text-right" style={{ color: d.rate > 20 ? "var(--destructive)" : "var(--warning)" }}>{d.rate}%</div>
            </motion.div>
          ))}
        </div>
      </Panel>

      <Panel title="Segment Churn Risk" subtitle="Risk level per customer segment" delay={0.3}>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
          {CUSTOMER_SEGMENTS.map((seg, i) => (
            <motion.div key={seg.segment} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 + i * 0.07 }}
              className="relative overflow-hidden rounded-xl p-4 text-center"
              style={{ background: "oklch(0.22 0.04 270 / 0.5)", border: "1px solid var(--glass-border)" }}>
              <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: seg.color }} />
              <div className="text-[11px] text-muted-foreground uppercase tracking-[0.12em]">{seg.segment}</div>
              <div className="mt-2 text-2xl font-bold" style={{ color: seg.churnRisk > 40 ? "var(--destructive)" : seg.churnRisk > 20 ? "var(--warning)" : "var(--success)" }}>
                {seg.churnRisk}%
              </div>
              <div className="mt-1 text-[11px] text-muted-foreground">{fmtNum(seg.count)} customers</div>
            </motion.div>
          ))}
        </div>
      </Panel>
      {/* Prescriptive Churn Engine */}
      <PrescriptiveChurnEngine />
    </div>
  );
}

// ── Interactive Prescriptive Churn Engine ────────────────────────────────
import { useState } from "react";
import { RefreshCw, Target, ArrowRight, Wand2, MessageCircleWarning } from "lucide-react";

function PrescriptiveChurnEngine() {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optComplete, setOptComplete] = useState(false);
  const [serverData, setServerData] = useState<any>(null);

  // Default Stats
  const baseHib = 62.1;
  const baseRisk = 34.5;
  const baseLoyal = 8.1;
  const baseChamp = 3.2;

  const curHib = optComplete && serverData ? serverData.metrics["Hibernating"] : baseHib;
  const curRisk = optComplete && serverData ? serverData.metrics["At Risk"] : baseRisk;
  const curLoyal = optComplete && serverData ? serverData.metrics["Loyal"] : baseLoyal;
  const curChamp = optComplete && serverData ? serverData.metrics["Champions"] : baseChamp;

  const handleOptimize = async () => {
    setIsOptimizing(true);
    setOptComplete(false);
    
    try {
      const res = await fetch("http://127.0.0.1:8765/api/optimize_churn", { method: "POST" });
      const data = await res.json();
      setServerData(data);
    } catch (e) {
      console.error("Backend fetch failed", e);
    }

    setTimeout(() => {
      setIsOptimizing(false);
      setOptComplete(true);
    }, 1500);
  };

  return (
    <Panel title="Prescriptive AI Retention Engine" subtitle="Turn 'At Risk' and 'Hibernating' customers into 'Champions' via Backend Strategy" delay={0.4}>
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_auto_1fr]">
        
        {/* Current vs Target */}
        <div className="rounded-xl border p-6 flex flex-col justify-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          <div className="text-sm font-bold flex items-center gap-2 mb-6 text-primary">
            <Target className="h-4 w-4" /> Goal: Retain Customers
          </div>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.66 0.24 25)" }}>Hibernating Risk</span>
                <span className="font-mono">{curHib.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.66 0.24 25)" }} initial={{ width: `${baseHib}%` }} animate={{ width: `${curHib}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.82 0.18 80)" }}>At Risk</span>
                <span className="font-mono">{curRisk.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.82 0.18 80)" }} initial={{ width: `${baseRisk}%` }} animate={{ width: `${curRisk}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.78 0.2 150)" }}>Loyal Growth</span>
                <span className="font-mono">{curLoyal.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.78 0.2 150)" }} initial={{ width: `${baseLoyal}%` }} animate={{ width: `${curLoyal}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.78 0.18 195)" }}>Champions Growth</span>
                <span className="font-mono">{curChamp.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.78 0.18 195)" }} initial={{ width: `${baseChamp}%` }} animate={{ width: `${curChamp}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-center py-4 xl:py-0">
          <button 
            onClick={handleOptimize}
            disabled={isOptimizing}
            className={`px-8 py-4 rounded-xl font-bold text-sm flex flex-col items-center justify-center gap-3 transition-all duration-300 shadow-xl
              ${isOptimizing ? "bg-muted text-muted-foreground cursor-wait animate-pulse" : 
                optComplete ? "bg-success text-success-foreground hover:scale-105 glow border border-success/50" : 
                "bg-primary text-primary-foreground hover:scale-105 glow"}`}
          >
            {isOptimizing ? (
              <><Activity className="h-8 w-8 animate-spin" /> Calling API...</>
            ) : optComplete ? (
              <><RefreshCw className="h-8 w-8" /> <span>Recalculate<br/>Retention Strategy</span></>
            ) : (
              <><Wand2 className="h-8 w-8" /> <span>Generate AI<br/>Action Plan</span></>
            )}
          </button>
        </div>

        {/* AI Strategies */}
        <div className="rounded-xl border p-6" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          <div className="text-sm font-bold flex items-center gap-2 mb-4 text-gold">
            <MessageCircleWarning className="h-4 w-4" /> Recommended Retention Campaigns
          </div>

          <div className="space-y-3">
            {(serverData?.action_plan || [
              { target: "Awaiting Python AI Engine...", strategy: "Click 'Generate AI Action Plan' to connect to the server." }
            ]).map((item: any, i: number) => (
              <motion.div key={i} 
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: optComplete ? 1 : 0.4, x: 0 }} 
                className={`p-3 rounded-lg border text-xs ${optComplete ? 'bg-black/20 border-white/10' : 'bg-transparent border-transparent'}`}>
                <div className="font-semibold text-destructive mb-1 flex items-center gap-1">
                  <ArrowRight className="w-3 h-3" /> Target Segment: <span className="text-muted-foreground font-normal">{item.target}</span>
                </div>
                {optComplete && (
                  <div className="font-semibold text-success flex items-center gap-1 mt-1.5">
                    <Wand2 className="w-3 h-3" /> AI Strategy: <span className="text-foreground">{item.strategy}</span>
                  </div>
                )}
                {item.expected_reduction && optComplete && (
                  <div className="text-muted-foreground text-[10px] mt-1 ml-4">Expected Drop in Churn: <span className="text-success">{item.expected_reduction}</span></div>
                )}
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </Panel>
  );
}
