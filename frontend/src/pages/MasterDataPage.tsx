import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Tabs, Tab, Table, TableBody, TableCell, TableHead, TableRow,
  CircularProgress, Alert
} from '@mui/material'
import adminService from '@/services/adminService'
import { useAuth } from '@/hooks/useAuth'

interface TabPanelProps { children: React.ReactNode; value: number; index: number }
function TabPanel({ children, value, index }: TabPanelProps) {
  return value === index ? <Box sx={{ pt: 2 }}>{children}</Box> : null
}

/**
 * BUAdmin / PracticeAdmin scoped view of master data.
 * Shows only BU-relevant subset of towers, skills, and sources (read-only).
 */
export default function MasterDataPage() {
  const { employee } = useAuth()
  const [tab, setTab] = useState(0)
  const [towers, setTowers] = useState<any[]>([])
  const [skills, setSkills] = useState<any[]>([])
  const [sources, setSources] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([
      adminService.getTowers(),
      adminService.getSkills(),
      adminService.getSources(),
    ])
      .then(([t, s, src]) => { setTowers(t); setSkills(s); setSources(src) })
      .catch(() => setError('Failed to load master data'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Master Data {employee?.bu ? `— ${employee.bu}` : ''}
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Tabs value={tab} onChange={(_, v) => setTab(v)}>
        <Tab label="Towers" />
        <Tab label="Skills" />
        <Tab label="Sources" />
      </Tabs>

      <TabPanel value={tab} index={0}>
        <Table size="small">
          <TableHead><TableRow><TableCell>Tower Name</TableCell><TableCell>Active</TableCell></TableRow></TableHead>
          <TableBody>
            {towers.map((t: any) => (
              <TableRow key={t.id}><TableCell>{t.tower_name}</TableCell><TableCell>{t.is_active ? 'Yes' : 'No'}</TableCell></TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <Table size="small">
          <TableHead><TableRow><TableCell>Skill</TableCell><TableCell>Group</TableCell><TableCell>Active</TableCell></TableRow></TableHead>
          <TableBody>
            {skills.map((s: any) => (
              <TableRow key={s.id}>
                <TableCell>{s.tech_name}</TableCell>
                <TableCell>{s.skill_group || '-'}</TableCell>
                <TableCell>{s.is_active ? 'Yes' : 'No'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>

      <TabPanel value={tab} index={2}>
        <Table size="small">
          <TableHead><TableRow><TableCell>Source Name</TableCell><TableCell>Active</TableCell></TableRow></TableHead>
          <TableBody>
            {sources.map((s: any) => (
              <TableRow key={s.id}><TableCell>{s.source_name}</TableCell><TableCell>{s.is_active ? 'Yes' : 'No'}</TableCell></TableRow>
            ))}
          </TableBody>
        </Table>
      </TabPanel>
    </Box>
  )
}
