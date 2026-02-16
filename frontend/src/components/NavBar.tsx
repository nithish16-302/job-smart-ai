"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken } from "@/lib/auth";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/jobs", label: "Jobs" },
  { href: "/applications", label: "Applications" },
  { href: "/admin", label: "Admin" },
];

export default function NavBar() {
  const pathname = usePathname();
  const router = useRouter();
  const token = typeof window !== "undefined" ? getToken() : "";

  if (!token || pathname === "/login") return null;

  return (
    <nav style={{ display: "flex", gap: 12, alignItems: "center", padding: 16, background: "#0f172a", color: "#fff" }}>
      <strong>Job Smart AI</strong>
      {links.map((l) => (
        <Link key={l.href} href={l.href} style={{ color: pathname === l.href ? "#93c5fd" : "#fff", textDecoration: "none" }}>
          {l.label}
        </Link>
      ))}
      <button
        style={{ marginLeft: "auto" }}
        onClick={() => {
          clearToken();
          router.replace("/login");
        }}
      >
        Logout
      </button>
    </nav>
  );
}
