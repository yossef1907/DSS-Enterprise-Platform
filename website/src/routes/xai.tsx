import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/xai-page";

export const Route = createFileRoute("/xai")({
  head: () => ({ meta: [{ title: "Explainable AI · DSS Pro" }, { name: "description", content: "SHAP feature importance & per-customer reasoning." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Explainable AI" subtitle="SHAP feature importance & per-customer reasoning." />
      <PageBody />
    </div>
  );
}
