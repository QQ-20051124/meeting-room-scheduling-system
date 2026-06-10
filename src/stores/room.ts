import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Room } from '@/types'
import { mockRooms } from '@/data/mock'

export const useRoomStore = defineStore('room', () => {
  const rooms = ref<Room[]>([])

  function loadRooms() {
    rooms.value = [...mockRooms]
  }

  function addRoom(room: Omit<Room, 'id' | 'createdAt'>): Room {
    const newRoom: Room = {
      ...room,
      id: String(Date.now()),
      createdAt: new Date().toISOString().split('T')[0]
    }
    rooms.value.push(newRoom)
    return newRoom
  }

  function deleteRoom(id: string): boolean {
    const index = rooms.value.findIndex(r => r.id === id)
    if (index !== -1) {
      rooms.value.splice(index, 1)
      return true
    }
    return false
  }

  function updateRoom(id: string, updates: Partial<Room>): boolean {
    const room = rooms.value.find(r => r.id === id)
    if (room) {
      Object.assign(room, updates)
      return true
    }
    return false
  }

  function getRoomById(id: string): Room | undefined {
    return rooms.value.find(r => r.id === id)
  }

  function getAvailableRooms(date: string, startTime: string, endTime: string, participantCount: number): Room[] {
    return rooms.value.filter(r => {
      if (r.status !== 'available') return false
      if (r.capacity < participantCount) return false
      return true
    })
  }

  return {
    rooms,
    loadRooms,
    addRoom,
    deleteRoom,
    updateRoom,
    getRoomById,
    getAvailableRooms
  }
})
