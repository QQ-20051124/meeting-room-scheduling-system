<template>
  <view class="container">
    <view v-if="!isLoggedIn" class="not-login">
      <view class="not-login-icon">👤</view>
      <text class="not-login-text">请先登录</text>
      <view class="btn-primary mt-30" @click="goToLogin">立即登录</view>
    </view>

    <view v-else class="profile-content">
      <view class="profile-header">
        <view class="avatar">
          <text class="avatar-text">{{ currentUser?.realName?.charAt(0) }}</text>
        </view>
        <view class="user-info">
          <text class="user-name">{{ currentUser?.realName }}</text>
          <text class="user-role">{{ currentUser?.role === 'admin' ? '管理员' : '普通用户' }}</text>
        </view>
      </view>

      <view class="menu-list">
        <view class="menu-item" @click="goToEditProfile">
          <text class="menu-icon">👤</text>
          <text class="menu-text">个人信息维护</text>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goToReservations">
          <text class="menu-icon">📅</text>
          <text class="menu-text">我的预约</text>
          <text class="menu-arrow">›</text>
        </view>
        <view v-if="isAdmin" class="menu-item" @click="goToAdmin">
          <text class="menu-icon">⚙️</text>
          <text class="menu-text">后台管理</text>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="handleLogout">
          <text class="menu-icon">🚪</text>
          <text class="menu-text">退出登录</text>
          <text class="menu-arrow">›</text>
        </view>
      </view>

      <view class="info-card">
        <text class="info-title">账户信息</text>
        <view class="info-row">
          <text class="info-label">用户名</text>
          <text class="info-value">{{ currentUser?.username }}</text>
        </view>
        <view class="info-row">
          <text class="info-label">邮箱</text>
          <text class="info-value">{{ currentUser?.email || '未填写' }}</text>
        </view>
        <view class="info-row">
          <text class="info-label">手机号</text>
          <text class="info-value">{{ currentUser?.phone || '未填写' }}</text>
        </view>
        <view class="info-row">
          <text class="info-label">注册时间</text>
          <text class="info-value">{{ currentUser?.createdAt }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn())
const currentUser = computed(() => userStore.currentUser)
const isAdmin = computed(() => userStore.isAdmin())

function goToLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}

function goToEditProfile() {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

function goToReservations() {
  uni.switchTab({ url: '/pages/reservation/list' })
}

function goToAdmin() {
  uni.navigateTo({ url: '/pages/admin/index' })
}

function handleLogout() {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.showToast({ title: '退出成功', icon: 'success' })
      }
    }
  })
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
  padding-bottom: 180rpx;
}

.not-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.not-login-icon {
  font-size: 120rpx;
  margin-bottom: 30rpx;
}

.not-login-text {
  font-size: 32rpx;
  color: $text-secondary;
}

.profile-content {
  padding: 20rpx;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 40rpx 30rpx;
  background: linear-gradient(135deg, $primary-color, $primary-light);
  border-radius: $radius;
  margin-bottom: 20rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 30rpx;
}

.avatar-text {
  font-size: 48rpx;
  color: $white;
  font-weight: bold;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 36rpx;
  font-weight: bold;
  color: $white;
  margin-bottom: 8rpx;
}

.user-role {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.menu-list {
  background: $white;
  border-radius: $radius;
  margin-bottom: 20rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:active {
    background: $bg-color;
  }
}

.menu-icon {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.menu-text {
  flex: 1;
  font-size: 28rpx;
  color: $text-color;
}

.menu-arrow {
  font-size: 36rpx;
  color: $text-light;
}

.info-card {
  background: $white;
  border-radius: $radius;
  padding: 30rpx;
}

.info-title {
  font-size: 30rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 20rpx;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
}

.info-label {
  font-size: 26rpx;
  color: $text-secondary;
}

.info-value {
  font-size: 26rpx;
  color: $text-color;
}
</style>
