import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { mockUsers } from '@/data/mock'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)

  function login(username: string, password: string): boolean {
    const user = mockUsers.find(u => u.username === username && u.password === password)
    if (user) {
      currentUser.value = user
      uni.setStorageSync('currentUser', JSON.stringify(user))
      return true
    }
    return false
  }

  function logout() {
    currentUser.value = null
    uni.removeStorageSync('currentUser')
  }

  function register(user: Omit<User, 'id' | 'createdAt'>): boolean {
    const exists = mockUsers.find(u => u.username === user.username)
    if (exists) {
      return false
    }
    const newUser: User = {
      ...user,
      id: String(Date.now()),
      createdAt: new Date().toISOString().split('T')[0]
    }
    mockUsers.push(newUser)
    currentUser.value = newUser
    uni.setStorageSync('currentUser', JSON.stringify(newUser))
    return true
  }

  function updateUser(updatedUser: Partial<User>) {
    if (currentUser.value) {
      Object.assign(currentUser.value, updatedUser)
      uni.setStorageSync('currentUser', JSON.stringify(currentUser.value))
    }
  }

  function loadUser() {
    const stored = uni.getStorageSync('currentUser')
    if (stored) {
      currentUser.value = JSON.parse(stored)
    }
  }

  const isAdmin = () => currentUser.value?.role === 'admin'
  const isLoggedIn = () => currentUser.value !== null

  return {
    currentUser,
    login,
    logout,
    register,
    updateUser,
    loadUser,
    isAdmin,
    isLoggedIn
  }
})
