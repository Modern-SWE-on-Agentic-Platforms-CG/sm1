import api from './api'

const adminService = {
  // Towers
  getTowers: () => api.get('/api/v1/admin/towers').then(r => r.data.data.items),
  createTower: (name: string) => api.post('/api/v1/admin/towers', { tower_name: name }).then(r => r.data.data),
  deleteTower: (id: number) => api.delete(`/api/v1/admin/towers/${id}`).then(r => r.data.data),

  // Skills
  getSkills: () => api.get('/api/v1/admin/skills').then(r => r.data.data.items),
  createSkill: (body: { tech_name: string; skill_group?: string; tower_id?: number }) =>
    api.post('/api/v1/admin/skills', body).then(r => r.data.data),
  updateSkill: (id: number, body: object) => api.put(`/api/v1/admin/skills/${id}`, body).then(r => r.data.data),
  deleteSkill: (id: number) => api.delete(`/api/v1/admin/skills/${id}`).then(r => r.data.data),

  // Sources
  getSources: () => api.get('/api/v1/admin/sources').then(r => r.data.data.items),
  createSource: (name: string) => api.post('/api/v1/admin/sources', { source_name: name }).then(r => r.data.data),
  deleteSource: (id: number) => api.delete(`/api/v1/admin/sources/${id}`).then(r => r.data.data),

  // Vendors
  getVendors: () => api.get('/api/v1/admin/vendors').then(r => r.data.data.items),
  createVendor: (body: { vendor_name: string; source_id?: number }) =>
    api.post('/api/v1/admin/vendors', body).then(r => r.data.data),
  deleteVendor: (id: number) => api.delete(`/api/v1/admin/vendors/${id}`).then(r => r.data.data),

  // SAP
  getSapCapabilities: () => api.get('/api/v1/admin/sap-capabilities').then(r => r.data.data.items),
  createSapCapability: (name: string) => api.post('/api/v1/admin/sap-capabilities', { capability_name: name }).then(r => r.data.data),
  getSapSkills: () => api.get('/api/v1/admin/sap-skills').then(r => r.data.data.items),
  createSapSkill: (name: string, capabilityId?: number) =>
    api.post('/api/v1/admin/sap-skills', { skill_name: name, capability_id: capabilityId }).then(r => r.data.data),

  // Approver DL
  getApproverDL: () => api.get('/api/v1/admin/approver-dl').then(r => r.data.data.items),
  createApproverDL: (body: { dl_email: string; dl_title?: string; level: string; tower_id?: number }) =>
    api.post('/api/v1/admin/approver-dl', body).then(r => r.data.data),
  deleteApproverDL: (id: number) => api.delete(`/api/v1/admin/approver-dl/${id}`).then(r => r.data.data),

  // Role Comments
  getRoleComments: () => api.get('/api/v1/admin/role-comments').then(r => r.data.data.items),
  createRoleComment: (roleId: number, text: string) =>
    api.post('/api/v1/admin/role-comments', { role_id: roleId, comment_text: text }).then(r => r.data.data),
  deleteRoleComment: (id: number) => api.delete(`/api/v1/admin/role-comments/${id}`).then(r => r.data.data),
}

export default adminService
