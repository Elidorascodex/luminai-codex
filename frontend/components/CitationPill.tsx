import React from "react";

export type CitationPillProps = {
  label: string;
  url?: string;
};

const CitationPill: React.FC<CitationPillProps> = ({ label, url }) => {
  const content = (
    <span className="inline-flex items-center gap-1 text-xs font-medium">
      <span>{label}</span>
      {url && <span aria-hidden="true">↗</span>}
    </span>
  );

  if (url) {
    return (
      <a
        href={url}
        target="_blank"
        rel="noreferrer"
        className="rounded-full border border-cyan-300/60 bg-cyan-500/10 px-3 py-1 text-cyan-100 transition hover:bg-cyan-500/20"
      >
        {content}
      </a>
    );
  }

  return (
    <span className="rounded-full border border-slate-500/60 bg-slate-700/30 px-3 py-1 text-slate-100">
      {content}
    </span>
  );
};

export default CitationPill;
