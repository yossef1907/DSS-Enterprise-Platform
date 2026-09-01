import { Outlet } from "@tanstack/react-router";
import { DssSidebar } from "./Sidebar";
import { Ticker } from "./Ticker";
import { motion, AnimatePresence } from "framer-motion";
import { useRouterState } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Moon, Sparkles, Droplets, Leaf, Palette } from "lucide-react";

const THEMES = [
  { id: "dark", name: "Night Mode", icon: Moon, color: "oklch(0.7 0.04 260)" },
  { id: "theme-space", name: "Space Mode", icon: Sparkles, color: "oklch(0.7 0.2 330)" },
  { id: "theme-ocean", name: "Ocean Mode", icon: Droplets, color: "oklch(0.8 0.15 180)" },
  { id: "theme-emerald", name: "Emerald Mode", icon: Leaf, color: "oklch(0.75 0.2 140)" },
];

export function DssLayout() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const [activeTheme, setActiveTheme] = useState("dark");
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Apply theme class to html element
    const root = document.documentElement;
    root.className = activeTheme; // Replaces existing classes
    // Keep 'dark' if needed by some tailwind plugins, but our custom classes will override variables
    if (activeTheme !== "dark") root.classList.add("dark", activeTheme);
  }, [activeTheme]);

  return (
    <div className="flex min-h-screen w-full grid-bg">
      <DssSidebar />
      <div className="flex min-w-0 flex-1 flex-col relative">
        {/* Theme Switcher */}
        <div className="absolute top-4 right-6 z-50">
          <div className="relative">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="flex h-10 w-10 items-center justify-center rounded-full glass hover:bg-white/5 transition-all glow"
              title="Change Theme"
            >
              <Palette className="h-5 w-5 text-primary" />
            </button>
            
            <AnimatePresence>
              {isOpen && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9, y: 10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: 10 }}
                  transition={{ duration: 0.2 }}
                  className="absolute right-0 top-12 w-48 rounded-xl glass-strong p-2 shadow-2xl flex flex-col gap-1"
                >
                  {THEMES.map((t) => {
                    const Icon = t.icon;
                    const isActive = activeTheme === t.id;
                    return (
                      <button
                        key={t.id}
                        onClick={() => {
                          setActiveTheme(t.id);
                          setIsOpen(false);
                        }}
                        className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all w-full text-left
                          ${isActive ? "bg-white/10 text-foreground" : "text-muted-foreground hover:bg-white/5 hover:text-foreground"}`}
                      >
                        <Icon className="h-4 w-4" style={{ color: isActive ? t.color : undefined }} />
                        <span>{t.name}</span>
                        {isActive && (
                          <motion.div
                            layoutId="theme-active"
                            className="ml-auto h-1.5 w-1.5 rounded-full"
                            style={{ background: t.color, boxShadow: `0 0 10px ${t.color}` }}
                          />
                        )}
                      </button>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        <main className="flex-1 px-6 py-6 lg:px-10 mt-10 lg:mt-0">
          <motion.div
            key={path}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
          >
            <Outlet />
          </motion.div>
        </main>
        <Ticker />
      </div>
    </div>
  );
}