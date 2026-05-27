import { useNavigate } from 'react-router-dom'
import { Box, Typography, Button, Chip, Stack } from '@mui/material'
import { useAuth } from '@/hooks/useAuth'

const ROLE_ROUTES: Record<string, string> = {
  'SAP Recruiter': '/upload',
  PMO: '/upload',
  Interviewer: '/dashboard',
  Admin: '/register-panel',
  TowerLead: '/work-flow',
  SLBULead: '/work-flow',
  NALead: '/work-flow',
  RecruiterLead: '/work-flow',
  BUAdmin: '/master-data',
  PracticeAdmin: '/master-data',
}

const DEFAULT_ROUTE = '/todolist'

export default function SelectRolePage() {
  const { employee, setActiveRole } = useAuth()
  const navigate = useNavigate()

  const handleRoleSelect = (role: string) => {
    setActiveRole(role)
    const path = ROLE_ROUTES[role] ?? DEFAULT_ROUTE
    navigate(path)
  }

  if (!employee) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography>Not authenticated</Typography>
      </Box>
    )
  }

  const roles = employee.roles ?? []

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 8, gap: 3 }}>
      <Typography variant="h4">Welcome, {employee.emp_name}</Typography>
      <Typography variant="body1" color="text.secondary">
        Select a role to continue
      </Typography>

      {roles.length === 0 ? (
        <Typography color="warning.main" variant="body1">
          No roles are assigned to your account. Please contact your administrator.
        </Typography>
      ) : (
        <Stack direction="row" flexWrap="wrap" gap={2} justifyContent="center">
          {roles.map((role) => (
            <Button
              key={role}
              variant="outlined"
              size="large"
              onClick={() => handleRoleSelect(role)}
              sx={{ minWidth: 160 }}
            >
              {role}
            </Button>
          ))}
        </Stack>
      )}
    </Box>
  )
}
