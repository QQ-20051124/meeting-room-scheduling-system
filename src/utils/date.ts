export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function formatTime(time: string): string {
  return time
}

export function getToday(): string {
  return formatDate(new Date())
}

export function getTomorrow(): string {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return formatDate(tomorrow)
}

export function isSameDay(date1: string, date2: string): boolean {
  return date1 === date2
}

export function isBefore(date1: string, date2: string): boolean {
  return new Date(date1) < new Date(date2)
}

export function isTimeBefore(time1: string, time2: string): boolean {
  const [h1, m1] = time1.split(':').map(Number)
  const [h2, m2] = time2.split(':').map(Number)
  return h1 < h2 || (h1 === h2 && m1 < m2)
}

export function isValidTimeRange(startTime: string, endTime: string): boolean {
  return isTimeBefore(startTime, endTime)
}

export function isPastTime(date: string, time: string): boolean {
  const now = new Date()
  const today = formatDate(now)
  const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  
  if (isBefore(date, today)) {
    return true
  }
  
  if (date === today && isTimeBefore(time, currentTime)) {
    return true
  }
  
  return false
}

export function generateTimeSlots(): string[] {
  const slots: string[] = []
  for (let h = 8; h <= 21; h++) {
    slots.push(`${String(h).padStart(2, '0')}:00`)
    if (h < 21) {
      slots.push(`${String(h).padStart(2, '0')}:30`)
    }
  }
  return slots
}
