import { useEffect, useState } from "react";
import { Navigate, useSearchParams } from "react-router-dom";
import { api, setToken } from "../api/client";

export default function AuthCallbackPage() {
  const [searchParams] = useSearchParams();
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    const code = searchParams.get("code");
    if (!code) {
      setError("Missing authorization code");
      return;
    }

    api
      .ssoCallback(code, searchParams.get("state") ?? undefined)
      .then((result) => {
        setToken(result.access_token);
        setDone(true);
      })
      .catch(() => setError("SSO login failed"));
  }, [searchParams]);

  if (done) {
    return <Navigate to="/cases" replace />;
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <p className="text-slate-600">Completing sign-in...</p>
    </div>
  );
}
