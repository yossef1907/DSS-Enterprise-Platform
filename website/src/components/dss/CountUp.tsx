import { useEffect, useRef, useState } from "react";

type Props = {
  to: number;
  duration?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
  compact?: boolean;
};

export function CountUp({ to, duration = 1400, decimals = 0, prefix = "", suffix = "", className, compact }: Props) {
  const [val, setVal] = useState(0);
  const startRef = useRef<number | null>(null);

  useEffect(() => {
    let raf: number;
    startRef.current = null;
    const step = (t: number) => {
      if (startRef.current === null) startRef.current = t;
      const p = Math.min(1, (t - startRef.current) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setVal(to * eased);
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [to, duration]);

  const formatted = (() => {
    if (compact) {
      if (Math.abs(val) >= 1e9) return (val / 1e9).toFixed(2) + "B";
      if (Math.abs(val) >= 1e6) return (val / 1e6).toFixed(2) + "M";
      if (Math.abs(val) >= 1e3) return (val / 1e3).toFixed(1) + "K";
    }
    return val.toLocaleString("en-US", { maximumFractionDigits: decimals, minimumFractionDigits: decimals });
  })();

  return (
    <span className={className}>
      {prefix}
      {formatted}
      {suffix}
    </span>
  );
}