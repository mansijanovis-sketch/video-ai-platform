import { useState } from 'react'
import { Link } from 'react-router-dom'
import EarlyAccessModal from '../components/EarlyAccessModal'

const problems = [
  {
    title: 'Tutorials are scattered',
    description: 'Important steps are buried in long videos, repeated explanations, and noisy demos.',
  },
  {
    title: 'Commands get lost',
    description: 'The exact terminal commands, file edits, and setup steps are hard to find when you replay a video.',
  },
  {
    title: 'Context is fragmented',
    description: 'Speech, code, visual changes, and timestamps live in different places, making the flow hard to follow.',
  },
]

const solutions = [
  {
    title: 'Structured guidance',
    description: 'Organize a tutorial into a clear sequence of actions, files, commands, and explanations.',
  },
  {
    title: 'Evidence-backed understanding',
    description: 'Combine transcript, code, OCR, visual context, and timing to connect what happened to what matters.',
  },
  {
    title: 'Developer-ready output',
    description: 'Turn a long walkthrough into a practical implementation guide you can follow step by step.',
  },
]

const features = [
  {
    title: 'Step-by-step guides',
    description: 'Break long tutorials into actionable implementation steps with context and timestamps.',
  },
  {
    title: 'Command tracking',
    description: 'Capture terminal commands and setup actions from the tutorial timeline.',
  },
  {
    title: 'Code and file awareness',
    description: 'Surface the files, edits, and code changes that matter most while building the project.',
  },
  {
    title: 'Transcript + visual evidence',
    description: 'Connect spoken guidance with what is visible on-screen for a fuller understanding.',
  },
  {
    title: 'Actionable timestamps',
    description: 'Jump directly to the exact moment a command, file change, or explanation happens.',
  },
  {
    title: 'Built for developers',
    description: 'Designed around the way technical tutorials are actually learned and implemented.',
  },
]

const steps = [
  {
    number: '01',
    title: 'Add a tutorial video',
    description: 'Upload a local recording or provide a supported public video URL.',
  },
  {
    number: '02',
    title: 'Extract evidence',
    description: 'VideoMind analyzes the transcript, code, visuals, and timeline to find relevant signals.',
  },
  {
    number: '03',
    title: 'Find the important actions',
    description: 'The system groups commands, file edits, and implementation moments into a usable flow.',
  },
  {
    number: '04',
    title: 'Deliver a guide',
    description: 'Turn the raw content into a step-by-step implementation plan with explanations and timestamps.',
  },
]

const audiences = [
  {
    title: 'Developers learning new stacks',
    description: 'Convert a complex tutorial into a practical, paced implementation path you can actually follow.',
  },
  {
    title: 'Teams documenting workflows',
    description: 'Capture how a project was built and turn it into reusable technical documentation.',
  },
  {
    title: 'Builders working from video content',
    description: 'Move from watching to building without losing the exact commands, files, and timestamps.',
  },
]

const exampleGuide = [
  {
    step: '01',
    title: 'Create React App',
    command: 'npx create-react-app react-tutorial',
    timestamp: '00:14',
    details: 'Initialize the project and create the base app structure.',
  },
  {
    step: '02',
    title: 'Install React Router',
    command: 'npm install react-router-dom',
    timestamp: '01:10',
    details: 'Add routing support so the app can move between screens.',
  },
  {
    step: '03',
    title: 'Update App.js',
    file: 'App.js',
    action: 'Replace component',
    timestamp: '31:34',
    details: 'Set up the entry component and route configuration for the app shell.',
  },
]

