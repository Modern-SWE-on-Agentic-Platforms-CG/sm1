import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, Button, TextField, CircularProgress, Alert, Pagination,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import candidateService from '@/services/candidateService'

export default function DateOfJoiningPage() {
  const [candidates, setCandidates] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [editDialog, setEditDialog] = useState<{ candidateId: number; name: string; currentDoj: Date | null } | null>(null)
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)
  const [saving, setSaving] = useState(false)
  const pageSize = 20

  const load = async () => {
    setLoading(true)
    try {
      const res = await candidateService.listCandidates({ page, page_size: pageSize, stage: 'Offer_Accepted' })
      setCandidates(res.items ?? [])
      setTotal(res.total ?? 0)
    } catch {
      setError('Failed to load candidates')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [page])

  const handleSave = async () => {
    if (!editDialog || !selectedDate) return
    setSaving(true)
    try {
      await candidateService.updateCandidate(editDialog.candidateId, {
        date_of_joining: selectedDate.toISOString().split('T')[0]
      })
      setEditDialog(null)
      load()
    } catch {
      setError('Failed to update DOJ')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Date of Joining</Typography>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Candidate</TableCell><TableCell>Status</TableCell>
              <TableCell>DOJ</TableCell><TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {candidates.map((c: any) => (
              <TableRow key={c.candidate_detail_id}>
                <TableCell>{c.candidate_name || c.candidate_detail_id}</TableCell>
                <TableCell><Chip label={c.current_status} size="small" /></TableCell>
                <TableCell>{c.date_of_joining ?? '—'}</TableCell>
                <TableCell>
                  <Button
                    size="small" variant="outlined"
                    onClick={() => {
                      setSelectedDate(c.date_of_joining ? new Date(c.date_of_joining) : null)
                      setEditDialog({ candidateId: c.candidate_detail_id, name: c.candidate_name, currentDoj: c.date_of_joining ? new Date(c.date_of_joining) : null })
                    }}
                  >Set DOJ</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />

        {editDialog && (
          <Dialog open onClose={() => setEditDialog(null)}>
            <DialogTitle>Set Date of Joining — {editDialog.name}</DialogTitle>
            <DialogContent sx={{ pt: 2 }}>
              <DatePicker
                label="Date of Joining"
                value={selectedDate}
                onChange={setSelectedDate}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setEditDialog(null)}>Cancel</Button>
              <Button variant="contained" onClick={handleSave} disabled={!selectedDate || saving}>
                {saving ? 'Saving...' : 'Save'}
              </Button>
            </DialogActions>
          </Dialog>
        )}
      </Box>
    </LocalizationProvider>
  )
}
