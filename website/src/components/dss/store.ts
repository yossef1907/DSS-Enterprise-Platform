import { create } from "zustand";

export type TestRecord = {
  id: string;
  date: string;
  name: string;
  category: string;
  price: number;
  discount: number;
  budget: number;
  successProb: number;
  decision: "GO" | "REVIEW" | "NO-GO";
};

type State = {
  history: TestRecord[];
  addTest: (t: TestRecord) => void;
  reset: () => void;
};

export const useLabStore = create<State>((set) => ({
  history: [],
  addTest: (t) => set((s: State) => ({ history: [t, ...s.history].slice(0, 30) })),
  reset: () => set({ history: [] }),
}));
