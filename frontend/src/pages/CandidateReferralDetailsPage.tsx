import React, { useEffect, useState } from 'react'
import { Box, Typography, CircularProgress, Alert, Paper, Chip, Grid } from '@mui/material'
import { useParams } from 'react-router-dom'
import referralService from '@/services/referralService'

export default function CandidateReferralDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const [data, setData] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    referralService.getCandidate(Number(id))
      .then(setData)
      .catch(() => setError('Referral not found'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <CircularProgress sx={{ m: 4 }} />
  if (error || !data) return <Alert severity="error" sx={{ m: 4 }}>{error}</Alert>

  const fields = [
    { label: 'Name', value: data.candidate_name },
    { label: 'Email', value: data.email },
    { label: 'Phone', value: data.phone },
    { label: 'Experience', value: data.experience_years != null ? `${data.experience_years} yrs` : null },
    { label: 'Current Company', value: data.current_company },
    { label: 'Current CTC', value: data.current_ctc },
    { label: 'Expected CTC', value: data.expected_ctc },
    { label: 'BU', value: data.bu },
    { label: 'Account', value: data.account },
  ]

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Referral Details</Typography>
      <Chip label={data.status ?? 'New'} color={data.status === 'Selected' ? 'success' : 'default'} sx={{ mb: 2 }} />
      <Paper sx={{ p: 3 }}>
        <Grid container spacing={2}>
          {fields.filter(f => f.value != null).map(f => (
            <Grid item xs={12} sm={6} key={f.label}>
              <Typography variant="caption" color="text.secondary">{f.label}</Typography>
              <Typography variant="body1">{f.value}</Typography>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  )
}
