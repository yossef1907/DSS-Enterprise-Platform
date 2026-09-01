import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/customers-page";

export const Route = createFileRoute("/customers")({
  head: () => ({ meta: [{ title: "Customer Intelligence 360 · DSS Pro" }, { name: "description", content: "Search, profile, and act on every customer." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Customer Intelligence 360" subtitle="Search, profile, and act on every customer." />
      <PageBody />
    </div>
  );
}
