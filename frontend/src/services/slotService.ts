import apiClient from './api'

export interface SlotCreate {
  skill_id?: number
  slot_date: string
  from_time: string
  to_time: string
  is_weekend_drive?: boolean
}

export async function createSlot(data: SlotCreate) {
  const resp = await apiClient.post('/api/v1/slots', data)
  return resp.data.data
}

export async function listSlots(status?: string, isWeekendDrive?: boolean) {
  const resp = await apiClient.get('/api/v1/slots', {
    params: { status, is_weekend_drive: isWeekendDrive },
  })
  return resp.data.data
}

export async function bulkUploadSlots(file: File) {
  const form = new FormData()
  form.append('file', file)
  const resp = await apiClient.post('/api/v1/slots/bulk', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resp.data.data
}

export async function updateSlotStatus(slotId: number, newStatus: string) {
  const resp = await apiClient.put(`/api/v1/slots/${slotId}`, null, {
    params: { new_status: newStatus },
  })
  return resp.data.data
}

export async function deleteSlot(slotId: number) {
  await apiClient.delete(`/api/v1/slots/${slotId}`)
}
