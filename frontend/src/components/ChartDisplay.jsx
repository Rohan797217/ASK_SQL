import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

// Vibrant chart colors
const CHART_COLORS = [
  '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
  '#38bdf8', '#22d3ee', '#34d399', '#4ade80',
  '#fbbf24', '#fb923c', '#f87171', '#f472b6',
]

/**
 * Auto-detect if the results are chart-friendly:
 * - Needs at least one string/label column and one numeric column
 * - Max 20 rows (charts get unreadable with too many bars)
 */
function detectChartability(columns, rows) {
  if (!columns || !rows || rows.length === 0 || rows.length > 20) {
    return null
  }

  // Find label column (first string-like column)
  let labelCol = null
  let valueCol = null

  for (const col of columns) {
    const sampleVal = rows[0][col]
    if (typeof sampleVal === 'string' && !labelCol) {
      labelCol = col
    }
    if (typeof sampleVal === 'number' && !valueCol) {
      valueCol = col
    }
  }

  if (labelCol && valueCol) {
    return { labelCol, valueCol }
  }

  return null
}

// Custom tooltip with dark theme styling
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null

  return (
    <div style={{
      background: 'rgba(13, 13, 26, 0.95)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '8px',
      padding: '10px 14px',
      backdropFilter: 'blur(10px)',
      boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)',
    }}>
      <p style={{
        color: '#f1f5f9',
        fontSize: '0.85rem',
        fontWeight: 600,
        marginBottom: 4,
      }}>
        {label}
      </p>
      <p style={{
        color: '#a78bfa',
        fontSize: '0.9rem',
        fontWeight: 500,
      }}>
        {typeof payload[0].value === 'number'
          ? payload[0].value.toLocaleString(undefined, { maximumFractionDigits: 2 })
          : payload[0].value}
      </p>
    </div>
  )
}

export default function ChartDisplay({ columns, rows }) {
  const chart = detectChartability(columns, rows)

  if (!chart) return null

  const chartData = rows.map(row => ({
    label: String(row[chart.labelCol]),
    value: Number(row[chart.valueCol]) || 0,
  }))

  return (
    <div className="chart-display">
      <div className="chart-display__header">
        <span className="chart-display__label">
          📊 Visualization
        </span>
      </div>
      <div className="chart-display__body">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 30 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255, 255, 255, 0.05)"
              vertical={false}
            />
            <XAxis
              dataKey="label"
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              tickLine={false}
              axisLine={{ stroke: 'rgba(255, 255, 255, 0.1)' }}
              angle={-35}
              textAnchor="end"
              height={60}
              interval={0}
            />
            <YAxis
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => {
                if (v >= 1000000) return `${(v / 1000000).toFixed(1)}M`
                if (v >= 1000) return `${(v / 1000).toFixed(1)}K`
                return v
              }}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99, 102, 241, 0.08)' }} />
            <Bar
              dataKey="value"
              radius={[4, 4, 0, 0]}
              maxBarSize={50}
            >
              {chartData.map((_, index) => (
                <Cell key={index} fill={CHART_COLORS[index % CHART_COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
