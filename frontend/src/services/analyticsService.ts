import api from './api'

const analyticsService = {
  getSummary: (bu?: string) =>
    api.get('/api/v1/reports/analytics/summary', { params: { bu } }).then(r => r.data.data),
  getStatusPie: (bu?: string) =>
    api.get('/api/v1/reports/analytics/status-pie', { params: { bu } }).then(r => r.data.data),
  getSourcePie: (bu?: string) =>
    api.get('/api/v1/reports/analytics/source-pie', { params: { bu } }).then(r => r.data.data),
  getChannelPie: (bu?: string) =>
    api.get('/api/v1/reports/analytics/channel-pie', { params: { bu } }).then(r => r.data.data),
  getInterviewLine: (days = 30, bu?: string) =>
    api.get('/api/v1/reports/analytics/interview-line', { params: { days, bu } }).then(r => r.data.data),
  getTrend: (months = 6, bu?: string) =>
    api.get('/api/v1/reports/analytics/trend', { params: { months, bu } }).then(r => r.data.data),
  getRejectionReasons: (bu?: string) =>
    api.get('/api/v1/reports/analytics/rejection-reasons', { params: { bu } }).then(r => r.data.data),
  getArcDeviations: (threshold = 15) =>
    api.get('/api/v1/reports/analytics/arc-deviations', { params: { threshold } }).then(r => r.data.data),
  getInterviewData: (page = 1, pageSize = 20, bu?: string) =>
    api.get('/api/v1/reports/analytics/interview-data', { params: { page, page_size: pageSize, bu } }).then(r => r.data.data),
}

export default analyticsService
