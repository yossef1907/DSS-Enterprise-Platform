const API_URL = "http://localhost:8765/api";

export async function fetchSalesData() {
  const res = await fetch(`${API_URL}/sales`);
  if (!res.ok) throw new Error("Failed to fetch sales data");
  return res.json();
}

export async function fetchMetrics() {
  const res = await fetch(`${API_URL}/metrics`);
  if (!res.ok) throw new Error("Failed to fetch metrics");
  return res.json();
}

export async function fetchChurnData() {
  const res = await fetch(`${API_URL}/churn`);
  if (!res.ok) throw new Error("Failed to fetch churn data");
  return res.json();
}

export async function fetchBasketData() {
  const res = await fetch(`${API_URL}/basket`);
  if (!res.ok) throw new Error("Failed to fetch basket data");
  return res.json();
}

export async function fetchForecastData() {
  const res = await fetch(`${API_URL}/forecast`);
  if (!res.ok) throw new Error("Failed to fetch forecast data");
  return res.json();
}

export async function fetchMarketingData() {
  const res = await fetch(`${API_URL}/marketing`);
  if (!res.ok) throw new Error("Failed to fetch marketing data");
  return res.json();
}

export async function fetchReportData(month?: string, force_ai: boolean = false) {
  let url = `${API_URL}/report`;
  const params = new URLSearchParams();
  if (month) params.append("month", month);
  if (force_ai) params.append("force_ai", "true");
  
  if (params.toString()) {
    url += `?${params.toString()}`;
  }
  
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch report data");
  return res.json();
}

export async function fetchCustomers() {
  const res = await fetch(`${API_URL}/customers`);
  if (!res.ok) throw new Error("Failed to fetch customers");
  return res.json();
}
