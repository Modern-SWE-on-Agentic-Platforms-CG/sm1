import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { Box, Card, CardContent, TextField, Button, Typography, Alert, CircularProgress } from '@mui/material'
import { login as apiLogin } from '@/services/authService'
import { useAuth } from '@/hooks/useAuth'
import { getApiErrorMessage } from '@/utils/errorMessage'

interface FormValues {
  email: string
  password: string
}

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>()
  const { login } = useAuth()
  const navigate = useNavigate()
  const [apiError, setApiError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (values: FormValues) => {
    setLoading(true)
    setApiError(null)
    try {
      const data = await apiLogin(values)
      login(data.access_token, data.employee)
      navigate('/selectrole')
    } catch (err: unknown) {
      setApiError(getApiErrorMessage(err, 'Login failed. Please verify email and password.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', bgcolor: 'grey.100' }}>
      <Card sx={{ minWidth: 360, p: 2 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom align="center">
            Smart Recruit
          </Typography>
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
            Sign in to continue
          </Typography>
          {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
          <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
            <TextField
              fullWidth label="Email" type="email" margin="normal"
              {...register('email', { required: 'Email is required' })}
              error={!!errors.email} helperText={errors.email?.message}
            />
            <TextField
              fullWidth label="Password" type="password" margin="normal"
              {...register('password', { required: 'Password is required' })}
              error={!!errors.password} helperText={errors.password?.message}
            />
            <Button
              type="submit" fullWidth variant="contained" sx={{ mt: 2 }}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={16} /> : null}
            >
              {loading ? 'Signing in…' : 'Sign In'}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}
