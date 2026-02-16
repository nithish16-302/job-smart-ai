"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, register } from "@/lib/api";
import { setToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleRegister = async () => {
    try {
      const res = await register({ full_name: fullName, email, password });
      setToken(res.access_token);
      router.replace("/dashboard");
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  const handleLogin = async () => {
    try {
      const res = await login({ email, password });
      setToken(res.access_token);
      router.replace("/dashboard");
    } catch (e: any) {
      setMsg(e.message);
    }
  };

  return (
    <main style={{ maxWidth: 480, margin: "60px auto", background: "#fff", borderRadius: 12, padding: 20 }}>
      <h2>Welcome to Job Smart AI</h2>
      <p>Login to continue</p>
      <div style={{ display: "grid", gap: 8 }}>
        <input placeholder="Full Name (for register)" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleRegister}>Register</button>
        </div>
      </div>
      {!!msg && <p style={{ color: "crimson" }}>{msg}</p>}
    </main>
  );
}
