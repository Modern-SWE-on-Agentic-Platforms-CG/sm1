import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import {
  Box, Typography, Paper, Grid, TextField, Button, MenuItem,
  Select, FormControl, InputLabel, Chip, OutlinedInput, Alert
} from '@mui/material'
import Navbar from '@/components/Navbar'
import { createEmployee, getPanelRoles, getPanelTechnologies } from '@/services/employeeService'
import { getApiErrorMessage } from '@/utils/errorMessage'

export default function PanelRegistrationPage() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm()
  const [roles, setRoles] = useState<any[]>([])
  const [technologies, setTechnologies] = useState<any[]>([])
  const [selectedRoles, setSelectedRoles] = useState<number[]>([])
  const [selectedTechs, setSelectedTechs] = useState<number[]>([])
  const [apiError, setApiError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    getPanelRoles().then(setRoles)
    getPanelTechnologies().then(setTechnologies)
  }, [])

  const onSubmit = async (values: any) => {
    setApiError(null)
    setSuccess(false)
    try {
      await createEmployee({
        ...values,
        role_ids: selectedRoles,
        technology_ids: selectedTechs,
      })
      setSuccess(true)
      reset()
      setSelectedRoles([])
      setSelectedTechs([])
    } catch (err: any) {
      setApiError(getApiErrorMessage(err, 'Registration failed. Please review form inputs.'))
    }
  }

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3, maxWidth: 800 }}>
        <Typography variant="h5" gutterBottom>Panel Registration</Typography>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>Employee registered successfully</Alert>}
        <Paper sx={{ p: 3 }}>
          <Box component="form" onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="Full Name" {...register('emp_name', { required: true })}
                  error={!!errors.emp_name} helperText={errors.emp_name ? 'Required' : ''} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="Email" type="email" {...register('email_id', { required: true })}
                  error={!!errors.email_id} helperText={errors.email_id ? 'Required' : ''} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="Password" type="password" {...register('password', { required: true })}
                  error={!!errors.password} helperText={errors.password ? 'Required' : ''} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="BU" {...register('bu')} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="Grade" {...register('grade')} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="Location" {...register('location')} />
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Roles</InputLabel>
                  <Select
                    multiple value={selectedRoles}
                    onChange={(e) => setSelectedRoles(e.target.value as number[])}
                    input={<OutlinedInput label="Roles" />}
                    renderValue={(selected) =>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as number[]).map((id) => (
                          <Chip key={id} label={roles.find(r => r.id === id)?.role_name ?? id} size="small" />
                        ))}
                      </Box>
                    }
                  >
                    {roles.map((r) => <MenuItem key={r.id} value={r.id}>{r.role_name}</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Technologies</InputLabel>
                  <Select
                    multiple value={selectedTechs}
                    onChange={(e) => setSelectedTechs(e.target.value as number[])}
                    input={<OutlinedInput label="Technologies" />}
                    renderValue={(selected) =>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as number[]).map((id) => (
                          <Chip key={id} label={technologies.find(t => t.id === id)?.tech_name ?? id} size="small" />
                        ))}
                      </Box>
                    }
                  >
                    {technologies.map((t) => <MenuItem key={t.id} value={t.id}>{t.tech_name}</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <Button type="submit" variant="contained" size="large">Register Employee</Button>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Box>
    </Box>
  )
}
