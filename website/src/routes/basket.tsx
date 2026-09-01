import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/basket-page";

export const Route = createFileRoute("/basket")({
  head: () => ({ meta: [{ title: "Market Basket Intelligence · DSS Pro" }, { name: "description", content: "722 association rules · max lift 7.59x." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Market Basket Intelligence" subtitle="722 association rules · max lift 7.59x." />
      <PageBody />
    </div>
  );
}
