"use client";

import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";
import { sourceHealth } from "@/lib/api";

export default function AdminPage() {
  const token = typeof window !== "undefined" ? getToken() : "";
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    (async () => {
      if (!token) return;
      const res = await sourceHealth(token);
      setData(res);
    })();
  }, []);

  return (
    <div className="grid">
      <h2>Admin: Source Health</h2>
      <section className="card">
        <h3>Jobs by Source</h3>
        <pre>{JSON.stringify(data?.source_counts || {}, null, 2)}</pre>
      </section>
      <section className="card">
        <h3>Recent Ingest Runs</h3>
        <pre>{JSON.stringify(data?.recent_ingest_runs || [], null, 2)}</pre>
      </section>
    </div>
  );
}
