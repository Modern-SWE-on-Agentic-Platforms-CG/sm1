import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Tabs, Tab, Table, TableBody, TableCell, TableHead, TableRow,
  Button, TextField, Dialog, DialogTitle, DialogContent, DialogActions,
  CircularProgress, Alert, IconButton
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import AddIcon from '@mui/icons-material/Add'
import adminService from '@/services/adminService'

interface TabPanelProps { children: React.ReactNode; value: number; index: number }
function TabPanel({ children, value, index }: TabPanelProps) {
  return value === index ? <Box sx={{ pt: 2 }}>{children}</Box> : null
}

function SimpleListTab({
  title, items, nameKey, onAdd, onDelete, addLabel
}: {
  title: string; items: any[]; nameKey: string; onAdd: (name: string) => Promise<void>;
  onDelete: (id: number) => Promise<void>; addLabel: string
}) {
  const [newName, setNewName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAdd = async () => {
    if (!newName.trim()) return
    setLoading(true)
    setError(null)
    try {
      await onAdd(newName.trim())
      setNewName('')
    } catch (err: any) {
      setError(err.response?.data?.error || 'Add failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      {error && <Alert severity="error" sx={{ mb: 1 }}>{error}</Alert>}
      <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
        <TextField size="small" label={addLabel} value={newName} onChange={e => setNewName(e.target.value)} />
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleAdd} disabled={loading}>Add</Button>
      </Box>
      <Table size="small">
        <TableHead><TableRow><TableCell>Name</TableCell><TableCell>Action</TableCell></TableRow></TableHead>
        <TableBody>
          {items.map(item => (
            <TableRow key={item.id}>
              <TableCell>{item[nameKey]}</TableCell>
              <TableCell>
                <IconButton size="small" color="error" onClick={() => onDelete(item.id)}>
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  )
}

export default function AdministrationPage() {
  const [tab, setTab] = useState(0)
  const [towers, setTowers] = useState<any[]>([])
  const [skills, setSkills] = useState<any[]>([])
  const [sources, setSources] = useState<any[]>([])
  const [vendors, setVendors] = useState<any[]>([])
  const [approverDL, setApproverDL] = useState<any[]>([])
  const [roleComments, setRoleComments] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const reload = async () => {
    setLoading(true)
    try {
      const [t, s, src, v, dl, rc] = await Promise.all([
        adminService.getTowers(),
        adminService.getSkills(),
        adminService.getSources(),
        adminService.getVendors(),
        adminService.getApproverDL(),
        adminService.getRoleComments(),
      ])
      setTowers(t); setSkills(s); setSources(src); setVendors(v); setApproverDL(dl); setRoleComments(rc)
    } catch {
      setError('Failed to load admin data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { reload() }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Administration</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Tabs value={tab} onChange={(_, v) => setTab(v)} variant="scrollable" scrollButtons="auto">
        <Tab label="Towers" />
        <Tab label="Skills" />
        <Tab label="Sources" />
        <Tab label="Vendors" />
        <Tab label="Approver DL" />
        <Tab label="Role Comments" />
      </Tabs>

      <TabPanel value={tab} index={0}>
        <SimpleListTab
          title="Tower Management" items={towers} nameKey="tower_name"
          addLabel="Tower Name"
          onAdd={async name => { await adminService.createTower(name); await reload() }}
          onDelete={async id => { await adminService.deleteTower(id); await reload() }}
        />
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <SimpleListTab
          title="Skill / Technology Management" items={skills} nameKey="tech_name"
          addLabel="Tech Name"
          onAdd={async name => { await adminService.createSkill({ tech_name: name }); await reload() }}
          onDelete={async id => { await adminService.deleteSkill(id); await reload() }}
        />
      </TabPanel>

      <TabPanel value={tab} index={2}>
        <SimpleListTab
          title="Source Management" items={sources} nameKey="source_name"
          addLabel="Source Name"
          onAdd={async name => { await adminService.createSource(name); await reload() }}
          onDelete={async id => { await adminService.deleteSource(id); await reload() }}
        />
      </TabPanel>

      <TabPanel value={tab} index={3}>
        <SimpleListTab
          title="Vendor Management" items={vendors} nameKey="vendor_name"
          addLabel="Vendor Name"
          onAdd={async name => { await adminService.createVendor({ vendor_name: name }); await reload() }}
          onDelete={async id => { await adminService.deleteVendor(id); await reload() }}
        />
      </TabPanel>

      <TabPanel value={tab} index={4}>
        <Typography variant="h6" gutterBottom>Approver DL</Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>DL Email</TableCell><TableCell>Title</TableCell><TableCell>Level</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {approverDL.map((dl: any) => (
              <TableRow key={dl.id}>
                <TableCell>{dl.dl_email}</TableCell>
                <TableCell>{dl.dl_title || '-'}</TableCell>
                <TableCell>{dl.level}</TableCell>
                <TableCell>
                  <IconButton size="small" color="error" onClick={async () => { await adminService.deleteApproverDL(dl.id); await reload() }}>
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      <TabPanel value={tab} index={5}>
        <Typography variant="h6" gutterBottom>Role Comments</Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Role ID</TableCell><TableCell>Comment</TableCell><TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {roleComments.map((rc: any) => (
              <TableRow key={rc.id}>
                <TableCell>{rc.role_id}</TableCell>
                <TableCell>{rc.comment_text}</TableCell>
                <TableCell>
                  <IconButton size="small" color="error" onClick={async () => { await adminService.deleteRoleComment(rc.id); await reload() }}>
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>
    </Box>
  )
}
