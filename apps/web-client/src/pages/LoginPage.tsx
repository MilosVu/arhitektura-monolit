import { type FormEvent, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { user, login } = useAuth();
  const [username, setUsername] = useState("hmueller");
  const [password, setPassword] = useState("mock");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) {
    return <Navigate to="/cases" replace />;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(username, password);
    } catch {
      setError("Login failed. Try username: hmueller");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-8 shadow-sm"
      >
        <h1 className="mb-1 text-2xl font-bold">Cortex AI</h1>
        <p className="mb-6 text-sm text-slate-500">Mock login — Active Directory stub</p>

        {error && (
          <div className="mb-4 rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>
        )}

        <label className="mb-4 block">
          <span className="mb-1 block text-sm font-medium">AD Username</span>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
            placeholder="hmueller"
          />
        </label>

        <label className="mb-6 block">
          <span className="mb-1 block text-sm font-medium">Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </label>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Signing in..." : "Sign in"}
        </button>

        <p className="mt-4 text-center text-xs text-slate-400">
          Demo users: hmueller (judge), aweber (clerk)
        </p>
      </form>
    </div>
  );
}
