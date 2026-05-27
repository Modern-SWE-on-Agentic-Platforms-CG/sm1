import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert, Pagination, Button, TextField,
  Dialog, DialogTitle, DialogContent, DialogActions, Select, MenuItem,
  FormControl, InputLabel
} from '@mui/material'
import l2Service from '@/services/l2Service'

const STATUS_OPTIONS = ['Pending', 'L2 Completed', 'L2 Selected', 'L2 Rejected', 'L2 No Show']

export default function L2ReportPage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editDialog, setEditDialog] = useState<any | null>(null)
  const [form, setForm] = useState({ l2_status: '', l2_feedback: '', l2_recommendation: '' })
  const [saving, setSaving] = useState(false)
  const pageSize = 20

  const load = () => {
    setLoading(true)
    l2Service.listCandidates({ page, page_size: pageSize })
      .then(r => { setItems(r.items ?? []); setTotal(r.total ?? 0) })
      .catch(() => setError('Failed to load L2 data'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [page])

  const handleSave = async () => {
    if (!editDialog) return
    setSaving(true)
    try {
      await l2Service.upsert(editDialog.candidate_detail_id, form)
      setEditDialog(null)
      load()
    } catch {
      setError('Save failed')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>L2 Report</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate ID</TableCell><TableCell>Interview Date</TableCell>
            <TableCell>Status</TableCell><TableCell>Recommendation</TableCell><TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map((r: any) => (
            <TableRow key={r.l2_select_id}>
              <TableCell>{r.candidate_detail_id}</TableCell>
              <TableCell>{r.l2_interview_date ?? '—'}</TableCell>
              <TableCell><Chip label={r.l2_status ?? 'Pending'} size="small" /></TableCell>
              <TableCell>{r.l2_recommendation ?? '—'}</TableCell>
              <TableCell>
                <Button size="small" onClick={() => {
                  setForm({ l2_status: r.l2_status ?? '', l2_feedback: r.l2_feedback ?? '', l2_recommendation: r.l2_recommendation ?? '' })
                  setEditDialog(r)
                }}>Edit</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />

      {editDialog && (
        <Dialog open onClose={() => setEditDialog(null)} fullWidth maxWidth="sm">
          <DialogTitle>Update L2 Record — Candidate {editDialog.candidate_detail_id}</DialogTitle>
          <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
            <FormControl size="small" fullWidth>
              <InputLabel>Status</InputLabel>
              <Select label="Status" value={form.l2_status} onChange={e => setForm(f => ({ ...f, l2_status: e.target.value }))}>
                {STATUS_OPTIONS.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
              </Select>
            </FormControl>
            <TextField label="Recommendation" size="small" fullWidth value={form.l2_recommendation}
              onChange={e => setForm(f => ({ ...f, l2_recommendation: e.target.value }))} />
            <TextField label="Feedback" multiline rows={3} size="small" fullWidth value={form.l2_feedback}
              onChange={e => setForm(f => ({ ...f, l2_feedback: e.target.value }))} />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditDialog(null)}>Cancel</Button>
            <Button variant="contained" onClick={handleSave} disabled={saving}>{saving ? 'Saving…' : 'Save'}</Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  )
}
