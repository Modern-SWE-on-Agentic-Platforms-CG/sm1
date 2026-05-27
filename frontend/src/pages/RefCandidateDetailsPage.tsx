import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Box, Typography, CircularProgress, Alert, Paper, Grid, Chip } from '@mui/material'
import referralService from '@/services/referralService'

export default function RefCandidateDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    referralService.getCandidate(Number(id))
      .then(setData)
      .catch(() => setError('Not found'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <CircularProgress sx={{ m: 4 }} />
  if (error || !data) return <Alert severity="error" sx={{ m: 4 }}>{error}</Alert>

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Referral — {data.candidate_name}</Typography>
      <Chip label={data.status ?? 'New'} color={data.status === 'Selected' ? 'success' : data.status === 'Rejected' ? 'error' : 'default'} sx={{ mb: 2 }} />
      <Paper sx={{ p: 3 }}>
        <Grid container spacing={2}>
          {[
            ['Email', data.email], ['Phone', data.phone], ['Experience', data.experience_years],
            ['Company', data.current_company], ['Current CTC', data.current_ctc], ['Expected CTC', data.expected_ctc],
            ['BU', data.bu], ['Account', data.account],
          ].filter(([, v]) => v != null).map(([label, value]) => (
            <Grid item xs={12} sm={6} key={String(label)}>
              <Typography variant="caption" color="text.secondary">{label}</Typography>
              <Typography>{value}</Typography>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  )
}
