import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/churn-page";

export const Route = createFileRoute("/churn")({
  head: () => ({ meta: [{ title: "Churn Risk Command Center · DSS Pro" }, { name: "description", content: "Identify and retain at-risk customers." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Churn Risk Command Center" subtitle="Identify and retain at-risk customers." />
      <PageBody />
    </div>
  );
}
