export default function Navbar({ city, setCity, onSearch }) {
  return (
    <nav style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '14px 24px', background: '#0f172a',
      borderBottom: '1px solid #1e293b'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '24px' }}>🌬️</span>
        <span style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>
          AirSense <span style={{ color: '#60a5fa' }}>AI</span>
        </span>
        <span style={{
          marginLeft: '8px', padding: '2px 10px', borderRadius: '20px',
          background: 'rgba(96,165,250,0.15)', color: '#60a5fa', fontSize: '11px'
        }}>
          ET Hackathon
        </span>
      </div>
      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          placeholder="Search city..."
          style={{
            padding: '8px 14px', borderRadius: '10px',
            background: '#1e293b', color: '#fff',
            border: '1px solid #334155', outline: 'none', fontSize: '14px', width: '180px'
          }}
        />
        <button
          onClick={onSearch}
          style={{
            padding: '8px 18px', borderRadius: '10px', border: 'none',
            background: '#3b82f6', color: '#fff', cursor: 'pointer',
            fontWeight: 600, fontSize: '14px'
          }}
        >
          Search
        </button>
      </div>
    </nav>
  )
}
