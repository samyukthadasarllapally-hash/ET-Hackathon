import { BrowserRouter, Routes, Route } from 'react-router-dom'
import CitizenDashboard from './pages/CitizenDashboard'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CitizenDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
