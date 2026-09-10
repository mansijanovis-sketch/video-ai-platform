import { useState } from 'react'
import { Link } from 'react-router-dom'
import EarlyAccessModal from '../components/EarlyAccessModal'

const capabilities = [
  {
    number: '01',
    title: 'General Analysis',
    description: 'Get a structured overview of what happens throughout a video.',
  },
  {
    number: '02',
    title: 'Summary',
    description: 'Quickly understand the main ideas without watching the entire video.',
  },
  {
    number: '03',
    title: 'Transcript',
    description: 'Search and review what was said with timestamps.',
  },
  {
    number: '04',
    title: 'Key Moments',
    description: 'Find important moments and jump directly to them.',
  },
  {
    number: '05',
    title: 'Visual Insights',
    description: 'Understand important information shown on screen through visual analysis and OCR.',
  },
  {
    number: '06',
    title: 'Developer Guide',
    description: 'Turn technical tutorials and coding demonstrations into structured implementation steps.',
  },
  {
    number: '07',
    title: 'Custom Analysis',
    description: 'Ask VideoMind to focus on the information that matters to you.',
  },
]

const sourceCards = [
  {
    title: 'Local Video',
    description: 'Upload a video directly from your device.',
  },
  {
    title: 'YouTube',
    description: 'Analyze supported public YouTube videos.',
  },
  {
    title: 'Video URL',
    description: 'Provide a supported public video URL.',
  },
]

const steps = [
  {
    number: '01',
    title: 'Add a video',
    description: 'Upload a local video or provide a supported video URL.',
  },
  {
    number: '02',
    title: 'Extract evidence',
    description: 'VideoMind processes speech, frames, visual information and other available evidence.',
  },
  {
    number: '03',
    title: 'Understand the content',
    description: 'The system combines evidence across the video to identify meaningful information.',
  },
  {
    number: '04',
    title: 'Get useful results',
    description: 'Explore summaries, transcripts, key moments, visual insights and specialized analysis.',
  },
]

const principles = [
  {
    title: 'Understand the whole video',
    description: 'Look beyond isolated transcripts.',
  },
  {
    title: 'Connect evidence',
    description: 'Relate speech, visuals and timestamps.',
  },
  {
    title: 'Make information useful',
    description: 'Turn raw video into something you can act on.',
  },
]

