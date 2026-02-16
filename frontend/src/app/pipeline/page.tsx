"use client";

import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";
import { latestLeadSourcing, runLeadSourcing } from "@/lib/api";

export default function PipelinePage() {
  const token = typeof window !== "undefined" ? getToken() : "";
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const loadLatest = async () => {
    if (!token) return;
    const res = await latestLeadSourcing(token);
    setData(res);
  };

  useEffect(() => {
    loadLatest();
  }, []);

  const runNow = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await runLeadSourcing(token);
      setData(res);
      setMsg("Lead sourcing run completed.");
    } catch (e: any) {
      setMsg(e.message || "Run failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid">
      <h2>Pipeline: Lead Sourcing</h2>
      <section className="card grid">
        <p>Stage 1 automation for Team-Soft LLC. Tech-wise lead discovery focused on Tier 2/3 and hard-to-fill markets.</p>
        <div className="row">
          <button onClick={runNow} disabled={loading}>{loading ? "Running..." : "Run Lead Sourcing Now"}</button>
          <button onClick={loadLatest}>Refresh Latest</button>
        </div>
        {!!msg && <p>{msg}</p>}
      </section>

      <section className="card">
        <h3>Summary</h3>
        <p><strong>Total Leads:</strong> {data?.total_leads ?? 0}</p>
        <p><strong>Leads with contact/domain enrichment:</strong> {data?.leads_with_contact ?? 0}</p>
        <pre>{JSON.stringify(data?.by_technology || {}, null, 2)}</pre>
      </section>

      <section className="card">
        <h3>Top Leads (sample)</h3>
        <div className="grid">
          {(data?.leads || []).slice(0, 15).map((l: any, i: number) => (
            <article key={i} className="card">
              <h3>{l.title}</h3>
              <p>{l.company} • {l.location}</p>
              <p>Tech: {(l.technologies || []).join(", ")} • score {l.lead_score}</p>
              <p><strong>Domain:</strong> {l?.contact?.company_domain || "Not found"}</p>
              <p><strong>Target titles:</strong> {(l?.contact?.target_contact_titles || []).slice(0,3).join(", ")}</p>
              <p><strong>Suggested emails:</strong> {(l?.contact?.suggested_emails || []).slice(0,3).join(", ") || "N/A"}</p>
              <a href={l.url} target="_blank">Open posting</a>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
