"use client";

import { useState } from "react";
import { getToken } from "@/lib/auth";
import { ingestJobs, personalizedJobs, saveJob } from "@/lib/api";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [msg, setMsg] = useState("");
  const token = typeof window !== "undefined" ? getToken() : "";

  const onIngest = async () => {
    if (!token) return;
    const res = await ingestJobs(token);
    setMsg(`Ingested. Fetched ${res.fetched}, inserted ${res.inserted}`);
  };

  const onLoad = async () => {
    if (!token) return;
    const res = await personalizedJobs(token);
    setJobs(res.jobs || []);
  };

  const onSave = async (jobId: number) => {
    if (!token) return;
    await saveJob(token, jobId);
    setMsg("Job saved to applications.");
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h2>Personalized Jobs</h2>
      <div style={{ display: "flex", gap: 8 }}>
        <button onClick={onIngest}>Sync Job Sources</button>
        <button onClick={onLoad}>Get Best Matches</button>
      </div>
      {!!msg && <p>{msg}</p>}
      <div style={{ display: "grid", gap: 12 }}>
        {jobs.map((j) => (
          <article key={j.id} style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
            <h3>{j.title}</h3>
            <p>{j.company} • {j.location}</p>
            <p><strong>Score:</strong> {j.score}</p>
            <p style={{ marginTop: 8 }}>{(j.description || "").slice(0, 180)}...</p>
            <div style={{ display: "flex", gap: 8 }}>
              <a href={j.apply_url} target="_blank">Apply</a>
              <button onClick={() => onSave(j.id)}>Save</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
