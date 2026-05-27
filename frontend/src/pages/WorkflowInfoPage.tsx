import React, { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  Box, Typography, CircularProgress, Alert, Divider, Chip,
  Table, TableBody, TableCell, TableHead, TableRow, Paper
} from '@mui/material'
import workflowService, { WorkflowComment, CTCHistoryEntry } from '@/services/workflowService'

export default function WorkflowInfoPage() {
  const [searchParams] = useSearchParams()
  const workflowId = Number(searchParams.get('workflowId'))
  const candidateId = Number(searchParams.get('candidateId'))

  const [comments, setComments] = useState<WorkflowComment[]>([])
  const [ctcHistory, setCtcHistory] = useState<CTCHistoryEntry[]>([])
  const [threshold, setThreshold] = useState<{ arc_threshold_percent: number } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!workflowId || !candidateId) return
    Promise.all([
      workflowService.getComments(workflowId),
      workflowService.getCTCHistory(candidateId),
      workflowService.getThreshold(),
    ])
      .then(([cmts, ctc, thr]) => {
        setComments(cmts)
        setCtcHistory(ctc)
        setThreshold(thr)
      })
      .catch(() => setError('Failed to load workflow details'))
      .finally(() => setLoading(false))
  }, [workflowId, candidateId])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Workflow Details</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {threshold && (
        <Alert severity="info" sx={{ mb: 2 }}>
          ARC Threshold: {threshold.arc_threshold_percent}% deviation triggers ARC flag
        </Alert>
      )}

      <Typography variant="h6" gutterBottom>CTC History</Typography>
      <Paper sx={{ mb: 3 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>CTC Value</TableCell>
              <TableCell>Changed By</TableCell>
              <TableCell>Changed At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ctcHistory.length === 0 ? (
              <TableRow><TableCell colSpan={3}>No CTC history</TableCell></TableRow>
            ) : ctcHistory.map(entry => (
              <TableRow key={entry.id}>
                <TableCell>{entry.ctc_value}</TableCell>
                <TableCell>{entry.changed_by || '-'}</TableCell>
                <TableCell>{new Date(entry.changed_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      <Typography variant="h6" gutterBottom>Comments & Actions History</Typography>
      <Paper>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>By</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Comment</TableCell>
              <TableCell>At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {comments.length === 0 ? (
              <TableRow><TableCell colSpan={4}>No comments yet</TableCell></TableRow>
            ) : comments.map(c => (
              <TableRow key={c.id}>
                <TableCell>{c.commenter_email}</TableCell>
                <TableCell>
                  <Chip
                    label={c.action}
                    color={c.action === 'Approved' ? 'success' : c.action === 'Rejected' ? 'error' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{c.comment_text || '-'}</TableCell>
                <TableCell>{new Date(c.created_at).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  )
}
