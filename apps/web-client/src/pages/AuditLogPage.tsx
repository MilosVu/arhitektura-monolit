import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { AuditLog } from "../api/types";

export default function AuditLogPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.auditLogs().then(setLogs).finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-500">Loading audit logs...</p>;

  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold">Audit Log</h2>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              <th className="px-4 py-3 font-medium">Time</th>
              <th className="px-4 py-3 font-medium">Action</th>
              <th className="px-4 py-3 font-medium">Resource</th>
              <th className="px-4 py-3 font-medium">Details</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b border-slate-100">
                <td className="px-4 py-3 text-slate-500">
                  {new Date(log.created_at).toLocaleString()}
                </td>
                <td className="px-4 py-3 font-mono text-xs">{log.action}</td>
                <td className="px-4 py-3">
                  {log.resource_type}/{log.resource_id}
                </td>
                <td className="px-4 py-3 text-slate-600">{log.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
