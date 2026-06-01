const API_URL = import.meta.env.VITE_API_URL || "/api";

function getToken(): string | null {
  return localStorage.getItem("cortex_token");
}

export function setToken(token: string | null) {
  if (token) {
    localStorage.setItem("cortex_token", token);
  } else {
    localStorage.removeItem("cortex_token");
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (response.status === 401) {
    setToken(null);
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  login: (username: string, password: string) =>
    request<{ access_token: string; user: import("./types").User }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  ssoUrl: () =>
    request<{ authorize_url: string; state: string }>("/auth/sso/url"),

  ssoCallback: (code: string, state?: string) =>
    request<{ access_token: string; user: import("./types").User }>("/auth/sso/callback", {
      method: "POST",
      body: JSON.stringify({ code, state }),
    }),

  me: () => request<import("./types").User>("/auth/me"),

  cases: () => request<import("./types").CaseSummary[]>("/cases"),

  case: (id: number) => request<import("./types").CaseDetail>(`/cases/${id}`),

  documents: (caseId: number) =>
    request<import("./types").DocumentSummary[]>(`/cases/${caseId}/documents`),

  document: (id: number) => request<import("./types").DocumentSummary>(`/documents/${id}`),

  triggerSync: (caseId: number) =>
    request<{ job_id: string; message: string }>(`/cases/${caseId}/sync`, { method: "POST" }),

  syncJob: (jobId: string) => request<import("./types").SyncJob>(`/sync/jobs/${jobId}`),

  createThread: (caseId: number) =>
    request<{ thread_id: string; case_id: number; created_at: string }>("/chat/threads", {
      method: "POST",
      body: JSON.stringify({ case_id: caseId }),
    }),

  threadHistory: (threadId: string) =>
    request<{ thread_id: string; messages: import("./types").ChatMessage[] }>(
      `/chat/threads/${threadId}`,
    ),

  translate: (documentId: number, targetLang = "de") =>
    request<import("./types").TranslateResponse>(`/documents/${documentId}/translate`, {
      method: "POST",
      body: JSON.stringify({ target_lang: targetLang }),
    }),

  auditLogs: () => request<import("./types").AuditLog[]>("/audit-logs"),

  systemStatus: () => request<import("./types").SystemStatus>("/system/status"),

  ragSearch: (caseId: number, query: string, limit = 5) =>
    request<import("./types").RagSearchResponse>(`/cases/${caseId}/search`, {
      method: "POST",
      body: JSON.stringify({ query, limit }),
    }),

  lookupLaw: (lawRef: string) => request<import("./types").LawNode>(`/laws/${lawRef}`),

  saveAssistantMessage: (threadId: string, content: string) =>
    request<{ status: string }>(`/chat/threads/${threadId}/assistant`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }),

  async *streamChat(threadId: string, message: string, caseId?: number) {
    const token = getToken();
    const response = await fetch(`${API_URL}/chat/threads/${threadId}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ message, case_id: caseId }),
    });

    if (!response.ok || !response.body) {
      throw new Error("Chat stream failed");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") return;
          try {
            const parsed = JSON.parse(data);
            yield parsed.content as string;
          } catch {
            // skip malformed chunks
          }
        }
      }
    }
  },
};
