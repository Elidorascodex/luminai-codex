import React from "react";

export type ChatBubbleUserProps = {
  text: string;
};

const ChatBubbleUser: React.FC<ChatBubbleUserProps> = ({ text }) => (
  <article className="ml-auto max-w-3xl rounded-3xl border border-slate-500/40 bg-slate-900/60 px-5 py-4 text-right text-slate-100 shadow-lg shadow-slate-900/30">
    <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
      Witness
    </p>
    <p className="mt-2 whitespace-pre-line text-base leading-relaxed">
      {text}
    </p>
  </article>
);

export default ChatBubbleUser;
