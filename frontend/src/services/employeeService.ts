import apiClient from './api'

export interface EmployeeCreate {
  emp_name: string
  email_id: string
  password: string
  location?: string
  grade?: string
  bu?: string
  practice?: string
  market_unit?: string
  account?: string
  organisation?: string
  role_ids?: number[]
  technology_ids?: number[]
  tower_names?: string[]
}

export async function createEmployee(data: EmployeeCreate) {
  const resp = await apiClient.post('/api/v1/employees', data)
  return resp.data.data
}

export async function listEmployees(page = 1, pageSize = 20, bu?: string) {
  const resp = await apiClient.get('/api/v1/employees', { params: { page, page_size: pageSize, bu } })
  return resp.data.data
}

export async function getEmployee(empId: number) {
  const resp = await apiClient.get(`/api/v1/employees/${empId}`)
  return resp.data.data
}

export async function updateEmployee(empId: number, data: Partial<EmployeeCreate>) {
  const resp = await apiClient.put(`/api/v1/employees/${empId}`, data)
  return resp.data.data
}

export async function deleteEmployee(empId: number) {
  await apiClient.delete(`/api/v1/employees/${empId}`)
}

export async function getPanelRoles() {
  const resp = await apiClient.get('/api/v1/panel/roles')
  return resp.data.data
}

export async function getPanelTechnologies() {
  const resp = await apiClient.get('/api/v1/panel/technologies')
  return resp.data.data
}

export async function getPanelBU(email: string) {
  const resp = await apiClient.get('/api/v1/panel/bu', { params: { email } })
  return resp.data.data
}
