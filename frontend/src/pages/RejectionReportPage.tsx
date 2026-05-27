import React, { useEffect, useState } from 'react'
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import analyticsService from '@/services/analyticsService'

export default function RejectionReportPage() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    analyticsService.getRejectionReasons()
      .then(setData)
      .catch(() => setError('Failed to load'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress sx={{ m: 4 }} />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Rejection Reasons Report</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Paper sx={{ p: 2 }}>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data} layout="vertical" margin={{ left: 120 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="reason" type="category" width={120} />
            <Tooltip />
            <Bar dataKey="count" fill="#f44336" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  )
}
