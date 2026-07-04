import { useState } from 'react'

// SQL keywords for syntax highlighting
const SQL_KEYWORDS = [
  'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER',
  'FULL', 'CROSS', 'ON', 'AND', 'OR', 'NOT', 'IN', 'IS', 'NULL', 'AS',
  'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
  'DISTINCT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'EXISTS', 'BETWEEN',
  'LIKE', 'ILIKE', 'ASC', 'DESC', 'WITH', 'RECURSIVE', 'TRUE', 'FALSE',
  'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'COALESCE', 'CAST',
  'DATE_TRUNC', 'EXTRACT', 'NOW', 'CURRENT_DATE', 'INTERVAL',
]

function highlightSQL(sql) {
  if (!sql) return ''

  // Escape HTML first
  let highlighted = sql
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // Highlight strings (single-quoted)
  highlighted = highlighted.replace(
    /('(?:[^'\\]|\\.)*')/g,
    '<span class="sql-string">$1</span>'
  )

  // Highlight numbers
  highlighted = highlighted.replace(
    /\b(\d+(?:\.\d+)?)\b/g,
    '<span class="sql-number">$1</span>'
  )

  // Highlight keywords (case-insensitive, whole words only)
  for (const keyword of SQL_KEYWORDS) {
    const regex = new RegExp(`\\b(${keyword})\\b`, 'gi')
    highlighted = highlighted.replace(regex, (match) => {
      // Don't re-highlight if already inside a span
      return `<span class="sql-keyword">${match.toUpperCase()}</span>`
    })
  }

  // Highlight comments
  highlighted = highlighted.replace(
    /(--.*$)/gm,
    '<span class="sql-comment">$1</span>'
  )

  return highlighted
}

export default function SqlDisplay({ sql }) {
  const [copied, setCopied] = useState(false)

  if (!sql) return null

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(sql)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement('textarea')
      textarea.value = sql
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="sql-display">
      <div className="sql-display__header">
        <span className="sql-display__label">
          💾 Generated SQL
        </span>
        <button
          className={`sql-display__copy ${copied ? 'sql-display__copy--copied' : ''}`}
          onClick={handleCopy}
          aria-label="Copy SQL"
        >
          {copied ? '✓ Copied' : '⎘ Copy'}
        </button>
      </div>
      <div
        className="sql-display__code"
        dangerouslySetInnerHTML={{ __html: highlightSQL(sql) }}
      />
    </div>
  )
}
