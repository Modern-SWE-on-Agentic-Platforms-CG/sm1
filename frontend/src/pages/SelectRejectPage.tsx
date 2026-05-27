import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, Button, TextField, CircularProgress, Alert, Pagination,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material'
import CheckIcon from '@mui/icons-material/Check'
import CloseIcon from '@mui/icons-material/Close'
import candidateService from '@/services/candidateService'
import { useNavigate } from 'react-router-dom'

export default function SelectRejectPage() {
  const [candidates, setCandidates] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [confirmDialog, setConfirmDialog] = useState<{ candidateId: number; action: 'L1 Selected' | 'L1 Rejected' } | null>(null)
  const navigate = useNavigate()
  const pageSize = 20

  const load = async () => {
    setLoading(true)
    try {
      const res = await candidateService.listCandidates({ page, page_size: pageSize, search, stage: 'L1' })
      setCandidates(res.items ?? [])
      setTotal(res.total ?? 0)
    } catch {
      setError('Failed to load candidates')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [page, search])

  const handleAction = async (candidateId: number, status: string) => {
    await candidateService.updateStatus(candidateId, { status })
    setConfirmDialog(null)
    load()
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>L1 Select / Reject</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TextField
        size="small" label="Search" value={search}
        onChange={e => { setSearch(e.target.value); setPage(1) }}
        sx={{ mb: 2, width: 300 }}
      />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate</TableCell><TableCell>Current Status</TableCell>
            <TableCell>Technology</TableCell><TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {candidates.map((c: any) => (
            <TableRow key={c.candidate_detail_id}>
              <TableCell>
                <Button size="small" onClick={() => navigate(`/candidate-details/${c.candidate_detail_id}`)}>
                  {c.candidate_name || c.candidate_detail_id}
                </Button>
              </TableCell>
              <TableCell><Chip label={c.current_status} size="small" /></TableCell>
              <TableCell>{c.technology || '-'}</TableCell>
              <TableCell>
                <Button
                  size="small" color="success" startIcon={<CheckIcon />}
                  onClick={() => setConfirmDialog({ candidateId: c.candidate_detail_id, action: 'L1 Selected' })}
                  sx={{ mr: 1 }}
                >Select</Button>
                <Button
                  size="small" color="error" startIcon={<CloseIcon />}
                  onClick={() => setConfirmDialog({ candidateId: c.candidate_detail_id, action: 'L1 Rejected' })}
                >Reject</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />

      {confirmDialog && (
        <Dialog open onClose={() => setConfirmDialog(null)}>
          <DialogTitle>Confirm {confirmDialog.action}</DialogTitle>
          <DialogContent>
            <Typography>Are you sure you want to mark this candidate as "{confirmDialog.action}"?</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialog(null)}>Cancel</Button>
            <Button
              variant="contained"
              color={confirmDialog.action === 'L1 Selected' ? 'success' : 'error'}
              onClick={() => handleAction(confirmDialog.candidateId, confirmDialog.action)}
            >Confirm</Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  )
}
