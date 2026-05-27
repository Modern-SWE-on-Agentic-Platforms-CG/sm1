import apiClient from './api'

export interface BookingCreate {
  candidate_detail_id: number
  interviewer_calendar_id: number
}

export interface DirectBookingCreate {
  candidate_detail_id: number
  interview_date: string
  from_time: string
  to_time: string
  panel_email?: string
  skill_id?: number
}

export async function getAvailableSlots(skillId?: number, interviewDate?: string) {
  const resp = await apiClient.get('/api/v1/bookings/available-slots', {
    params: { skill_id: skillId, interview_date: interviewDate },
  })
  return resp.data.data
}

export async function bookSlot(data: BookingCreate) {
  const resp = await apiClient.post('/api/v1/bookings', data)
  return resp.data.data
}

export async function directBook(data: DirectBookingCreate) {
  const resp = await apiClient.post('/api/v1/bookings/direct', data)
  return resp.data.data
}

export async function rescheduleBooking(bookingId: number, data: object) {
  const resp = await apiClient.put(`/api/v1/bookings/${bookingId}/reschedule`, data)
  return resp.data.data
}

export async function cancelBooking(bookingId: number) {
  await apiClient.delete(`/api/v1/bookings/${bookingId}`)
}

export async function getTodoList() {
  const resp = await apiClient.get('/api/v1/bookings/todo')
  return resp.data.data
}

export async function getWeeklyView() {
  const resp = await apiClient.get('/api/v1/bookings/weekly')
  return resp.data.data
}

export async function getPendingFeedback() {
  const resp = await apiClient.get('/api/v1/bookings/pending-feedback')
  return resp.data.data
}
