import AuthGuard from "@/components/AuthGuard";
import NavBar from "@/components/NavBar";
import Providers from "@/components/Providers";
import "./globals.css";

export const metadata = {
  title: "Job Smart AI",
  description: "Personalized job discovery from resume + location",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AuthGuard>
            <NavBar />
            <div className="container">{children}</div>
          </AuthGuard>
        </Providers>
      </body>
    </html>
  );
}
