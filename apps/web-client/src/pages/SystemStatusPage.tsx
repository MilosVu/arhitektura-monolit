import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { ComponentStatus, SystemStatus } from "../api/types";

const statusColor: Record<string, string> = {
  ok: "border-green-200 bg-green-50 text-green-800",
  degraded: "border-yellow-200 bg-yellow-50 text-yellow-800",
  down: "border-red-200 bg-red-50 text-red-800",
};

const dotColor: Record<string, string> = {
  ok: "bg-green-500",
  degraded: "bg-yellow-500",
  down: "bg-red-500",
};

function ComponentCard({ component }: { component: ComponentStatus }) {
  return (
    <div className={`rounded-lg border p-4 ${statusColor[component.status] || "border-slate-200 bg-white"}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-full ${dotColor[component.status] || "bg-slate-400"}`} />
          <span className="font-medium">{component.name}</span>
        </div>
        {component.latency_ms != null && (
          <span className="text-xs opacity-70">{component.latency_ms} ms</span>
        )}
      </div>
      {component.detail && (
        <p className="mt-2 text-xs opacity-80">{component.detail}</p>
      )}
    </div>
  );
}

export default function SystemStatusPage() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState("");

  const load = () => {
    api
      .systemStatus()
      .then(setStatus)
      .catch((e) => setError(String(e)));
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">System Status</h2>
          <p className="text-sm text-slate-500">
            Health check svih komponenti arhitekture
            {status && ` · ${new Date(status.checked_at).toLocaleTimeString()}`}
          </p>
        </div>
        {status && (
          <span
            className={`rounded-full px-3 py-1 text-sm font-medium capitalize ${statusColor[status.overall]}`}
          >
            {status.overall}
          </span>
        )}
      </div>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

      {status ? (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {status.components.map((c) => (
            <ComponentCard key={c.name} component={c} />
          ))}
        </div>
      ) : (
        <p className="text-slate-500">Loading system status...</p>
      )}

      <div className="mt-8 rounded-lg border border-slate-200 bg-white p-4">
        <h3 className="mb-3 font-medium">Dev Tools</h3>
        <div className="flex flex-wrap gap-3 text-sm">
          <a href="http://localhost:15672" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            RabbitMQ UI (:15672)
          </a>
          <a href="http://localhost:7474" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            Neo4j Browser (:7474)
          </a>
          <a href="http://localhost:5555" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            Celery Flower (:5555)
          </a>
          <a href="http://localhost:8080/v1/meta" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            Weaviate (:8080)
          </a>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            API Gateway Docs
          </a>
          <a href="http://localhost:8001/docs" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
            AI Agents Docs
          </a>
        </div>
      </div>
    </div>
  );
}
