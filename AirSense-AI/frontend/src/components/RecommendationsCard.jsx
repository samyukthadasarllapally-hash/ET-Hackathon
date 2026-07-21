export default function RecommendationsCard({ data }) {
  if (!data) return null

  const colorMap = {
    green: '#22c55e', yellow: '#eab308',
    orange: '#f97316', red: '#ef4444', maroon: '#be123c'
  }
  const badgeColor = colorMap[data.color] || '#3b82f6'

  return (
    <div style={{
      background: '#0f172a', borderRadius: '16px', padding: '24px',
      border: '1px solid #1e293b'
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '16px' }}>💡 Health Advisory</p>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
        <span style={{
          padding: '4px 14px', borderRadius: '20px', fontSize: '13px',
          fontWeight: 600, color: '#fff', background: badgeColor
        }}>
          {data.level}
        </span>
        <span style={{ color: '#94a3b8', fontSize: '13px' }}>😷 {data.mask}</span>
      </div>

      <p style={{
        color: '#e2e8f0', fontSize: '14px', lineHeight: '1.6',
        background: '#1e293b', borderRadius: '12px', padding: '12px', marginBottom: '12px'
      }}>
        {data.advisory}
      </p>

      <div style={{
        background: 'rgba(59,130,246,0.1)', border: '1px solid rgba(59,130,246,0.3)',
        borderRadius: '10px', padding: '10px 12px'
      }}>
        <p style={{ color: '#60a5fa', fontSize: '12px' }}>🗺 {data.route_suggestion}</p>
      </div>
    </div>
  )
}
