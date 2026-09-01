import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/forecast-page";

export const Route = createFileRoute("/forecast")({
  head: () => ({ meta: [{ title: "Sales Forecasting · DSS Pro" }, { name: "description", content: "Holt-Winters & ARIMA projections." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Sales Forecasting" subtitle="Holt-Winters & ARIMA projections." />
      <PageBody />
    </div>
  );
}
