"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken } from "@/lib/auth";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/pipeline", label: "Pipeline" },
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
    <nav className="nav">
      <div className="nav-inner">
        <strong>Job Smart AI</strong>
        {links.map((l) => (
          <Link key={l.href} href={l.href} className={`nav-link ${pathname === l.href ? "active" : ""}`}>
            {l.label}
          </Link>
        ))}
        <span className="spacer" />
        <button
          onClick={() => {
            clearToken();
            router.replace("/login");
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
