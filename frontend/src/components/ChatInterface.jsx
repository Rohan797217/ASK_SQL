import { useState, useRef, useEffect } from 'react'
import SqlDisplay from './SqlDisplay'
import ResultsTable from './ResultsTable'
import ChartDisplay from './ChartDisplay'
import LoadingSpinner from './LoadingSpinner'

const SUGGESTIONS = [
  { icon: '📊', text: 'What are the top 5 products by total revenue?' },
  { icon: '🌍', text: 'How many customers are from each country?' },
  { icon: '📦', text: 'Which orders haven\'t been shipped yet?' },
  { icon: '📈', text: 'Show monthly order counts' },
  { icon: '👤', text: 'Which employee handled the most orders?' },
  { icon: '🏷️', text: 'What is the average product price per category?' },
]

export default function ChatInterface({ messages, isLoading, onAsk }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isLoading) return
    onAsk(trimmed)
    setInput('')
  }

  function handleSuggestionClick(text) {
    if (isLoading) return
    onAsk(text)
  }

  const hasMessages = messages.length > 0

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {!hasMessages && (
          <div className="welcome">
            <div className="welcome__icon">🔍</div>
            <h2 className="welcome__title">Ask your database anything</h2>
            <p className="welcome__desc">
              Type a question in plain English and I'll generate the SQL,
              run it against the database, and show you the results — all with safety guardrails.
            </p>
            <div className="welcome__suggestions">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  className="welcome__suggestion"
                  onClick={() => handleSuggestionClick(s.text)}
                  disabled={isLoading}
                >
                  <span className="welcome__suggestion-icon">{s.icon}</span>
                  {s.text}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message message--${msg.role}`}>
            {msg.role === 'user' ? (
              <div className="message__bubble message__bubble--user">
                <p className="message__text">{msg.content}</p>
              </div>
            ) : (
              <div className="message__bubble message__bubble--assistant">
                {msg.content.provider && (
                  <div className="message__provider">
                    🤖 {msg.content.provider}
                  </div>
                )}

                {msg.content.sql && (
                  <SqlDisplay sql={msg.content.sql} />
                )}

                {msg.content.explanation && !msg.content.error && (
                  <div className="message__explanation">
                    {msg.content.explanation}
                  </div>
                )}

                {msg.content.error && (
                  <div className="message__error">
                    <span className="message__error-icon">⚠️</span>
                    <span>{msg.content.error}</span>
                  </div>
                )}

                {msg.content.results && msg.content.results.length > 0 && (
                  <>
                    <ResultsTable
                      columns={msg.content.columns}
                      rows={msg.content.results}
                      rowCount={msg.content.row_count}
                    />
                    <ChartDisplay
                      columns={msg.content.columns}
                      rows={msg.content.results}
                    />
                  </>
                )}
              </div>
            )}
          </div>
        ))}

        {isLoading && <LoadingSpinner />}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <form className="chat-input__form" onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            id="question-input"
            type="text"
            className="chat-input__input"
            placeholder="Ask a question about your data..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            autoComplete="off"
          />
          <button
            id="submit-button"
            type="submit"
            className="chat-input__submit"
            disabled={isLoading || !input.trim()}
            aria-label="Send question"
          >
            ➤
          </button>
        </form>
        <p className="chat-input__hint">
          Powered by RAG + Gemini/Groq/Ollama · Read-only queries only · Results limited to 500 rows
        </p>
      </div>
    </div>
  )
}
