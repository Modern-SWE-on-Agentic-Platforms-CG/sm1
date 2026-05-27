import React, { useState } from 'react'
import {
  Box, Typography, Button, Alert, CircularProgress, Paper, LinearProgress
} from '@mui/material'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import weekendDriveService from '@/services/weekendDriveService'

export default function ImportWeekendDrivePage() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{ created: number; errors: number } | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleImport = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await weekendDriveService.importSlots(file)
      setResult(res)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Import failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ p: 3, maxWidth: 600 }}>
      <Typography variant="h5" gutterBottom>Import Weekend Drive Slots</Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="body2" sx={{ mb: 2 }}>
          Upload an Excel file with columns: <strong>emp_id, slot_date, from_time, to_time</strong> (optional: skill_id)
        </Typography>

        <Button
          variant="outlined"
          component="label"
          startIcon={<UploadFileIcon />}
          sx={{ mb: 2 }}
        >
          {file ? file.name : 'Choose Excel File'}
          <input type="file" accept=".xlsx,.xls" hidden onChange={e => setFile(e.target.files?.[0] ?? null)} />
        </Button>

        {file && (
          <Box sx={{ mb: 2 }}>
            <Button variant="contained" onClick={handleImport} disabled={loading}>
              {loading ? 'Importing…' : 'Import'}
            </Button>
          </Box>
        )}
        {loading && <LinearProgress />}
      </Paper>

      {error && <Alert severity="error">{error}</Alert>}
      {result && (
        <Alert severity={result.errors > 0 ? 'warning' : 'success'}>
          Import complete: <strong>{result.created} slots created</strong>
          {result.errors > 0 && `, ${result.errors} rows skipped`}
        </Alert>
      )}
    </Box>
  )
}
