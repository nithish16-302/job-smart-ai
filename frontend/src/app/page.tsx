export default function HomePage() {
  return (
    <main style={{ maxWidth: 900, margin: '40px auto', padding: 24 }}>
      <h1>Job Smart AI</h1>
      <p>Resume-aware job matching MVP is now scaffolded.</p>

      <section style={{ background: 'white', borderRadius: 12, padding: 16, marginTop: 16 }}>
        <h2>MVP Flow</h2>
        <ol>
          <li>User login</li>
          <li>Upload resume + choose location</li>
          <li>Get personalized jobs from multiple sources</li>
        </ol>
      </section>
    </main>
  );
}
