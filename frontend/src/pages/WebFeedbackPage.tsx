import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  Box, Typography, Button, TextField, MenuItem, CircularProgress,
  Alert, Slider, Card, CardContent, Divider
} from '@mui/material'
import { useForm, Controller } from 'react-hook-form'
import feedbackService, { FeedbackTemplate, FeedbackSubmitRequest } from '@/services/feedbackService'

interface FormValues {
  parameter_scores: Record<string, number>
  overall_rating: 'Select' | 'Hold' | 'Reject'
  overall_remarks: string
}

/**
 * Mobile-accessible feedback form for web/tablet view.
 * Same data model as FeedbackFormPage but with simplified layout.
 */
export default function WebFeedbackPage() {
  const { bookingId } = useParams<{ bookingId: string }>()
  const [template, setTemplate] = useState<FeedbackTemplate | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [submitted, setSubmitted] = useState(false)

  const { control, handleSubmit } = useForm<FormValues>({
    defaultValues: { parameter_scores: {}, overall_rating: 'Select', overall_remarks: '' }
  })

  useEffect(() => {
    if (!bookingId) return
    feedbackService.getTemplate(Number(bookingId))
      .then(setTemplate)
      .catch(() => setError('Failed to load feedback template'))
      .finally(() => setLoading(false))
  }, [bookingId])

  const onSubmit = async (values: FormValues) => {
    if (!bookingId) return
    setSubmitting(true)
    setError(null)
    try {
      await feedbackService.submit(Number(bookingId), {
        parameter_scores: values.parameter_scores,
        overall_rating: values.overall_rating,
        overall_remarks: values.overall_remarks || undefined,
      })
      setSubmitted(true)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Submission failed')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 2 }} />
  if (submitted) return (
    <Box sx={{ p: 2, textAlign: 'center' }}>
      <Alert severity="success">Feedback submitted successfully! Thank you.</Alert>
    </Box>
  )

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        {template?.form_title || 'Interview Feedback'}
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <form onSubmit={handleSubmit(onSubmit)}>
        {template?.sections.map((section) => (
          <Card key={section.section_name} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="subtitle1" fontWeight="bold">{section.section_name}</Typography>
              <Divider sx={{ my: 1 }} />
              {section.parameters.map((param) => (
                <Box key={param.id} sx={{ mb: 1.5 }}>
                  <Typography variant="caption">
                    {param.parameter_name} (0–{param.max_score})
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
                        size="small"
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
          render={({ field }) => (
            <TextField {...field} select fullWidth label="Recommendation" size="small" sx={{ mb: 1.5 }}>
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
            <TextField {...field} fullWidth multiline rows={2} label="Remarks" size="small" sx={{ mb: 2 }} />
          )}
        />

        <Button type="submit" variant="contained" fullWidth disabled={submitting}>
          {submitting ? 'Submitting…' : 'Submit'}
        </Button>
      </form>
    </Box>
  )
}
