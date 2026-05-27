import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  CircularProgress, Alert, Button, Dialog, DialogTitle, DialogContent,
  DialogActions, Select, MenuItem, FormControl, InputLabel
} from '@mui/material'
import api from '@/services/api'

export default function ChangeRolesPage() {
  const [employees, setEmployees] = useState<any[]>([])
  const [roles, setRoles] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editDialog, setEditDialog] = useState<{ empId: number; name: string; currentRole: string } | null>(null)
  const [newRole, setNewRole] = useState('')
  const [saving, setSaving] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const [empRes, roleRes] = await Promise.all([
        api.get('/api/v1/employees').then(r => r.data.data.items ?? r.data.data),
        api.get('/api/v1/employees/roles').then(r => r.data.data).catch(() => []),
      ])
      setEmployees(Array.isArray(empRes) ? empRes : empRes.items ?? [])
      setRoles(Array.isArray(roleRes) ? roleRes.map((r: any) => r.role_name ?? r) : [])
    } catch {
      setError('Failed to load employees')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSave = async () => {
    if (!editDialog || !newRole) return
    setSaving(true)
    try {
      await api.patch(`/api/v1/employees/${editDialog.empId}/role`, { role: newRole })
      setEditDialog(null)
      load()
    } catch {
      setError('Role change failed')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Change Employee Roles</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Employee ID</TableCell><TableCell>Name</TableCell>
            <TableCell>Email</TableCell><TableCell>Current Role</TableCell><TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {employees.map((e: any) => (
            <TableRow key={e.employee_id ?? e.emp_id}>
              <TableCell>{e.employee_id ?? e.emp_id}</TableCell>
              <TableCell>{e.employee_name ?? e.name}</TableCell>
              <TableCell>{e.email_id ?? e.email}</TableCell>
              <TableCell>{e.role ?? e.current_role ?? '—'}</TableCell>
              <TableCell>
                <Button size="small" variant="outlined"
                  onClick={() => {
                    setNewRole(e.role ?? '')
                    setEditDialog({ empId: e.employee_id ?? e.emp_id, name: e.employee_name ?? e.name, currentRole: e.role ?? '' })
                  }}>
                  Change Role
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {editDialog && (
        <Dialog open onClose={() => setEditDialog(null)} fullWidth maxWidth="xs">
          <DialogTitle>Change Role — {editDialog.name}</DialogTitle>
          <DialogContent sx={{ pt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>New Role</InputLabel>
              <Select value={newRole} onChange={e => setNewRole(e.target.value)} label="New Role">
                {roles.map(r => <MenuItem key={r} value={r}>{r}</MenuItem>)}
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditDialog(null)}>Cancel</Button>
            <Button variant="contained" onClick={handleSave} disabled={!newRole || saving}>
              {saving ? 'Saving…' : 'Save'}
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  )
}
