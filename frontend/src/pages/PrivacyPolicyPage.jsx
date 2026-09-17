import { Link } from 'react-router-dom'

function PrivacyPolicyPage() {
  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-header-inner">
          <Link to="/" className="landing-brand" aria-label="VideoMind home">
            <span className="landing-brand-mark">V</span>
            <span className="landing-brand-text">VideoMind</span>
          </Link>

          <nav className="landing-nav" aria-label="Privacy navigation">
            <Link to="/">Home</Link>
            <Link to="/#features">Features</Link>
          </nav>
        </div>
      </header>

      <main>
        <section className="landing-section" style={{ paddingTop: '72px', paddingBottom: '72px' }}>
          <div className="section-heading narrow-heading" style={{ textAlign: 'left', maxWidth: '760px' }}>
            <p className="section-kicker">Privacy Policy</p>
            <h2>Privacy policy</h2>
            <p className="section-copy" style={{ marginTop: '18px' }}>
              Effective date: <strong>To be confirmed</strong>
            </p>
          </div>

          <div className="guide-panel" style={{ maxWidth: '820px', marginTop: '36px' }}>
            <div className="guide-header">
              <div>
                <p className="guide-label">Overview</p>
                <h3>How we handle early-access signup information</h3>
              </div>
            </div>

            <div className="guide-step-body" style={{ padding: '22px 22px 10px' }}>
              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Information collected</span>
                  <span>Name and email address provided through the early-access form.</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Purpose</span>
                  <span>To manage early-access signups, communicate launch updates, and contact you about access or product news.</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Storage</span>
                  <span>Data is stored in a backend system only when the public API endpoint is connected. This frontend does not use browser localStorage as the final production storage mechanism.</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Retention</span>
                  <span>Data is retained only as long as necessary to support early-access communication, launch updates, or as required by applicable retention practices.</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Deletion</span>
                  <span>If you want your information removed or updated, contact the team at <strong>hello@videomind.in</strong> or the designated support address once confirmed by the product owner.</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Contact</span>
                  <span>For privacy questions, use the placeholder contact email: <strong>privacy@videomind.in</strong> (replace with the official address before launch).</span>
                </div>
              </div>

              <div className="implementation-card" style={{ marginBottom: '14px' }}>
                <div className="implementation-line">
                  <span className="implementation-label">Notes</span>
                  <span>This page is a launch placeholder. Final legal review should confirm the final company name, contact address, retention policy, and jurisdiction-specific requirements before public launch.</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="landing-footer-inner">
          <div>
            <p className="landing-footer-brand">VideoMind</p>
            <p className="landing-footer-tagline">Understand any video. Get what matters.</p>
          </div>

          <div className="landing-footer-links" aria-label="Footer links">
            <Link to="/">Home</Link>
            <Link to="/#features">Features</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default PrivacyPolicyPage
