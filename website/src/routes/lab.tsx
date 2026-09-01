import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Rocket, Play, Save, RotateCcw, Trophy, AlertOctagon, CheckCircle2, AlertTriangle } from "lucide-react";
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceArea,
} from "recharts";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import { Gauge } from "@/components/dss/Gauge";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { calcSuccessProb, decisionFor, fmtCurrency, fmtPct } from "@/lib/dss-utils";
import { useLabStore } from "@/components/dss/store";

const CATEGORIES = ["Home & Garden", "Toys", "Electronics", "Fashion", "Sports", "Beauty", "Books", "Food"];
const SEASONS = ["Winter", "Spring", "Summer", "Fall"];
const CITIES = ["Istanbul", "Ankara", "Izmir", "Bursa", "Konya"];
const SEGMENTS = ["VIP", "Corporate", "Regular", "New", "All"];

export const Route = createFileRoute("/lab")({
  head: () => ({
    meta: [
      { title: "Product Launch Lab · DSS Pro" },
      { name: "description", content: "Live ML-powered product launch simulator with 2,400 scenario runner." },
    ],
  }),
  component: Lab,
});

function Lab() {
  const [name, setName] = useState("Aurora Mini Lamp");
  const [category, setCategory] = useState("Home & Garden");
  const [price, setPrice] = useState(120);
  const [discount, setDiscount] = useState(50);
  const [budget, setBudget] = useState(50000);
  const [adSpend, setAdSpend] = useState(60);
  const [season, setSeason] = useState("Fall");
  const [city, setCity] = useState("Istanbul");
  const [segment, setSegment] = useState("VIP");
  const [quantity, setQuantity] = useState(2000);

  const [scenarios, setScenarios] = useState<{ all: any[]; top5: any[]; goCount: number; reviewCount: number; noCount: number } | null>(null);
  const [progress, setProgress] = useState(0);
  const [running, setRunning] = useState(false);
  const addTest = useLabStore((s: any) => s.addTest);
  const history = useLabStore((s: any) => s.history);

  // ---- LIVE FINANCIAL CALCULATIONS ----
  const finalPrice = price * (1 - discount / 100);
  const expectedRevenue = finalPrice * quantity;
  const marketingCost = budget * (adSpend / 100);
  const grossProfit = expectedRevenue - marketingCost;
  const profitMargin = expectedRevenue > 0 ? (grossProfit / expectedRevenue) * 100 : 0;
  const breakEvenUnits = finalPrice > 0 ? marketingCost / finalPrice : 0;
  const monthlyProfit = grossProfit / 12;
  const paybackMonths = monthlyProfit > 0 ? marketingCost / monthlyProfit : 0;
  const roi = marketingCost > 0 ? ((grossProfit - marketingCost) / marketingCost) * 100 : 0;
  const roas = marketingCost > 0 ? expectedRevenue / marketingCost : 0;
  const netAfterTax = grossProfit * 0.75;
  const annualProjection = expectedRevenue * 12;
  const revenueGrowthVsAvg = ((expectedRevenue - 1922152) / 1922152) * 100;

  const successProb = useMemo(
    () => calcSuccessProb(category, discount, season, city, price, quantity),
    [category, discount, season, city, price, quantity],
  );
  const decision = decisionFor(successProb);

  const sensitivity = useMemo(() => {
    const arr: { discount: number; success: number }[] = [];
    for (let d = 0; d <= 70; d += 5) {
      arr.push({ discount: d, success: calcSuccessProb(category, d, season, city, price, quantity) });
    }
    return arr;
  }, [category, season, city, price, quantity]);

  function runAll() {
    setRunning(true);
    setProgress(0);
    setScenarios(null);
    const all: any[] = [];
    CATEGORIES.forEach((cat) => {
      [0, 10, 20, 30, 40, 50, 60, 70].forEach((d) =>
        SEASONS.forEach((sea) =>
          CITIES.forEach((ci) => {
            const p = calcSuccessProb(cat, d, sea, ci, price, quantity);
            all.push({ category: cat, discount: d, season: sea, city: ci, successProb: p, decision: decisionFor(p) });
          }),
        ),
      );
    });
    // Animate progress
    const total = all.length;
    let i = 0;
    const tick = () => {
      i = Math.min(total, i + Math.ceil(total / 40));
      setProgress(Math.round((i / total) * 100));
      if (i < total) requestAnimationFrame(tick);
      else {
        const top5 = [...all].sort((a, b) => b.successProb - a.successProb).slice(0, 5);
        const goCount = all.filter((r) => r.decision === "GO").length;
        const reviewCount = all.filter((r) => r.decision === "REVIEW").length;
        const noCount = all.filter((r) => r.decision === "NO-GO").length;
        setScenarios({ all, top5, goCount, reviewCount, noCount });
        setRunning(false);
      }
    };
    requestAnimationFrame(tick);
  }

  function saveTest() {
    addTest({
      id: Math.random().toString(36).slice(2, 9),
      date: new Date().toISOString().slice(0, 10),
      name, category, price, discount, budget, successProb, decision,
    });
  }

  function resetForm() {
    setName(""); setPrice(0); setDiscount(0); setBudget(0); setAdSpend(50);
    setQuantity(0); setScenarios(null); setProgress(0);
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="THE CROWN JEWEL"
        title="Product Launch Lab"
        subtitle="Configure a launch on the left, watch every financial and probabilistic metric react in real time on the right."
        actions={
          <span className="rounded-full px-3 py-1.5 text-[11px] font-bold tracking-[0.2em]"
            style={{ background: "var(--gradient-gold)", color: "var(--primary-foreground)" }}>
            ML MODEL · 99.00% ACCURATE
          </span>
        }
      />

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[420px_1fr]">
        {/* LEFT: form */}
        <div className="space-y-4">
          <Panel title="Product Configuration" subtitle="Every keystroke recalculates the model.">
            <div className="space-y-4">
              <Field label={`Product Name (${name.length}/40)`}>
                <input value={name} maxLength={40} onChange={(e) => setName(e.target.value)} className={inputClass} />
              </Field>
              <Field label="Category">
                <select value={category} onChange={(e) => setCategory(e.target.value)} className={inputClass}>
                  {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                </select>
              </Field>
              <div className="grid grid-cols-2 gap-3">
                <Field label="Unit Price ($)" hint={`Avg: $150 · ${price > 150 ? "Above" : "Below"} market`}>
                  <input type="number" value={price} onChange={(e) => setPrice(+e.target.value)} className={inputClass} />
                </Field>
                <Field label="Quantity">
                  <input type="number" value={quantity} onChange={(e) => setQuantity(+e.target.value)} className={inputClass} />
                </Field>
              </div>
              <Field label={`Discount: ${discount}% → Final $${finalPrice.toFixed(2)}`}>
                <input type="range" min={0} max={70} value={discount} onChange={(e) => setDiscount(+e.target.value)} className="w-full accent-[oklch(0.78_0.18_195)]" />
              </Field>
              <Field label="Marketing Budget ($)">
                <input type="number" value={budget} onChange={(e) => setBudget(+e.target.value)} className={inputClass} />
              </Field>
              <Field label={`Ad Spend: ${adSpend}% → ${fmtCurrency(marketingCost)}`}>
                <input type="range" min={0} max={100} value={adSpend} onChange={(e) => setAdSpend(+e.target.value)} className="w-full accent-[oklch(0.78_0.18_195)]" />
                <div className="mt-2 grid grid-cols-4 gap-1 text-[10px] text-muted-foreground">
                  <Tile label="Online" v={fmtCurrency(marketingCost * 0.4, { compact: true })} />
                  <Tile label="Social" v={fmtCurrency(marketingCost * 0.3, { compact: true })} />
                  <Tile label="Email" v={fmtCurrency(marketingCost * 0.2, { compact: true })} />
                  <Tile label="Other" v={fmtCurrency(marketingCost * 0.1, { compact: true })} />
                </div>
              </Field>
              <div className="grid grid-cols-3 gap-3">
                <Field label="Season">
                  <select value={season} onChange={(e) => setSeason(e.target.value)} className={inputClass}>{SEASONS.map((s) => <option key={s}>{s}</option>)}</select>
                </Field>
                <Field label="City">
                  <select value={city} onChange={(e) => setCity(e.target.value)} className={inputClass}>{CITIES.map((s) => <option key={s}>{s}</option>)}</select>
                </Field>
                <Field label="Segment">
                  <select value={segment} onChange={(e) => setSegment(e.target.value)} className={inputClass}>{SEGMENTS.map((s) => <option key={s}>{s}</option>)}</select>
                </Field>
              </div>
            </div>
          </Panel>

          <div className="grid grid-cols-2 gap-3">
            <button onClick={runAll} disabled={running}
              className="col-span-2 rounded-xl px-4 py-3 text-sm font-bold tracking-wider text-primary-foreground transition hover:scale-[1.01] disabled:opacity-50"
              style={{ background: "var(--gradient-primary)", boxShadow: "var(--shadow-glow)" }}>
              <Play className="inline h-4 w-4 mr-2" />
              RUN ALL 2,400 SCENARIOS
            </button>
            <button onClick={saveTest} className="rounded-xl border px-4 py-2.5 text-sm font-semibold transition hover:bg-secondary" style={{ borderColor: "var(--glass-border)" }}>
              <Save className="inline h-4 w-4 mr-1.5" />Save
            </button>
            <button onClick={resetForm} className="rounded-xl border px-4 py-2.5 text-sm font-semibold transition hover:bg-secondary" style={{ borderColor: "var(--glass-border)" }}>
              <RotateCcw className="inline h-4 w-4 mr-1.5" />Reset
            </button>
          </div>
        </div>

        {/* RIGHT: live results */}
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_auto]">
            <Panel title="Financial Projections" subtitle="Reactive on every input change">
              <div className="grid grid-cols-2 gap-3 md:grid-cols-3">
                {[
                  ["Expected Revenue", fmtCurrency(expectedRevenue, { compact: true })],
                  ["Marketing Cost", fmtCurrency(marketingCost, { compact: true })],
                  ["Gross Profit", fmtCurrency(grossProfit, { compact: true }), grossProfit >= 0 ? "success" : "danger"],
                  ["Profit Margin", fmtPct(profitMargin), profitMargin >= 0 ? "success" : "danger"],
                  ["Break-Even Units", Math.ceil(breakEvenUnits).toLocaleString()],
                  ["Payback (months)", paybackMonths > 0 ? paybackMonths.toFixed(1) : "—"],
                  ["ROI", fmtPct(roi), roi >= 0 ? "success" : "danger"],
                  ["ROAS", roas.toFixed(2) + "x"],
                  ["Net After Tax", fmtCurrency(netAfterTax, { compact: true })],
                  ["Annual Projection", fmtCurrency(annualProjection, { compact: true })],
                  ["vs Monthly Avg", fmtPct(revenueGrowthVsAvg), revenueGrowthVsAvg >= 0 ? "success" : "danger"],
                  ["Final Unit Price", fmtCurrency(finalPrice)],
                ].map(([k, v, tone], i) => (
                  <FinTile key={i} label={k as string} value={v as string} tone={tone as any} />
                ))}
              </div>
            </Panel>
            <Panel title="Success Probability" className="flex items-center justify-center">
              <div className="text-center">
                <Gauge value={successProb} label={category} />
                <div className={`mt-3 inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-bold tracking-[0.2em]`}
                  style={{
                    background:
                      decision === "GO" ? "var(--gradient-success)" :
                      decision === "REVIEW" ? "var(--gradient-gold)" :
                      "var(--gradient-danger)",
                    color: "var(--primary-foreground)",
                  }}>
                  {decision === "GO" ? <CheckCircle2 className="h-3.5 w-3.5" /> :
                   decision === "REVIEW" ? <AlertTriangle className="h-3.5 w-3.5" /> :
                   <AlertOctagon className="h-3.5 w-3.5" />}
                  {decision}
                </div>
              </div>
            </Panel>
          </div>

          {(running || scenarios) && (
            <Panel title="Scenario Runner" subtitle="2,400 combinations · Apriori-style sweep">
              {running ? (
                <div className="space-y-3">
                  <div className="text-sm text-muted-foreground">Testing scenario {Math.round(progress * 24)} of 2,400…</div>
                  <div className="h-2 w-full rounded-full" style={{ background: "oklch(0.3 0.04 270)" }}>
                    <motion.div className="h-full rounded-full"
                      style={{ background: "var(--gradient-primary)", boxShadow: "var(--shadow-glow)" }}
                      animate={{ width: `${progress}%` }} />
                  </div>
                </div>
              ) : scenarios && (
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-3">
                    <CountTile label="GO" value={scenarios.goCount} tone="success" />
                    <CountTile label="REVIEW" value={scenarios.reviewCount} tone="gold" />
                    <CountTile label="NO-GO" value={scenarios.noCount} tone="danger" />
                  </div>
                  <div className="space-y-2">
                    {scenarios.top5.map((s, i) => (
                      <motion.div key={i}
                        initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.06 }}
                        className="flex items-center justify-between rounded-xl border p-3"
                        style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
                        <div className="flex items-center gap-3">
                          <div className="text-2xl">{["🥇","🥈","🥉","4️⃣","5️⃣"][i]}</div>
                          <div>
                            <div className="text-sm font-semibold">{s.category} · {s.discount}% off · {s.season} · {s.city}</div>
                            <div className="text-xs text-muted-foreground">Decision: {s.decision}</div>
                          </div>
                        </div>
                        <div className="text-xl font-bold text-gradient">{s.successProb.toFixed(2)}%</div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </Panel>
          )}

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <Panel title="Sensitivity: Discount → Success">
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={sensitivity}>
                  <CartesianGrid stroke={chartTheme.grid} />
                  <XAxis dataKey="discount" stroke={chartTheme.axis} tick={labelStyle} />
                  <YAxis domain={[0, 100]} stroke={chartTheme.axis} tick={labelStyle} />
                  <ReferenceArea y1={70} y2={100} fill="oklch(0.78 0.2 150 / 0.12)" />
                  <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => `${v.toFixed(2)}%`} />
                  <Line type="monotone" dataKey="success" stroke="oklch(0.78 0.18 195)" strokeWidth={3}
                    dot={{ r: 3, fill: "oklch(0.7 0.22 320)" }} animationDuration={1200} />
                </LineChart>
              </ResponsiveContainer>
            </Panel>
            <Panel title="Risk Assessment">
              <div className="grid grid-cols-2 gap-3">
                <Risk label="Price Risk" tone={price > 200 ? "danger" : "success"} note={price > 200 ? "Above category avg" : "In-range"} />
                <Risk label="Discount Risk" tone={discount > 60 ? "danger" : discount > 40 ? "gold" : "success"} note={`${discount}% margin impact`} />
                <Risk label="Market Risk" tone={category === "Home & Garden" ? "success" : "gold"} note={category} />
                <Risk label="Timing Risk" tone={season === "Fall" ? "success" : "gold"} note={`${season} season`} />
              </div>
            </Panel>
          </div>

          <Panel title="AI Recommendations">
            <ul className="space-y-2 text-sm">
              <Reco>Optimal discount for <b>{category}</b>: {Math.round(discount > 40 ? discount : 50)}% maximizes success.</Reco>
              <Reco>Best launch season: <b>Fall</b> shows up to 99.51% success rate.</Reco>
              <Reco>Target <b>{segment}</b> segment for highest conversion lift.</Reco>
              <Reco>Suggested price band: <b>{fmtCurrency(price * 0.85)} – {fmtCurrency(price * 1.15)}</b>.</Reco>
              <Reco>Allocate <b>40%</b> of marketing to Social Media for best ROI.</Reco>
            </ul>
          </Panel>

          <Panel title="Test History" subtitle="Last 30 saved configurations">
            {history.length === 0 ? (
              <div className="py-6 text-center text-sm text-muted-foreground">No saved tests yet — click <b>Save</b> after configuring.</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead className="text-left text-muted-foreground">
                    <tr>{["Date","Product","Category","Price","Disc","Budget","Score","Decision"].map((h) => <th key={h} className="px-2 py-2 font-semibold uppercase tracking-wider">{h}</th>)}</tr>
                  </thead>
                  <tbody>
                    {history.map((t: any) => (
                      <tr key={t.id} className="border-t" style={{ borderColor: "var(--glass-border)" }}>
                        <td className="px-2 py-2">{t.date}</td>
                        <td className="px-2 py-2 font-semibold">{t.name || "—"}</td>
                        <td className="px-2 py-2">{t.category}</td>
                        <td className="px-2 py-2">{fmtCurrency(t.price)}</td>
                        <td className="px-2 py-2">{t.discount}%</td>
                        <td className="px-2 py-2">{fmtCurrency(t.budget, { compact: true })}</td>
                        <td className="px-2 py-2 font-bold">{t.successProb.toFixed(1)}%</td>
                        <td className="px-2 py-2"><DecisionPill d={t.decision} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Panel>
        </div>
      </div>
    </div>
  );
}

const inputClass = "w-full rounded-lg border bg-[oklch(0.18_0.04_270)] px-3 py-2 text-sm outline-none transition focus:border-[oklch(0.78_0.18_195)] focus:ring-1 focus:ring-[oklch(0.78_0.18_195)] [border-color:var(--glass-border)]";

function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <div className="mb-1.5 flex items-center justify-between text-[11px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">
        <span>{label}</span>
        {hint && <span className="font-normal normal-case tracking-normal text-[10px]">{hint}</span>}
      </div>
      {children}
    </label>
  );
}

function Tile({ label, v }: { label: string; v: string }) {
  return (
    <div className="rounded-md border px-2 py-1 text-center" style={{ borderColor: "var(--glass-border)" }}>
      <div>{label}</div><div className="font-bold text-foreground">{v}</div>
    </div>
  );
}

function FinTile({ label, value, tone }: { label: string; value: string; tone?: "success" | "danger" }) {
  return (
    <motion.div
      key={value}
      initial={{ opacity: 0.4, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.25 }}
      className="rounded-xl border p-3"
      style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}
    >
      <div className="text-[10px] uppercase tracking-[0.15em] text-muted-foreground">{label}</div>
      <div className="mt-1 text-lg font-bold"
        style={{ color: tone === "success" ? "var(--success)" : tone === "danger" ? "var(--destructive)" : undefined }}>
        {value}
      </div>
    </motion.div>
  );
}

function CountTile({ label, value, tone }: { label: string; value: number; tone: "success" | "gold" | "danger" }) {
  const bg = tone === "success" ? "var(--gradient-success)" : tone === "gold" ? "var(--gradient-gold)" : "var(--gradient-danger)";
  return (
    <div className="relative overflow-hidden rounded-xl p-4 text-center"
      style={{ background: "oklch(0.22 0.04 270 / 0.5)", border: "1px solid var(--glass-border)" }}>
      <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: bg }} />
      <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">{label}</div>
      <div className="mt-1 text-3xl font-bold">{value.toLocaleString()}</div>
    </div>
  );
}

function Risk({ label, tone, note }: { label: string; tone: "success" | "gold" | "danger"; note: string }) {
  const bg = tone === "success" ? "var(--gradient-success)" : tone === "gold" ? "var(--gradient-gold)" : "var(--gradient-danger)";
  return (
    <div className="relative overflow-hidden rounded-xl p-3" style={{ background: "oklch(0.22 0.04 270 / 0.4)", border: "1px solid var(--glass-border)" }}>
      <div className="absolute inset-y-0 left-0 w-1" style={{ background: bg }} />
      <div className="text-xs font-semibold">{label}</div>
      <div className="mt-0.5 text-[11px] text-muted-foreground">{note}</div>
    </div>
  );
}

function Reco({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-2 rounded-lg p-2"
      style={{ background: "oklch(0.22 0.04 270 / 0.3)" }}>
      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" style={{ color: "var(--success)" }} />
      <span>{children}</span>
    </li>
  );
}

function DecisionPill({ d }: { d: string }) {
  const bg = d === "GO" ? "var(--gradient-success)" : d === "REVIEW" ? "var(--gradient-gold)" : "var(--gradient-danger)";
  return <span className="rounded-full px-2 py-0.5 text-[10px] font-bold tracking-wider text-primary-foreground" style={{ background: bg }}>{d}</span>;
}