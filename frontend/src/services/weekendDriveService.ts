import api from './api'

const weekendDriveService = {
  listSlots: (params?: { page?: number; page_size?: number }) =>
    api.get('/api/v1/weekend-drive/slots', { params }).then(r => r.data.data),

  importSlots: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/api/v1/weekend-drive/import', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(r => r.data.data)
  },
}

export default weekendDriveService
