import React, { useEffect, useState } from 'react'
import { Box, Typography, Grid, Paper, CircularProgress, Alert } from '@mui/material'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import analyticsService from '@/services/analyticsService'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']

export default function DashboardReportsPage() {
  const [summary, setSummary] = useState<any>(null)
  const [statusPie, setStatusPie] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([analyticsService.getSummary(), analyticsService.getStatusPie()])
      .then(([s, pie]) => { setSummary(s); setStatusPie(pie) })
      .catch(() => setError('Failed to load analytics'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Dashboard Reports</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {summary && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {[
            { label: 'Total Candidates', value: summary.total_candidates },
            { label: 'Total Offers', value: summary.total_offers },
            { label: 'Total Joinings', value: summary.total_joinings },
            { label: 'Pending Feedback', value: summary.pending_feedback },
          ].map(stat => (
            <Grid item xs={12} sm={6} md={3} key={stat.label}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h4" color="primary">{stat.value}</Typography>
                <Typography variant="body2" color="text.secondary">{stat.label}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>Status Distribution</Typography>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={statusPie} dataKey="value" nameKey="name" outerRadius={100} label>
              {statusPie.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  )
}
