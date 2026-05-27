import api from './api'

export interface WorkflowCandidate {
  workflow_id: number
  candidate_detail_id: number
  candidate_name: string
  skill: string | null
  current_ctc: string | null
  exp_ctc: string | null
  offer_ctc: string | null
  current_level: string
  status: string
  arc_deviation: boolean
}

export interface WorkflowComment {
  id: number
  commenter_email: string
  comment_text: string | null
  action: string
  created_at: string
}

export interface CTCHistoryEntry {
  id: number
  ctc_value: string
  changed_by: string | null
  changed_at: string
}

const workflowService = {
  getCandidates: async (page = 1, pageSize = 20) => {
    const response = await api.get('/api/v1/workflow/candidates', {
      params: { page, page_size: pageSize },
    })
    return response.data.data
  },

  action: async (workflowId: number, action: string, comment?: string) => {
    const response = await api.post(`/api/v1/workflow/${workflowId}/action`, { action, comment })
    return response.data.data
  },

  getComments: async (workflowId: number): Promise<WorkflowComment[]> => {
    const response = await api.get(`/api/v1/workflow/${workflowId}/comments`)
    return response.data.data.items
  },

  getCTCHistory: async (candidateId: number): Promise<CTCHistoryEntry[]> => {
    const response = await api.get(`/api/v1/workflow/ctc-history/${candidateId}`)
    return response.data.data.items
  },

  getThreshold: async () => {
    const response = await api.get('/api/v1/workflow/threshold')
    return response.data.data
  },

  getApproverDL: async () => {
    const response = await api.get('/api/v1/workflow/approver-dl')
    return response.data.data.items
  },
}

export default workflowService
