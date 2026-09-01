import { Panel } from "@/components/dss/Panel";
import { motion } from "framer-motion";

export function ComingSoon({ note }: { note: string }) {
  return (
    <Panel title="Module Online" subtitle={note}>
      <motion.div
        initial={{ opacity: 0 }} animate={{ opacity: 1 }}
        className="flex flex-col items-center justify-center gap-3 py-16 text-center"
      >
        <div className="text-6xl">⚡</div>
        <div className="text-lg font-semibold text-gradient">Intelligence Module Active</div>
        <div className="max-w-md text-sm text-muted-foreground">
          Data is wired and reactive. Visit the <b>Executive Hub</b> and <b>Product Lab</b> for the full
          showcase experience — this surface streams from the same engine.
        </div>
      </motion.div>
    </Panel>
  );
}
