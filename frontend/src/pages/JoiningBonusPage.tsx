import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  TablePagination, MenuItem, TextField, CircularProgress, Alert, Button,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material'
import joiningBonusService, { JoiningBonusEntry } from '@/services/joiningBonusService'

export default function JoiningBonusPage() {
  const [items, setItems] = useState<JoiningBonusEntry[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [statusFilter, setStatusFilter] = useState('')
  const [dlOptions, setDlOptions] = useState<any[]>([])
  const [editDialog, setEditDialog] = useState<{ open: boolean; entry: JoiningBonusEntry | null }>({ open: false, entry: null })
  const [newStatus, setNewStatus] = useState('')
  const [newDL, setNewDL] = useState('')

  const load = (p = 0) => {
    setLoading(true)
    joiningBonusService.list(statusFilter || undefined, p + 1, 20)
      .then(data => { setItems(data.items); setTotal(data.total) })
      .catch(() => setError('Failed to load JB data'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load(page)
    joiningBonusService.getDLOptions().then(setDlOptions).catch(() => {})
  }, [page, statusFilter])

  const openEdit = (entry: JoiningBonusEntry) => {
    setEditDialog({ open: true, entry })
    setNewStatus(entry.status)
    setNewDL(entry.dl_email || '')
  }

  const saveEdit = async () => {
    if (!editDialog.entry) return
    try {
      await joiningBonusService.update(editDialog.entry.id, newStatus, newDL || undefined)
      setEditDialog({ open: false, entry: null })
      load(page)
    } catch {
      setError('Update failed')
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Joining Bonus Management</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <TextField
        select label="Filter by Status" value={statusFilter}
        onChange={e => { setStatusFilter(e.target.value); setPage(0) }}
        size="small" sx={{ mb: 2, minWidth: 180 }}
      >
        <MenuItem value="">All</MenuItem>
        {['Pending', 'Approved', 'Paid', 'Cancelled'].map(s => (
          <MenuItem key={s} value={s}>{s}</MenuItem>
        ))}
      </TextField>

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate</TableCell>
            <TableCell>Bonus Amount</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>DL Email</TableCell>
            <TableCell>Updated By</TableCell>
            <TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map(item => (
            <TableRow key={item.id} hover>
              <TableCell>{item.candidate_name || item.candidate_detail_id}</TableCell>
              <TableCell>{item.bonus_amount != null ? `₹${item.bonus_amount}` : '-'}</TableCell>
              <TableCell>{item.status}</TableCell>
              <TableCell>{item.dl_email || '-'}</TableCell>
              <TableCell>{item.updated_by || '-'}</TableCell>
              <TableCell>
                <Button size="small" onClick={() => openEdit(item)}>Edit</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <TablePagination
        component="div" count={total} page={page}
        onPageChange={(_, p) => setPage(p)} rowsPerPage={20} rowsPerPageOptions={[20]}
      />

      <Dialog open={editDialog.open} onClose={() => setEditDialog({ open: false, entry: null })} maxWidth="xs" fullWidth>
        <DialogTitle>Update Joining Bonus</DialogTitle>
        <DialogContent>
          <TextField select fullWidth label="Status" value={newStatus}
            onChange={e => setNewStatus(e.target.value)} sx={{ mt: 1, mb: 2 }}>
            {['Pending', 'Approved', 'Paid', 'Cancelled'].map(s => (
              <MenuItem key={s} value={s}>{s}</MenuItem>
            ))}
          </TextField>
          <TextField select fullWidth label="DL Email" value={newDL}
            onChange={e => setNewDL(e.target.value)}>
            <MenuItem value="">None</MenuItem>
            {dlOptions.map((dl: any) => (
              <MenuItem key={dl.id} value={dl.dl_email}>{dl.dl_title || dl.dl_email}</MenuItem>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialog({ open: false, entry: null })}>Cancel</Button>
          <Button onClick={saveEdit} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
