import { useState, useEffect } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'

// VITE_API_URL is set in Vercel dashboard to point at the Render backend.
// In local dev, fall back to localhost:8000.
const API_BASE = import.meta.env.VITE_API_URL
  || (import.meta.env.DEV ? 'http://localhost:8000' : '')

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [healthStatus, setHealthStatus] = useState(null)

  // Check backend health on mount
  useEffect(() => {
    checkHealth()
  }, [])

  async function checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`)
      const data = await res.json()
      setHealthStatus(data)
    } catch {
      setHealthStatus({ status: 'offline', database: 'unknown', rag_initialized: false, available_providers: [] })
    }
  }

  async function handleAsk(question) {
    // Add user message
    const userMessage = { role: 'user', content: question, timestamp: Date.now() }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })

      const data = await res.json()

      // Add assistant message
      const assistantMessage = {
        role: 'assistant',
        content: data,
        timestamp: Date.now(),
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: {
          question,
          sql: '',
          results: [],
          columns: [],
          row_count: 0,
          explanation: '',
          error: `Failed to connect to the backend. Please make sure the server is running at ${API_BASE}`,
          provider: '',
        },
        timestamp: Date.now(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const isConnected = healthStatus?.status === 'healthy'

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header__brand">
          <div className="app-header__logo">⚡</div>
          <div>
            <h1 className="app-header__title">AskSQL</h1>
            <p className="app-header__subtitle">Text-to-SQL AI Assistant</p>
          </div>
        </div>
        <div className="app-header__status">
          <span className={`app-header__status-dot ${!isConnected ? 'app-header__status-dot--error' : ''}`}></span>
          {isConnected ? 'Connected' : 'Offline'}
          {healthStatus?.available_providers?.length > 0 && (
            <span> · {healthStatus.available_providers.join(', ')}</span>
          )}
        </div>
      </header>

      <ChatInterface
        messages={messages}
        isLoading={isLoading}
        onAsk={handleAsk}
      />
    </div>
  )
}

export default App
