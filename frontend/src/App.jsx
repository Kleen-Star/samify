import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { getHealth } from "./services/api";

function StatusPage() {
  const [state, setState] = useState({ status: "loading", data: null });

  useEffect(() => {
    getHealth()
      .then((res) => setState({ status: "ok", data: res.data }))
      .catch(() => setState({ status: "error", data: null }));
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <section className="w-full max-w-md rounded-2xl bg-card p-6 shadow">
        <h1 className="font-display text-2xl text-primary">Samify</h1>
        <p className="mt-1 text-sm opacity-70">Stage 1 — foundation check</p>
        <div className="mt-6" aria-live="polite">
          {state.status === "loading" && <p>Checking backend…</p>}
          {state.status === "error" && (
            <p role="alert" className="text-red-600">We couldn't reach the API. Please try again.</p>
          )}
          {state.status === "ok" && (
            <ul className="space-y-1">
              <li>API: <strong>{state.data.api}</strong></li>
              <li>Database: <strong>{state.data.database}</strong></li>
            </ul>
          )}
        </div>
      </section>
    </main>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<StatusPage />} />
    </Routes>
  );
}
