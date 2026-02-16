"use client";

import { useEffect, useState } from "react";
import { dashboardStages, me, uploadResume, getAlerts } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [stages, setStages] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [location, setLocation] = useState("Remote");
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState("");

  const token = typeof window !== "undefined" ? getToken() : "";

  const refresh = async () => {
    if (!token) return;
    const [p, s, a] = await Promise.all([me(token), dashboardStages(token), getAlerts(token)]);
    setProfile(p);
    setStages(s);
    setAlerts(a.alerts || []);
    if (p?.preferred_location) setLocation(p.preferred_location);
  };

  useEffect(() => {
    refresh();
  }, []);

  const onUpload = async () => {
    if (!token || !file) return setMsg("Choose resume file first.");
    await uploadResume(token, file, location);
    setMsg("Resume uploaded and location saved.");
    await refresh();
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h2>Dashboard</h2>

      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Profile</h3>
        <p><strong>Name:</strong> {profile?.full_name || "-"}</p>
        <p><strong>Email:</strong> {profile?.email || "-"}</p>
        <p><strong>Preferred Location:</strong> {profile?.preferred_location || "-"}</p>
      </section>

      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Onboarding: Resume + Location</h3>
        <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Preferred Location" />
        <div style={{ height: 8 }} />
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <div style={{ height: 8 }} />
        <button onClick={onUpload}>Save Resume</button>
        {!!msg && <p>{msg}</p>}
      </section>

      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Pipeline Snapshot</h3>
        <pre>{JSON.stringify(stages || {}, null, 2)}</pre>
      </section>

      <section style={{ background: "#fff", borderRadius: 12, padding: 16 }}>
        <h3>Alerts</h3>
        <ul>
          {alerts.map((a, i) => (
            <li key={i}>{a.message}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
