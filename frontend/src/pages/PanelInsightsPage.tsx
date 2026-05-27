import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Paper, Grid, CircularProgress, Alert
} from '@mui/material'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '@/services/api'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

export default function PanelInsightsPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Use status-pie scoped to interviewer activity
    api.get('/api/v1/reports/analytics/source-pie')
      .then(r => setData(r.data.data ?? []))
      .catch(() => setError('Failed to load panel insights'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Panel Insights</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Interview Source Distribution</Typography>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
                  {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="body1" color="text.secondary">
              Panel insights show the interviewer panel's involvement across candidate sources.
              Use the reports section for more detailed analytics.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
