import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [video, setVideo] = useState(null)
  const [videoUrl, setVideoUrl] = useState('')
  const [detections, setDetections] = useState([])
  const [ocrResults, setOcrResults] = useState([])
  const [description, setDescription] = useState('')
  const [objectSummary, setObjectSummary] = useState([])
  const [timeline, setTimeline] = useState([])

  const [uploading, setUploading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState('')

  const handleFileChange = (event) => {
    const file = event.target.files?.[0]

    if (!file) {
      return
    }

    setSelectedFile(file)
    setVideo(null)
    setDetections([])
    setOcrResults([])
    setDescription('')
    setObjectSummary([])
    setTimeline([])
    setError('')

    const localUrl = URL.createObjectURL(file)
    setVideoUrl(localUrl)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a video first.')
      return
    }

    setUploading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch(
        `${API_URL}/videos/upload`,
        {
          method: 'POST',
          body: formData,
        }
      )

      if (!response.ok) {
        throw new Error('Video upload failed.')
      }

      const data = await response.json()

      setVideo(data)

      if (data.filename) {
        setVideoUrl(
          `${API_URL}/uploads/${encodeURIComponent(data.filename)}`
        )
      }

    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const handleAnalyze = async () => {
    if (!video?.id) {
      setError('Please upload the video first.')
      return
    }

    setAnalyzing(true)
    setError('')

    try {
      const response = await fetch(
        `${API_URL}/videos/${video.id}/analyze`,
        {
          method: 'POST',
        }
      )

      if (!response.ok) {
        throw new Error('Video analysis failed.')
      }

      const data = await response.json()

      setDescription(data.description || '')
      setOcrResults(data.ocr_results || [])
      setObjectSummary(data.object_summary || [])
      setTimeline(data.timeline || [])

      setVideo((previous) => ({
        ...previous,
        status: data.status,
        frames_processed: data.frames_processed,
        detections_created: data.detections_created,
      }))

      await loadDetections(video.id)

    } catch (err) {
      setError(err.message)
    } finally {
      setAnalyzing(false)
    }
  }

  const loadDetections = async (videoId) => {
    try {
      const response = await fetch(
        `${API_URL}/videos/${videoId}/detections`
      )

      if (!response.ok) {
        throw new Error('Could not load detections.')
      }

      const data = await response.json()

      setDetections(data.detections || [])
    } catch (err) {
      setError(err.message)
    }
  }

  const formatTime = (seconds) => {
    if (seconds === null || seconds === undefined) {
      return '0.00s'
    }

    const totalSeconds = Math.max(0, Math.floor(Number(seconds)))
    const minutes = Math.floor(totalSeconds / 60)
    const remainingSeconds = totalSeconds % 60
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`
  }

  return (
    <div className="app">

      <header className="app-header">
        <div>
          <p className="eyebrow">AI VIDEO ANALYSIS</p>
          <h1>Video AI Platform</h1>
          <p className="subtitle">
            Upload a video and analyze objects, visible text,
            scenes, and video content.
          </p>
        </div>
      </header>

      <main className="container">

        {/* Upload Section */}
        <section className="card upload-card">

          <div className="section-header">
            <div>
              <p className="section-label">STEP 01</p>
              <h2>Upload Video</h2>
            </div>
          </div>

          <label className="upload-box">

            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
            />

            <div className="upload-icon">
              ↑
            </div>

            <strong>
              {selectedFile
                ? selectedFile.name
                : 'Choose a video file'}
            </strong>

            <span>
              MP4, MOV, AVI and other video formats
            </span>

          </label>

          {selectedFile && !video && (
            <button
              className="primary-button"
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Upload Video'}
            </button>
          )}

        </section>

        {/* Error */}
        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

        {/* Video Section */}
        {video && (
          <section className="card">

            <div className="section-header">
              <div>
                <p className="section-label">STEP 02</p>
                <h2>Video Preview</h2>
              </div>

              <span
                className={`status ${video.status === 'completed'
                    ? 'status-success'
                    : 'status-default'
                  }`}
              >
                {video.status || 'uploaded'}
              </span>
            </div>

            <div className="video-wrapper">
              <video
                src={videoUrl}
                controls
                className="video-player"
              />
            </div>

            <div className="video-info">

              <div>
                <span>Filename</span>
                <strong>{video.filename}</strong>
              </div>

              <div>
                <span>Duration</span>
                <strong>
                  {video.duration
                    ? `${Number(video.duration).toFixed(2)} sec`
                    : '-'}
                </strong>
              </div>

              <div>
                <span>FPS</span>
                <strong>
                  {video.fps
                    ? Number(video.fps).toFixed(2)
                    : '-'}
                </strong>
              </div>

              <div>
                <span>Video ID</span>
                <strong>#{video.id}</strong>
              </div>

            </div>

            <button
              className="primary-button analyze-button"
              onClick={handleAnalyze}
              disabled={analyzing}
            >
              {analyzing
                ? 'Analyzing Video...'
                : 'Analyze Video'}
            </button>

          </section>
        )}

        {/* AI Description */}
        {description && (
          <section className="card">

            <div className="section-header">
              <div>
                <p className="section-label">AI UNDERSTANDING</p>
                <h2>Video Description</h2>
              </div>
            </div>

            <div className="description-box">
              {description}
            </div>

            {video && (
              <div className="analysis-stats">

                <div>
                  <strong>
                    {video.frames_processed ?? 0}
                  </strong>
                  <span>Frames Processed</span>
                </div>

                <div>
                  <strong>
                    {video.detections_created ?? 0}
                  </strong>
                  <span>Detections</span>
                </div>

                <div>
                  <strong>
                    {ocrResults.length}
                  </strong>
                  <span>OCR Frames</span>
                </div>

              </div>
            )}

          </section>
        )}

        {/* Detections */}
        {detections.length > 0 && (
          <section className="card">

            <div className="section-header">
              <div>
                <p className="section-label">COMPUTER VISION</p>
                <h2>Detected Objects</h2>
              </div>
            </div>

            <div className="detection-list">

              {detections.map((detection) => (
                <div
                  className="detection-item"
                  key={detection.id}
                >

                  <div className="detection-main">
                    <strong>
                      {detection.label}
                    </strong>

                    <span>
                      {formatTime(detection.timestamp)}
                    </span>
                  </div>

                  <div className="confidence">
                    {(Number(detection.confidence) * 100).toFixed(1)}%
                  </div>

                </div>
              ))}

            </div>

          </section>
        )}

        {objectSummary.length > 0 && (
          <section className="card">
            <div className="section-header">
              <div>
                <p className="section-label">OBJECT SUMMARY</p>
                <h2>Objects Throughout the Video</h2>
              </div>
            </div>
            <div className="summary-grid">
              {objectSummary.map((object) => (
                <div className="summary-item" key={object.label}>
                  <strong>{object.label}</strong>
                  <span>{object.appearances} appearances · {formatTime(object.first_seen)}–{formatTime(object.last_seen)}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {timeline.length > 0 && (
          <section className="card">
            <div className="section-header">
              <div>
                <p className="section-label">VIDEO TIMELINE</p>
                <h2>Timestamped Events</h2>
              </div>
            </div>
            <div className="timeline-list">
              {timeline.map((event, index) => (
                <div className="timeline-item" key={`${event.type}-${event.timestamp}-${index}`}>
                  <time>{formatTime(event.timestamp)}</time>
                  <div><strong>{event.label}</strong>{event.detail && <span>{event.detail}</span>}</div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* OCR */}
        {ocrResults.length > 0 && (
          <section className="card">

            <div className="section-header">
              <div>
                <p className="section-label">TEXT RECOGNITION</p>
                <h2>Visible Text</h2>
              </div>
            </div>

            <div className="ocr-list">

              {ocrResults.map((result, index) => (
                <div
                  className="ocr-item"
                  key={`${result.timestamp}-${index}`}
                >

                  <div className="ocr-time">
                    {formatTime(result.timestamp)}
                  </div>

                  <div className="ocr-text">
                    {result.text}
                  </div>

                </div>
              ))}

            </div>

          </section>
        )}

      </main>

      <footer>
        Video AI Platform · Local AI Processing
      </footer>

    </div>
  )
}

export default App
