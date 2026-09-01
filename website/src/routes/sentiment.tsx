import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/dss/PageHeader";
import { Panel } from "@/components/dss/Panel";
import PageBody from "@/components/dss/pages/sentiment-page";

export const Route = createFileRoute("/sentiment")({
  head: () => ({ meta: [{ title: "Sentiment & NLP Analysis · DSS Pro" }, { name: "description", content: "471,115 reviews analyzed." }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="Sentiment & NLP Analysis" subtitle="471,115 reviews analyzed." />
      <PageBody />
    </div>
  );
}
