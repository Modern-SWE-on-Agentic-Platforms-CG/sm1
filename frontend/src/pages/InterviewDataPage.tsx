import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  CircularProgress, Alert, Pagination, TextField
} from '@mui/material'
import analyticsService from '@/services/analyticsService'

export default function InterviewDataPage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [bu, setBu] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const pageSize = 20

  useEffect(() => {
    setLoading(true)
    analyticsService.getInterviewData(page, pageSize, bu || undefined)
      .then(r => { setItems(r.items ?? []); setTotal(r.total ?? 0) })
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [page, bu])

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Interview Data</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TextField size="small" label="Filter BU" value={bu} onChange={e => { setBu(e.target.value); setPage(1) }} sx={{ mb: 2, width: 240 }} />
      {loading ? <CircularProgress /> : (
        <>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Booking ID</TableCell><TableCell>Candidate ID</TableCell>
                <TableCell>Interview Date</TableCell><TableCell>From</TableCell><TableCell>To</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((b: any) => (
                <TableRow key={b.recruiter_calendar_id}>
                  <TableCell>{b.recruiter_calendar_id}</TableCell>
                  <TableCell>{b.candidate_detail_id}</TableCell>
                  <TableCell>{b.interview_date}</TableCell>
                  <TableCell>{b.interview_from_time}</TableCell>
                  <TableCell>{b.interview_to_time}</TableCell>
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
