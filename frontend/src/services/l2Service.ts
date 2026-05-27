import api from './api'

const l2Service = {
  listCandidates: (params?: { page?: number; page_size?: number; status?: string }) =>
    api.get('/api/v1/l2/candidates', { params }).then(r => r.data.data),

  upsert: (candidateId: number, body: {
    l2_interview_date?: string
    l2_feedback?: string
    l2_recommendation?: string
    l2_status?: string
  }) => api.put(`/api/v1/l2/candidates/${candidateId}`, body).then(r => r.data.data),

  getAging: () => api.get('/api/v1/l2/aging').then(r => r.data.data),
}

export default l2Service
