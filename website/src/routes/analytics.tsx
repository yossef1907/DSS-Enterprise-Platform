import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/analytics-page";

export const Route = createFileRoute("/analytics")({
  head: () => ({ meta: [{ title: "Advanced Analytics Hub · DSS Pro" }, { name: "description", content: "OLAP cube · bootstrap CI · drill-downs." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Advanced Analytics Hub" subtitle="OLAP cube · bootstrap CI · drill-downs." />
      <PageBody />
    </div>
  );
}
