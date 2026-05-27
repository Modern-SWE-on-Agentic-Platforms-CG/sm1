import { useState } from 'react'
import { Box, Typography, Paper, Alert, LinearProgress } from '@mui/material'
import Navbar from '@/components/Navbar'
import FileUpload from '@/components/FileUpload'
import { uploadCandidates } from '@/services/candidateService'
import { getApiErrorMessage } from '@/utils/errorMessage'

export default function UploadPage() {
  const [result, setResult] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async (file: File) => {
    setLoading(true)
    setResult(null)
    try {
      const data = await uploadCandidates(file)
      setResult(data)
    } catch (err: any) {
      setResult({ error: getApiErrorMessage(err, 'Upload failed. Please use a valid Excel file.') })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3, maxWidth: 600 }}>
        <Typography variant="h5" gutterBottom>Upload Candidates</Typography>
        <Paper sx={{ p: 3 }}>
          <FileUpload label="Drop candidate Excel file here (.xlsx)" onChange={handleUpload} />
          {loading && <LinearProgress sx={{ mt: 2 }} />}
          {result && (
            <Box sx={{ mt: 2 }}>
              {result.error
                ? <Alert severity="error">{result.error}</Alert>
                : (
                  <Alert severity="success">
                    Imported: {result.imported} | Duplicates: {result.duplicates} | Errors: {result.errors}
                  </Alert>
                )
              }
              {result.error_file_url && (
                <a href={result.error_file_url} download style={{ display: 'block', marginTop: 8 }}>
                  Download error file
                </a>
              )}
            </Box>
          )}
        </Paper>
      </Box>
    </Box>
  )
}
