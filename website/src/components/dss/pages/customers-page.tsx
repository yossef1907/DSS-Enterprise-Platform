import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchCustomers } from "@/lib/api";
import { Panel } from "@/components/dss/Panel";
import { StatCard } from "@/components/dss/StatCard";
import { CountUp } from "@/components/dss/CountUp";
import { tooltipStyle, labelStyle, chartTheme } from "@/components/dss/ChartTheme";
import { CLV_SEGMENTS, CUSTOMER_SEGMENTS_RFM, PROJECT_METRICS, CUSTOMERS as STATIC_CUSTOMERS } from "@/data/dss";
import { METRICS } from "@/data/dss-metrics";
import { fmtCurrency, fmtNum } from "@/lib/dss-utils";
import { Users, Star, TrendingUp, DollarSign, Activity, Shield, Search, ShoppingBag, CreditCard, User, MapPin } from "lucide-react";
import {
  ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import { motion } from "framer-motion";

const totalCustomers = PROJECT_METRICS.totalCustomers;
const totalCLV = PROJECT_METRICS.totalCLV;
const avgCLV = PROJECT_METRICS.avgCLV;

export default function CustomersPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['customers_list'],
    queryFn: fetchCustomers,
  });

  const apiCustomers = data?.customers || [];
  
  // Use API customers if loaded, otherwise fallback to first static customer while loading
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>("");
  
  const selectedCustomer = useMemo(() => {
    if (apiCustomers.length > 0) {
      if (selectedCustomerId) {
        return apiCustomers.find((c: any) => c.id === selectedCustomerId) || apiCustomers[0];
      }
      return apiCustomers[0];
    }
    return STATIC_CUSTOMERS[0];
  }, [apiCustomers, selectedCustomerId]);

  // Derived metrics
  const profit = selectedCustomer.totalSpent ? selectedCustomer.totalSpent * 0.24 : 0;
  
  // Estimate sentiment/churn based on rating
  const rating = selectedCustomer.avgRating || 4.0;
  const sentiment = rating >= 4.5 ? "Positive" : rating < 3.0 ? "Negative" : "Neutral";
  const churnRisk = rating < 3.0 ? "High" : rating >= 4.5 ? "Low" : "Medium";
  const churnScore = rating < 3.0 ? 0.85 : rating >= 4.5 ? 0.12 : 0.45;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Total Customers" value={<CountUp to={totalCustomers} compact />} icon={<Users className="h-4 w-4" />} accent="primary" delay={0} />
        <StatCard label="Total CLV Portfolio" value={<CountUp to={totalCLV} prefix="$" compact />} icon={<DollarSign className="h-4 w-4" />} accent="gold" delay={0.05} />
        <StatCard label="Avg CLV" value={<CountUp to={avgCLV} prefix="$" decimals={2} />} icon={<Star className="h-4 w-4" />} accent="success" delay={0.1} />
        <StatCard label="Median CLV" value={<CountUp to={PROJECT_METRICS.medianCLV} prefix="$" decimals={2} />} icon={<Activity className="h-4 w-4" />} accent="primary" delay={0.15} />
        <StatCard label="Platinum Tier" value={<CountUp to={CLV_SEGMENTS[0].customers} compact />} sublabel={`$${(CLV_SEGMENTS[0].avgCLV / 1000).toFixed(0)}K avg CLV`} icon={<Shield className="h-4 w-4" />} accent="gold" delay={0.2} />
        <StatCard label="Revenue Growth" value={<CountUp to={METRICS.growth_rev} suffix="%" decimals={1} />} icon={<TrendingUp className="h-4 w-4" />} accent="success" delay={0.25} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Panel title="Customer Segments by CLV Tier" subtitle="Customer count and avg CLV per tier" delay={0.1}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={CLV_SEGMENTS}>
              <CartesianGrid stroke={chartTheme.grid} />
              <XAxis dataKey="segment" stroke={chartTheme.axis} tick={labelStyle} />
              <YAxis stroke={chartTheme.axis} tick={labelStyle} tickFormatter={(v) => fmtNum(v)} />
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtNum(v), "Customers"]} />
              <Bar dataKey="customers" radius={[6, 6, 0, 0]}>
                {CLV_SEGMENTS.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        <Panel title="CLV Distribution by Tier" subtitle="Share of total portfolio value" delay={0.15}>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={CLV_SEGMENTS} dataKey="totalCLV" nameKey="segment" cx="50%" cy="50%" outerRadius={95} innerRadius={40}
                label={({ segment, percent }) => `${segment} ${(percent * 100).toFixed(0)}%`} labelLine={false}>
                {CLV_SEGMENTS.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Pie>
              <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmtCurrency(v, { compact: true }), "Portfolio CLV"]} />
            </PieChart>
          </ResponsiveContainer>
        </Panel>
      </div>

      {/* INDIVIDUAL CUSTOMER LOOKUP */}
      <Panel title="Customer Deep-Dive (Customer 360)" subtitle="Select from thousands of real customers to view their personalized intelligence profile" delay={0.2}>
        <div className="flex flex-col gap-6 md:flex-row">
          <div className="w-full md:w-1/3 space-y-4">
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">Select Customer ID / Name</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                {isLoading ? (
                  <div className="w-full rounded-xl border py-2.5 pl-10 pr-4 text-sm bg-black/20 text-muted-foreground" style={{ borderColor: "var(--glass-border)" }}>Loading database...</div>
                ) : (
                  <select 
                    className="w-full appearance-none rounded-xl border bg-transparent py-2.5 pl-10 pr-4 text-sm font-medium focus:outline-none focus:ring-2"
                    style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)", ringColor: "var(--primary)" }}
                    value={selectedCustomer.id}
                    onChange={(e) => setSelectedCustomerId(e.target.value)}
                  >
                    {apiCustomers.map((c: any) => (
                      <option key={c.id} value={c.id} style={{ background: "oklch(0.18 0.04 270)" }}>
                        {c.id} — {c.name}
                      </option>
                    ))}
                  </select>
                )}
              </div>
            </div>
            
            <motion.div key={selectedCustomer.id} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="rounded-xl border p-5 relative overflow-hidden" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.4)" }}>
              <div className="absolute top-0 right-0 w-24 h-24 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10" />
              
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full text-lg font-bold shadow-lg" style={{ background: "var(--gradient-primary)", color: "white" }}>
                  {selectedCustomer.name.charAt(0)}{selectedCustomer.name.split(' ')[1]?.[0] || ''}
                </div>
                <div>
                  <div className="text-xl font-bold truncate pr-4">{selectedCustomer.name}</div>
                  <div className="text-sm text-muted-foreground font-mono">{selectedCustomer.id !== "Unknown Customer" ? selectedCustomer.id : "No ID"}</div>
                </div>
              </div>

              {/* Personal Info Box */}
              {selectedCustomer.age && (
                <div className="mt-4 grid grid-cols-2 gap-2 p-3 rounded-lg border bg-black/20" style={{ borderColor: "var(--glass-border)" }}>
                  <div className="flex items-center gap-2">
                    <User className="h-3.5 w-3.5 text-primary" />
                    <span className="text-xs font-medium">{selectedCustomer.gender}, {selectedCustomer.age} yrs</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="h-3.5 w-3.5 text-primary" />
                    <span className="text-xs font-medium truncate">{selectedCustomer.city}</span>
                  </div>
                  <div className="flex items-center gap-2 col-span-2">
                    <Star className="h-3.5 w-3.5 text-gold" />
                    <span className="text-xs font-medium">Avg Rating: {selectedCustomer.avgRating?.toFixed(1)} / 5.0</span>
                  </div>
                </div>
              )}

              <div className="mt-4 space-y-3">
                <div className="flex justify-between border-b pb-2" style={{ borderColor: "var(--glass-border)" }}>
                  <span className="text-sm text-muted-foreground">Category Focus</span>
                  <span className="font-semibold text-gradient max-w-[150px] truncate text-right">{selectedCustomer.topCategory || "Mixed"}</span>
                </div>
                <div className="flex justify-between border-b pb-2" style={{ borderColor: "var(--glass-border)" }}>
                  <span className="text-sm text-muted-foreground">Sentiment</span>
                  <span className="font-semibold" style={{ color: sentiment === "Positive" ? "var(--success)" : sentiment === "Negative" ? "var(--destructive)" : "var(--gold)" }}>
                    {sentiment}
                  </span>
                </div>
                <div className="flex justify-between pt-1">
                  <span className="text-sm text-muted-foreground">Churn Risk</span>
                  <span className="font-semibold" style={{ color: churnRisk === "Low" ? "var(--success)" : churnRisk === "High" ? "var(--destructive)" : "var(--gold)" }}>
                    {churnRisk} ({(churnScore * 100).toFixed(1)}%)
                  </span>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="grid flex-1 grid-cols-2 gap-4">
            <motion.div key={`spend-${selectedCustomer.id}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.3)" }}>
              <div className="flex items-center gap-2 text-muted-foreground mb-2">
                <CreditCard className="h-4 w-4" />
                <span className="text-xs font-semibold uppercase">Total Spend & Payments</span>
              </div>
              <div className="text-3xl font-bold">{fmtCurrency(selectedCustomer.totalSpent || 0)}</div>
              <div className="mt-1 text-sm text-muted-foreground">Across <span className="font-bold text-foreground">{selectedCustomer.orders || 1}</span> historical orders</div>
            </motion.div>

            <motion.div key={`profit-${selectedCustomer.id}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }} className="rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.3)" }}>
              <div className="flex items-center gap-2 text-muted-foreground mb-2">
                <Activity className="h-4 w-4" />
                <span className="text-xs font-semibold uppercase">Est. Net Profit</span>
              </div>
              <div className="text-3xl font-bold" style={{ color: "var(--success)" }}>{fmtCurrency(profit)}</div>
              <div className="mt-1 text-sm text-muted-foreground">Based on approx. 24% margin</div>
            </motion.div>

            <motion.div key={`clv-${selectedCustomer.id}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="rounded-xl border p-4" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.3)" }}>
              <div className="flex items-center gap-2 text-muted-foreground mb-2">
                <TrendingUp className="h-4 w-4" />
                <span className="text-xs font-semibold uppercase">Predicted Lifetime Value</span>
              </div>
              <div className="text-3xl font-bold text-gradient-gold">{fmtCurrency((selectedCustomer.totalSpent || 0) * 1.5 + 200)}</div>
              <div className="mt-1 text-sm text-muted-foreground">Future expected revenue (AI Est)</div>
            </motion.div>

            <motion.div key={`focus-${selectedCustomer.id}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="rounded-xl border p-4 flex flex-col justify-center text-center relative overflow-hidden" style={{ borderColor: "var(--glass-border)", background: "var(--primary)/10" }}>
              <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: "var(--gradient-primary)" }} />
              <div className="text-[11px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-1">Customer Sentiment</div>
              <div className="text-4xl font-bold mt-2" style={{ color: sentiment === "Positive" ? "var(--success)" : sentiment === "Negative" ? "var(--destructive)" : "var(--gold)" }}>
                {sentiment}
              </div>
            </motion.div>
          </div>
        </div>
      </Panel>

      {/* RFM Segments */}
      <Panel title="RFM Segment Analysis" subtitle="Champions · Loyal · Potential · At-Risk" delay={0.25}>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {CUSTOMER_SEGMENTS_RFM.map((seg, i) => {
            const colors = ["oklch(0.78 0.18 195)", "oklch(0.78 0.2 150)", "oklch(0.82 0.18 80)", "oklch(0.66 0.24 25)"];
            return (
              <motion.div key={seg.segment} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 + i * 0.08 }}
                className="relative overflow-hidden rounded-xl border p-4 text-center" style={{ borderColor: "var(--glass-border)", background: "oklch(0.22 0.04 270 / 0.5)" }}>
                <div className="absolute inset-x-0 top-0 h-[2px]" style={{ background: colors[i] }} />
                <div className="text-xs text-muted-foreground">{seg.segment}</div>
                <div className="mt-2 text-2xl font-bold">{fmtNum(seg.count)}</div>
                <div className="mt-1 text-xs font-semibold text-gradient">{fmtCurrency(seg.avgCLV, { compact: true })} avg CLV</div>
                <div className="mt-0.5 text-[11px] text-muted-foreground">RFM: {seg.rfmScore}/15</div>
              </motion.div>
            );
          })}
        </div>
      </Panel>

      {/* CLV Tier Table */}
      <Panel title="CLV Tier Breakdown" subtitle="Portfolio value and customer count per tier" delay={0.35}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--glass-border)" }}>
                {["Tier", "Customers", "Avg CLV", "Portfolio Value", "Share"].map((h) => (
                  <th key={h} className="px-4 py-2.5 text-left text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {CLV_SEGMENTS.map((row, i) => {
                const share = (row.totalCLV / totalCLV * 100).toFixed(1);
                return (
                  <motion.tr key={row.segment} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 + i * 0.07 }}
                    className="border-b hover:bg-white/[0.03]" style={{ borderColor: "var(--glass-border)" }}>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-2.5 w-2.5 rounded-full" style={{ background: row.color }} />
                        <span className="font-semibold">{row.segment}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">{fmtNum(row.customers)}</td>
                    <td className="px-4 py-3 font-bold">{fmtCurrency(row.avgCLV, { compact: true })}</td>
                    <td className="px-4 py-3 font-bold text-gradient">{fmtCurrency(row.totalCLV, { compact: true })}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-20 rounded-full overflow-hidden" style={{ background: "oklch(0.3 0.04 270)" }}>
                          <div className="h-full rounded-full" style={{ width: `${share}%`, background: row.color }} />
                        </div>
                        <span>{share}%</span>
                      </div>
                    </td>
                  </motion.tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}
