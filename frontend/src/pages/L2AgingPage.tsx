import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert
} from '@mui/material'
import l2Service from '@/services/l2Service'

export default function L2AgingPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    l2Service.getAging()
      .then(setData)
      .catch(() => setError('Failed to load L2 aging data'))
      .finally(() => setLoading(false))
  }, [])

  const agingColor = (days: number | null) => {
    if (!days) return 'default'
    if (days > 14) return 'error'
    if (days > 7) return 'warning'
    return 'success'
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>L2 Aging Report (Pending)</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate ID</TableCell><TableCell>Name</TableCell>
            <TableCell>L2 Date</TableCell><TableCell>Aging (Days)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((r: any) => (
            <TableRow key={r.l2_select_id}>
              <TableCell>{r.candidate_id}</TableCell>
              <TableCell>{r.candidate_name ?? '—'}</TableCell>
              <TableCell>{r.l2_interview_date ?? '—'}</TableCell>
              <TableCell>
                <Chip
                  label={r.aging_days != null ? `${r.aging_days}d` : '—'}
                  color={agingColor(r.aging_days) as any}
                  size="small"
                />
              </TableCell>
            </TableRow>
          ))}
          {data.length === 0 && (
            <TableRow><TableCell colSpan={4} align="center">No pending L2 interviews</TableCell></TableRow>
          )}
        </TableBody>
      </Table>
    </Box>
  )
}
