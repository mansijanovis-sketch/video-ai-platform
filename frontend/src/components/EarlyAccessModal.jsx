import { useCallback, useEffect, useMemo, useState } from 'react'

const STORAGE_KEY = 'videomind-early-access'

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

function EarlyAccessModal({ isOpen, onClose }) {
  const [formData, setFormData] = useState({ name: '', email: '' })
  const [errors, setErrors] = useState({})
  const [isSubmitted, setIsSubmitted] = useState(false)

  const resetState = useCallback(() => {
    setFormData({ name: '', email: '' })
    setErrors({})
    setIsSubmitted(false)
  }, [])

  const handleClose = useCallback(() => {
    resetState()
    onClose()
  }, [onClose, resetState])

  useEffect(() => {
    if (!isOpen) {
      return undefined
    }

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        handleClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleClose, isOpen])

  const canSubmit = useMemo(
    () => formData.name.trim() && formData.email.trim() && !errors.email,
    [errors.email, formData.email, formData.name],
  )

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({ ...previous, [name]: value }))

    if (errors[name]) {
      setErrors((previous) => ({ ...previous, [name]: '' }))
    }

    if (name === 'email' && value) {
      setErrors((previous) => ({
        ...previous,
        email: isValidEmail(value) ? '' : 'Please enter a valid email address.',
      }))
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    const nextErrors = {}

    if (!formData.name.trim()) {
      nextErrors.name = 'Please enter your name.'
    }

    if (!formData.email.trim()) {
      nextErrors.email = 'Please enter your email.'
    } else if (!isValidEmail(formData.email.trim())) {
      nextErrors.email = 'Please enter a valid email address.'
    }

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors)
      return
    }

    const submission = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      submittedAt: new Date().toISOString(),
    }

    try {
      const storedLeads = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
      const nextLeads = Array.isArray(storedLeads) ? [...storedLeads, submission] : [submission]
      localStorage.setItem(STORAGE_KEY, JSON.stringify(nextLeads))
    } catch (error) {
      console.error('Failed to save early-access lead locally:', error)
    }

    setIsSubmitted(true)
    setErrors({})
  }

  if (!isOpen) {
    return null
  }

  return (
    <div
      className="early-access-backdrop"
      onClick={handleClose}
      role="presentation"
    >
      <div
        className="early-access-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="early-access-title"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          className="modal-close-button"
          aria-label="Close early access form"
          onClick={handleClose}
        >
          ×
        </button>

        {isSubmitted ? (
          <div className="early-access-success">
            <div className="success-badge">✓</div>
            <h3 id="early-access-title">You’re on the list.</h3>
            <p>
              Thanks for your interest in VideoMind. This demo stores the submission locally in the browser for now,
              and the implementation can be replaced with a real API later.
            </p>
            <button type="button" className="modal-primary-button" onClick={handleClose}>
              Close
            </button>
          </div>
        ) : (
          <>
            <p className="modal-kicker">Early access</p>
            <h3 id="early-access-title">Join the first wave.</h3>
            <p className="modal-copy">
              VideoMind is still being built. Join the early-access list to follow the launch and get access when we’re ready.
            </p>

            <form className="early-access-form" onSubmit={handleSubmit} noValidate>
              <div className="field-group">
                <label htmlFor="early-access-name">Name</label>
                <input
                  id="early-access-name"
                  name="name"
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Your name"
                  aria-invalid={Boolean(errors.name)}
                />
                {errors.name && <span className="field-error">{errors.name}</span>}
              </div>

              <div className="field-group">
                <label htmlFor="early-access-email">Email</label>
                <input
                  id="early-access-email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  aria-invalid={Boolean(errors.email)}
                />
                {errors.email && <span className="field-error">{errors.email}</span>}
              </div>

              <button type="submit" className="modal-primary-button" disabled={!canSubmit}>
                Join Early Access
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  )
}

export default EarlyAccessModal
