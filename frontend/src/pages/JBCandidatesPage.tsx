import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  TablePagination, TextField, CircularProgress, Alert, MenuItem
} from '@mui/material'
import joiningBonusService, { JoiningBonusEntry } from '@/services/joiningBonusService'

export default function JBCandidatesPage() {
  const [items, setItems] = useState<JoiningBonusEntry[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [buFilter, setBuFilter] = useState('')

  const load = (p = 0) => {
    setLoading(true)
    joiningBonusService.listByBU(buFilter || undefined, p + 1, 20)
      .then(data => { setItems(data.items); setTotal(data.total) })
      .catch(() => setError('Failed to load JB candidates'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load(page) }, [page, buFilter])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>JB Candidates (Recruiter View)</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TextField
        label="BU Filter" value={buFilter} onChange={e => { setBuFilter(e.target.value); setPage(0) }}
        size="small" sx={{ mb: 2, minWidth: 200 }}
      />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate</TableCell>
            <TableCell>Bonus Amount</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>DL Email</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map(item => (
            <TableRow key={item.id} hover>
              <TableCell>{item.candidate_name || item.candidate_detail_id}</TableCell>
              <TableCell>{item.bonus_amount != null ? `₹${item.bonus_amount}` : '-'}</TableCell>
              <TableCell>{item.status}</TableCell>
              <TableCell>{item.dl_email || '-'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <TablePagination
        component="div" count={total} page={page}
        onPageChange={(_, p) => setPage(p)} rowsPerPage={20} rowsPerPageOptions={[20]}
      />
    </Box>
  )
}
