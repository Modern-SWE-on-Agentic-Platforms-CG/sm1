import { useState, useEffect } from 'react'
import {
  Box, Typography, Paper, TextField, Button, Alert,
  Table, TableBody, TableCell, TableHead, TableRow, MenuItem, Select, FormControl, InputLabel
} from '@mui/material'
import Navbar from '@/components/Navbar'
import { getAvailableSlots, bookSlot, directBook } from '@/services/bookingService'
import { listCandidates } from '@/services/candidateService'
import { getApiErrorMessage } from '@/utils/errorMessage'

export default function BookingFormPage() {
  const [skillId, setSkillId] = useState<string>('')
  const [interviewDate, setInterviewDate] = useState('')
  const [availableSlots, setAvailableSlots] = useState<any[]>([])
  const [candidates, setCandidates] = useState<any[]>([])
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null)
  const [selectedCandidate, setSelectedCandidate] = useState<number | null>(null)
  const [bookingResult, setBookingResult] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listCandidates().then((d) => setCandidates(d.items ?? []))
  }, [])

  const handleSearch = async () => {
    const data = await getAvailableSlots(skillId ? Number(skillId) : undefined, interviewDate || undefined)
    setAvailableSlots(data.items ?? [])
  }

  const handleBook = async () => {
    if (!selectedSlot || !selectedCandidate) return
    setError(null)
    try {
      const result = await bookSlot({ candidate_detail_id: selectedCandidate, interviewer_calendar_id: selectedSlot })
      setBookingResult(result)
    } catch (err: any) {
      setError(getApiErrorMessage(err, 'Booking failed. Please pick a valid candidate and slot.'))
    }
  }

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Book Interview Slot</Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
            <TextField label="Skill ID" value={skillId} onChange={e => setSkillId(e.target.value)} sx={{ width: 120 }} />
            <TextField label="Date" type="date" InputLabelProps={{ shrink: true }}
              value={interviewDate} onChange={e => setInterviewDate(e.target.value)} />
            <Button variant="contained" onClick={handleSearch}>Search</Button>
          </Box>
        </Paper>

        {availableSlots.length > 0 && (
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>Available Slots</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>From</TableCell>
                  <TableCell>To</TableCell>
                  <TableCell>Select</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {availableSlots.map((s: any) => (
                  <TableRow key={s.interviewer_calendar_id}
                    selected={selectedSlot === s.interviewer_calendar_id}
                    onClick={() => setSelectedSlot(s.interviewer_calendar_id)}
                    sx={{ cursor: 'pointer' }}>
                    <TableCell>{s.interviewer_calendar_id}</TableCell>
                    <TableCell>{s.slot_date}</TableCell>
                    <TableCell>{new Date(s.from_time).toLocaleTimeString()}</TableCell>
                    <TableCell>{new Date(s.to_time).toLocaleTimeString()}</TableCell>
                    <TableCell>{selectedSlot === s.interviewer_calendar_id ? '✓' : ''}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        )}

        {availableSlots.length === 0 && (
          <Alert severity="info" sx={{ mb: 3 }}>
            No available slots found. Try searching without date or with a different skill.
          </Alert>
        )}

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Book Slot</Typography>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Candidate</InputLabel>
            <Select value={selectedCandidate ?? ''} onChange={e => setSelectedCandidate(Number(e.target.value))} label="Candidate">
              {candidates.map((c: any) => (
                <MenuItem key={c.candidate_detail_id} value={c.candidate_detail_id}>
                  {c.candidate_name} ({c.email_id})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Button variant="contained" onClick={handleBook} disabled={!selectedSlot || !selectedCandidate}>
            Book
          </Button>
          {bookingResult && (
            <Alert severity="success" sx={{ mt: 2 }}>
              Booked! Meeting link: {bookingResult.meeting_link}
            </Alert>
          )}
        </Paper>
      </Box>
    </Box>
  )
}
