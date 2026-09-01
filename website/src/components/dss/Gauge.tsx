import { motion } from "framer-motion";

export function Gauge({ value, label, size = 180 }: { value: number; label?: string; size?: number }) {
  const v = Math.max(0, Math.min(100, value));
  const r = size / 2 - 14;
  const c = 2 * Math.PI * r;
  const offset = c * (1 - v / 100);
  const color =
    v >= 80 ? "var(--success)" :
    v >= 60 ? "var(--warning)" :
    v >= 30 ? "oklch(0.78 0.18 50)" :
    "var(--destructive)";
  return (
    <div className="relative inline-flex flex-col items-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size/2} cy={size/2} r={r} stroke="oklch(0.4 0.04 270 / 0.4)" strokeWidth="10" fill="none" />
        <motion.circle
          cx={size/2} cy={size/2} r={r} stroke={color} strokeWidth="10" fill="none" strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.4, ease: "easeOut" }}
          style={{ filter: `drop-shadow(0 0 10px ${color})` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div className="text-3xl font-bold tracking-tight" style={{ color }}>
          {v.toFixed(1)}<span className="text-base text-muted-foreground">%</span>
        </div>
        {label && <div className="mt-1 text-[10px] uppercase tracking-[0.2em] text-muted-foreground">{label}</div>}
      </div>
    </div>
  );
}
