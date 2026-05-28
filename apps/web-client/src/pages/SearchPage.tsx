import { type FormEvent, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { RagChunk } from "../api/types";

export default function SearchPage() {
  const { caseId } = useParams<{ caseId: string }>();
  const [query, setQuery] = useState("Vertrag");
  const [chunks, setChunks] = useState<RagChunk[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const id = Number(caseId);

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const result = await api.ragSearch(id, query.trim());
      setChunks(result.chunks);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Link to={`/cases/${caseId}`} className="text-sm text-blue-600 hover:underline">
        ← Back to case
      </Link>
      <h2 className="mt-2 mb-4 text-xl font-semibold">RAG Document Search</h2>
      <p className="mb-4 text-sm text-slate-500">
        Pretraga kroz Weaviate (BM25) — chunkovi se upisuju nakon ingestion sync-a.
      </p>

      <form onSubmit={handleSearch} className="mb-6 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search documents..."
          className="flex-1 rounded border border-slate-300 px-4 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {searched && chunks.length === 0 && !loading && (
        <p className="text-sm text-slate-500">
          No results. Try syncing the case first to ingest documents into Weaviate.
        </p>
      )}

      <div className="space-y-3">
        {chunks.map((chunk, i) => (
          <div key={i} className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="mb-2 flex items-center justify-between">
              <span className="font-medium">{chunk.filename}</span>
              <span className="rounded bg-blue-100 px-2 py-0.5 text-xs text-blue-800">
                score: {chunk.score.toFixed(2)}
              </span>
            </div>
            <p className="text-sm text-slate-600">{chunk.content}</p>
            <p className="mt-1 text-xs text-slate-400">document_id: {chunk.document_id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
