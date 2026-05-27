import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

interface Slot {
  interviewer_calendar_id: number
  slot_date: string
  from_time: string
  to_time: string
  slot_status: 'Available' | 'Booked' | 'Interviewed' | 'Pending'
}

const STATUS_COLOR: Record<string, string> = {
  Available: '#4caf50',
  Booked: '#e91e63',
  Interviewed: '#9e9e9e',
  Pending: '#ffeb3b',
}

interface Props {
  events: Slot[]
  onSlotClick?: (slotId: number) => void
}

export default function SlotCalendar({ events, onSlotClick }: Props) {
  const calendarEvents = events.map((s) => ({
    id: String(s.interviewer_calendar_id),
    start: s.from_time,
    end: s.to_time,
    title: s.slot_status,
    backgroundColor: STATUS_COLOR[s.slot_status] ?? '#2196f3',
    borderColor: STATUS_COLOR[s.slot_status] ?? '#2196f3',
  }))

  return (
    <FullCalendar
      plugins={[timeGridPlugin, interactionPlugin]}
      initialView="timeGridWeek"
      events={calendarEvents}
      eventClick={(info) => onSlotClick?.(Number(info.event.id))}
      height="auto"
    />
  )
}
