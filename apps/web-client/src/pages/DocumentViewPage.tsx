import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { DocumentSummary } from "../api/types";

export default function DocumentViewPage() {
  const { caseId, documentId } = useParams<{ caseId: string; documentId: string }>();
  const [doc, setDoc] = useState<DocumentSummary | null>(null);

  useEffect(() => {
    if (!documentId) return;
    api.document(Number(documentId)).then(setDoc);
  }, [documentId]);

  if (!doc) return <p className="text-slate-500">Loading document...</p>;

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <Link to={`/cases/${caseId}`} className="text-sm text-blue-600 hover:underline">
            ← Back to case
          </Link>
          <h2 className="mt-1 text-xl font-semibold">{doc.filename}</h2>
        </div>
        <Link
          to={`/cases/${caseId}/documents/${documentId}/translate`}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Translate
        </Link>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-8">
        <div className="flex h-96 items-center justify-center rounded border-2 border-dashed border-slate-300 bg-slate-50">
          <div className="text-center text-slate-400">
            <p className="text-lg font-medium">PDF Viewer Placeholder</p>
            <p className="mt-1 text-sm">{doc.filename}</p>
            <p className="mt-1 text-xs">{doc.page_count ?? "?"} pages · {doc.status}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
