import { useState, useEffect } from 'react'
import { Box, Typography, Paper, Divider, Button, TextField, MenuItem, Alert } from '@mui/material'
import Navbar from '@/components/Navbar'
import SlotCalendar from '@/components/SlotCalendar'
import FileUpload from '@/components/FileUpload'
import { listSlots, createSlot, bulkUploadSlots } from '@/services/slotService'
import { useAuth } from '@/hooks/useAuth'
import { getApiErrorMessage } from '@/utils/errorMessage'

export default function DashboardPage() {
  const { employee } = useAuth()
  const [slots, setSlots] = useState<any[]>([])
  const [slotForm, setSlotForm] = useState({ slot_date: '', from_time: '', to_time: '', skill_id: '' })
  const [slotError, setSlotError] = useState<string | null>(null)
  const [uploadResult, setUploadResult] = useState<any | null>(null)

  const fetchSlots = async () => {
    try {
      const data = await listSlots()
      setSlots(data.items ?? [])
    } catch {
      // ignore
    }
  }

  useEffect(() => { fetchSlots() }, [])

  const handleCreateSlot = async () => {
    setSlotError(null)
    try {
      await createSlot({
        slot_date: slotForm.slot_date,
        from_time: new Date(slotForm.slot_date + 'T' + slotForm.from_time).toISOString(),
        to_time: new Date(slotForm.slot_date + 'T' + slotForm.to_time).toISOString(),
        skill_id: slotForm.skill_id ? Number(slotForm.skill_id) : undefined,
      })
      fetchSlots()
    } catch (err: any) {
      setSlotError(getApiErrorMessage(err, 'Failed to create slot. Please check date/time values.'))
    }
  }

  const handleBulkUpload = async (file: File) => {
    try {
      const result = await bulkUploadSlots(file)
      setUploadResult(result)
      fetchSlots()
    } catch (err: any) {
      setUploadResult({ error: getApiErrorMessage(err, 'Upload failed. Please check file format and columns.') })
    }
  }

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Interviewer Dashboard — {employee?.emp_name}
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Create Slot</Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <TextField label="Date" type="date" InputLabelProps={{ shrink: true }}
              value={slotForm.slot_date} onChange={e => setSlotForm(f => ({ ...f, slot_date: e.target.value }))} />
            <TextField label="From" type="time" InputLabelProps={{ shrink: true }}
              value={slotForm.from_time} onChange={e => setSlotForm(f => ({ ...f, from_time: e.target.value }))} />
            <TextField label="To" type="time" InputLabelProps={{ shrink: true }}
              value={slotForm.to_time} onChange={e => setSlotForm(f => ({ ...f, to_time: e.target.value }))} />
            <Button variant="contained" onClick={handleCreateSlot}>Create</Button>
          </Box>
          {slotError && <Alert severity="error" sx={{ mt: 1 }}>{slotError}</Alert>}
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Bulk Upload Slots (.xlsx)</Typography>
          <FileUpload onChange={handleBulkUpload} />
          {uploadResult && (
            <Box sx={{ mt: 1 }}>
              {uploadResult.error
                ? <Alert severity="error">{uploadResult.error}</Alert>
                : <Alert severity="success">Created: {uploadResult.created} | Errors: {uploadResult.errors}</Alert>
              }
              {uploadResult.error_file_url && (
                <Button href={uploadResult.error_file_url} size="small" sx={{ mt: 1 }}>Download Error File</Button>
              )}
            </Box>
          )}
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>My Slots</Typography>
          <SlotCalendar events={slots} />
        </Paper>
      </Box>
    </Box>
  )
}
