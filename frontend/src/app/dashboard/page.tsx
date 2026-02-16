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
    <div className="grid">
      <h2>Dashboard</h2>
      <div className="row">
        <section className="card" style={{ minWidth: 180 }}><p>Sourced</p><div className="kpi">{stages?.sourced ?? 0}</div></section>
        <section className="card" style={{ minWidth: 180 }}><p>Applied</p><div className="kpi">{stages?.applied ?? 0}</div></section>
        <section className="card" style={{ minWidth: 180 }}><p>Interviews</p><div className="kpi">{stages?.stages?.interview ?? 0}</div></section>
      </div>

      <section className="card grid">
        <h3>Profile</h3>
        <p><strong>{profile?.full_name || "-"}</strong> • {profile?.email || "-"}</p>
        <p>Preferred location: {profile?.preferred_location || "-"}</p>
      </section>

      <section className="card grid">
        <h3>Onboarding</h3>
        <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Preferred Location" />
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <div className="row"><button onClick={onUpload}>Save Resume</button></div>
        {!!msg && <p>{msg}</p>}
      </section>

      <section className="card">
        <h3>Alerts</h3>
        <ul>{alerts.map((a, i) => <li key={i}>{a.message}</li>)}</ul>
      </section>
    </div>
  );
}
