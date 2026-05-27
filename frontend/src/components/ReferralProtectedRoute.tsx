import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

const REFERRAL_ROLES = ['Recruiter', 'RecruiterLead', 'Admin', 'PMO']

interface ReferralProtectedRouteProps {
  children: React.ReactNode
}

export default function ReferralProtectedRoute({ children }: ReferralProtectedRouteProps) {
  const { token, employee, activeRole } = useAuth()
  if (!token) return <Navigate to="/login" replace />

  const role = activeRole ?? employee?.roles?.[0]
  if (!role || !REFERRAL_ROLES.includes(role)) return <Navigate to="/dashboard" replace />
  return <>{children}</>
}
