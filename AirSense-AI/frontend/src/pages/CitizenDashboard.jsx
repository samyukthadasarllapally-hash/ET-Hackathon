import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import AQICard from '../components/AQICard'
import WeatherCard from '../components/WeatherCard'
import PollutantsCard from '../components/PollutantsCard'
import RecommendationsCard from '../components/RecommendationsCard'
import HeatMap from '../components/HeatMap'
import { getWeather, getAQI, getForecast, getRecommendations } from '../api'

function Skeleton() {
  return (
    <div style={{
      background: 'linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%)',
      backgroundSize: '200% 100%',
      animation: 'shimmer 1.5s infinite',
      borderRadius: '16px',
      height: '200px'
    }} />
  )
}

export default function CitizenDashboard() {
  const [city, setCity]            = useState('Hyderabad')
  const [searchCity, setSearchCity] = useState('Hyderabad')
  const [weather, setWeather]      = useState(null)
  const [aqi, setAqi]              = useState(null)
  const [forecast, setForecast]    = useState(null)
  const [recs, setRecs]            = useState(null)
  const [loading, setLoading]      = useState(true)
  const [error, setError]          = useState(null)

  async function fetchAll(c) {
    setLoading(true)
    setError(null)
    try {
      const [w, a, f] = await Promise.all([
        getWeather(c),
        getAQI(c),
        getForecast(c),
      ])
      setWeather(w.data)
      setAqi(a.data)
      setForecast(f.data)
      const rec = await getRecommendations(Math.round(f.data.currentAQI))
      setRecs(rec.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch data. Check API keys and backend.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAll(searchCity) }, [searchCity])

  function onSearch() {
    const trimmed = city.trim()
    if (trimmed) setSearchCity(trimmed)
  }

  return (
    <div style={{ minHeight: '100vh', background: '#020617', color: '#f1f5f9' }}>
      <style>{`
        @keyframes shimmer {
          0%   { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>

      <Navbar city={city} setCity={setCity} onSearch={onSearch} />

      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '24px 16px' }}>

        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 style={{ fontSize: '22px', fontWeight: 700, color: '#fff' }}>🌆 Citizen Dashboard</h1>
            <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '4px' }}>
              Live air quality intelligence · {searchCity}
            </p>
          </div>
          <button
            onClick={() => fetchAll(searchCity)}
            disabled={loading}
            style={{
              padding: '8px 16px', borderRadius: '10px', border: 'none',
              background: loading ? '#334155' : '#3b82f6', color: '#fff',
              cursor: loading ? 'not-allowed' : 'pointer', fontSize: '13px'
            }}
          >
            {loading ? '⟳ Loading...' : '⟳ Refresh'}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div style={{
            marginBottom: '16px', padding: '14px 16px',
            background: 'rgba(239,68,68,0.15)', border: '1px solid #ef4444',
            borderRadius: '12px', color: '#fca5a5', fontSize: '13px'
          }}>
            ⚠ {error}
          </div>
        )}

        {/* Row 1 */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          {loading ? <Skeleton /> : <AQICard data={forecast} />}
          {loading ? <Skeleton /> : <WeatherCard data={weather} />}
        </div>

        {/* Row 2 */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          {loading ? <Skeleton /> : <PollutantsCard data={aqi} />}
          {loading ? <Skeleton /> : <RecommendationsCard data={recs} />}
        </div>

        {/* Map */}
        {!loading && weather && (
          <HeatMap lat={weather.lat} lon={weather.lon} aqi={forecast?.currentAQI} city={searchCity} />
        )}

        <p style={{ textAlign: 'center', color: '#334155', fontSize: '11px', marginTop: '24px' }}>
          AirSense AI · OpenWeather · Random Forest ML · ET Hackathon 2026
        </p>
      </div>
    </div>
  )
}
