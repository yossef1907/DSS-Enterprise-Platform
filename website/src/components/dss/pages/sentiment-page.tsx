import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { SENTIMENT } from "@/data/dss";
import { fmtNum } from "@/lib/dss-utils";
import { MessageSquare, ThumbsUp, ThumbsDown, Star, Activity, Brain } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, RadarChart, Radar, PolarGrid, PolarAngleAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { motion } from "framer-motion";

const sources = SENTIMENT.bySources;
const avgScore = sources.reduce((s, d) => s + (d.positive * 5 + d.neutral * 3 + d.negative * 1) / 100, 0) / sources.length;
const bestSource = sources.reduce((a, b) => a.positive > b.positive ? a : b);
const worstSource = sources.reduce((a, b) => a.negative > b.negative ? a : b);

export default function SentimentPage() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Total Reviews" value={<CountUp to={SENTIMENT.total} compact />} icon={<MessageSquare className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="Positive" value={<CountUp to={SENTIMENT.positive.count} compact />} sublabel={`${SENTIMENT.positive.pct}% of total`} icon={<ThumbsUp className="h-4 w-4" />} accent="success" delay={0.05} />
        <StatCard label="Neutral" value={<CountUp to={SENTIMENT.neutral.count} compact />} sublabel={`${SENTIMENT.neutral.pct}% of total`} icon={<Activity className="h-4 w-4" />} accent="gold" delay={0.1} />
        <StatCard label="Negative" value={<CountUp to={SENTIMENT.negative.count} compact />} sublabel={`${SENTIMENT.negative.pct}% of total`} icon={<ThumbsDown className="h-4 w-4" />} accent="danger" delay={0.15} />
        <StatCard label="Best Source" value={bestSource.source} sublabel={`${bestSource.positive}% positive`} icon={<Star className="h-4 w-4" />} accent="primary" delay={0.2} />
        <StatCard label="Avg NLP Score" value={<CountUp to={avgScore} suffix="/5" decimals={2} />} icon={<Brain className="h-4 w-4" />} accent="gold" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Sentiment Distribution by Source" subtitle="Positive · Neutral · Negative % per dataset" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={sources}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="source" stroke={chartTheme.axis} tick={labelStyle} angle={-20} textAnchor="end" height={45} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => `${v}%`} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v}%`, ""]} />
              <Bar dataKey="positive" name="Positive" stackId="a" fill="oklch(0.78 0.2 150)" />
              <Bar dataKey="neutral" name="Neutral" stackId="a" fill="oklch(0.82 0.18 80)" />
              <Bar dataKey="negative" name="Negative" stackId="a" fill="oklch(0.66 0.24 25)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="NLP Score Radar by Source" subtitle="Weighted sentiment score per dataset" delay={0.15}>
          <ResponsiveContainer width="100%" height={260}>
            <RadarChart data={sources.map((s) => ({ ...s, score: (s.positive * 5 + s.neutral * 3 + s.negative * 1) / 100 }))}>
              <PolarGrid stroke={chartTheme.grid} />
              <PolarAngleAxis dataKey="source" tick={labelStyle} />
              <Radar name="NLP Score" dataKey="score" stroke="oklch(0.78 0.18 195)" fill="oklch(0.78 0.18 195)" fillOpacity={0.25} strokeWidth={2} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`${v.toFixed(2)}/5`, "NLP Score"]} />
            </RadarChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      {/* Overall sentiment donut */}
      <Panel title="Overall Sentiment Breakdown" subtitle={`${fmtNum(SENTIMENT.total)} reviews analyzed across all datasets`} delay={0.25}>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div className="space-y-3">
            {[
              { label: "Positive", data: SENTIMENT.positive, color: "oklch(0.78 0.2 150)" },
              { label: "Neutral", data: SENTIMENT.neutral, color: "oklch(0.82 0.18 80)" },
              { label: "Negative", data: SENTIMENT.negative, color: "oklch(0.66 0.24 25)" },
            ].map((item, i) => (
              <motion.div key={item.label} initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.1 }}
                className="flex items-center gap-4 rounded-xl border p-4 relative overflow-hidden" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
                {/* Colored Accent Line on the left */}
                <div className="absolute inset-y-0 left-0 w-1.5" style={{ background: item.color, boxShadow: `0 0 10px ${item.color}` }} />
                
                <div className="text-3xl font-bold ml-2" style={{ color: item.color }}>{item.data.pct}%</div>
                <div className="flex-1">
                  <div className="font-semibold">{item.label}</div>
                  <div className="text-xs text-muted-foreground">{fmtNum(item.data.count)} reviews</div>
                  <div className="mt-1 h-1.5 w-full rounded-full" style={{ background: "oklch(0.3 0.04 270)" }}>
                    <motion.div className="h-full rounded-full" initial={{ width: 0 }} animate={{ width: `${item.data.pct}%` }} transition={{ delay: 0.4 + i * 0.1, duration: 0.8 }}
                      style={{ background: item.color }} />
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="space-y-3">
            {sources.map((d, i) => (
              <motion.div key={d.source} initial={{ opacity: 0, x: 12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.35 + i * 0.07 }}
                className="rounded-xl border p-3" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
                <div className="mb-1.5 flex justify-between">
                  <span className="font-semibold capitalize">{d.source}</span>
                  <span className="text-xs text-muted-foreground">{d.positive}% pos / {d.negative}% neg</span>
                </div>
                <div className="flex h-2 w-full overflow-hidden rounded-full" style={{ background: "oklch(0.3 0.04 270)" }}>
                  <div style={{ width: `${d.positive}%`, background: "oklch(0.78 0.2 150)" }} />
                  <div style={{ width: `${d.neutral}%`, background: "oklch(0.82 0.18 80)" }} />
                  <div style={{ width: `${d.negative}%`, background: "oklch(0.66 0.24 25)" }} />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </Panel>
      {/* Prescriptive Sentiment Engine */}
      <PrescriptiveSentimentEngine />
    </div>
  );
}

// ── Interactive Prescriptive Sentiment Engine ────────────────────────────────
import { useState } from "react";
import { Wand2, Target, ArrowRight, CheckCircle2, MessageCircleWarning, RefreshCw } from "lucide-react";

function PrescriptiveSentimentEngine() {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optComplete, setOptComplete] = useState(false);
  const [serverData, setServerData] = useState<any>(null);

  // Default Stats
  const basePos = 39.1;
  const baseNeu = 44.5;
  const baseNeg = 16.3;

  const currentPos = optComplete && serverData ? serverData.metrics.positive : basePos;
  const currentNeu = optComplete && serverData ? serverData.metrics.neutral : baseNeu;
  const currentNeg = optComplete && serverData ? serverData.metrics.negative : baseNeg;

  const handleOptimize = async () => {
    setIsOptimizing(true);
    setOptComplete(false);
    
    try {
      const res = await fetch("http://127.0.0.1:8765/api/optimize_sentiment", {
        method: "POST"
      });
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
    <Panel title="Prescriptive AI Sentiment Engine" subtitle="Turn Negative and Neutral feedback into 5-Star Promoters via Backend NLP" delay={0.4}>
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_auto_1fr]">
        
        {/* Current vs Target */}
        <div className="rounded-xl border p-6 flex flex-col justify-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          <div className="text-sm font-bold flex items-center gap-2 mb-6 text-primary">
            <Target className="h-4 w-4" /> Goal: Flip Sentiments
          </div>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.78 0.2 150)" }}>Positive</span>
                <span className="font-mono">{currentPos.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.78 0.2 150)" }} initial={{ width: `${basePos}%` }} animate={{ width: `${currentPos}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.82 0.18 80)" }}>Neutral</span>
                <span className="font-mono">{currentNeu.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.82 0.18 80)" }} initial={{ width: `${baseNeu}%` }} animate={{ width: `${currentNeu}%` }} transition={{ duration: 1, type: "spring" }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="font-bold" style={{ color: "oklch(0.66 0.24 25)" }}>Negative</span>
                <span className="font-mono">{currentNeg.toFixed(1)}%</span>
              </div>
              <div className="h-2 w-full rounded-full overflow-hidden bg-black/20">
                <motion.div layout className="h-full" style={{ background: "oklch(0.66 0.24 25)" }} initial={{ width: `${baseNeg}%` }} animate={{ width: `${currentNeg}%` }} transition={{ duration: 1, type: "spring" }} />
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
                optComplete ? "bg-success text-success-foreground hover:scale-105 glow" : 
                "bg-primary text-primary-foreground hover:scale-105 glow"}`}
          >
            {isOptimizing ? (
              <><Activity className="h-8 w-8 animate-spin" /> Calling API...</>
            ) : optComplete ? (
              <><RefreshCw className="h-8 w-8" /> <span>Recalculate<br/>AI Strategy</span></>
            ) : (
              <><Wand2 className="h-8 w-8" /> <span>Call Python<br/>AI Backend</span></>
            )}
          </button>
        </div>

        {/* NLP Root Cause Fixes */}
        <div className="rounded-xl border p-6" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
          <div className="text-sm font-bold flex items-center gap-2 mb-4 text-gold">
            <MessageCircleWarning className="h-4 w-4" /> Top Negative Drivers & AI Fixes
          </div>

          <div className="space-y-3">
            {(serverData?.action_plan || [
              { issue: "Awaiting Python NLP Engine...", fix: "Click 'Call Python AI Backend' to connect to the server and fetch dynamic solutions." }
            ]).map((item: any, i: number) => (
              <motion.div key={i} 
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: optComplete ? 1 : 0.4, x: 0 }} 
                className={`p-3 rounded-lg border text-xs ${optComplete ? 'bg-black/20 border-white/10' : 'bg-transparent border-transparent'}`}>
                <div className="font-semibold text-destructive mb-1 flex items-center gap-1">
                  <ArrowRight className="w-3 h-3" /> Root Cause: <span className="text-muted-foreground font-normal">{item.issue}</span>
                </div>
                {optComplete && (
                  <div className="font-semibold text-success flex items-center gap-1 mt-1.5">
                    <Wand2 className="w-3 h-3" /> AI Solution: <span className="text-foreground">{item.fix}</span>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </Panel>
  );
}
