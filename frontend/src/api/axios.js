import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // Directly using your backend URL
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor
api.interceptors.request.use(config => {
  // You can add auth tokens here if needed
  // config.headers.Authorization = `Bearer ${token}`
  return config
})

// Add response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    // Handle errors globally
    if (error.response) {
      console.error('API Error:', error.response.status, error.response.data)
    } else {
      console.error('API Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api