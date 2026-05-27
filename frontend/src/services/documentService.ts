import api from './api'

const documentService = {
  downloadResume: (candidateId: number) =>
    api.get(`/api/v1/candidates/${candidateId}/resume`, { responseType: 'blob' }),

  downloadAttachment: (candidateId: number, commentId: number) =>
    api.get(`/api/v1/candidates/${candidateId}/comments/${commentId}/attachment`, { responseType: 'blob' }),

  listExportHistory: (page = 1, pageSize = 20) =>
    api.get('/api/v1/exports/history', { params: { page, page_size: pageSize } }).then(r => r.data.data),

  deleteExport: (exportId: number) =>
    api.delete(`/api/v1/exports/history/${exportId}`).then(r => r.data.data),

  downloadExport: (exportId: number) =>
    api.get(`/api/v1/exports/${exportId}/download`, { responseType: 'blob' }),
}

export function triggerBlobDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export default documentService
