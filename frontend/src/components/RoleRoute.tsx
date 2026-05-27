import { useAuth } from '@/hooks/useAuth'
import type { ReactNode } from 'react'
import { Box, Typography } from '@mui/material'

interface Props {
  children: ReactNode
  allowedRoles: string[]
}

export default function RoleRoute({ children, allowedRoles }: Props) {
  const { activeRole, employee } = useAuth()

  // If on /selectrole page itself, render normally
  const isSelectRolePath = window.location.pathname === '/selectrole'
  if (isSelectRolePath) {
    return <>{children}</>
  }

  const role = activeRole ?? employee?.roles[0]
  if (!role || !allowedRoles.includes(role)) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h6" color="error">
          Access Denied — you do not have the required role to view this page.
        </Typography>
      </Box>
    )
  }
  return <>{children}</>
}
