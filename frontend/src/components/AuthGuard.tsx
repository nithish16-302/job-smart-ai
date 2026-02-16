"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";

const PUBLIC_ROUTES = ["/login"];

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const token = getToken();
    const isPublic = PUBLIC_ROUTES.includes(pathname);

    if (!token && !isPublic) {
      router.replace("/login");
      return;
    }
    if (token && pathname === "/login") {
      router.replace("/dashboard");
    }
  }, [pathname, router]);

  return <>{children}</>;
}
