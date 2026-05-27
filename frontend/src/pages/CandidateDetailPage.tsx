import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import {
  Box, Typography, Paper, Grid, TextField, Button, MenuItem,
  Select, FormControl, InputLabel, Alert, Divider, List, ListItem, ListItemText
} from '@mui/material'
import Navbar from '@/components/Navbar'
import FileUpload from '@/components/FileUpload'
import {
  getCandidate, updateCandidate, changeStatus, getStatusOptions,
  addComment, listComments, downloadResume, uploadResume
} from '@/services/candidateService'
import { getApiErrorMessage } from '@/utils/errorMessage'

export default function CandidateDetailPage() {
  const { id } = useParams<{ id: string }>()
  const candidateId = Number(id)
  const { register, handleSubmit, reset } = useForm()
  const [candidate, setCandidate] = useState<any | null>(null)
  const [statusOptions, setStatusOptions] = useState<Record<string, string[]>>({})
  const [comments, setComments] = useState<any[]>([])
  const [newComment, setNewComment] = useState('')
  const [statusMsg, setStatusMsg] = useState<string | null>(null)
  const [commentFile, setCommentFile] = useState<File | null>(null)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [resumeMsg, setResumeMsg] = useState<{ kind: 'error' | 'success'; text: string } | null>(null)

  useEffect(() => {
    getCandidate(candidateId).then(setCandidate)
    getStatusOptions().then(setStatusOptions)
    listComments(candidateId).then(setComments)
  }, [candidateId])

  useEffect(() => {
    if (candidate) reset(candidate)
  }, [candidate, reset])

  const onSave = async (values: any) => {
    const updated = await updateCandidate(candidateId, values)
    setCandidate(updated)
  }

  const onStatusChange = async (toStatus: string) => {
    try {
      const updated = await changeStatus(candidateId, toStatus)
      setCandidate(updated)
      setStatusMsg(null)
    } catch (err: any) {
      setStatusMsg(getApiErrorMessage(err, 'Status change failed'))
    }
  }

  const onAddComment = async () => {
    try {
      await addComment(candidateId, newComment, commentFile ?? undefined)
      setNewComment('')
      setCommentFile(null)
      const updated = await listComments(candidateId)
      setComments(updated)
      setStatusMsg(null)
    } catch (err) {
      setStatusMsg(getApiErrorMessage(err, 'Failed to add comment'))
    }
  }

  const onUploadResume = async () => {
    if (!resumeFile) {
      setResumeMsg({ kind: 'error', text: 'Please choose a resume file first.' })
      return
    }

    try {
      const updated = await uploadResume(candidateId, resumeFile)
      setCandidate(updated)
      setResumeMsg({ kind: 'success', text: 'Resume uploaded successfully.' })
      setResumeFile(null)
    } catch (err) {
      const message = getApiErrorMessage(err, 'Resume upload failed')

      // Backward-compatible fallback when API supports attachment upload only.
      if (message.includes('Method Not Allowed')) {
        try {
          await addComment(candidateId, 'Resume uploaded as attachment', resumeFile)
          const updatedComments = await listComments(candidateId)
          setComments(updatedComments)
          setResumeMsg({ kind: 'success', text: 'Resume uploaded as attachment in comments.' })
          setResumeFile(null)
          return
        } catch (fallbackErr) {
          setResumeMsg({ kind: 'error', text: getApiErrorMessage(fallbackErr, 'Resume upload failed') })
          return
        }
      }

      setResumeMsg({ kind: 'error', text: message })
    }
  }

  const handleDownloadResume = async () => {
    const url = await downloadResume(candidateId)
    const a = document.createElement('a')
    a.href = url
    a.download = `resume_${candidateId}`
    a.click()
  }

  if (!candidate) return <Box sx={{ p: 4 }}>Loading…</Box>

  const nextStatuses = statusOptions[candidate.overall_status] ?? []

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>{candidate.candidate_name}</Typography>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          Status: <strong>{candidate.overall_status}</strong>
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Box component="form" onSubmit={handleSubmit(onSave)}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}><TextField fullWidth label="Name" {...register('candidate_name')} /></Grid>
              <Grid item xs={12} md={6}><TextField fullWidth label="Email" {...register('email_id')} /></Grid>
              <Grid item xs={12} md={4}><TextField fullWidth label="Total Exp" {...register('total_exp')} /></Grid>
              <Grid item xs={12} md={4}><TextField fullWidth label="Current Company" {...register('current_company')} /></Grid>
              <Grid item xs={12} md={4}><TextField fullWidth label="Notice Period" {...register('notice_period')} /></Grid>
              <Grid item xs={12} md={4}><TextField fullWidth label="Current CTC" {...register('current_ctc')} /></Grid>
              <Grid item xs={12} md={4}><TextField fullWidth label="Expected CTC" {...register('exp_ctc')} /></Grid>
              <Grid item xs={12}><Button type="submit" variant="contained">Save Changes</Button></Grid>
            </Grid>
          </Box>
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Change Status</Typography>
          {statusMsg && <Alert severity="error" sx={{ mb: 1 }}>{statusMsg}</Alert>}
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {nextStatuses.map((s) => (
              <Button key={s} variant="outlined" size="small" onClick={() => onStatusChange(s)}>{s}</Button>
            ))}
            {nextStatuses.length === 0 && <Typography variant="body2" color="text.secondary">No further transitions available</Typography>}
          </Box>
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Resume</Typography>
          {resumeMsg && <Alert severity={resumeMsg.kind} sx={{ mb: 1 }}>{resumeMsg.text}</Alert>}
          <Box sx={{ mb: 2 }}>
            <FileUpload
              label="Upload resume (.pdf, .doc, .docx)"
              accept=".pdf,.doc,.docx"
              onChange={(f) => setResumeFile(f)}
            />
            <Button sx={{ mt: 1 }} variant="contained" onClick={onUploadResume}>Upload Resume</Button>
          </Box>
          {candidate.resume_path
            ? <Button variant="outlined" onClick={handleDownloadResume}>Download Resume</Button>
            : <Typography variant="body2" color="text.secondary">No resume on file</Typography>
          }
        </Paper>

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Comments</Typography>
          <List dense>
            {comments.map((c: any) => (
              <ListItem key={c.id} divider>
                <ListItemText
                  primary={c.comment_text}
                  secondary={`By ${c.created_by} at ${new Date(c.created_at).toLocaleString()}`}
                />
              </ListItem>
            ))}
          </List>
          <Divider sx={{ my: 2 }} />
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField
              label="New Comment" multiline rows={2} fullWidth
              value={newComment} onChange={(e) => setNewComment(e.target.value)}
            />
            <FileUpload
              label="Attach file (optional)"
              accept=".pdf,.doc,.docx,.png,.jpg"
              onChange={(f) => setCommentFile(f)}
            />
            <Button variant="contained" onClick={onAddComment} sx={{ alignSelf: 'flex-start' }}>
              Add Comment
            </Button>
          </Box>
        </Paper>
      </Box>
    </Box>
  )
}
