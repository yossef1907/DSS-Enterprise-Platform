import { createFileRoute } from '@tanstack/react-router';
import { PageHeader } from '@/components/dss/PageHeader';
import ReportPage from '@/components/dss/pages/report-page';

export const Route = createFileRoute('/report')({
  head: () => ({ meta: [{ title: "AI Performance Report" }] }),
  component: Page,
});

function Page() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="DSS PRO" title="AI Performance Report" subtitle="Monthly executive summary, root cause analysis, and strategic recommendations." />
      <ReportPage />
    </div>
  );
}
