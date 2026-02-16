"use client";

import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";
import { myApplications, updateApplicationStage } from "@/lib/api";

const stages = ["saved", "applied", "interview", "offer", "rejected"];

export default function ApplicationsPage() {
  const token = typeof window !== "undefined" ? getToken() : "";
  const [applications, setApplications] = useState<any[]>([]);

  const refresh = async () => {
    if (!token) return;
    const res = await myApplications(token);
    setApplications(res.applications || []);
  };

  useEffect(() => {
    refresh();
  }, []);

  const onStage = async (id: number, stage: string) => {
    if (!token) return;
    await updateApplicationStage(token, id, stage);
    await refresh();
  };

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <h2>Application Tracker</h2>
      {applications.map((a) => (
        <article key={a.application_id} style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
          <h3>{a.job.title}</h3>
          <p>{a.job.company} • {a.job.location}</p>
          <p>Current stage: <strong>{a.stage}</strong></p>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {stages.map((s) => (
              <button key={s} onClick={() => onStage(a.application_id, s)} disabled={s === a.stage}>
                {s}
              </button>
            ))}
          </div>
        </article>
      ))}
    </div>
  );
}
