import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert, Pagination, TextField
} from '@mui/material'
import api from '@/services/api'

export default function FeedbackFormReportPage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [bu, setBu] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const pageSize = 20

  useEffect(() => {
    setLoading(true)
    api.get('/api/v1/reports/feedback-form-report', { params: { page, page_size: pageSize, bu: bu || undefined } })
      .then(r => { setItems(r.data.data.items); setTotal(r.data.data.total) })
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [page, bu])

  const recColor = (rec: string | null) =>
    rec === 'Strongly Recommend' ? 'success' :
    rec === 'Recommend' ? 'primary' :
    rec === 'Not Recommend' ? 'error' : 'default'

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Feedback Form Report</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TextField size="small" label="Filter by BU" value={bu} onChange={e => { setBu(e.target.value); setPage(1) }} sx={{ mb: 2, width: 240 }} />
      {loading ? <CircularProgress /> : (
        <>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Booking ID</TableCell><TableCell>Candidate</TableCell>
                <TableCell>Technology</TableCell><TableCell>Interview Date</TableCell>
                <TableCell>Recommendation</TableCell><TableCell>Score</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((r: any) => (
                <TableRow key={r.booking_id}>
                  <TableCell>{r.booking_id}</TableCell>
                  <TableCell>{r.candidate_name}</TableCell>
                  <TableCell>{r.technology}</TableCell>
                  <TableCell>{r.interview_date}</TableCell>
                  <TableCell>
                    {r.recommendation
                      ? <Chip label={r.recommendation} size="small" color={recColor(r.recommendation) as any} />
                      : <Chip label="Pending" size="small" />}
                  </TableCell>
                  <TableCell>{r.overall_score ?? '—'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />
        </>
      )}
    </Box>
  )
}