const faqs = [
  {
    question: 'What is VideoMind?',
    answer:
      'VideoMind is a developer-focused platform that helps turn coding tutorials and technical videos into structured, step-by-step implementation guides built from transcript, code, file, and visual evidence.',
  },
  {
    question: 'Is this feature fully production-ready?',
    answer:
      'VideoMind is currently under active development. The project is being built as a working prototype and a foundation for deeper tutorial-to-guide automation, with some capabilities planned and evolving over time.',
  },
  {
    question: 'What kinds of content does it help with?',
    answer:
      'It is designed for tutorials, coding walkthroughs, technical demos, setup instructions, and code-heavy videos where developers need commands, file changes, and explanations captured in a clear order.',
  },
  {
    question: 'Does it handle timestamps and evidence?',
    answer:
      'Yes. The platform is designed to connect actions to the moments they happened, making it easier to reference exact moments in a tutorial and understand why a step mattered.',
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
            <a href="#problem">Problem</a>
            <a href="#solution">Solution</a>
            <a href="#how-it-works">How it works</a>
            <a href="#features">Features</a>
            <a href="#faq">FAQ</a>
          </nav>

          <button type="button" className="landing-nav-button" onClick={() => setIsModalOpen(true)}>
            Join Early Access
          </button>
        </div>
      </header>

      <main>
        <section className="landing-hero">
          <div className="landing-hero-content">
            <p className="landing-eyebrow">
              <span className="eyebrow-dot" aria-hidden="true"></span>
              AI-powered tutorial intelligence
            </p>

            <h1>Stop Watching. Start Building.</h1>

            <p className="landing-subtitle">
              Turn coding tutorials into step-by-step implementation guides with commands, code, files,
              explanations, and timestamps.
            </p>

            <div className="landing-cta-row">
              <button type="button" className="primary-cta" onClick={() => setIsModalOpen(true)}>
                Join Early Access
              </button>
              <a href="#how-it-works" className="secondary-cta">
                See How It Works
              </a>
            </div>

            <div className="landing-chip-row" aria-label="Tutorial sources">
              <span>Local video</span>
              <span>YouTube</span>
              <span>Public tutorial links</span>
              <span>Step-by-step output</span>
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
                <span className="pipeline-title">VideoMind workflow</span>
              </div>

              <div className="pipeline-body">
                <div className="pipeline-node">Tutorial video</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node accent">Transcript + code + visuals + timing</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node">Action extraction</div>
                <div className="pipeline-arrow" aria-hidden="true">↓</div>
                <div className="pipeline-node strong">Implementation guide</div>
              </div>
            </div>
          </div>
        </section>

        <section className="landing-section" id="problem">
          <div className="section-heading">
            <p className="section-kicker">Problem</p>
            <h2>Technical tutorials are hard to turn into real work.</h2>
          </div>

          <div className="info-grid info-grid-3">
            {problems.map(({ title, description }) => (
              <article key={title} className="info-card">
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section alt-section" id="solution">
          <div className="section-heading">
            <p className="section-kicker">Solution</p>
            <h2>VideoMind turns raw tutorial content into usable implementation flow.</h2>
          </div>

          <div className="info-grid info-grid-3">
            {solutions.map(({ title, description }) => (
              <article key={title} className="info-card accent-card">
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section" id="how-it-works">
          <div className="section-heading">
            <p className="section-kicker">How it works</p>
            <h2>From video to a buildable action plan.</h2>
          </div>

          <div className="steps-grid" aria-label="VideoMind process">
            {steps.map(({ number, title, description }) => (
              <article key={number} className="step-card">
                <div className="step-number">{number}</div>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section" id="features">
          <div className="section-heading">
            <p className="section-kicker">Features</p>
            <h2>Purpose-built for tutorial-driven development.</h2>
          </div>

          <div className="info-grid info-grid-3">
            {features.map(({ title, description }) => (
              <article key={title} className="feature-card">
                <span className="feature-badge" aria-hidden="true">•</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section example-section" id="example-guide">
          <div className="section-heading narrow-heading">
            <p className="section-kicker">Example guide</p>
            <h2>Example of the output VideoMind is designed to generate.</h2>
            <p className="section-copy">
              Instead of searching through a long tutorial, get the implementation steps, files, commands, and
              timestamps in one place. This illustrative example shows the type of output VideoMind is intended to
              produce.
            </p>
          </div>

          <div className="guide-panel" aria-label="Example implementation guide">
            <div className="guide-header">
              <div>
                <p className="guide-label">Example output</p>
                <h3>React tutorial walkthrough</h3>
              </div>
              <span className="guide-status">Illustrative</span>
            </div>

            <ol className="guide-steps">
              {exampleGuide.map(({ step, title, command, timestamp, details, file, action }) => (
                <li key={step} className="guide-step">
                  <div className="guide-step-index">{step}</div>
                  <div className="guide-step-body">
                    <div className="guide-step-topline">
                      <h4>{title}</h4>
                      <span>{timestamp}</span>
                    </div>

                    <div className="implementation-card">
                      <div className="implementation-line">
                        <span className="implementation-label">Command</span>
                        <code>{command}</code>
                      </div>

                      {file ? (
                        <div className="implementation-line">
                          <span className="implementation-label">File</span>
                          <span>{file}</span>
                        </div>
                      ) : null}

                      {action ? (
                        <div className="implementation-line">
                          <span className="implementation-label">Action</span>
                          <span>{action}</span>
                        </div>
                      ) : null}
                    </div>

                    <p>{details}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="landing-section" id="audience">
          <div className="section-heading">
            <p className="section-kicker">Target audience</p>
            <h2>Built for the people who learn by doing.</h2>
          </div>

          <div className="info-grid info-grid-3">
            {audiences.map(({ title, description }) => (
              <article key={title} className="audience-card">
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section alt-section" id="why-videomind">
          <div className="section-heading">
            <p className="section-kicker">Why VideoMind</p>
            <h2>More than a transcript. A buildable understanding.</h2>
          </div>

          <div className="why-grid">
            <article className="why-card">
              <h3>Developer-first</h3>
              <p>VideoMind is designed around real engineering workflows, not passive viewing.</p>
            </article>
            <article className="why-card">
              <h3>Evidence-aware</h3>
              <p>It connects the signal across spoken explanation, visible code, and the timeline.</p>
            </article>
            <article className="why-card">
              <h3>Action-oriented</h3>
              <p>The goal is to help you move from learning to implementation with less friction.</p>
            </article>
          </div>
        </section>

        <section className="landing-section faq-section" id="faq">
          <div className="section-heading narrow-heading">
            <p className="section-kicker">FAQ</p>
            <h2>Questions developers usually ask.</h2>
          </div>

          <div className="faq-list">
            {faqs.map(({ question, answer }) => (
              <details key={question} className="faq-item" open={question === 'What is VideoMind?'}>
                <summary>{question}</summary>
                <p>{answer}</p>
              </details>
            ))}
          </div>
        </section>

        <section className="landing-cta-section">
          <div className="landing-cta-panel">
            <p className="section-kicker light">Under active development</p>
            <h2>Stop watching. Start building.</h2>
            <p>
              VideoMind is a platform in progress. Join the early-access list to follow the roadmap and get access to
              the next stages as the product matures.
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
            <p className="landing-footer-tagline">Stop Watching. Start Building.</p>
          </div>

          <div className="landing-footer-links" aria-label="Footer links">
            <a href="#problem">Problem</a>
            <a href="#solution">Solution</a>
            <a href="#features">Features</a>
            <a href="#how-it-works">How it works</a>
            <button type="button" onClick={() => setIsModalOpen(true)}>
              Join Early Access
            </button>
          </div>
        </div>

        <div className="landing-footer-bottom">
          <p>© 2026 VideoMind</p>
          <p>Built for developers learning from technical video.</p>
        </div>
      </footer>

      <EarlyAccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  )
}

export default LandingPage
