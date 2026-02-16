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
