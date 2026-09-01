import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/score-page";

export const Route = createFileRoute("/score")({
  head: () => ({ meta: [{ title: "Project Score & Inventory · DSS Pro" }, { name: "description", content: "14 components · 109 tables · 200 files." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Project Score & Inventory" subtitle="14 components · 109 tables · 200 files." />
      <PageBody />
    </div>
  );
}
