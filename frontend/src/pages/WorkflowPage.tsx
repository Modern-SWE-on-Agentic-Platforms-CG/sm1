import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box, Typography, Button, Chip, CircularProgress, Alert,
  Dialog, DialogTitle, DialogContent, DialogActions, TextField, MenuItem,
  Table, TableBody, TableCell, TableHead, TableRow, TablePagination
} from '@mui/material'
import workflowService, { WorkflowCandidate } from '@/services/workflowService'

export default function WorkflowPage() {
  const navigate = useNavigate()
  const [candidates, setCandidates] = useState<WorkflowCandidate[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [rowsPerPage] = useState(20)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [actionDialog, setActionDialog] = useState<{ open: boolean; workflowId: number | null }>({
    open: false, workflowId: null
  })
  const [actionType, setActionType] = useState('Approved')
  const [actionComment, setActionComment] = useState('')
  const [actionLoading, setActionLoading] = useState(false)

  const load = (p = 0) => {
    setLoading(true)
    workflowService.getCandidates(p + 1, rowsPerPage)
      .then(data => { setCandidates(data.items); setTotal(data.total) })
      .catch(() => setError('Failed to load workflow candidates'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load(page) }, [page])

  const openAction = (workflowId: number) => {
    setActionDialog({ open: true, workflowId })
    setActionType('Approved')
    setActionComment('')
  }

  const submitAction = async () => {
    if (!actionDialog.workflowId) return
    setActionLoading(true)
    try {
      await workflowService.action(actionDialog.workflowId, actionType, actionComment || undefined)
      setActionDialog({ open: false, workflowId: null })
      load(page)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Action failed')
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Offer Approval Workflow</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate</TableCell>
            <TableCell>Current CTC</TableCell>
            <TableCell>Offer CTC</TableCell>
            <TableCell>Level</TableCell>
            <TableCell>ARC</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {candidates.map(c => (
            <TableRow key={c.workflow_id} hover>
              <TableCell>
                <Button variant="text" size="small" onClick={() => navigate(`/work-flow-info?workflowId=${c.workflow_id}&candidateId=${c.candidate_detail_id}`)}>
                  {c.candidate_name}
                </Button>
              </TableCell>
              <TableCell>{c.current_ctc || '-'}</TableCell>
              <TableCell>{c.offer_ctc || '-'}</TableCell>
              <TableCell>{c.current_level}</TableCell>
              <TableCell>
                {c.arc_deviation && <Chip label="ARC Deviation" color="warning" size="small" />}
              </TableCell>
              <TableCell>
                <Button size="small" variant="outlined" onClick={() => openAction(c.workflow_id)}>
                  Act
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={(_, p) => setPage(p)}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[20]}
      />

      <Dialog open={actionDialog.open} onClose={() => setActionDialog({ open: false, workflowId: null })} maxWidth="xs" fullWidth>
        <DialogTitle>Workflow Action</DialogTitle>
        <DialogContent>
          <TextField
            select fullWidth label="Action" value={actionType}
            onChange={e => setActionType(e.target.value)} sx={{ mt: 1, mb: 2 }}
          >
            <MenuItem value="Approved">Approve</MenuItem>
            <MenuItem value="Rejected">Reject</MenuItem>
            <MenuItem value="Comment">Comment Only</MenuItem>
          </TextField>
          <TextField
            fullWidth multiline rows={3} label="Comment (optional)"
            value={actionComment} onChange={e => setActionComment(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setActionDialog({ open: false, workflowId: null })}>Cancel</Button>
          <Button onClick={submitAction} variant="contained" disabled={actionLoading}>
            {actionLoading ? 'Saving…' : 'Submit'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
