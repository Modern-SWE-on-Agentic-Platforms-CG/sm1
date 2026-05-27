import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  Box, Typography, Button, TextField, MenuItem, CircularProgress,
  Alert, Divider, Slider, Card, CardContent
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import feedbackService, { FeedbackTemplate, FeedbackSubmitRequest } from '@/services/feedbackService'
import { getApiErrorMessage } from '@/utils/errorMessage'

interface FormValues {
  parameter_scores: Record<string, number>
  overall_rating: 'Select' | 'Hold' | 'Reject'
  overall_remarks: string
}

export default function FeedbackFormPage() {
  const { bookingId } = useParams<{ bookingId: string }>()
  const [template, setTemplate] = useState<FeedbackTemplate | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pdfPath, setPdfPath] = useState<string | null>(null)

  const { control, handleSubmit, formState: { errors } } = useForm<FormValues>({
    defaultValues: { parameter_scores: {}, overall_rating: 'Select', overall_remarks: '' }
  })

  useEffect(() => {
    if (!bookingId) return
    feedbackService.getTemplate(Number(bookingId))
      .then(setTemplate)
      .catch((err) => setError(getApiErrorMessage(err, 'Failed to load feedback template')))
      .finally(() => setLoading(false))
  }, [bookingId])

  const onSubmit = async (values: FormValues) => {
    if (!bookingId) return
    setSubmitting(true)
    setError(null)
    try {
      const payload: FeedbackSubmitRequest = {
        parameter_scores: values.parameter_scores,
        overall_rating: values.overall_rating,
        overall_remarks: values.overall_remarks || undefined,
      }
      const result = await feedbackService.submit(Number(bookingId), payload)
      setPdfPath(result.pdf_path)
    } catch (err: any) {
      setError(getApiErrorMessage(err, 'Submission failed. Please check required fields.'))
    } finally {
      setSubmitting(false)
    }
  }

  const handleDownloadPdf = async () => {
    if (!bookingId) return
    try {
      const blob = await feedbackService.downloadPdf(Number(bookingId))
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `feedback_${bookingId}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      setError(getApiErrorMessage(err, 'PDF download failed'))
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />
  if (!template) return <Alert severity="error">Template not found</Alert>

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h5" gutterBottom>{template.form_title}</Typography>
      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
        Technology: {template.tech_name}
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {pdfPath && (
        <Alert severity="success" sx={{ mb: 2 }} action={
          <Button size="small" onClick={handleDownloadPdf}>Download PDF</Button>
        }>
          Feedback submitted successfully!
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        {template.sections.map((section) => (
          <Card key={section.section_name} sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>{section.section_name}</Typography>
              <Divider sx={{ mb: 2 }} />
              {section.parameters.map((param) => (
                <Box key={param.id} sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    {param.parameter_name} (max {param.max_score})
                  </Typography>
                  <Controller
                    name={`parameter_scores.${param.id}`}
                    control={control}
                    defaultValue={0}
                    render={({ field }) => (
                      <Slider
                        {...field}
                        min={0}
                        max={param.max_score}
                        step={1}
                        marks
                        valueLabelDisplay="auto"
                        onChange={(_, v) => field.onChange(v)}
                      />
                    )}
                  />
                </Box>
              ))}
            </CardContent>
          </Card>
        ))}

        <Controller
          name="overall_rating"
          control={control}
          rules={{ required: 'Required' }}
          render={({ field }) => (
            <TextField
              {...field}
              select
              fullWidth
              label="Overall Recommendation"
              sx={{ mb: 2 }}
              error={!!errors.overall_rating}
              helperText={errors.overall_rating?.message}
            >
              <MenuItem value="Select">Select</MenuItem>
              <MenuItem value="Hold">Hold</MenuItem>
              <MenuItem value="Reject">Reject</MenuItem>
            </TextField>
          )}
        />

        <Controller
          name="overall_remarks"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              multiline
              rows={3}
              label="Overall Remarks"
              sx={{ mb: 2 }}
            />
          )}
        />

        <Button type="submit" variant="contained" disabled={submitting || !!pdfPath}>
          {submitting ? 'Submitting…' : 'Submit Feedback'}
        </Button>
      </form>
    </Box>
  )
}
