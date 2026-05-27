import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  CircularProgress, Alert, Chip
} from '@mui/material'
import analyticsService from '@/services/analyticsService'

export default function ArcDeviationPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    analyticsService.getArcDeviations(15)
      .then(setData)
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>ARC Deviation Report (≥15%)</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate ID</TableCell><TableCell>Name</TableCell>
            <TableCell>CTC Offered</TableCell><TableCell>CTC ARC</TableCell>
            <TableCell>Deviation</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((r: any) => (
            <TableRow key={r.candidate_id}>
              <TableCell>{r.candidate_id}</TableCell>
              <TableCell>{r.candidate_name ?? '—'}</TableCell>
              <TableCell>{r.ctc_offered}</TableCell>
              <TableCell>{r.ctc_arc}</TableCell>
              <TableCell>
                <Chip
                  label={`${r.deviation_pct}%`}
                  color={r.deviation_pct > 25 ? 'error' : 'warning'}
                  size="small"
                />
              </TableCell>
            </TableRow>
          ))}
          {data.length === 0 && (
            <TableRow><TableCell colSpan={5} align="center">No deviations found</TableCell></TableRow>
          )}
        </TableBody>
      </Table>
    </Box>
  )
}
