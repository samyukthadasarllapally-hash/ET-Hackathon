export default function PollutantsCard({ data }) {
  if (!data) return null

  const pollutants = [
    { label: 'PM2.5', val: data.pm25, unit: 'µg/m³', safe: 25 },
    { label: 'PM10',  val: data.pm10, unit: 'µg/m³', safe: 50 },
    { label: 'NO₂',  val: data.no2,  unit: 'µg/m³', safe: 40 },
    { label: 'SO₂',  val: data.so2,  unit: 'µg/m³', safe: 20 },
    { label: 'CO',   val: data.co,   unit: 'µg/m³', safe: 4000 },
    { label: 'O₃',   val: data.o3,   unit: 'µg/m³', safe: 100 },
  ]

  return (
    <div style={{
      background: '#0f172a', borderRadius: '16px', padding: '24px',
      border: '1px solid #1e293b'
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '16px' }}>🧪 Pollutant Levels</p>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        {pollutants.map(({ label, val, unit, safe }) => {
          const pct = Math.min(100, (val / safe) * 100)
          const barColor = pct < 50 ? '#22c55e' : pct < 80 ? '#eab308' : '#ef4444'
          return (
            <div key={label} style={{
              background: '#1e293b', borderRadius: '12px', padding: '12px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ color: '#fff', fontSize: '13px', fontWeight: 600 }}>{label}</span>
                <span style={{ color: '#64748b', fontSize: '11px' }}>{val} {unit}</span>
              </div>
              <div style={{ background: '#334155', borderRadius: '4px', height: '6px' }}>
                <div style={{
                  width: `${pct}%`, height: '6px',
                  borderRadius: '4px', background: barColor,
                  transition: 'width 0.8s ease'
                }} />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
