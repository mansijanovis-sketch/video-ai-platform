import { useRef, useState } from 'react'
import './AppPage.css'

function AppPage() {
  const fileInputRef = useRef(null)

  const [sourceType, setSourceType] = useState('upload')
  const [videoFile, setVideoFile] = useState(null)
  const [videoUrl, setVideoUrl] = useState('')
  const [analysisType, setAnalysisType] = useState('general')
  const [error, setError] = useState('')

  const handleFileChange = (event) => {
    const file = event.target.files?.[0]

    if (!file) {
      return
    }

    setError('')
    setVideoFile(file)
  }

  const handleDrop = (event) => {
    event.preventDefault()

    const file = event.dataTransfer.files?.[0]

    if (!file) {
      return
    }

    if (!file.type.startsWith('video/')) {
      setError('Please select a valid video file.')
      return
    }

    setError('')
    setVideoFile(file)
  }

  const handleBrowse = () => {
    fileInputRef.current?.click()
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    setError('')

    if (sourceType === 'upload' && !videoFile) {
      setError('Please upload a video file.')
      return
    }

    if (sourceType === 'url' && !videoUrl.trim()) {
      setError('Please enter a video URL.')
      return
    }

    console.log({
      sourceType,
      videoFile,
      videoUrl,
      analysisType,
    })
  }

  const analysisOptions = [
    {
      id: 'general',
      title: 'General Analysis',
      description: 'Understand the video and its important content.',
    },
    {
      id: 'summary',
      title: 'Summary',
      description: 'Get a concise summary of the video.',
    },
    {
      id: 'transcript',
      title: 'Transcript',
      description: 'Extract and organize spoken content.',
    },
    {
      id: 'moments',
      title: 'Key Moments',
      description: 'Find important events and timestamps.',
    },
    {
      id: 'developer',
      title: 'Developer Guide',
      description: 'Turn coding tutorials into implementation steps.',
    },
    {
      id: 'custom',
      title: 'Custom Analysis',
      description: 'Define what you want VideoMind to find.',
    },
  ]

  return (
    <div className="app">
      <header className="navbar">
        <div className="navbar-inner">
          <a href="/" className="brand">
            <span className="brand-mark">V</span>
            <span className="brand-name">VideoMind</span>
          </a>

          <nav className="nav-links" aria-label="Primary navigation">
            <a href="/#how-it-works">How it works</a>
            <a href="/#capabilities">Capabilities</a>
          </nav>

          <a href="/#analyze" className="nav-button">
            Analyze Video
          </a>
        </div>
      </header>

      <main>
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-badge">
              <span className="badge-dot"></span>
              Video understanding platform
            </div>

            <h1>
              Understand any video.
              <br />
              <span>Get what matters.</span>
            </h1>

            <p className="hero-description">
              Upload a video or paste a public video URL. VideoMind analyzes the content and turns it into useful,
              structured information.
            </p>

            <div className="hero-tags">
              <span>Local videos</span>
              <span>YouTube</span>
              <span>Video URLs</span>
              <span>More sources</span>
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-window">
              <div className="window-header">
                <div className="window-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <div className="window-title">VideoMind Analysis</div>
              </div>

              <div className="visual-content">
                <div className="visual-label">VIDEO UNDERSTANDING</div>

                <h3>Analyze what happens inside a video.</h3>

                <div className="visual-row">
                  <div className="visual-icon">01</div>

                  <div>
                    <strong>Transcript</strong>
                    <p>Speech converted into timestamped text.</p>
                  </div>
                </div>

                <div className="visual-row">
                  <div className="visual-icon">02</div>

                  <div>
                    <strong>Visual Evidence</strong>
                    <p>Frames, scenes, OCR and detected events.</p>
                  </div>
                </div>

                <div className="visual-row">
                  <div className="visual-icon">03</div>

                  <div>
                    <strong>Structured Output</strong>
                    <p>Turn raw video evidence into useful results.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="analyzer-section" id="analyze">
          <div className="section-heading">
            <p className="section-eyebrow">START ANALYZING</p>

            <h2>Give VideoMind a video.</h2>

            <p>
              Upload a local video or provide a public video URL, then choose what you want to understand.
            </p>
          </div>

          <div className="analyzer-card">
            <div className="source-tabs">
              <button
                type="button"
                className={sourceType === 'upload' ? 'source-tab active' : 'source-tab'}
                onClick={() => {
                  setSourceType('upload')
                  setError('')
                }}
              >
                <span className="tab-icon">↑</span>
                Upload Video
              </button>

              <button
                type="button"
                className={sourceType === 'url' ? 'source-tab active' : 'source-tab'}
                onClick={() => {
                  setSourceType('url')
                  setError('')
                }}
              >
                <span className="tab-icon">↗</span>
                Video URL
              </button>
            </div>

            <div className="source-input">
              {sourceType === 'upload' ? (
                <>
                  <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileChange} hidden />

                  <div className="upload-zone" onDragOver={(event) => event.preventDefault()} onDrop={handleDrop} onClick={handleBrowse}>
                    <div className="upload-icon">↑</div>

                    {videoFile ? (
                      <>
                        <h3>{videoFile.name}</h3>

                        <p>{(videoFile.size / (1024 * 1024)).toFixed(2)} MB</p>

                        <button
                          type="button"
                          className="change-file-button"
                          onClick={(event) => {
                            event.stopPropagation()
                            handleBrowse()
                          }}
                        >
                          Choose another video
                        </button>
                      </>
                    ) : (
                      <>
                        <h3>Drop your video here</h3>

                        <p>or click to browse files</p>

                        <span className="supported-formats">MP4 · MOV · WebM · MKV · AVI</span>
                      </>
                    )}
                  </div>
                </>
              ) : (
                <div className="url-zone">
                  <div className="url-input-header">
                    <span className="url-large-icon">↗</span>

                    <div>
                      <h3>Paste a video URL</h3>

                      <p>Use a public video URL from a supported source.</p>
                    </div>
                  </div>

                  <input
                    type="url"
                    value={videoUrl}
                    onChange={(event) => {
                      setVideoUrl(event.target.value)
                      setError('')
                    }}
                    placeholder="https://..."
                    className="video-url-input"
                  />

                  <p className="url-help">
                    YouTube, direct video URLs and other supported video sources can be handled by the ingestion layer.
                  </p>
                </div>
              )}
            </div>

            <div className="analysis-selector">
              <div className="analysis-selector-header">
                <div>
                  <p className="selector-label">ANALYSIS TYPE</p>

                  <h3>What do you want from this video?</h3>
                </div>
              </div>

              <div className="analysis-grid">
                {analysisOptions.map((option) => (
                  <button
                    type="button"
                    key={option.id}
                    className={analysisType === option.id ? 'analysis-option active' : 'analysis-option'}
                    onClick={() => setAnalysisType(option.id)}
                  >
                    <span className="option-check">{analysisType === option.id ? '✓' : ''}</span>

                    <span className="option-content">
                      <strong>{option.title}</strong>

                      <small>{option.description}</small>
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {error && <div className="form-error">{error}</div>}

            <button type="button" className="main-analyze-button" onClick={handleSubmit}>
              Analyze Video
              <span>→</span>
            </button>

            <p className="privacy-note">Video processing will run through your VideoMind analysis pipeline.</p>
          </div>
        </section>

        <section className="capabilities-section" id="capabilities">
          <div className="section-heading">
            <p className="section-eyebrow">ONE PLATFORM</p>

            <h2>
              Different videos.
              <br />
              Different answers.
            </h2>

            <p>
              VideoMind provides a common video understanding layer and specialized analysis for different use cases.
            </p>
          </div>

          <div className="capability-grid">
            <div className="capability-card">
              <span className="capability-number">01</span>

              <h3>General Video Analysis</h3>

              <p>Understand the overall content, scenes, events and important moments.</p>
            </div>

            <div className="capability-card">
              <span className="capability-number">02</span>

              <h3>Learning &amp; Education</h3>

              <p>Turn lectures and educational videos into structured notes and useful references.</p>
            </div>

            <div className="capability-card">
              <span className="capability-number">03</span>

              <h3>Developer Analysis</h3>

              <p>Extract commands, files, code changes and implementation steps from coding tutorials.</p>
            </div>

            <div className="capability-card">
              <span className="capability-number">04</span>

              <h3>Custom Analysis</h3>

              <p>Analyze a video according to the information the user wants to extract.</p>
            </div>
          </div>
        </section>

        <section className="how-section" id="how-it-works">
          <div className="section-heading">
            <p className="section-eyebrow">HOW IT WORKS</p>

            <h2>From raw video to structured intelligence.</h2>

            <p>VideoMind processes different types of video sources through a common evidence pipeline.</p>
          </div>

          <div className="process-grid">
            <div className="process-card">
              <span>01</span>
              <h3>Add a video</h3>
              <p>Upload a local video or provide a public video URL.</p>
            </div>

            <div className="process-card">
              <span>02</span>
              <h3>Extract evidence</h3>
              <p>VideoMind processes speech, frames, visual information and other available evidence.</p>
            </div>

            <div className="process-card">
              <span>03</span>
              <h3>Understand the content</h3>
              <p>The system combines evidence across the video to identify meaningful information.</p>
            </div>

            <div className="process-card">
              <span>04</span>
              <h3>Get useful results</h3>
              <p>Explore summaries, transcripts, key moments, visual insights and specialized analysis.</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <p>© 2026 VideoMind</p>
          <p>Built with curiosity and a lot of video processing.</p>
        </div>
      </footer>
    </div>
  )
}

export default AppPage
