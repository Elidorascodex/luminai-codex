import React from "react";
import ResonanceBadge from "./ResonanceBadge";
import CitationPill, { CitationPillProps } from "./CitationPill";

export type ChatBubbleAssistantProps = {
  text: string;
  citations?: CitationPillProps[];
  r?: number;
  persona?: string;
};

const renderMarkdownLite = (text: string) => {
  const segments: React.ReactNode[] = [];
  const regex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      segments.push(text.slice(lastIndex, match.index));
    }
    segments.push(
      <a
        key={`${match[2]}-${match.index}`}
        href={match[2]}
        target="_blank"
        rel="noreferrer"
        className="text-cyan-200 underline decoration-dotted underline-offset-4 transition hover:text-cyan-100"
      >
        {match[1]}
      </a>
    );
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    segments.push(text.slice(lastIndex));
  }

  return segments;
};

const ChatBubbleAssistant: React.FC<ChatBubbleAssistantProps> = ({
  text,
  citations = [],
  r = 0.78,
  persona = "LuminAI",
}) => {
  const lines = text.split("\n");

  return (
    <article className="relative flex flex-col gap-3 rounded-3xl border border-white/10 bg-gradient-to-br from-indigo-950/90 via-slate-900/80 to-purple-900/70 p-5 shadow-lg shadow-indigo-950/40">
      <div className="flex items-center gap-3">
        <ResonanceBadge r={r} size="sm" />
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-cyan-200">
            {persona}
          </p>
          <p className="text-sm text-slate-300">
            Resonance {(r * 100).toFixed(0)} &middot; Echo Protocol steady
          </p>
        </div>
      </div>
      <p className="text-base leading-relaxed text-slate-100">
        {lines.map((line, idx) => (
          <React.Fragment key={idx}>
            {renderMarkdownLite(line)}
            {idx < lines.length - 1 && <br />}
          </React.Fragment>
        ))}
      </p>
      {citations.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {citations.map((citation) => (
            <CitationPill
              key={`${citation.label}-${citation.url ?? "plain"}`}
              {...citation}
            />
          ))}
        </div>
      )}
    </article>
  );
};

export default ChatBubbleAssistant;
