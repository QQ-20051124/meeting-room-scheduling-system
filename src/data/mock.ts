import type { User, Room, Reservation, QueueItem } from '@/types'

export const mockUsers: User[] = [
  {
    id: '1',
    username: 'admin',
    password: '123456',
    realName: '管理员',
    role: 'admin',
    phone: '13800138000',
    email: 'admin@example.com',
    createdAt: '2024-01-01'
  },
  {
    id: '2',
    username: 'student001',
    password: '123456',
    realName: '张三',
    role: 'user',
    phone: '13800138001',
    email: 'zhangsan@example.com',
    createdAt: '2024-01-02'
  },
  {
    id: '3',
    username: 'student002',
    password: '123456',
    realName: '李四',
    role: 'user',
    phone: '13800138002',
    email: 'lisi@example.com',
    createdAt: '2024-01-03'
  }
]

export const mockRooms: Room[] = [
  {
    id: '1',
    code: 'RM001',
    name: '第一会议室',
    capacity: 20,
    location: '教学楼A栋301',
    equipment: '投影仪、白板、音响',
    status: 'available',
    createdAt: '2024-01-01'
  },
  {
    id: '2',
    code: 'RM002',
    name: '第二会议室',
    capacity: 15,
    location: '教学楼A栋302',
    equipment: '投影仪、白板',
    status: 'available',
    createdAt: '2024-01-01'
  },
  {
    id: '3',
    code: 'RM003',
    name: '第三会议室',
    capacity: 30,
    location: '教学楼B栋201',
    equipment: '投影仪、白板、音响、视频会议',
    status: 'maintenance',
    createdAt: '2024-01-01'
  },
  {
    id: '4',
    code: 'RM004',
    name: '第四会议室',
    capacity: 10,
    location: '教学楼B栋202',
    equipment: '白板',
    status: 'available',
    createdAt: '2024-01-01'
  },
  {
    id: '5',
    code: 'RM005',
    name: '第五会议室',
    capacity: 25,
    location: '综合楼101',
    equipment: '投影仪、白板、音响、视频会议',
    status: 'available',
    createdAt: '2024-01-01'
  }
]

const today = new Date().toISOString().split('T')[0]

export const mockReservations: Reservation[] = [
  {
    id: '1',
    userId: '2',
    roomId: '1',
    roomCode: 'RM001',
    roomName: '第一会议室',
    date: today,
    startTime: '09:00',
    endTime: '11:00',
    meetingTopic: '社团招新筹备会议',
    participantCount: 15,
    applicant: '张三',
    status: 'approved',
    createdAt: '2024-01-10'
  },
  {
    id: '2',
    userId: '3',
    roomId: '2',
    roomCode: 'RM002',
    roomName: '第二会议室',
    date: today,
    startTime: '14:00',
    endTime: '16:00',
    meetingTopic: '学习小组讨论会',
    participantCount: 8,
    applicant: '李四',
    status: 'approved',
    createdAt: '2024-01-11'
  },
  {
    id: '3',
    userId: '2',
    roomId: '4',
    roomCode: 'RM004',
    roomName: '第四会议室',
    date: today,
    startTime: '10:00',
    endTime: '12:00',
    meetingTopic: '项目小组会议',
    participantCount: 6,
    applicant: '张三',
    status: 'pending',
    createdAt: '2024-01-12'
  }
]

export const mockQueue: QueueItem[] = [
  {
    id: '1',
    userId: '3',
    date: today,
    startTime: '15:00',
    endTime: '17:00',
    meetingTopic: '学生会工作会议',
    participantCount: 12,
    applicant: '李四',
    priority: 1,
    createdAt: '2024-01-12'
  }
]

export const timeSlots = [
  '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
  '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
  '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
  '20:00', '20:30', '21:00'
]
