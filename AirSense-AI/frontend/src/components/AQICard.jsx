function getColor(aqi) {
  if (aqi <= 50)  return { main: '#22c55e', bg: 'rgba(34,197,94,0.15)',   label: 'Good' }
  if (aqi <= 100) return { main: '#eab308', bg: 'rgba(234,179,8,0.15)',   label: 'Satisfactory' }
  if (aqi <= 200) return { main: '#f97316', bg: 'rgba(249,115,22,0.15)',  label: 'Moderate' }
  if (aqi <= 300) return { main: '#ef4444', bg: 'rgba(239,68,68,0.15)',   label: 'Poor' }
  if (aqi <= 400) return { main: '#a855f7', bg: 'rgba(168,85,247,0.15)', label: 'Very Poor' }
  return           { main: '#be123c',  bg: 'rgba(190,18,60,0.15)',   label: 'Hazardous' }
}

function ForecastBox({ label, aqi }) {
  const c = getColor(aqi)
  return (
    <div style={{
      background: '#1e293b', borderRadius: '12px', padding: '12px',
      textAlign: 'center', border: `1px solid ${c.main}33`
    }}>
      <p style={{ color: '#94a3b8', fontSize: '11px', marginBottom: '4px' }}>{label} forecast</p>
      <p style={{ fontSize: '26px', fontWeight: 700, color: c.main }}>{aqi}</p>
      <p style={{ color: '#94a3b8', fontSize: '11px' }}>{c.label}</p>
    </div>
  )
}

export default function AQICard({ data }) {
  if (!data) return null
  const c = getColor(data.currentAQI)

  return (
    <div style={{
      background: '#0f172a', borderRadius: '16px', padding: '24px',
      border: '1px solid #1e293b'
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '8px' }}>
        📍 Current AQI — {data.city}
      </p>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '16px', marginBottom: '20px' }}>
        <span style={{ fontSize: '72px', fontWeight: 800, color: c.main, lineHeight: 1 }}>
          {data.currentAQI}
        </span>
        <div style={{ marginBottom: '8px' }}>
          <span style={{
            padding: '4px 14px', borderRadius: '20px', fontSize: '13px',
            fontWeight: 600, color: '#fff', background: c.main
          }}>
            {data.category}
          </span>
          <p style={{ color: '#475569', fontSize: '11px', marginTop: '4px' }}>
            🤖 {data.source}
          </p>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
        <ForecastBox label="24h" aqi={data.forecast24h?.aqi} />
        <ForecastBox label="48h" aqi={data.forecast48h?.aqi} />
        <ForecastBox label="72h" aqi={data.forecast72h?.aqi} />
      </div>
    </div>
  )
}
