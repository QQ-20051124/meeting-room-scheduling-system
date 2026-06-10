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
      createdAt: new Date().toISOString().split('T')[0],
      schoolId: '',
      isCertified: false
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

  function certify(certInfo: { schoolId: string; realName: string; phone: string; email: string; role: string }): boolean {
    if (!currentUser.value) return false
    
    currentUser.value.schoolId = certInfo.schoolId
    currentUser.value.realName = certInfo.realName
    currentUser.value.phone = certInfo.phone
    currentUser.value.email = certInfo.email
    currentUser.value.role = certInfo.role
    currentUser.value.isCertified = true
    
    uni.setStorageSync('currentUser', JSON.stringify(currentUser.value))
    return true
  }

  function changePassword(oldPassword: string, newPassword: string): boolean {
    if (!currentUser.value) return false
    
    if (currentUser.value.password !== oldPassword) {
      return false
    }
    
    currentUser.value.password = newPassword
    uni.setStorageSync('currentUser', JSON.stringify(currentUser.value))
    return true
  }

  const isAdmin = () => currentUser.value?.role === 'admin'
  const isLoggedIn = () => currentUser.value !== null
  const isCertified = () => currentUser.value?.isCertified === true

  return {
    currentUser,
    login,
    logout,
    register,
    updateUser,
    loadUser,
    certify,
    changePassword,
    isAdmin,
    isLoggedIn,
    isCertified
  }
})
