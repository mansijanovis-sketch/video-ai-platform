import { useState } from 'react'
import './AppPage.css'
import { createYouTubeVideo, getTranscript, getTutorialSteps, getVideoEvidence } from '../services/api'

const youtubeUrlPattern = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=[\w-]{11}(?:[&#].*)?|youtu\.be\/[\w-]{11}(?:\?.*)?|youtube\.com\/shorts\/[\w-]{11}(?:\?.*)?)$/i

const stages = [
  ['received', 'Receiving tutorial'],
  ['transcript', 'Fetching transcript'],
  ['actions', 'Extracting implementation steps'],
  ['guide', 'Building guide'],
]

function formatTime(seconds) {
  const value = Number(seconds)
  if (!Number.isFinite(value)) return '--:--'

  const totalSeconds = Math.max(0, Math.floor(value))
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const remainder = totalSeconds % 60
  const parts = [hours, minutes, remainder]

  if (hours > 0) {
    return parts.map((part) => String(part).padStart(2, '0')).join(':')
  }

  return `${String(minutes).padStart(2, '0')}:${String(remainder).padStart(2, '0')}`
}

function formatTimestamp(step) {
  const start = formatTime(step.start_time)
  if (step.end_time === undefined || step.end_time === null) return start
  return `${start}-${formatTime(step.end_time)}`
}

function actionLabel(action) {
  const labels = {
    run_command: 'Command',
    create_file: 'Create file',
    edit_file: 'Edit file',
  }

  return labels[action] || 'Implementation step'
}

function stepValue(step) {
  return step.value || step.path || step.name || ''
}

function instructionFor(step) {
  const value = stepValue(step)
  const action = step.action

  if (action === 'create_file' && value) {
    return `Create a new file named ${value}.`
  }

  if (action === 'edit_file' && value) {
    const operation = step.operation ? step.operation.toLowerCase() : 'edit'
    return `${operation === 'replace' ? 'Replace' : 'Edit'} the existing ${value} component with the implementation shown in the tutorial.`
  }

  if (action === 'run_command') {
    const command = value.toLowerCase()
    if (command.startsWith('npx create-react-app')) return 'Create the React application.'
    if (command.startsWith('cd ')) return 'Move into the React project directory.'
    if (command === 'yarn start') return 'Start the development server.'
    if (command.includes('react-router-dom')) return 'Install React Router.'
    return 'Run the command shown in the tutorial.'
  }

  return step.instruction || 'Follow the implementation step shown in the tutorial.'
}

function AppPage() {
  const [url, setUrl] = useState('')
  const [state, setState] = useState('idle')
  const [stage, setStage] = useState('received')
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [copiedStep, setCopiedStep] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    const trimmedUrl = url.trim()

    if (!trimmedUrl) {
      setError('Paste a YouTube tutorial URL to continue.')
      setState('error')
      return
    }

    if (!youtubeUrlPattern.test(trimmedUrl)) {
      setError('Enter a valid YouTube watch, Shorts, or youtu.be URL.')
      setState('error')
      return
    }

    setError('')
    setState('submitting')
    setStage('received')

    try {
      const video = await createYouTubeVideo(trimmedUrl)
      if (!video?.id) throw new Error('The backend returned an invalid tutorial record.')

      setState('processing')
      setStage('transcript')
      const transcript = await getTranscript(video.id)
      if (!Array.isArray(transcript?.segments) || transcript.segments.length === 0) {
        throw new Error('No transcript is available for this tutorial.')
      }

      setStage('actions')
      const stepsResponse = await getTutorialSteps(video.id)
      if (!stepsResponse || !Array.isArray(stepsResponse.steps)) {
        throw new Error('The backend returned an invalid implementation guide.')
      }

      const steps = stepsResponse.steps
      let evidence = []
      try {
        const evidenceResponse = await getVideoEvidence(video.id)
        evidence = Array.isArray(evidenceResponse?.evidence) ? evidenceResponse.evidence : []
      } catch {
        // Step-level transcript evidence remains available when the collection is unavailable.
      }

      setStage('guide')
      setResult({ video, steps, evidence, url: trimmedUrl })
      setState('completed')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Tutorial analysis failed. Please try again.')
      setState('error')
    }
  }

  const copyCommand = async (step, stepKey) => {
    const command = stepValue(step)
    if (!command || !navigator.clipboard) return

    try {
      await navigator.clipboard.writeText(command)
      setCopiedStep(stepKey)
      window.setTimeout(() => setCopiedStep(null), 1600)
    } catch {
      setError('The command could not be copied. Please select it manually.')
    }
  }

  const renderStep = (step, index) => {
    const value = stepValue(step)
    const stepKey = step.id || `${step.step}-${step.start_time}-${index}`
    const evidenceText = step.evidence?.text?.trim()
    const isCommand = step.action === 'run_command'
    const isFileAction = step.action === 'create_file' || step.action === 'edit_file'

    return (
      <article className="step-card" key={stepKey}>
        <div className="step-number">{String(index + 1).padStart(2, '0')}</div>
        <div className="step-content">
          <div className="step-meta">
            <span>{actionLabel(step.action)}</span>
            {step.confidence ? <span>{Math.round(Number(step.confidence) * 100)}% confidence</span> : null}
          </div>
          <h3>{instructionFor(step)}</h3>

          {isCommand && value && (
            <div className="step-detail command-detail">
              <span className="detail-label">Command</span>
              <div className="command-row">
                <code>{value}</code>
                <button type="button" onClick={() => copyCommand(step, stepKey)}>
                  {copiedStep === stepKey ? 'Copied' : 'Copy'}
                </button>
              </div>
            </div>
          )}

          {isFileAction && value && (
            <div className="step-detail file-detail">
              <span className="detail-label">File</span>
              <code>{value}</code>
              {step.operation && <span className="operation-label">Operation: {String(step.operation).replace(/^./, (letter) => letter.toUpperCase())}</span>}
            </div>
          )}

          <p className="timestamp">Timestamp: {formatTimestamp(step)}</p>

          {evidenceText && (
            <details className="evidence-detail">
              <summary>Evidence</summary>
              <div className="evidence-content">
                <span className="detail-label">Transcript evidence</span>
                <blockquote>{evidenceText}</blockquote>
              </div>
            </details>
          )}
        </div>
      </article>
    )
  }

  return (
    <div className="app-page">
      <header className="app-header">
        <a href="/" className="app-brand"><span>V</span>VideoMind</a>
        <a href="/" className="app-back-link">Back to home</a>
      </header>

      <main className="app-main">
        <section className="app-intro">
          <p className="app-kicker">Developer tutorial intelligence</p>
          <h1>Turn coding tutorials into buildable steps.</h1>
          <p>Paste a YouTube coding tutorial and VideoMind will extract the implementation steps, commands, files, and supporting evidence.</p>
        </section>

        <section className="analyzer-panel" aria-labelledby="analyzer-title">
          <div className="panel-heading">
            <div><p className="app-kicker">Start an analysis</p><h2 id="analyzer-title">Analyze a YouTube tutorial</h2></div>
            <span className="panel-status">{state === 'completed' ? 'Complete' : 'MVP'}</span>
          </div>
          <form onSubmit={handleSubmit}>
            <label htmlFor="youtube-url">YouTube URL</label>
            <div className="url-submit-row">
              <input id="youtube-url" type="url" value={url} onChange={(event) => { setUrl(event.target.value); if (state === 'error') setState('idle') }} placeholder="Paste YouTube tutorial URL" disabled={state === 'submitting' || state === 'processing'} />
              <button type="submit" disabled={state === 'submitting' || state === 'processing'}>{state === 'submitting' || state === 'processing' ? 'Analyzing...' : 'Analyze Tutorial'} <span aria-hidden="true">→</span></button>
            </div>
            <p className="example-url">Example: https://www.youtube.com/watch?v=...</p>
          </form>
          {error && <div className="error-message" role="alert">{error}</div>}
        </section>

        {(state === 'submitting' || state === 'processing') && <section className="progress-panel" aria-live="polite"><h2>Analyzing tutorial</h2><div className="progress-list">{stages.map(([id, label]) => { const currentIndex = stages.findIndex(([stageId]) => stageId === stage); const itemIndex = stages.findIndex(([stageId]) => stageId === id); const icon = itemIndex < currentIndex ? '✓' : itemIndex === currentIndex ? '●' : '○'; return <div className={`progress-item ${itemIndex <= currentIndex ? 'active' : ''}`} key={id}><span>{icon}</span>{itemIndex + 1}. {label}</div> })}</div></section>}

        {result && state === 'completed' && <section className="guide-section"><div className="guide-header"><div><p className="app-kicker">Implementation Guide</p><h2>{result.video.title || result.video.filename || 'YouTube tutorial'}</h2><a href={result.url} target="_blank" rel="noreferrer">{result.url}</a></div><span>{result.steps.length} {result.steps.length === 1 ? 'step' : 'steps'}</span></div>{result.steps.length > 0 ? <div className="steps-list">{result.steps.map(renderStep)}</div> : <div className="empty-guide"><h3>No implementation steps were detected yet.</h3><p>The transcript was processed, but VideoMind could not identify reliable developer actions.</p></div>}</section>}
      </main>
    </div>
  )
}

export default AppPage
