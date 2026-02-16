import AuthGuard from "@/components/AuthGuard";
import NavBar from "@/components/NavBar";

export const metadata = {
  title: "Job Smart AI",
  description: "Personalized job discovery from resume + location",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "Inter, sans-serif", margin: 0, background: "#f8fafc" }}>
        <AuthGuard>
          <NavBar />
          <div style={{ maxWidth: 1100, margin: "20px auto", padding: 16 }}>{children}</div>
        </AuthGuard>
      </body>
    </html>
  );
}
