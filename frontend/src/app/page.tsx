"use client";

import { useState } from "react";
import { login, register, uploadResume, me } from "@/lib/api";

export default function HomePage() {
  const [token, setToken] = useState<string>("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [location, setLocation] = useState("Remote");
  const [file, setFile] = useState<File | null>(null);
  const [output, setOutput] = useState<string>("");

  const onRegister = async () => {
    try {
      const data = await register({ email, full_name: fullName, password });
      setToken(data.access_token);
      setOutput("Registered successfully. Token saved in memory.");
    } catch (e: any) {
      setOutput(e.message);
    }
  };

  const onLogin = async () => {
    try {
      const data = await login({ email, password });
      setToken(data.access_token);
      setOutput("Logged in successfully.");
    } catch (e: any) {
      setOutput(e.message);
    }
  };

  const onUpload = async () => {
    if (!token || !file) return setOutput("Login and choose a resume first.");
    try {
      const data = await uploadResume(token, file, location);
      setOutput(JSON.stringify(data, null, 2));
    } catch (e: any) {
      setOutput(e.message);
    }
  };

  const onProfile = async () => {
    if (!token) return setOutput("Login first.");
    try {
      const data = await me(token);
      setOutput(JSON.stringify(data, null, 2));
    } catch (e: any) {
      setOutput(e.message);
    }
  };

  return (
    <main style={{ maxWidth: 980, margin: "24px auto", padding: 20 }}>
      <h1>Job Smart AI — Milestone 2</h1>
      <p>Auth + resume parsing + location preferences are now wired.</p>

      <section style={{ display: "grid", gap: 12, background: "#fff", padding: 16, borderRadius: 12 }}>
        <h3>1) Register / Login</h3>
        <input placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={onRegister}>Register</button>
          <button onClick={onLogin}>Login</button>
          <button onClick={onProfile}>My Profile</button>
        </div>
      </section>

      <section style={{ display: "grid", gap: 12, background: "#fff", padding: 16, borderRadius: 12, marginTop: 16 }}>
        <h3>2) Upload resume + location</h3>
        <input placeholder="Preferred location" value={location} onChange={(e) => setLocation(e.target.value)} />
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={onUpload}>Upload Resume</button>
      </section>

      <section style={{ background: "#0f172a", color: "#e2e8f0", padding: 16, borderRadius: 12, marginTop: 16 }}>
        <h3>Response</h3>
        <pre style={{ whiteSpace: "pre-wrap" }}>{output || "No actions yet."}</pre>
      </section>
    </main>
  );
}
