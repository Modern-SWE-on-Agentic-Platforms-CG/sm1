import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Chip, CircularProgress, Alert, Pagination, Button, TextField,
  Select, MenuItem, FormControl, InputLabel
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import referralService from '@/services/referralService'

const STATUS_OPTIONS = ['New', 'Screening', 'Interview', 'Selected', 'Rejected', 'On Hold']

export default function CandidateReferralPage() {
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [bu, setBu] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const pageSize = 20

  const load = () => {
    setLoading(true)
    referralService.listCandidates({ page, page_size: pageSize, bu: bu || undefined })
      .then(r => { setItems(r.items ?? []); setTotal(r.total ?? 0) })
      .catch(() => setError('Failed to load referrals'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [page, bu])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Referral Candidates</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <TextField size="small" label="Filter BU" value={bu} onChange={e => { setBu(e.target.value); setPage(1) }} sx={{ mb: 2, width: 200, mr: 2 }} />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell><TableCell>Name</TableCell><TableCell>Email</TableCell>
            <TableCell>BU</TableCell><TableCell>Account</TableCell><TableCell>Status</TableCell><TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map((c: any) => (
            <TableRow key={c.referral_candidate_id}>
              <TableCell>{c.referral_candidate_id}</TableCell>
              <TableCell>
                <Button size="small" onClick={() => navigate(`/referral-details/${c.referral_candidate_id}`)}>
                  {c.candidate_name}
                </Button>
              </TableCell>
              <TableCell>{c.email}</TableCell>
              <TableCell>{c.bu ?? '—'}</TableCell>
              <TableCell>{c.account ?? '—'}</TableCell>
              <TableCell>
                <Chip label={c.status ?? 'New'} size="small"
                  color={c.status === 'Selected' ? 'success' : c.status === 'Rejected' ? 'error' : 'default'} />
              </TableCell>
              <TableCell>
                <FormControl size="small" sx={{ minWidth: 140 }}>
                  <Select displayEmpty defaultValue="" onChange={async e => {
                    if (e.target.value) {
                      await referralService.updateStatus(c.referral_candidate_id, e.target.value as string)
                      load()
                    }
                  }}>
                    <MenuItem value=""><em>Update status…</em></MenuItem>
                    {STATUS_OPTIONS.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                  </Select>
                </FormControl>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />
    </Box>
  )
}
