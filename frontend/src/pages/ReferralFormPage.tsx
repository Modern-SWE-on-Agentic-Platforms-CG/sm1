import React, { useEffect, useState } from 'react'
import {
  Box, Typography, TextField, Button, Alert, CircularProgress,
  Paper, MenuItem, Select, FormControl, InputLabel, Autocomplete
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import referralService from '@/services/referralService'

interface FormValues {
  candidate_name: string
  email: string
  phone: string
  technology_id: string
  notice_period_id: string
  location_id: string
  experience_years: string
  current_company: string
  current_ctc: string
  expected_ctc: string
}

export default function ReferralFormPage() {
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>()
  const [technologies, setTechnologies] = useState<any[]>([])
  const [noticePeriods, setNoticePeriods] = useState<any[]>([])
  const [locations, setLocations] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([
      referralService.getTechnologies(),
      referralService.getNoticePeriods(),
      referralService.getLocations(),
    ]).then(([t, n, l]) => { setTechnologies(t); setNoticePeriods(n); setLocations(l) })
  }, [])

  const onSubmit = async (data: FormValues) => {
    setLoading(true)
    setError(null)
    try {
      await referralService.submitReferral({
        ...data,
        technology_id: data.technology_id ? Number(data.technology_id) : undefined,
        notice_period_id: data.notice_period_id ? Number(data.notice_period_id) : undefined,
        location_id: data.location_id ? Number(data.location_id) : undefined,
        experience_years: data.experience_years ? Number(data.experience_years) : undefined,
        current_ctc: data.current_ctc ? Number(data.current_ctc) : undefined,
        expected_ctc: data.expected_ctc ? Number(data.expected_ctc) : undefined,
      })
      setSuccess(true)
      reset()
    } catch (err: any) {
      setError(err.response?.data?.error || 'Submission failed')
    } finally {
      setLoading(false)
    }
  }

  if (success) return (
    <Box sx={{ p: 3 }}>
      <Alert severity="success">Your referral has been submitted successfully!</Alert>
    </Box>
  )

  return (
    <Box sx={{ p: 3, maxWidth: 600 }}>
      <Typography variant="h5" gutterBottom>Refer a Candidate</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Paper sx={{ p: 3 }}>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller name="candidate_name" control={control} rules={{ required: 'Required' }} defaultValue=""
            render={({ field }) => <TextField {...field} label="Candidate Name" error={!!errors.candidate_name} helperText={errors.candidate_name?.message} />} />

          <Controller name="email" control={control} rules={{ required: 'Required' }} defaultValue=""
            render={({ field }) => <TextField {...field} label="Email" type="email" error={!!errors.email} helperText={errors.email?.message} />} />

          <Controller name="phone" control={control} defaultValue=""
            render={({ field }) => <TextField {...field} label="Phone" />} />

          <Controller name="technology_id" control={control} defaultValue=""
            render={({ field }) => (
              <FormControl><InputLabel>Technology</InputLabel>
                <Select {...field} label="Technology">
                  {technologies.map((t: any) => <MenuItem key={t.id} value={t.id}>{t.tech_name}</MenuItem>)}
                </Select>
              </FormControl>
            )} />

          <Controller name="notice_period_id" control={control} defaultValue=""
            render={({ field }) => (
              <FormControl><InputLabel>Notice Period</InputLabel>
                <Select {...field} label="Notice Period">
                  {noticePeriods.map((n: any) => <MenuItem key={n.id} value={n.id}>{n.notice_period}</MenuItem>)}
                </Select>
              </FormControl>
            )} />

          <Controller name="location_id" control={control} defaultValue=""
            render={({ field }) => (
              <FormControl><InputLabel>Location</InputLabel>
                <Select {...field} label="Location">
                  {locations.map((l: any) => <MenuItem key={l.id} value={l.id}>{l.location_name}</MenuItem>)}
                </Select>
              </FormControl>
            )} />

          <Controller name="experience_years" control={control} defaultValue=""
            render={({ field }) => <TextField {...field} label="Experience (years)" type="number" />} />

          <Controller name="current_company" control={control} defaultValue=""
            render={({ field }) => <TextField {...field} label="Current Company" />} />

          <Controller name="current_ctc" control={control} defaultValue=""
            render={({ field }) => <TextField {...field} label="Current CTC (LPA)" type="number" />} />

          <Controller name="expected_ctc" control={control} defaultValue=""
            render={({ field }) => <TextField {...field} label="Expected CTC (LPA)" type="number" />} />

          <Button type="submit" variant="contained" disabled={loading}>
            {loading ? <CircularProgress size={20} /> : 'Submit Referral'}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}
