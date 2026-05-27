import apiClient from './api'

interface LoginRequest {
  email: string
  password: string
}

export async function login(data: LoginRequest) {
  const resp = await apiClient.post('/api/v1/auth/login', data)
  return resp.data.data
}

export async function getMe() {
  const resp = await apiClient.get('/api/v1/auth/me')
  return resp.data.data
}

export async function logout() {
  await apiClient.post('/api/v1/auth/logout')
  localStorage.removeItem('access_token')
  localStorage.removeItem('employee')
  localStorage.removeItem('active_role')
}
