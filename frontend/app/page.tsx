"use client";

import React, { useState } from "react";
import Header from "../components/Header";
import ChatBubbleAssistant from "../components/ChatBubbleAssistant";
import ChatBubbleUser from "../components/ChatBubbleUser";
import Composer from "../components/Composer";
import NotebookStub from "../components/NotebookStub";
import {
  mockMessages,
  Message,
  notebookEntries,
} from "../lib/mockData";

export default function Page() {
  const [messages, setMessages] = useState<Message[]>(mockMessages);
  const [notebookOpen, setNotebookOpen] = useState(true);

  const addAssistantEcho = (text: string, timestamp: Date): Message => ({
    id: `assistant-${timestamp.getTime()}`,
    role: "assistant",
    persona: "Airth 📚",
    text: `I heard: “${text.slice(0, 180)}”\n\nNotebook sync is ready when you are.`,
    citations: [{ label: "Notebook Sync" }],
    r: 0.81,
    timestamp: timestamp.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
  });

  const handleSend = (text: string) => {
    const createdAt = new Date();
    const userMessage: Message = {
      id: `user-${createdAt.getTime()}`,
      role: "user",
      text,
      timestamp: createdAt.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, userMessage, addAssistantEcho(text, createdAt)]);
  };

  return (
    <main className="min-h-screen bg-[#050510] text-white">
      <Header userName="Witness" rScore={0.87} />
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-6 lg:flex-row lg:px-6 lg:py-10">
        <section className="flex flex-1 flex-col rounded-3xl border border-white/5 bg-white/[0.03] p-4 shadow-2xl shadow-slate-950/40">
          <div
            className="flex-1 space-y-4 overflow-y-auto pr-1"
            style={{ maxHeight: "calc(100vh - 260px)" }}
            data-testid="chat-stream"
          >
            {messages.map((message) =>
              message.role === "assistant" ? (
                <ChatBubbleAssistant
                  key={message.id}
                  text={message.text}
                  citations={message.citations}
                  r={message.r}
                  persona={message.persona}
                />
              ) : (
                <ChatBubbleUser key={message.id} text={message.text} />
              )
            )}
          </div>
          <div className="mt-4">
            <Composer
              onSend={handleSend}
              onOpenNotebook={() => setNotebookOpen(true)}
            />
          </div>
        </section>
        <NotebookStub
          open={notebookOpen}
          onClose={() => setNotebookOpen(false)}
          onOpen={() => setNotebookOpen(true)}
          entries={notebookEntries}
        />
      </div>
    </main>
  );
}
