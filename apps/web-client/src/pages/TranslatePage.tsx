import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { DocumentSummary, TranslateResponse } from "../api/types";

export default function TranslatePage() {
  const { caseId, documentId } = useParams<{ caseId: string; documentId: string }>();
  const [doc, setDoc] = useState<DocumentSummary | null>(null);
  const [translation, setTranslation] = useState<TranslateResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!documentId) return;
    api.document(Number(documentId)).then(setDoc);
  }, [documentId]);

  const handleTranslate = async () => {
    if (!documentId) return;
    setLoading(true);
    try {
      const result = await api.translate(Number(documentId), "de");
      setTranslation(result);
    } finally {
      setLoading(false);
    }
  };

  if (!doc) return <p className="text-slate-500">Loading...</p>;

  return (
    <div>
      <Link to={`/cases/${caseId}/documents/${documentId}`} className="text-sm text-blue-600 hover:underline">
        ← Back to document
      </Link>
      <h2 className="mt-2 mb-4 text-xl font-semibold">Translate: {doc.filename}</h2>

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h3 className="mb-2 text-sm font-medium text-slate-500">Original (PDF)</h3>
          <div className="flex h-80 items-center justify-center rounded border border-dashed border-slate-300 bg-slate-50 text-slate-400">
            PDF placeholder — {doc.filename}
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <div className="mb-2 flex items-center justify-between">
            <h3 className="text-sm font-medium text-slate-500">Translation</h3>
            <button
              onClick={handleTranslate}
              disabled={loading}
              className="rounded bg-blue-600 px-3 py-1 text-xs font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Translating..." : "Run Translation Agent"}
            </button>
          </div>
          <div className="h-80 overflow-auto rounded border border-slate-200 bg-slate-50 p-4 text-sm whitespace-pre-wrap">
            {translation ? translation.translated_text : "Click to run translation via ai-agents service..."}
          </div>
        </div>
      </div>
    </div>
  );
}
