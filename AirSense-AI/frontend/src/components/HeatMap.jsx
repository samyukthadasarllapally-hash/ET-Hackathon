import { MapContainer, TileLayer, Circle, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

function getColor(aqi) {
  if (aqi <= 50)  return '#22c55e'
  if (aqi <= 100) return '#eab308'
  if (aqi <= 200) return '#f97316'
  if (aqi <= 300) return '#ef4444'
  return '#a855f7'
}

export default function HeatMap({ lat, lon, aqi, city }) {
  if (!lat || !lon) return null
  const color = getColor(aqi)

  return (
    <div style={{
      background: '#0f172a', borderRadius: '16px',
      border: '1px solid #1e293b', overflow: 'hidden', marginBottom: '16px'
    }}>
      <p style={{ color: '#94a3b8', fontSize: '12px', padding: '16px 20px 8px' }}>
        🗺 Pollution Map — {city}
      </p>
      <MapContainer
        center={[lat, lon]}
        zoom={11}
        style={{ height: '320px', width: '100%' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='© OpenStreetMap contributors'
        />
        <Circle
          center={[lat, lon]}
          radius={8000}
          pathOptions={{ color, fillColor: color, fillOpacity: 0.3, weight: 2 }}
        >
          <Popup>
            <div style={{ textAlign: 'center' }}>
              <b>{city}</b><br />
              AQI: <span style={{ color, fontWeight: 700 }}>{aqi}</span>
            </div>
          </Popup>
        </Circle>
      </MapContainer>
    </div>
  )
}
