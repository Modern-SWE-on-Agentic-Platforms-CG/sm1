import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert, Pagination, TextField
} from '@mui/material'
import api from '@/services/api'

export default function CandidateApprovalDataPage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [bu, setBu] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const pageSize = 20

  useEffect(() => {
    setLoading(true)
    api.get('/api/v1/reports/offer-approve-candidates', { params: { page, page_size: pageSize, bu: bu || undefined } })
      .then(r => { setItems(r.data.data.items); setTotal(r.data.data.total) })
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [page, bu])

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Offer Approved Candidates</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TextField size="small" label="Filter by BU" value={bu} onChange={e => { setBu(e.target.value); setPage(1) }} sx={{ mb: 2, width: 240 }} />
      {loading ? <CircularProgress /> : (
        <>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell><TableCell>Name</TableCell><TableCell>BU</TableCell>
                <TableCell>Status</TableCell><TableCell>Technology</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((c: any) => (
                <TableRow key={c.candidate_detail_id}>
                  <TableCell>{c.candidate_detail_id}</TableCell>
                  <TableCell>{c.candidate_name}</TableCell>
                  <TableCell>{c.business_unit}</TableCell>
                  <TableCell><Chip label={c.current_status} size="small" color="success" /></TableCell>
                  <TableCell>{c.technology}</TableCell>
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
