import { AppBar, Toolbar, Typography, Chip, Button, Box } from '@mui/material'
import { useAuth } from '@/hooks/useAuth'
import { logout as apiLogout } from '@/services/authService'
import { useNavigate } from 'react-router-dom'

const ROLE_MENUS: Record<string, Array<{ label: string; path: string }>> = {
  Admin: [
    { label: 'Register Panel', path: '/register-panel' },
    { label: 'Administration', path: '/administration' },
    { label: 'Master Data', path: '/master-data' },
    { label: 'Candidates', path: '/candidate-details' },
    { label: 'Upload', path: '/upload' },
    { label: 'Booking', path: '/booking-form' },
    { label: 'Reports', path: '/dashboard-reports' },
  ],
  Recruiter: [
    { label: 'Todo', path: '/todolist' },
    { label: 'Candidates', path: '/candidate-details' },
    { label: 'Upload', path: '/upload' },
    { label: 'Booking', path: '/booking-form' },
    { label: 'Reports', path: '/dashboard-reports' },
  ],
  PMO: [
    { label: 'Todo', path: '/todolist' },
    { label: 'Candidates', path: '/candidate-details' },
    { label: 'Upload', path: '/upload' },
    { label: 'Booking', path: '/booking-form' },
    { label: 'Reports', path: '/dashboard-reports' },
  ],
  Interviewer: [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'Todo', path: '/todolist' },
    { label: 'Interview Data', path: '/interview-data' },
    { label: 'Feedback Report', path: '/feedback-form-report' },
  ],
  RecruiterLead: [
    { label: 'Workflow', path: '/work-flow' },
    { label: 'Todo', path: '/todolist' },
    { label: 'Reports', path: '/dashboard-reports' },
  ],
  TowerLead: [
    { label: 'Workflow', path: '/work-flow' },
    { label: 'Workflow Info', path: '/work-flow-info' },
  ],
  SLBULead: [
    { label: 'Workflow', path: '/work-flow' },
    { label: 'Workflow Info', path: '/work-flow-info' },
  ],
  NALead: [
    { label: 'Workflow', path: '/work-flow' },
    { label: 'Workflow Info', path: '/work-flow-info' },
  ],
  BUAdmin: [
    { label: 'Master Data', path: '/master-data' },
    { label: 'Joining Bonus', path: '/joiningbonus' },
  ],
  PracticeAdmin: [{ label: 'Master Data', path: '/master-data' }],
  'SAP Recruiter': [
    { label: 'Upload', path: '/upload' },
    { label: 'Candidates', path: '/candidate-details' },
  ],
}

export default function Navbar() {
  const { employee, activeRole, logout } = useAuth()
  const navigate = useNavigate()
  const menuItems = activeRole ? (ROLE_MENUS[activeRole] ?? []) : []

  const handleLogout = async () => {
    try {
      await apiLogout()
    } finally {
      logout()
      navigate('/login')
    }
  }

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Smart Recruit Platform
        </Typography>
        {employee && (
          <Button
            color="inherit"
            size="small"
            onClick={() => navigate('/selectrole')}
            sx={{ mr: 1, textTransform: 'none' }}
          >
            Switch Role
          </Button>
        )}
        {menuItems.length > 0 && (
          <Box
            sx={{
              display: 'flex',
              gap: 0.5,
              mr: 1,
              overflowX: 'auto',
              maxWidth: { xs: 180, sm: 360, md: 560 },
            }}
          >
            {menuItems.map((item) => (
              <Button
                key={item.path}
                color="inherit"
                size="small"
                onClick={() => navigate(item.path)}
                sx={{ textTransform: 'none', whiteSpace: 'nowrap', minWidth: 'auto', px: 1 }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        )}
        {activeRole && (
          <Chip
            label={activeRole}
            color="secondary"
            size="small"
            sx={{ mr: 2, color: 'white', fontWeight: 600 }}
          />
        )}
        {employee && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">{employee.emp_name}</Typography>
            <Button color="inherit" onClick={handleLogout} size="small">
              Logout
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  )
}
