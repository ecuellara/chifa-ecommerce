import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/'

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  // no pegues token en login/register/refresh
  if (config.url.includes('auth/login') || config.url.includes('auth/register') || config.url.includes('auth/refresh')) return config
  const token = localStorage.getItem('chifa_access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const orig = error.config
    if (error.response?.status === 401 && !orig._retry && !orig.url.includes('auth/')) {
      orig._retry = true
      try {
        const rt = localStorage.getItem('chifa_refresh')
        const r = await axios.post(`${API_URL}auth/refresh/`, { refresh: rt })
        localStorage.setItem('chifa_access', r.data.access)
        orig.headers.Authorization = `Bearer ${r.data.access}`
        return api(orig)
      } catch (e) {
        localStorage.removeItem('chifa_access'); localStorage.removeItem('chifa_refresh'); localStorage.removeItem('chifa_user')
      }
    }
    throw error
  }
)

export default api