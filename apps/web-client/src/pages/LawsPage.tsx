import { type FormEvent, useState } from "react";
import { api } from "../api/client";
import type { LawNode } from "../api/types";

const QUICK_REFS = ["stgb-146", "or-41", "zpo-80"];

export default function LawsPage() {
  const [lawRef, setLawRef] = useState("stgb-146");
  const [law, setLaw] = useState<LawNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const lookup = async (ref: string) => {
    setLoading(true);
    setError("");
    setLawRef(ref);
    try {
      const result = await api.lookupLaw(ref);
      setLaw(result);
    } catch (e) {
      setError(String(e));
      setLaw(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    lookup(lawRef.trim());
  };

  return (
    <div>
      <h2 className="mb-1 text-xl font-semibold">Law Lookup (Neo4j)</h2>
      <p className="mb-6 text-sm text-slate-500">
        LawLink stub — pretraga švajcarskih zakona iz Knowledge Graph baze.
      </p>

      <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
        <input
          value={lawRef}
          onChange={(e) => setLawRef(e.target.value)}
          placeholder="e.g. stgb-146"
          className="flex-1 rounded border border-slate-300 px-4 py-2 text-sm font-mono"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Lookup"}
        </button>
      </form>

      <div className="mb-6 flex gap-2">
        {QUICK_REFS.map((ref) => (
          <button
            key={ref}
            type="button"
            onClick={() => lookup(ref)}
            className="rounded border border-slate-300 px-3 py-1 text-xs font-mono hover:bg-slate-50"
          >
            {ref}
          </button>
        ))}
      </div>

      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

      {law && (
        <div className="rounded-lg border border-slate-200 bg-white p-6">
          <p className="font-mono text-xs text-slate-400">{law.ref}</p>
          <h3 className="mt-1 text-lg font-semibold">{law.title}</h3>
          <p className="mt-1 font-medium text-blue-700">{law.article}</p>
          <p className="mt-4 text-sm leading-relaxed text-slate-700">{law.content}</p>
          <p className="mt-4 text-xs text-slate-400">
            Valid from: {law.valid_from}
            {law.valid_to && ` · Valid to: ${law.valid_to}`}
          </p>
        </div>
      )}
    </div>
  );
}
