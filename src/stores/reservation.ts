import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Reservation, QueueItem } from '@/types'
import { mockReservations, mockQueue } from '@/data/mock'
import { notifyConflict, notifyApproval, notifyRejection, notifyCancellation, notifyQueueTurn } from '@/utils/notification'

export const useReservationStore = defineStore('reservation', () => {
  const reservations = ref<Reservation[]>([...mockReservations])
  const queue = ref<QueueItem[]>([...mockQueue])

  function checkConflict(roomId: string, date: string, startTime: string, endTime: string, excludeId?: string): { hasConflict: boolean, reason?: string } {
    const conflicting = reservations.value.find(r => {
      if (r.id === excludeId) return false
      if (r.roomId !== roomId) return false
      if (r.date !== date) return false
      if (r.status === 'cancelled' || r.status === 'rejected') return false
      return !(endTime <= r.startTime || startTime >= r.endTime)
    })
    
    if (conflicting) {
      return {
        hasConflict: true,
        reason: `该时段已被"${conflicting.applicant}"预约用于"${conflicting.meetingTopic}"`
      }
    }
    return { hasConflict: false }
  }

  function addReservation(reservation: Omit<Reservation, 'id' | 'createdAt'>): Reservation {
    // 检查是否有冲突
    const conflict = checkConflict(reservation.roomId, reservation.date, reservation.startTime, reservation.endTime)
    
    const newReservation: Reservation = {
      ...reservation,
      id: String(Date.now()),
      createdAt: new Date().toISOString().split('T')[0],
      hasConflict: conflict.hasConflict,
      conflictReason: conflict.reason,
      notified: false
    }
    
    if (conflict.hasConflict) {
      // 如果有冲突，添加到等待队列
      notifyConflict(reservation.roomName, reservation.date, `${reservation.startTime}-${reservation.endTime}`, conflict.reason!)
      addToQueue({
        userId: reservation.userId,
        date: reservation.date,
        startTime: reservation.startTime,
        endTime: reservation.endTime,
        meetingTopic: reservation.meetingTopic,
        participantCount: reservation.participantCount,
        applicant: reservation.applicant
      })
    } else {
      reservations.value.push(newReservation)
      notifyApproval(reservation.roomName, reservation.date, `${reservation.startTime}-${reservation.endTime}`)
    }
    
    return newReservation
  }

  function updateReservation(id: string, updates: Partial<Reservation>): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      Object.assign(reservation, updates)
      return true
    }
    return false
  }

  function cancelReservation(id: string): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      reservation.status = 'cancelled'
      notifyCancellation(reservation.roomName, reservation.date)
      processQueue()
      return true
    }
    return false
  }

  function approveReservation(id: string): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      reservation.status = 'approved'
      reservation.notified = true
      notifyApproval(reservation.roomName, reservation.date, `${reservation.startTime}-${reservation.endTime}`)
      return true
    }
    return false
  }

  function rejectReservation(id: string, reason?: string): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      reservation.status = 'rejected'
      notifyRejection(reservation.roomName, reason || '未知原因')
      return true
    }
    return false
  }

  function addToQueue(item: Omit<QueueItem, 'id' | 'createdAt' | 'priority'>): QueueItem {
    const newItem: QueueItem = {
      ...item,
      id: String(Date.now()),
      createdAt: new Date().toISOString().split('T')[0],
      priority: queue.value.length + 1
    }
    queue.value.push(newItem)
    return newItem
  }

  function removeFromQueue(id: string): boolean {
    const index = queue.value.findIndex(q => q.id === id)
    if (index !== -1) {
      queue.value.splice(index, 1)
      queue.value.forEach((q, i) => { q.priority = i + 1 })
      return true
    }
    return false
  }

  function processQueue() {
    queue.value.sort((a, b) => a.priority - b.priority)
    
    // 检查队列中的预约是否有可用的会议室
    const availableSpots = queue.value.filter((item, index) => {
      const room = item as any
      const hasConflict = checkConflict(room.roomId || '', item.date, item.startTime, item.endTime)
      return !hasConflict.hasConflict
    })
    
    if (availableSpots.length > 0) {
      const firstItem = availableSpots[0]
      notifyQueueTurn(firstItem.userId, firstItem.meetingTopic, firstItem.date, `${firstItem.startTime}-${firstItem.endTime}`)
    }
  }

  function isRoomAvailable(roomId: string, date: string, startTime: string, endTime: string): boolean {
    const conflicting = reservations.value.some(r => {
      if (r.roomId !== roomId) return false
      if (r.date !== date) return false
      if (r.status === 'cancelled' || r.status === 'rejected') return false
      return !(endTime <= r.startTime || startTime >= r.endTime)
    })
    return !conflicting
  }

  const userReservations = computed(() => (userId: string) => {
    return reservations.value.filter(r => r.userId === userId)
  })

  const pendingReservations = computed(() => {
    return reservations.value.filter(r => r.status === 'pending')
  })

  const getRoomSchedule = computed(() => (roomId: string, date: string) => {
    return reservations.value.filter(r => r.roomId === roomId && r.date === date)
  })

  return {
    reservations,
    queue,
    addReservation,
    updateReservation,
    cancelReservation,
    approveReservation,
    rejectReservation,
    addToQueue,
    removeFromQueue,
    processQueue,
    isRoomAvailable,
    userReservations,
    pendingReservations,
    getRoomSchedule
  }
})
