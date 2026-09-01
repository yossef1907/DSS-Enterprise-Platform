import { useQuery } from "@tanstack/react-query";
import { fetchReportData } from "@/lib/api";
import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { fmtCurrency } from "@/lib/dss-utils";
import { motion } from "framer-motion";
import { FileText, TrendingUp, TrendingDown, Lightbulb, AlertTriangle, CheckCircle, RefreshCcw, DollarSign } from "lucide-react";
import { useState } from "react";

export default function ReportPage() {
  const [selectedMonth, setSelectedMonth] = useState<string | undefined>(undefined);

  const { data, isLoading, isError, dataUpdatedAt, isFetching, refetch } = useQuery({
    queryKey: ['monthly_report', selectedMonth],
    queryFn: () => fetchReportData(selectedMonth, false), // false means use cache by default
    refetchInterval: 60000, 
    refetchOnWindowFocus: false, 
  });

  const handleForceAI = async () => {
    // Call the API directly with force_ai=true to overwrite the cache, then refetch
    await fetchReportData(selectedMonth, true);
    refetch();
  };

  if (isLoading) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center gap-4 text-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        <div>
          <div className="font-bold text-lg text-gradient">Generating AI Performance Report...</div>
          <div className="text-sm text-muted-foreground">Analyzing latest monthly events and transactions</div>
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="flex h-[60vh] flex-col items-center justify-center text-center text-destructive">
        <AlertTriangle className="h-12 w-12 mb-4 opacity-50" />
        <div className="font-bold text-lg">Report Generation Failed</div>
        <div className="text-sm opacity-80">Could not connect to the DSS Python Backend.</div>
      </div>
    );
  }

  const { is_positive, percentage, difference, current_revenue, previous_revenue, causes, solutions, month, available_months } = data;
  const isLoss = !is_positive;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div className="space-y-6" variants={containerVariants} initial="hidden" animate="visible">
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/20 text-primary">
            <FileText className="h-5 w-5" />
          </div>
          <div>
            <div className="font-bold text-lg flex items-center gap-2">
              AI Performance & Advisory Report
              <span className="text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded-full border border-primary/20 uppercase tracking-widest font-bold">Fast Cached</span>
            </div>
            <div className="text-sm text-muted-foreground">Reporting Period: <span className="font-semibold text-foreground">{month}</span></div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {available_months && available_months.length > 0 && (
            <select 
              value={selectedMonth || month} 
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="bg-black/30 border border-white/10 rounded-md px-3 py-1.5 text-sm outline-none focus:ring-1 focus:ring-primary cursor-pointer text-foreground"
            >
              {available_months.map((m: string) => (
                <option key={m} value={m} className="bg-background text-foreground">{m}</option>
              ))}
            </select>
          )}
          
          <button 
            onClick={handleForceAI}
            disabled={isFetching}
            className="flex items-center gap-2 text-xs font-bold text-black bg-gradient-to-r from-primary to-primary-hover px-4 py-1.5 rounded-md hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            <Lightbulb className={`h-3.5 w-3.5 ${isFetching ? 'animate-pulse' : ''}`} />
            {isFetching ? 'Analyzing...' : '✨ Ask AI (Fresh Insight)'}
          </button>

          <div className="hidden sm:flex items-center gap-2 text-xs text-muted-foreground bg-black/20 px-3 py-1.5 rounded-full border border-white/5">
            <RefreshCcw className="h-3 w-3 animate-spin-slow" />
            Live Sync
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <motion.div variants={itemVariants}>
          <StatCard label="Current Month Revenue" value={<CountUp to={current_revenue} prefix="$" compact />} icon={<DollarSign className="h-4 w-4" />} accent="primary" delay={0} />
        </motion.div>
        <motion.div variants={itemVariants}>
          <StatCard label="Previous Month Revenue" value={<CountUp to={previous_revenue} prefix="$" compact />} icon={<DollarSign className="h-4 w-4" />} accent="gold" delay={0.1} />
        </motion.div>
        <motion.div variants={itemVariants}>
          <StatCard 
            label={isLoss ? "Net Loss" : "Net Profit"} 
            value={<CountUp to={Math.abs(difference)} prefix="$" compact />} 
            icon={isLoss ? <TrendingDown className="h-4 w-4 text-destructive" /> : <TrendingUp className="h-4 w-4 text-success" />} 
            accent={isLoss ? "danger" : "success"} 
            delay={0.2} 
          />
        </motion.div>
        <motion.div variants={itemVariants}>
          <div className="relative overflow-hidden rounded-xl border p-5 text-center h-full flex flex-col justify-center" style={{ borderColor: "var(--glass-border)", background: isLoss ? "var(--destructive)/10" : "var(--success)/10" }}>
            <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: isLoss ? "var(--gradient-danger)" : "var(--gradient-success)" }} />
            <div className="text-[11px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-1">MoM Performance</div>
            <div className="text-4xl font-bold" style={{ color: isLoss ? "var(--destructive)" : "var(--success)" }}>
              {isLoss ? "" : "+"}{percentage.toFixed(1)}%
            </div>
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Causes Panel */}
        <motion.div variants={itemVariants} className="h-full">
          <Panel 
            title={isLoss ? "Root Causes for Decline" : "Primary Growth Drivers"} 
            subtitle="AI analysis of the primary factors driving this month's performance" 
            delay={0}
            className="h-full"
          >
            <div className="space-y-4 mt-2">
              {causes.map((cause: string, i: number) => (
                <motion.div 
                  key={i} 
                  initial={{ opacity: 0, x: -20 }} 
                  animate={{ opacity: 1, x: 0 }} 
                  transition={{ delay: 0.3 + (i * 0.1) }}
                  className="flex items-start gap-3 rounded-xl border p-4" 
                  style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}
                >
                  <div className="mt-0.5 shrink-0">
                    {isLoss ? <AlertTriangle className="h-5 w-5 text-destructive" /> : <CheckCircle className="h-5 w-5 text-success" />}
                  </div>
                  <p className="text-sm font-medium leading-relaxed">{cause}</p>
                </motion.div>
              ))}
            </div>
          </Panel>
        </motion.div>

        {/* Solutions/Ideas Panel */}
        <motion.div variants={itemVariants} className="h-full">
          <Panel 
            title={isLoss ? "Strategic Action Plan" : "Future Strategic Ideas"} 
            subtitle="Actionable recommendations generated by the AI Engine" 
            delay={0.1}
            className="h-full"
          >
            <div className="space-y-4 mt-2">
              {solutions.map((solution: string, i: number) => (
                <motion.div 
                  key={i} 
                  initial={{ opacity: 0, x: 20 }} 
                  animate={{ opacity: 1, x: 0 }} 
                  transition={{ delay: 0.4 + (i * 0.1) }}
                  className="flex items-start gap-3 rounded-xl border p-4 relative overflow-hidden" 
                  style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}
                >
                  <div className="absolute inset-y-0 left-0 w-1" style={{ background: isLoss ? "var(--gradient-gold)" : "var(--gradient-primary)" }} />
                  <div className="mt-0.5 shrink-0 mr-3">
                    <Lightbulb className="h-5 w-5 text-gold" style={{ color: "var(--gold)" }} />
                  </div>
                  <p className="text-sm font-medium leading-relaxed flex-1">{solution}</p>
                </motion.div>
              ))}
            </div>
          </Panel>
        </motion.div>
      </div>
    </motion.div>
  );
}
