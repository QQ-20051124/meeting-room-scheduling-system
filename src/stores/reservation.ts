import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Reservation, QueueItem } from '@/types'
import { mockReservations, mockQueue } from '@/data/mock'

export const useReservationStore = defineStore('reservation', () => {
  const reservations = ref<Reservation[]>([...mockReservations])
  const queue = ref<QueueItem[]>([...mockQueue])

  function addReservation(reservation: Omit<Reservation, 'id' | 'createdAt'>): Reservation {
    const newReservation: Reservation = {
      ...reservation,
      id: String(Date.now()),
      createdAt: new Date().toISOString().split('T')[0]
    }
    reservations.value.push(newReservation)
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
      processQueue()
      return true
    }
    return false
  }

  function approveReservation(id: string): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      reservation.status = 'approved'
      return true
    }
    return false
  }

  function rejectReservation(id: string): boolean {
    const reservation = reservations.value.find(r => r.id === id)
    if (reservation) {
      reservation.status = 'rejected'
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
