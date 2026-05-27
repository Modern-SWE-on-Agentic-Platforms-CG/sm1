import apiClient from './api'

export async function uploadCandidates(file: File) {
  const form = new FormData()
  form.append('file', file)
  const resp = await apiClient.post('/api/v1/candidates/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data.data
}

export async function listCandidates(page = 1, pageSize = 20, status?: string, skillId?: number) {
  const resp = await apiClient.get('/api/v1/candidates', {
    params: { page, page_size: pageSize, status, skill_id: skillId },
  })
  return resp.data.data
}

export async function getCandidate(id: number) {
  const resp = await apiClient.get(`/api/v1/candidates/${id}`)
  return resp.data.data
}

export async function updateCandidate(id: number, data: object) {
  const resp = await apiClient.put(`/api/v1/candidates/${id}`, data)
  return resp.data.data
}

export async function changeStatus(id: number, toStatus: string, notes?: string) {
  const resp = await apiClient.post(`/api/v1/candidates/${id}/status`, { to_status: toStatus, notes })
  return resp.data.data
}

export async function getStatusOptions() {
  const resp = await apiClient.get('/api/v1/candidates/status-options')
  return resp.data.data
}

export async function addComment(id: number, commentText: string | null, attachment?: File) {
  const form = new FormData()
  if (commentText) form.append('comment_text', commentText)
  if (attachment) form.append('attachment', attachment)
  const resp = await apiClient.post(`/api/v1/candidates/${id}/comments`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data.data
}

export async function listComments(id: number) {
  const resp = await apiClient.get(`/api/v1/candidates/${id}/comments`)
  return resp.data.data
}

export async function updateDOJ(id: number, doj: string) {
  const resp = await apiClient.put(`/api/v1/candidates/${id}`, { doj })
  return resp.data.data
}

export async function updateSkill(id: number, skillId: number) {
  const resp = await apiClient.put(`/api/v1/candidates/${id}`, { skill_id: skillId })
  return resp.data.data
}

export async function downloadResume(id: number): Promise<string> {
  const resp = await apiClient.get(`/api/v1/candidates/${id}/resume`, { responseType: 'blob' })
  return URL.createObjectURL(resp.data)
}

export async function uploadResume(id: number, file: File) {
  const form = new FormData()
  form.append('file', file)
  const resp = await apiClient.post(`/api/v1/candidates/${id}/resume`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data.data
}

const candidateService = {
  uploadCandidates,
  listCandidates,
  getCandidate,
  updateCandidate,
  changeStatus,
  getStatusOptions,
  addComment,
  listComments,
  updateDOJ,
  updateSkill,
  downloadResume,
  uploadResume,
}

export default candidateService
