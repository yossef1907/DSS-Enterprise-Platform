import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Hexagon, BarChart3, Users, AlertTriangle, ShoppingCart, Rocket, TrendingUp,
  Gem, Megaphone, MessageSquare, Microscope, Boxes, Star, Sparkles, ChevronLeft,
} from "lucide-react";
import { NAV_ITEMS } from "@/data/dss";
import { useState } from "react";

const ICONS: Record<string, typeof Hexagon> = {
  Hexagon, BarChart3, Users, AlertTriangle, ShoppingCart, Rocket, TrendingUp,
  Gem, Megaphone, MessageSquare, Microscope, Boxes, Star,
};

export function DssSidebar() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`${collapsed ? "w-[72px]" : "w-[260px]"} shrink-0 sticky top-0 h-screen transition-all duration-300 z-30`}
      style={{ background: "var(--sidebar)", backdropFilter: "blur(24px)" }}
    >
      <div className="flex h-full flex-col border-r" style={{ borderColor: "var(--sidebar-border)" }}>
        <div className="flex items-center gap-2 px-4 py-5">
          <div className="relative">
            <div className="absolute inset-0 rounded-lg blur-md" style={{ background: "var(--gradient-primary)" }} />
            <div className="relative flex h-9 w-9 items-center justify-center rounded-lg" style={{ background: "var(--gradient-primary)" }}>
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
          </div>
          {!collapsed && (
            <div className="flex flex-col leading-none">
              <span className="text-sm font-bold tracking-wider">DSS PRO</span>
              <span className="text-[10px] text-muted-foreground tracking-[0.2em]">v1.0 · ENTERPRISE</span>
            </div>
          )}
        </div>

        <nav className="flex-1 overflow-y-auto scrollbar-thin px-2 pb-3">
          {NAV_ITEMS.map((group) => (
            <div key={group.group} className="mb-3">
              {!collapsed && (
                <div className="px-3 pb-1.5 pt-2 text-[10px] font-semibold tracking-[0.2em] text-muted-foreground/70">
                  {group.group}
                </div>
              )}
              <ul className="space-y-1">
                {group.items.map((item) => {
                  const Icon = ICONS[item.icon] ?? Hexagon;
                  const active = path === item.to;
                  const featured = (item as any).featured;
                  return (
                    <li key={item.to}>
                      <Link
                        to={item.to}
                        className={`group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all
                          ${active ? "text-foreground" : "text-muted-foreground hover:text-foreground"}`}
                      >
                        {active && (
                          <motion.span
                            layoutId="active-pill"
                            className="absolute inset-0 rounded-lg"
                            style={{ background: "var(--gradient-primary)", opacity: 0.18, boxShadow: "var(--shadow-glow)" }}
                            transition={{ type: "spring", stiffness: 400, damping: 32 }}
                          />
                        )}
                        {active && (
                          <span className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[3px] rounded-r"
                            style={{ background: "var(--gradient-primary)" }} />
                        )}
                        <Icon className="relative h-4 w-4 shrink-0" />
                        {!collapsed && <span className="relative truncate">{item.label}</span>}
                        {!collapsed && featured && (
                          <span className="relative ml-auto rounded-full px-1.5 py-0.5 text-[9px] font-bold"
                            style={{ background: "var(--gradient-gold)", color: "var(--primary-foreground)" }}>
                            HOT
                          </span>
                        )}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>

        <button
          onClick={() => setCollapsed((c) => !c)}
          className="m-3 flex items-center justify-center gap-2 rounded-lg border py-2 text-xs text-muted-foreground hover:text-foreground transition"
          style={{ borderColor: "var(--sidebar-border)" }}
        >
          <ChevronLeft className={`h-3.5 w-3.5 transition-transform ${collapsed ? "rotate-180" : ""}`} />
          {!collapsed && "Collapse"}
        </button>
      </div>
    </aside>
  );
}