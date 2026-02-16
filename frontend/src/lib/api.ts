const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function register(payload: { email: string; full_name: string; password: string }) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Registration failed");
  return res.json();
}

export async function login(payload: { email: string; password: string }) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
}

export async function googleLogin(credential: string) {
  const res = await fetch(`${API_BASE}/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ credential }),
  });
  if (!res.ok) throw new Error("Google login failed");
  return res.json();
}

export async function uploadResume(token: string, file: File, location: string) {
  const form = new FormData();
  form.append("file", file);
  form.append("location", location);
  const res = await fetch(`${API_BASE}/resume/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) throw new Error("Resume upload failed");
  return res.json();
}

export async function me(token: string) {
  const res = await fetch(`${API_BASE}/profile/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Fetch profile failed");
  return res.json();
}

export async function ingestJobs(token: string) {
  const res = await fetch(`${API_BASE}/jobs/ingest`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Ingest failed");
  return res.json();
}

export async function personalizedJobs(token: string) {
  const res = await fetch(`${API_BASE}/jobs/personalized`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Fetch jobs failed");
  return res.json();
}

export async function dashboardStages(token: string) {
  const res = await fetch(`${API_BASE}/dashboard/stages`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Dashboard fetch failed");
  return res.json();
}

export async function saveJob(token: string, jobId: number) {
  const res = await fetch(`${API_BASE}/applications/save/${jobId}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Save job failed");
  return res.json();
}

export async function myApplications(token: string) {
  const res = await fetch(`${API_BASE}/applications/mine`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Load applications failed");
  return res.json();
}

export async function updateApplicationStage(token: string, applicationId: number, stage: string) {
  const res = await fetch(`${API_BASE}/applications/stage/${applicationId}?stage=${encodeURIComponent(stage)}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Stage update failed");
  return res.json();
}

export async function getAlerts(token: string) {
  const res = await fetch(`${API_BASE}/alerts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Alerts fetch failed");
  return res.json();
}

export async function sourceHealth(token: string) {
  const res = await fetch(`${API_BASE}/admin/source-health`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Source health fetch failed");
  return res.json();
}

export async function runLeadSourcing(token: string) {
  const res = await fetch(`${API_BASE}/lead-sourcing/run-now`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Lead sourcing run failed");
  return res.json();
}

export async function latestLeadSourcing(token: string) {
  const res = await fetch(`${API_BASE}/lead-sourcing/latest`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Lead sourcing latest failed");
  return res.json();
}