function LandingPage() {
  const [isModalOpen, setIsModalOpen] = useState(false)

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-header-inner">
          <Link to="/" className="landing-brand" aria-label="VideoMind home">
            <span className="landing-brand-mark">V</span>
            <span className="landing-brand-text">VideoMind</span>
          </Link>

          <nav className="landing-nav" aria-label="Landing page navigation">
            <a href="#how-it-works">How it works</a>
            <a href="#capabilities">Capabilities</a>
            <a href="#why-videomind">Why VideoMind</a>
          </nav>

          <Link to="/app" className="landing-nav-button">
            Open VideoMind
          </Link>
        </div>
      </header>

      <main>
        <section className="landing-hero">
          <div className="landing-hero-content">
            <div className="landing-eyebrow">
              <span className="eyebrow-dot" aria-hidden="true"></span>
              Video understanding platform
            </div>

            <h1>Understand any video. Get what matters.</h1>

            <p className="landing-subtitle">
              VideoMind turns videos into structured, useful information — from summaries and transcripts to key
              moments, visual insights, and step-by-step understanding.
            </p>

            <div className="landing-cta-row">
              <Link to="/app" className="primary-cta">
                Explore VideoMind
              </Link>
              <button type="button" className="secondary-cta" onClick={() => setIsModalOpen(true)}>
                Join Early Access
              </button>
            </div>

            <div className="landing-chip-row" aria-label="Supported source types">
              <span>Local video</span>
              <span>YouTube</span>
              <span>Public video URLs</span>
              <span>More sources</span>
            </div>
          </div>

          <div className="landing-visual-panel" aria-label="VideoMind pipeline diagram">
            <div className="pipeline-card">
              <div className="pipeline-header">
                <div className="pipeline-dots" aria-hidden="true">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="pipeline-title">VideoMind pipeline</span>
              </div>

              <div className="pipeline-body">
                <div className="pipeline-node">Video</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node accent">Speech + Frames + Visual Evidence</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node">Video Understanding</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node strong">Useful Results</div>
              </div>
            </div>
          </div>
        </section>

        <section className="landing-trust-strip">
          <div className="landing-section-shell">
            <p className="landing-trust-label">Built to understand videos, not just generate transcripts.</p>
            <p className="landing-trust-copy">
              VideoMind combines multiple sources of evidence from a video to build a structured understanding of what
              was said, shown and demonstrated.
            </p>
          </div>
        </section>

        <section className="landing-section" id="capabilities">
          <div className="landing-section-header">
            <p className="landing-section-kicker">Capabilities</p>
            <h2>What VideoMind can help you understand</h2>
          </div>

          <div className="landing-capability-grid">
            {capabilities.map(({ number, title, description }) => (
              <article key={title} className="landing-capability-card">
                <span className="landing-capability-number">{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section alt-section" id="how-it-works">
          <div className="landing-section-header">
            <p className="landing-section-kicker">How it works</p>
            <h2>From video to understanding</h2>
          </div>

          <div className="landing-timeline" aria-label="VideoMind workflow steps">
            {steps.map(({ number, title, description }) => (
              <div key={title} className="landing-timeline-item">
                <div className="timeline-marker" aria-hidden="true">
                  <span>{number}</span>
                </div>
                <div className="timeline-content">
                  <h3>{title}</h3>
                  <p>{description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="landing-section">
          <div className="landing-section-header">
            <p className="landing-section-kicker">Multiple video sources</p>
            <h2>Start with the video you already have</h2>
          </div>

          <div className="landing-source-grid">
            {sourceCards.map(({ title, description }) => (
              <article key={title} className="landing-source-card">
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
            <article className="landing-source-card muted-card">
              <h3>More sources coming</h3>
              <p>Support for additional public video sources is being developed.</p>
            </article>
          </div>
        </section>

        <section className="landing-section developer-section">
          <div className="developer-copy-block">
            <p className="landing-section-kicker">Developer use case</p>
            <h2>For tutorials, demos and technical videos</h2>
            <p>
              Long technical videos often contain the exact command, file change or implementation detail you need —
              buried inside an hour of content.
            </p>
          </div>

          <div className="landing-transform-card">
            <div className="transform-flow">
              <span>Long tutorial</span>
              <span className="flow-arrow" aria-hidden="true">↓</span>
              <span>VideoMind</span>
              <span className="flow-arrow" aria-hidden="true">↓</span>
              <span>Project setup</span>
              <span>Commands</span>
              <span>Files</span>
              <span>Code changes</span>
              <span>Important timestamps</span>
              <span>Implementation steps</span>
            </div>

            <Link to="/app" className="landing-secondary-action">
              Explore Developer Guide
            </Link>
          </div>
        </section>

        <section className="landing-section" id="why-videomind">
          <div className="landing-section-header">
            <p className="landing-section-kicker">Why VideoMind</p>
            <h2>Why we&apos;re building VideoMind</h2>
          </div>

          <div className="landing-why-copy">
            <p>
              Videos contain more than spoken words. Important information can appear in code editors, presentations,
              diagrams, interfaces, demonstrations and visual changes.
            </p>
            <p>
              VideoMind is being built to combine these different signals into a more useful understanding of the
              video.
            </p>
          </div>

          <div className="landing-principle-grid">
            {principles.map(({ title, description }) => (
              <article key={title} className="landing-principle-card">
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section alt-section">
          <div className="landing-section-header">
            <p className="landing-section-kicker">Built from the ground up</p>
            <h2>Built from the ground up</h2>
          </div>

          <p className="landing-technology-copy">
            We&apos;re building VideoMind&apos;s core video-understanding pipeline ourselves using open-source technologies
            and our own processing and machine-learning systems.
          </p>

          <div className="landing-tech-pipeline" aria-label="Core technology pipeline">
            <div className="tech-step">Video</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">FFmpeg / Video Processing</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">Speech / Transcript</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">Frame Analysis</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">OCR / Visual Evidence</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">Temporal Understanding</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">Structured Video Representation</div>
            <div className="tech-arrow" aria-hidden="true">↓</div>
            <div className="tech-step">VideoMind Results</div>
          </div>
        </section>

        <section className="landing-cta-section">
          <div className="landing-cta-panel">
            <p className="landing-section-kicker light">Early access</p>
            <h2>Be among the first to explore VideoMind.</h2>
            <p>
              VideoMind is currently being built. Join the early-access list to follow the launch and get access when
              we&apos;re ready.
            </p>
            <button type="button" className="primary-cta" onClick={() => setIsModalOpen(true)}>
              Join Early Access
            </button>
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
            <a href="#how-it-works">How it works</a>
            <a href="#capabilities">Capabilities</a>
            <Link to="/app">Open VideoMind</Link>
            <button type="button" onClick={() => setIsModalOpen(true)}>
              Early Access
            </button>
          </div>
        </div>

        <div className="landing-footer-bottom">
          <p>© 2026 VideoMind</p>
          <p>Built with curiosity and a lot of video processing.</p>
        </div>
      </footer>

      <EarlyAccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  )
}

export default LandingPage
