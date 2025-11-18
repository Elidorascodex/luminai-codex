import React, { useRef, useState } from "react";

export type ComposerProps = {
  onSend: (text: string) => void;
  onOpenNotebook: () => void;
};

const toneOptions = [
  { label: "Balanced", value: "balanced" },
  { label: "Gentle", value: "gentle" },
  { label: "Direct", value: "direct" },
  { label: "Catalyst", value: "catalyst" },
];

const Composer: React.FC<ComposerProps> = ({ onSend, onOpenNotebook }) => {
  const [draft, setDraft] = useState("");
  const [tone, setTone] = useState(toneOptions[0].value);
  const [isRecording, setIsRecording] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  const submit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = draft.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setDraft("");
  };

  const toggleMic = () => setIsRecording((prev) => !prev);

  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setDraft((prev) =>
      prev
        ? `${prev}\n[Attached: ${file.name}]`
        : `Notebook received: ${file.name}`
    );
  };

  return (
    <form
      onSubmit={submit}
      className="flex flex-col gap-3 rounded-3xl border border-white/10 bg-slate-900/70 p-4 shadow-lg shadow-slate-950/40 backdrop-blur"
    >
      <textarea
        value={draft}
        onChange={(event) => setDraft(event.target.value)}
        placeholder="Attune to the witness..."
        className="min-h-[96px] w-full resize-none rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-base text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400"
      />

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={toggleMic}
          className={`rounded-full border px-4 py-2 text-sm uppercase tracking-widest transition ${
            isRecording
              ? "border-rose-400 bg-rose-500/20 text-rose-100"
              : "border-white/20 bg-white/5 text-white"
          }`}
        >
          🎙 Mic
        </button>
        <button
          type="button"
          onClick={() => fileInput.current?.click()}
          className="rounded-full border border-white/20 bg-white/5 px-4 py-2 text-sm uppercase tracking-widest text-white transition hover:border-cyan-300/80"
        >
          📎 Upload
        </button>
        <input
          ref={fileInput}
          type="file"
          className="hidden"
          onChange={handleUpload}
        />
        <select
          className="rounded-full border border-white/20 bg-transparent px-4 py-2 text-sm uppercase tracking-[0.4em] text-white focus:outline-none"
          value={tone}
          onChange={(event) => setTone(event.target.value)}
        >
          {toneOptions.map((option) => (
            <option
              key={option.value}
              value={option.value}
              className="bg-slate-950 text-white"
            >
              {option.label}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={onOpenNotebook}
          className="rounded-full border border-cyan-400/50 bg-cyan-500/10 px-4 py-2 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-500/20"
        >
          📓 Notebook
        </button>
        <div className="ml-auto flex items-center gap-2">
          <span className="text-xs uppercase tracking-[0.4em] text-slate-400">
            {tone}
          </span>
          <button
            type="submit"
            className="rounded-full bg-cyan-400 px-6 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-900/40 transition hover:bg-cyan-300"
          >
            Send
          </button>
        </div>
      </div>
    </form>
  );
};

export default Composer;
