export default function WeatherCard({ data }) {
  if (!data) return null

  const stats = [
    { icon: '💧', label: 'Humidity',   val: `${data.humidity}%` },
    { icon: '💨', label: 'Wind',       val: `${data.windSpeed} m/s` },
    { icon: '🌡️', label: 'Feels Like', val: `${data.feels_like}°C` },
    { icon: '📊', label: 'Pressure',   val: `${data.pressure} hPa` },
  ]

  return (
    <div style={{
      background: '#0f172a', borderRadius: '16px', padding: '24px',
      border: '1px solid #1e293b'
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '12px' }}>
        🌤 Weather — {data.city}, {data.country}
      </p>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
        <img
          src={`https://openweathermap.org/img/wn/${data.icon}@2x.png`}
          alt={data.description}
          style={{ width: '64px', height: '64px' }}
        />
        <div>
          <p style={{ fontSize: '48px', fontWeight: 700, color: '#fff', lineHeight: 1 }}>
            {data.temperature}°C
          </p>
          <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '4px' }}>{data.description}</p>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        {stats.map(({ icon, label, val }) => (
          <div key={label} style={{
            background: '#1e293b', borderRadius: '12px', padding: '12px',
            display: 'flex', alignItems: 'center', gap: '10px'
          }}>
            <span style={{ fontSize: '20px' }}>{icon}</span>
            <div>
              <p style={{ color: '#64748b', fontSize: '11px' }}>{label}</p>
              <p style={{ color: '#fff', fontWeight: 600, fontSize: '14px' }}>{val}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
