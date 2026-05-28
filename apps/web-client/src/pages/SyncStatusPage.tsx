import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import type { SyncJob } from "../api/types";

export default function SyncStatusPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<SyncJob | null>(null);

  useEffect(() => {
    if (!jobId) return;

    const poll = () => {
      api.syncJob(jobId).then(setJob);
    };

    poll();
    const interval = setInterval(poll, 2000);
    return () => clearInterval(interval);
  }, [jobId]);

  if (!job) return <p className="text-slate-500">Loading sync job...</p>;

  const isDone = job.status === "completed" || job.status === "failed";

  return (
    <div className="mx-auto max-w-lg">
      <h2 className="mb-4 text-xl font-semibold">Alfresco Sync</h2>

      <div className="rounded-lg border border-slate-200 bg-white p-6">
        <div className="mb-2 flex justify-between text-sm">
          <span className="font-medium capitalize">{job.status}</span>
          <span className="text-slate-500">{job.progress}%</span>
        </div>

        <div className="mb-4 h-3 overflow-hidden rounded-full bg-slate-200">
          <div
            className={`h-full transition-all duration-500 ${
              job.status === "failed" ? "bg-red-500" : "bg-blue-600"
            }`}
            style={{ width: `${job.progress}%` }}
          />
        </div>

        <p className="mb-1 text-sm text-slate-600">{job.message}</p>
        <p className="text-xs text-slate-400">
          Documents: {job.total_documents} · Job ID: {job.id}
        </p>

        {isDone && (
          <Link
            to={`/cases/${job.case_id}`}
            className="mt-4 inline-block rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Back to Case
          </Link>
        )}
      </div>
    </div>
  );
}
