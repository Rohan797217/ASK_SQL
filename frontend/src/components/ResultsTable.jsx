export default function ResultsTable({ columns, rows, rowCount }) {
  if (!rows || rows.length === 0) return null

  return (
    <div className="results-table">
      <div className="results-table__header">
        <span className="results-table__label">
          📋 Results
        </span>
        <span className="results-table__count">
          {rowCount} row{rowCount !== 1 ? 's' : ''}
        </span>
      </div>
      <div className="results-table__wrapper">
        <table className="results-table__table">
          <thead>
            <tr>
              {columns.map((col, i) => (
                <th key={i}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {columns.map((col, colIdx) => (
                  <td key={colIdx}>
                    {formatValue(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function formatValue(val) {
  if (val === null || val === undefined) {
    return '—'
  }
  if (typeof val === 'number') {
    // Format large numbers with commas, keep decimals reasonable
    if (Number.isInteger(val)) {
      return val.toLocaleString()
    }
    return val.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  }
  if (typeof val === 'boolean') {
    return val ? '✓ Yes' : '✗ No'
  }
  return String(val)
}
