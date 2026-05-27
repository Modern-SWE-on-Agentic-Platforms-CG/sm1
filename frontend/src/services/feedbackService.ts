import api from './api'

export interface FeedbackParameter {
  id: number
  parameter_name: string
  max_score: number
  param_order: number
}

export interface FeedbackSection {
  section_name: string
  parameters: FeedbackParameter[]
}

export interface FeedbackTemplate {
  template_id: number
  form_title: string
  tech_name: string
  sections: FeedbackSection[]
}

export interface FeedbackSubmitRequest {
  parameter_scores: Record<string, number>
  overall_rating: 'Select' | 'Hold' | 'Reject'
  overall_remarks?: string
  is_revisit?: boolean
}

export interface FeedbackResult {
  feedback_id: number
  pdf_path: string | null
  overall_rating: string
}

const feedbackService = {
  getTemplate: async (bookingId: number): Promise<FeedbackTemplate> => {
    const response = await api.get(`/api/v1/feedback/template/${bookingId}`)
    return response.data.data
  },

  submit: async (bookingId: number, data: FeedbackSubmitRequest): Promise<FeedbackResult> => {
    const response = await api.post(`/api/v1/feedback/${bookingId}`, data)
    return response.data.data
  },

  downloadPdf: async (bookingId: number): Promise<Blob> => {
    const response = await api.get(`/api/v1/feedback/${bookingId}/pdf`, {
      responseType: 'blob',
    })
    return response.data
  },

  listTemplates: async () => {
    const response = await api.get('/api/v1/feedback/templates')
    return response.data.data
  },
}

export default feedbackService
