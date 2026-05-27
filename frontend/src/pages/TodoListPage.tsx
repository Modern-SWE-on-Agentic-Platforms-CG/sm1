import { useState, useEffect } from 'react'
import {
  Box, Typography, Paper, Tabs, Tab, Chip, Button, Alert,
  Table, TableBody, TableCell, TableHead, TableRow, Link,
  Select, MenuItem, FormControl
} from '@mui/material'
import Navbar from '@/components/Navbar'
import SlotCalendar from '@/components/SlotCalendar'
import { getTodoList, getWeeklyView, getPendingFeedback } from '@/services/bookingService'
import candidateService from '@/services/candidateService'

interface TabPanelProps { children: React.ReactNode; value: number; index: number }
function TabPanel({ children, value, index }: TabPanelProps) {
  return <div hidden={value !== index}>{value === index && <Box sx={{ pt: 2 }}>{children}</Box>}</div>
}

export default function TodoListPage() {
  const [tab, setTab] = useState(0)
  const [todoData, setTodoData] = useState<any>(null)
  const [weeklyBookings, setWeeklyBookings] = useState<any[]>([])
  const [pendingFeedback, setPendingFeedback] = useState<any[]>([])

  useEffect(() => {
    getTodoList().then(setTodoData)
    getWeeklyView().then((d) => setWeeklyBookings(d.items ?? []))
    getPendingFeedback().then((d) => setPendingFeedback(d.items ?? []))
  }, [])

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>To-Do List</Typography>
        <Tabs value={tab} onChange={(_, v) => setTab(v)}>
          <Tab label="Today's Interviews" />
          <Tab label="Pending Feedback" />
          <Tab label="Weekly View" />
        </Tabs>

        <TabPanel value={tab} index={0}>
          <Paper sx={{ p: 2 }}>
            {(todoData?.today_interviews ?? []).length === 0
              ? <Typography color="text.secondary">No interviews today</Typography>
              : (
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Booking ID</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Meeting Link</TableCell>
                      <TableCell>Update Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {todoData.today_interviews.map((b: any) => (
                      <TableRow key={b.recruiter_calendar_id}>
                        <TableCell>{b.recruiter_calendar_id}</TableCell>
                        <TableCell>{b.interview_date}</TableCell>
                        <TableCell>
                          {b.meeting_link ? <Link href={b.meeting_link} target="_blank">Join</Link> : '—'}
                        </TableCell>
                        <TableCell>
                          {b.candidate_detail_id && (
                            <FormControl size="small" sx={{ minWidth: 160 }}>
                              <Select
                                displayEmpty
                                defaultValue=""
                                onChange={async e => {
                                  if (e.target.value) {
                                    await candidateService.updateStatus(b.candidate_detail_id, { status: e.target.value as string })
                                    getTodoList().then(setTodoData)
                                  }
                                }}
                              >
                                <MenuItem value=""><em>Update status…</em></MenuItem>
                                <MenuItem value="L1 Completed">L1 Completed</MenuItem>
                                <MenuItem value="L1 No Show">L1 No Show</MenuItem>
                                <MenuItem value="L1 Cancelled">L1 Cancelled</MenuItem>
                                <MenuItem value="L2 Completed">L2 Completed</MenuItem>
                                <MenuItem value="L2 No Show">L2 No Show</MenuItem>
                              </Select>
                            </FormControl>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )
            }
          </Paper>
        </TabPanel>

        <TabPanel value={tab} index={1}>
          <Paper sx={{ p: 2 }}>
            {pendingFeedback.length === 0
              ? <Typography color="text.secondary">No pending feedback</Typography>
              : (
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Booking ID</TableCell>
                      <TableCell>Date</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {pendingFeedback.map((b: any) => (
                      <TableRow key={b.recruiter_calendar_id} sx={{ bgcolor: 'warning.light' }}>
                        <TableCell>{b.recruiter_calendar_id}</TableCell>
                        <TableCell>{b.interview_date}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )
            }
          </Paper>
        </TabPanel>

        <TabPanel value={tab} index={2}>
          <Paper sx={{ p: 2 }}>
            <SlotCalendar
              events={weeklyBookings.map((b: any) => ({
                interviewer_calendar_id: b.recruiter_calendar_id,
                slot_date: b.interview_date,
                from_time: b.interview_from_time,
                to_time: b.interview_to_time,
                slot_status: 'Booked',
              }))}
            />
          </Paper>
        </TabPanel>
      </Box>
    </Box>
  )
}
