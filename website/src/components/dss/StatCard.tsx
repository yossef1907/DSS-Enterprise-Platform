import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";

export function StatCard({
  label, value, sublabel, change, icon, accent, delay = 0, children,
}: {
  label: string;
  value: ReactNode;
  sublabel?: string;
  change?: number;
  icon?: ReactNode;
  accent?: "primary" | "gold" | "success" | "danger" | "accent";
  delay?: number;
  children?: ReactNode;
}) {
  const accentVar =
    accent === "gold" ? "var(--gradient-gold)" :
    accent === "success" ? "var(--gradient-success)" :
    accent === "danger" ? "var(--gradient-danger)" :
    accent === "accent" ? "linear-gradient(135deg, oklch(0.7 0.22 320), oklch(0.78 0.18 195))" :
    "var(--gradient-primary)";

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: "easeOut" }}
      className="glass relative overflow-hidden p-5 group"
    >
      <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: accentVar }} />
      <div
        className="absolute -right-6 -top-6 h-24 w-24 rounded-full opacity-30 blur-2xl transition-opacity group-hover:opacity-60"
        style={{ background: accentVar }}
      />
      <div className="relative flex items-start justify-between">
        <div>
          <div className="text-[11px] font-medium uppercase tracking-[0.18em] text-muted-foreground">{label}</div>
          <div className="mt-2 text-3xl font-bold tracking-tight">{value}</div>
          {sublabel && <div className="mt-1 text-xs text-muted-foreground">{sublabel}</div>}
          {change !== undefined && (
            <div className="mt-2 inline-flex items-center gap-1 text-xs font-semibold"
              style={{ color: change >= 0 ? "var(--success)" : "var(--destructive)" }}>
              {change >= 0 ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
              {Math.abs(change).toFixed(2)}%
            </div>
          )}
        </div>
        {icon && (
          <div className="rounded-xl p-2.5" style={{ background: accentVar }}>
            <div className="text-primary-foreground">{icon}</div>
          </div>
        )}
      </div>
      {children && <div className="relative mt-3">{children}</div>}
    </motion.div>
  );
}