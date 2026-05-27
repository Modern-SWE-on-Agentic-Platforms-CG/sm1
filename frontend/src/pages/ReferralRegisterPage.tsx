import React, { useState } from 'react'
import {
  Box, Typography, TextField, Button, Alert, Paper, CircularProgress
} from '@mui/material'

// Public registration page — uses same ReferralFormPage but wrapped with a branding header
export default function ReferralRegisterPage() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.100', display: 'flex', alignItems: 'center', justifyContent: 'center', py: 4 }}>
      <Box sx={{ width: '100%', maxWidth: 640 }}>
        <Paper sx={{ p: 3, mb: 2 }}>
          <Typography variant="h4" color="primary" gutterBottom>SmartHire Referral Portal</Typography>
          <Typography variant="body2" color="text.secondary">
            Know someone great? Refer them to join our team. Fill in the form below.
          </Typography>
        </Paper>
        {/* Lazy import to avoid circular route issues */}
        <React.Suspense fallback={<CircularProgress sx={{ m: 2 }} />}>
          <ReferralFormInner />
        </React.Suspense>
      </Box>
    </Box>
  )
}

const ReferralFormInner = React.lazy(() => import('./ReferralFormPage'))
