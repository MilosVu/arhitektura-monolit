import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { CaseDetail, DocumentSummary } from "../api/types";

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  syncing: "bg-blue-100 text-blue-800",
  ingesting: "bg-purple-100 text-purple-800",
  ready: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
};

export default function CaseDetailPage() {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<CaseDetail | null>(null);
  const [documents, setDocuments] = useState<DocumentSummary[]>([]);
  const [syncing, setSyncing] = useState(false);

  const id = Number(caseId);

  useEffect(() => {
    if (!id) return;
    Promise.all([api.case(id), api.documents(id)]).then(([c, docs]) => {
      setCaseData(c);
      setDocuments(docs);
    });
  }, [id]);

  const handleSync = async () => {
    setSyncing(true);
    try {
      const result = await api.triggerSync(id);
      navigate(`/sync/${result.job_id}`);
    } finally {
      setSyncing(false);
    }
  };

  if (!caseData) return <p className="text-slate-500">Loading case...</p>;

  return (
    <div>
      <div className="mb-6 flex items-start justify-between">
        <div>
          <p className="font-mono text-sm text-slate-500">{caseData.case_number}</p>
          <h2 className="text-xl font-semibold">{caseData.title}</h2>
          {caseData.description && (
            <p className="mt-1 text-sm text-slate-600">{caseData.description}</p>
          )}
        </div>
        <div className="flex gap-2">
          <Link
            to={`/cases/${id}/chat`}
            className="rounded border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50"
          >
            AI Chat
          </Link>
          <Link
            to={`/cases/${id}/search`}
            className="rounded border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50"
          >
            RAG Search
          </Link>
          <button
            onClick={handleSync}
            disabled={syncing}
            className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {syncing ? "Starting..." : "Sinhronizuj (Alfresco)"}
          </button>
        </div>
      </div>

      <h3 className="mb-3 font-medium">Documents</h3>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              <th className="px-4 py-3 font-medium">Filename</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Pages</th>
              <th className="px-4 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id} className="border-b border-slate-100">
                <td className="px-4 py-3">{doc.filename}</td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[doc.status] || "bg-slate-100"}`}
                  >
                    {doc.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate-500">{doc.page_count ?? "—"}</td>
                <td className="px-4 py-3">
                  <Link
                    to={`/cases/${id}/documents/${doc.id}`}
                    className="mr-3 text-blue-600 hover:underline"
                  >
                    View
                  </Link>
                  <Link
                    to={`/cases/${id}/documents/${doc.id}/translate`}
                    className="text-blue-600 hover:underline"
                  >
                    Translate
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
