import api from './api'

const supplyService = {
  getDemand: (params?: { page?: number; page_size?: number; batch_id?: number }) =>
    api.get('/api/v1/supply/demand', { params }).then(r => r.data.data),
  createDemand: (body: object) => api.post('/api/v1/supply/demand', body).then(r => r.data.data),
  getBench: (params?: { page?: number; page_size?: number; batch_id?: number }) =>
    api.get('/api/v1/supply/bench', { params }).then(r => r.data.data),
  createBench: (body: object) => api.post('/api/v1/supply/bench', body).then(r => r.data.data),
  getSummary: () => api.get('/api/v1/supply/summary').then(r => r.data.data),
  getBatches: () => api.get('/api/v1/supply/demand-batches').then(r => r.data.data),
}

export default supplyService
