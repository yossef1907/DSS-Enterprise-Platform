export const chartTheme = {
  axis: "oklch(0.7 0.03 260)",
  grid: "oklch(0.5 0.05 270 / 0.15)",
  tooltipBg: "oklch(0.18 0.04 270 / 0.95)",
  tooltipBorder: "oklch(0.7 0.05 260 / 0.25)",
};

export const tooltipStyle = {
  background: chartTheme.tooltipBg,
  border: `1px solid ${chartTheme.tooltipBorder}`,
  borderRadius: 12,
  color: "white",
  fontSize: 12,
  backdropFilter: "blur(12px)",
};
export const labelStyle = { color: "oklch(0.7 0.03 260)", fontSize: 11 };