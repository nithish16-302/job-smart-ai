export const metadata = {
  title: 'Job Smart AI',
  description: 'Personalized job discovery from resume + location'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Inter, sans-serif', margin: 0, background: '#f8fafc' }}>
        {children}
      </body>
    </html>
  );
}
