import api from './api'

const referralService = {
  // Public (no auth required)
  getTechnologies: () => api.get('/api/v1/referral/technologies').then(r => r.data.data),
  getNoticePeriods: () => api.get('/api/v1/referral/notice-periods').then(r => r.data.data),
  getLocations: () => api.get('/api/v1/referral/locations').then(r => r.data.data),
  submitReferral: (body: object) => api.post('/api/v1/referral/submit', body).then(r => r.data.data),

  // Protected
  listCandidates: (params?: { page?: number; page_size?: number; bu?: string; account?: string }) =>
    api.get('/api/v1/referral/candidates', { params }).then(r => r.data.data),
  getCandidate: (id: number) => api.get(`/api/v1/referral/candidates/${id}`).then(r => r.data.data),
  updateStatus: (id: number, status: string) =>
    api.patch(`/api/v1/referral/candidates/${id}/status`, null, { params: { status } }).then(r => r.data.data),
  getReportsByBU: () => api.get('/api/v1/referral/reports/by-bu').then(r => r.data.data),
  getReportsByAccount: () => api.get('/api/v1/referral/reports/by-account').then(r => r.data.data),
}

export default referralService
