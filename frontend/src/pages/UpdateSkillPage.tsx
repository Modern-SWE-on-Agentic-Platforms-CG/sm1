import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Table, TableBody, TableCell, TableHead, TableRow,
  Button, TextField, CircularProgress, Alert, Pagination,
  Dialog, DialogTitle, DialogContent, DialogActions, Autocomplete
} from '@mui/material'
import candidateService from '@/services/candidateService'
import adminService from '@/services/adminService'

export default function UpdateSkillPage() {
  const [candidates, setCandidates] = useState<any[]>([])
  const [skills, setSkills] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [editDialog, setEditDialog] = useState<{ candidateId: number; name: string; skill: string } | null>(null)
  const [newSkill, setNewSkill] = useState<string>('')
  const [saving, setSaving] = useState(false)
  const pageSize = 20

  const load = async () => {
    setLoading(true)
    try {
      const [res, skillList] = await Promise.all([
        candidateService.listCandidates({ page, page_size: pageSize, search }),
        adminService.getSkills(),
      ])
      setCandidates(res.items ?? [])
      setTotal(res.total ?? 0)
      setSkills(skillList)
    } catch {
      setError('Failed to load')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [page, search])

  const handleSave = async () => {
    if (!editDialog) return
    setSaving(true)
    try {
      await candidateService.updateCandidate(editDialog.candidateId, { technology: newSkill })
      setEditDialog(null)
      load()
    } catch {
      setError('Failed to update skill')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  const skillOptions = skills.map((s: any) => s.tech_name)

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Update Skill / Technology</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TextField
        size="small" label="Search" value={search}
        onChange={e => { setSearch(e.target.value); setPage(1) }}
        sx={{ mb: 2, width: 300 }}
      />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Candidate</TableCell><TableCell>Current Skill</TableCell><TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {candidates.map((c: any) => (
            <TableRow key={c.candidate_detail_id}>
              <TableCell>{c.candidate_name || c.candidate_detail_id}</TableCell>
              <TableCell>{c.technology || '—'}</TableCell>
              <TableCell>
                <Button
                  size="small" variant="outlined"
                  onClick={() => {
                    setNewSkill(c.technology || '')
                    setEditDialog({ candidateId: c.candidate_detail_id, name: c.candidate_name, skill: c.technology || '' })
                  }}
                >Update</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Pagination count={Math.ceil(total / pageSize)} page={page} onChange={(_, p) => setPage(p)} sx={{ mt: 2 }} />

      {editDialog && (
        <Dialog open onClose={() => setEditDialog(null)} fullWidth maxWidth="xs">
          <DialogTitle>Update Skill — {editDialog.name}</DialogTitle>
          <DialogContent sx={{ pt: 2 }}>
            <Autocomplete
              freeSolo
              options={skillOptions}
              value={newSkill}
              onChange={(_, val) => setNewSkill(val ?? '')}
              onInputChange={(_, val) => setNewSkill(val)}
              renderInput={params => <TextField {...params} label="Skill / Technology" fullWidth />}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditDialog(null)}>Cancel</Button>
            <Button variant="contained" onClick={handleSave} disabled={!newSkill || saving}>
              {saving ? 'Saving...' : 'Save'}
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  )
}
