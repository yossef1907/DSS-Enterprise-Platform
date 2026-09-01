import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/marketing-page";

export const Route = createFileRoute("/marketing")({
  head: () => ({ meta: [{ title: "Marketing ROI Intelligence · DSS Pro" }, { name: "description", content: "-41.1% → +184.97% transformation." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Marketing ROI Intelligence" subtitle="-41.1% → +184.97% transformation." />
      <PageBody />
    </div>
  );
}
