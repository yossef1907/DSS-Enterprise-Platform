import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/sales-page";

export const Route = createFileRoute("/sales")({
  head: () => ({ meta: [{ title: "Sales Intelligence · DSS Pro" }, { name: "description", content: "Live sales, channel mix, and growth trends." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Sales Intelligence" subtitle="Live sales, channel mix, and growth trends." />
      <PageBody />
    </div>
  );
}
