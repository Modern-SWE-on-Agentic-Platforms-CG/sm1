import React, { useEffect, useState } from 'react'
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import analyticsService from '@/services/analyticsService'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']

export default function ChannelInsightsPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    analyticsService.getChannelPie()
      .then(setData)
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Channel Insights</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Paper sx={{ p: 2 }}>
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" outerRadius={120} label>
              {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  )
}
