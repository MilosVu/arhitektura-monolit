import { type FormEvent, useEffect, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { ChatMessage } from "../api/types";

export default function ChatPage() {
  const { caseId, threadId: urlThreadId } = useParams<{ caseId: string; threadId?: string }>();
  const navigate = useNavigate();
  const [threadId, setThreadId] = useState<string | null>(urlThreadId || null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const id = Number(caseId);

  useEffect(() => {
    if (urlThreadId) {
      setThreadId(urlThreadId);
      api.threadHistory(urlThreadId).then((h) => setMessages(h.messages));
    } else {
      api.createThread(id).then((t) => {
        setThreadId(t.thread_id);
        navigate(`/cases/${caseId}/chat/${t.thread_id}`, { replace: true });
      });
    }
  }, [urlThreadId, id, caseId, navigate]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !threadId || streaming) return;

    const userMsg: ChatMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setStreaming(true);

    const assistantMsg: ChatMessage = { role: "assistant", content: "" };
    setMessages((prev) => [...prev, assistantMsg]);

    try {
      let assistantContent = "";
      for await (const chunk of api.streamChat(threadId, userMsg.content, id)) {
        assistantContent += chunk;
        setMessages((prev) => {
          const updated = [...prev];
          const last = updated[updated.length - 1];
          if (last.role === "assistant") {
            last.content = assistantContent;
          }
          return updated;
        });
      }
      if (assistantContent) {
        await api.saveAssistantMessage(threadId, assistantContent);
      }
    } catch {
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last.role === "assistant") {
          last.content = "Error: Could not reach AI agents service.";
        }
        return updated;
      });
    } finally {
      setStreaming(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col">
      <div className="mb-4">
        <Link to={`/cases/${caseId}`} className="text-sm text-blue-600 hover:underline">
          ← Back to case
        </Link>
        <h2 className="text-xl font-semibold">AI Chat</h2>
        {threadId && <p className="text-xs text-slate-400">Thread: {threadId}</p>}
      </div>

      <div className="flex-1 overflow-auto rounded-lg border border-slate-200 bg-white p-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-3 ${msg.role === "user" ? "text-right" : "text-left"}`}
          >
            <span
              className={`inline-block max-w-[80%] rounded-lg px-4 py-2 text-sm ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-800"
              }`}
            >
              {msg.content}
              {streaming && i === messages.length - 1 && msg.role === "assistant" && (
                <span className="ml-1 animate-pulse">▊</span>
              )}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSend} className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about this case..."
          className="flex-1 rounded border border-slate-300 px-4 py-2 text-sm"
          disabled={streaming}
        />
        <button
          type="submit"
          disabled={streaming || !input.trim()}
          className="rounded bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
