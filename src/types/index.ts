export interface User {
  id: string
  username: string
  password: string
  realName: string
  role: 'admin' | 'user'
  phone: string
  email: string
  createdAt: string
}

export interface Room {
  id: string
  code: string
  name: string
  capacity: number
  location: string
  equipment: string
  status: 'available' | 'unavailable' | 'maintenance'
  createdAt: string
}

export interface Reservation {
  id: string
  userId: string
  roomId: string
  roomCode: string
  roomName: string
  date: string
  startTime: string
  endTime: string
  meetingTopic: string
  participantCount: number
  applicant: string
  status: 'pending' | 'approved' | 'rejected' | 'completed' | 'cancelled'
  createdAt: string
}

export interface QueueItem {
  id: string
  userId: string
  date: string
  startTime: string
  endTime: string
  meetingTopic: string
  participantCount: number
  applicant: string
  priority: number
  createdAt: string
}

export interface TimeSlot {
  time: string
  available: boolean
}
