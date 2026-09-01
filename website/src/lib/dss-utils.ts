export const fmtCurrency = (n: number, opts: { compact?: boolean } = {}) => {
  if (opts.compact) {
    if (Math.abs(n) >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
    if (Math.abs(n) >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
    if (Math.abs(n) >= 1e3) return `$${(n / 1e3).toFixed(1)}K`;
  }
  return `$${n.toLocaleString("en-US", { maximumFractionDigits: 2 })}`;
};
export const fmtNum = (n: number, d = 0) =>
  n.toLocaleString("en-US", { maximumFractionDigits: d, minimumFractionDigits: d });
export const fmtPct = (n: number, d = 1) => `${n.toFixed(d)}%`;

export function calcSuccessProb(
  category: string,
  discount: number,
  season: string,
  city: string,
  price: number,
  quantity: number,
) {
  // Heuristic: maps to provided scenario data tendencies
  let base = 50;
  if (category === "Home & Garden") base = 80;
  else if (category === "Toys") base = 55;
  else if (category === "Electronics") base = 50;
  else if (category === "Fashion") base = 48;
  else if (category === "Sports") base = 45;
  else if (category === "Beauty") base = 42;
  else if (category === "Books") base = 40;
  else if (category === "Food") base = 47;

  // Discount sweet spot at 40-50
  const dCurve = -0.012 * (discount - 50) * (discount - 50) + 18;
  base += dCurve;

  if (season === "Fall") base += 8;
  else if (season === "Spring") base += 4;
  else if (season === "Winter") base -= 2;
  else if (season === "Summer") base += 1;

  if (city === "Istanbul") base += 6;
  else if (city === "Ankara") base += 2;
  else if (city === "Izmir") base += 1;

  // price/quantity damping
  if (price > 500) base -= 4;
  if (quantity < 50) base -= 3;
  if (quantity > 1000) base += 2;

  return Math.max(2, Math.min(99.9, base));
}

export function decisionFor(prob: number) {
  if (prob >= 70) return "GO" as const;
  if (prob >= 40) return "REVIEW" as const;
  return "NO-GO" as const;
}