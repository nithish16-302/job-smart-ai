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
    setMsg(`Synced sources. fetched=${res.fetched}, inserted=${res.inserted}`);
  };

  const onLoad = async () => {
    if (!token) return;
    const res = await personalizedJobs(token);
    setJobs(res.jobs || []);
  };

  const onSave = async (jobId: number) => {
    if (!token) return;
    await saveJob(token, jobId);
    setMsg("Saved to tracker.");
  };

  return (
    <div className="grid">
      <h2>Personalized Jobs</h2>
      <div className="row">
        <button onClick={onIngest}>Sync Sources</button>
        <button onClick={onLoad}>Load Best Matches</button>
      </div>
      {!!msg && <p>{msg}</p>}
      <div className="grid">
        {jobs.map((j) => (
          <article key={j.id} className="card">
            <h3>{j.title}</h3>
            <p>{j.company} • {j.location} • score {j.score}</p>
            <p>{(j.description || "").replace(/<[^>]+>/g, "").slice(0, 200)}...</p>
            <div className="row">
              <a href={j.apply_url} target="_blank">Apply</a>
              <button onClick={() => onSave(j.id)}>Save</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
