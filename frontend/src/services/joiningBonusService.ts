import api from './api'

export interface JoiningBonusEntry {
  id: number
  candidate_detail_id: number
  candidate_name: string | null
  bonus_amount: number | null
  status: string
  dl_email: string | null
  updated_by?: string | null
  updated_at?: string
}

const joiningBonusService = {
  list: async (status?: string, page = 1, pageSize = 20) => {
    const response = await api.get('/api/v1/joining-bonus', {
      params: { status, page, page_size: pageSize },
    })
    return response.data.data
  },

  listByBU: async (bu?: string, page = 1, pageSize = 20) => {
    const response = await api.get('/api/v1/joining-bonus/bu', {
      params: { bu, page, page_size: pageSize },
    })
    return response.data.data
  },

  update: async (id: number, status: string, dlEmail?: string) => {
    const response = await api.put(`/api/v1/joining-bonus/${id}`, { status, dl_email: dlEmail })
    return response.data.data
  },

  getDLOptions: async () => {
    const response = await api.get('/api/v1/joining-bonus/dl-options')
    return response.data.data.items
  },
}

export default joiningBonusService
