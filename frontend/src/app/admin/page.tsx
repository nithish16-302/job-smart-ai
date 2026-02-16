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
    <div style={{ display: "grid", gap: 16 }}>
      <h2>Admin: Source Health</h2>
      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Job Count by Source</h3>
        <pre>{JSON.stringify(data?.source_counts || {}, null, 2)}</pre>
      </section>
      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Recent Ingest Runs</h3>
        <pre>{JSON.stringify(data?.recent_ingest_runs || [], null, 2)}</pre>
      </section>
    </div>
  );
}
