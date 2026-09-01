import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/clv-page";

export const Route = createFileRoute("/clv")({
  head: () => ({ meta: [{ title: "Customer Lifetime Value · DSS Pro" }, { name: "description", content: ".08B portfolio across 4 segments." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Customer Lifetime Value" subtitle=".08B portfolio across 4 segments." />
      <PageBody />
    </div>
  );
}
