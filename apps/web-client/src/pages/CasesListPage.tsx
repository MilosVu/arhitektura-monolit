import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { CaseSummary } from "../api/types";

export default function CasesListPage() {
  const [cases, setCases] = useState<CaseSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.cases().then(setCases).finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-500">Loading cases...</p>;

  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold">Cases</h2>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              <th className="px-4 py-3 font-medium">Case Number</th>
              <th className="px-4 py-3 font-medium">Title</th>
              <th className="px-4 py-3 font-medium">Documents</th>
              <th className="px-4 py-3 font-medium">Last Synced</th>
              <th className="px-4 py-3 font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c) => (
              <tr key={c.id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-4 py-3 font-mono text-xs">{c.case_number}</td>
                <td className="px-4 py-3">{c.title}</td>
                <td className="px-4 py-3">{c.document_count}</td>
                <td className="px-4 py-3 text-slate-500">
                  {c.last_synced_at ? new Date(c.last_synced_at).toLocaleString() : "Never"}
                </td>
                <td className="px-4 py-3">
                  <Link to={`/cases/${c.id}`} className="text-blue-600 hover:underline">
                    Open
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
