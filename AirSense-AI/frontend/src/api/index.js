import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getWeather         = (city) => api.get(`/weather/current?city=${city}`)
export const getAQI             = (city) => api.get(`/aqi/current?city=${city}`)
export const getForecast        = (city) => api.get(`/prediction/forecast?city=${city}`)
export const getRecommendations = (aqi)  => api.get(`/recommendations/citizen?zone_id=z001&aqi=${aqi}`)
export const sendChat           = (query) => api.post('/chat/query', { query, zone_id: 'z001' })
