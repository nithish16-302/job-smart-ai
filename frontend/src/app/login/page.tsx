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
    <main className="grid" style={{ maxWidth: 500, margin: "60px auto" }}>
      <section className="card grid">
        <h2>Welcome back 👋</h2>
        <p>Login or create account to continue.</p>
        <input placeholder="Full Name (for register)" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <div className="row">
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleRegister}>Register</button>
        </div>
        {!!msg && <p style={{ color: "crimson" }}>{msg}</p>}
      </section>
    </main>
  );
}
