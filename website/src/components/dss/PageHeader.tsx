import { motion } from "framer-motion";
import type { ReactNode } from "react";

export function PageHeader({
  eyebrow, title, subtitle, actions,
}: { eyebrow?: string; title: string; subtitle?: string; actions?: ReactNode }) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        {eyebrow && (
          <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-2 text-[11px] font-semibold tracking-[0.3em] text-primary"
          >
            {eyebrow}
          </motion.div>
        )}
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
          <span className="text-gradient">{title}</span>
        </h1>
        {subtitle && <p className="mt-2 max-w-2xl text-sm text-muted-foreground">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}