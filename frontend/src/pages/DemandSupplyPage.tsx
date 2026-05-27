import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Grid, Paper, Tabs, Tab, Table, TableBody, TableCell,
  TableHead, TableRow, CircularProgress, Alert, Pagination, Chip
} from '@mui/material'
import supplyService from '@/services/supplyService'

interface TabPanelProps { children: React.ReactNode; value: number; index: number }
function TabPanel({ children, value, index }: TabPanelProps) {
  return value === index ? <Box sx={{ pt: 2 }}>{children}</Box> : null
}

export default function DemandSupplyPage() {
  const [tab, setTab] = useState(0)
  const [summary, setSummary] = useState<any>(null)
  const [demand, setDemand] = useState<{ items: any[]; total: number }>({ items: [], total: 0 })
  const [bench, setBench] = useState<{ items: any[]; total: number }>({ items: [], total: 0 })
  const [demandPage, setDemandPage] = useState(1)
  const [benchPage, setBenchPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const pageSize = 20

  useEffect(() => {
    Promise.all([
      supplyService.getSummary(),
      supplyService.getDemand({ page: demandPage, page_size: pageSize }),
      supplyService.getBench({ page: benchPage, page_size: pageSize }),
    ])
      .then(([s, d, b]) => { setSummary(s); setDemand(d); setBench(b) })
      .catch(() => setError('Failed to load supply/demand data'))
      .finally(() => setLoading(false))
  }, [demandPage, benchPage])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Demand / Supply</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {summary && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {[
            { label: 'Total Demand', value: summary.total_demand, color: 'primary.main' },
            { label: 'Total Bench', value: summary.total_bench, color: 'success.main' },
            { label: 'Matched', value: summary.matched, color: 'info.main' },
            { label: 'Gap', value: summary.gap, color: 'error.main' },
          ].map(s => (
            <Grid item xs={6} sm={3} key={s.label}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h4" sx={{ color: s.color }}>{s.value}</Typography>
                <Typography variant="body2" color="text.secondary">{s.label}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 1 }}>
        <Tab label="Demand" />
        <Tab label="Bench" />
      </Tabs>

      <TabPanel value={tab} index={0}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Role</TableCell><TableCell>BU</TableCell><TableCell>Account</TableCell>
              <TableCell>Technology</TableCell><TableCell>Headcount</TableCell><TableCell>Target Date</TableCell>
              <TableCell>Priority</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {demand.items.map((d: any) => (
              <TableRow key={d.demand_id}>
                <TableCell>{d.role_name}</TableCell>
                <TableCell>{d.bu ?? '—'}</TableCell>
                <TableCell>{d.account ?? '—'}</TableCell>
                <TableCell>{d.technology ?? '—'}</TableCell>
                <TableCell>{d.headcount ?? '—'}</TableCell>
                <TableCell>{d.target_date ?? '—'}</TableCell>
                <TableCell>
                  {d.priority && <Chip label={d.priority} size="small" color={d.priority === 'High' ? 'error' : d.priority === 'Medium' ? 'warning' : 'default'} />}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Pagination count={Math.ceil(demand.total / pageSize)} page={demandPage} onChange={(_, p) => setDemandPage(p)} sx={{ mt: 2 }} />
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell><TableCell>Technology</TableCell>
              <TableCell>Experience</TableCell><TableCell>Location</TableCell>
              <TableCell>BU</TableCell><TableCell>Available From</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bench.items.map((b: any) => (
              <TableRow key={b.bench_id}>
                <TableCell>{b.emp_name}</TableCell>
                <TableCell>{b.technology ?? '—'}</TableCell>
                <TableCell>{b.experience_years != null ? `${b.experience_years} yrs` : '—'}</TableCell>
                <TableCell>{b.location ?? '—'}</TableCell>
                <TableCell>{b.bu ?? '—'}</TableCell>
                <TableCell>{b.available_from ?? '—'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Pagination count={Math.ceil(bench.total / pageSize)} page={benchPage} onChange={(_, p) => setBenchPage(p)} sx={{ mt: 2 }} />
      </TabPanel>
    </Box>
  )
}
