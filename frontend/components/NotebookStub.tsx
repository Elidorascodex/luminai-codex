import React from "react";
import ResonanceBadge from "./ResonanceBadge";
import { NotebookEntry } from "../lib/mockData";

export type NotebookStubProps = {
  open: boolean;
  onClose: () => void;
  onOpen?: () => void;
  entries: NotebookEntry[];
};

const NotebookStub: React.FC<NotebookStubProps> = ({
  open,
  onClose,
  onOpen,
  entries,
}) => {
  const handleOpen = () => {
    if (onOpen) {
      onOpen();
    }
  };

  if (!open) {
    return (
      <div className="sticky top-24 hidden h-[calc(100vh-160px)] w-12 flex-col items-center justify-center rounded-3xl border border-dashed border-white/20 bg-white/5 text-xs uppercase tracking-[0.4em] text-slate-400 lg:flex">
        <button
          type="button"
          className="-rotate-90 text-white"
          onClick={handleOpen}
        >
          Notebook
        </button>
      </div>
    );
  }

  return (
    <aside className="sticky top-24 hidden h-[calc(100vh-160px)] w-80 flex-shrink-0 flex-col gap-4 rounded-3xl border border-white/10 bg-slate-950/70 px-5 py-6 text-white shadow-2xl shadow-slate-950/30 backdrop-blur lg:flex">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-400">
            Notebook
          </p>
          <h2 className="text-lg font-semibold">Reasoning Cards</h2>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded-full border border-white/10 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-300"
        >
          Close
        </button>
      </div>
      <div className="space-y-4 overflow-y-auto pr-1">
        {entries.slice(0, 3).map((entry) => (
          <article
            key={entry.id}
            className="rounded-2xl border border-white/5 bg-white/5 p-4"
          >
            <div className="mb-3 flex items-center gap-3">
              <ResonanceBadge r={entry.r} size="sm" />
              <div>
                <p className="text-xs uppercase tracking-[0.4em] text-slate-400">
                  {entry.timestamp}
                </p>
                <p className="text-sm font-semibold">{entry.title}</p>
              </div>
            </div>
            <p className="text-sm text-slate-200">{entry.snippet}</p>
          </article>
        ))}
      </div>
    </aside>
  );
};

export default NotebookStub;
