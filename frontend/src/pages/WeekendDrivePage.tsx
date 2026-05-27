import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert, Pagination, Button
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import weekendDriveService from '@/services/weekendDriveService'

export default function WeekendDrivePage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const pageSize = 20

  useEffect(() => {
    setLoading(true)
    weekendDriveService.listSlots({ page, page_size: pageSize })
      .then(r => { setItems(r.items ?? []); setTotal(r.total ?? 0) })
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [page])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Weekend Drive Slots</Typography>
        <Button variant="contained" onClick={() => navigate('/import-weekend-drive')}>
          Import Slots
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Slot ID</TableCell><TableCell>Date</TableCell>
            <TableCell>From</TableCell><TableCell>To</TableCell>
            <TableCell>Emp ID</TableCell><TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map((s: any) => (
            <TableRow key={s.interviewer_calendar_id}>
              <TableCell>{s.interviewer_calendar_id}</TableCell>
              <TableCell>{s.slot_date}</TableCell>
              <TableCell>{s.from_time ? new Date(s.from_time).toLocaleTimeString() : '—'}</TableCell>
              <TableCell>{s.to_time ? new Date(s.to_time).toLocaleTimeString() : '—'}</TableCell>
              <TableCell>{s.emp_id}</TableCell>
              <TableCell><Chip label={s.slot_status} size="small" /></TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />
    </Box>
  )
}
