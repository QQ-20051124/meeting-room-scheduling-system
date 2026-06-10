<template>
  <view class="container">
    <view class="header">
      <view class="logo">
        <text class="logo-text">会议室调度系统</text>
        <text class="logo-sub">校园专属</text>
      </view>
    </view>

    <view v-if="!isLoggedIn" class="auth-section">
      <view class="card">
        <view class="btn-primary" @click="goToLogin">用户登录</view>
        <view class="btn-secondary mt-20" @click="goToRegister">用户注册</view>
      </view>
    </view>

    <view v-else class="main-section">
      <view class="greeting">
        <text class="greeting-text">欢迎, {{ currentUser?.realName }}</text>
        <text class="greeting-role">{{ currentUser?.role === 'admin' ? '管理员' : '普通用户' }}</text>
      </view>

      <view class="quick-actions">
        <view class="action-card" @click="goToRoomList">
          <view class="action-icon">🏢</view>
          <text class="action-title">查看会议室</text>
          <text class="action-desc">浏览可用会议室</text>
        </view>
        <view class="action-card" @click="goToApply">
          <view class="action-icon">📅</view>
          <text class="action-title">预约会议室</text>
          <text class="action-desc">申请使用会议室</text>
        </view>
        <view class="action-card" @click="goToAutoAssign">
          <view class="action-icon">🤖</view>
          <text class="action-title">自动分配</text>
          <text class="action-desc">智能匹配会议室</text>
        </view>
        <view class="action-card" v-if="isAdmin" @click="goToAdmin">
          <view class="action-icon">⚙️</view>
          <text class="action-title">后台管理</text>
          <text class="action-desc">管理系统设置</text>
        </view>
      </view>

      <view class="info-card">
        <view class="info-header">
          <text class="info-title">今日预约</text>
          <text class="info-count">{{ todayReservations.length }}</text>
        </view>
        <view class="info-list">
          <view v-for="res in todayReservations.slice(0, 3)" :key="res.id" class="info-item">
            <view class="info-room">{{ res.roomName }}</view>
            <view class="info-time">{{ res.startTime }} - {{ res.endTime }}</view>
            <view :class="['info-status', res.status]">{{ getStatusText(res.status) }}</view>
          </view>
          <view v-if="todayReservations.length === 0" class="info-empty">
            <text>暂无今日预约</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useReservationStore } from '@/stores/reservation'
import { getToday } from '@/utils/date'

const userStore = useUserStore()
const reservationStore = useReservationStore()

const isLoggedIn = computed(() => userStore.isLoggedIn())
const currentUser = computed(() => userStore.currentUser)
const isAdmin = computed(() => userStore.isAdmin())

const todayReservations = computed(() => {
  if (!userStore.currentUser) return []
  return reservationStore.userReservations(userStore.currentUser.id).filter(r => r.date === getToday())
})

function getStatusText(status: string): string {
  const map: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}

function goToRegister() {
  uni.navigateTo({ url: '/pages/user/register' })
}

function goToRoomList() {
  uni.switchTab({ url: '/pages/room/list' })
}

function goToApply() {
  uni.navigateTo({ url: '/pages/reservation/apply' })
}

function goToAutoAssign() {
  uni.navigateTo({ url: '/pages/reservation/auto' })
}

function goToAdmin() {
  uni.navigateTo({ url: '/pages/admin/index' })
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 40rpx 30rpx;
  padding-bottom: 180rpx;
}

.header {
  text-align: center;
  padding: 60rpx 0;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-text {
  font-size: 48rpx;
  font-weight: bold;
  color: $primary-color;
}

.logo-sub {
  font-size: 28rpx;
  color: $text-light;
  margin-top: 10rpx;
}

.auth-section {
  margin-top: 100rpx;
}

.greeting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40rpx;
  padding: 30rpx;
  background: $white;
  border-radius: $radius;
}

.greeting-text {
  font-size: 36rpx;
  font-weight: bold;
  color: $text-color;
}

.greeting-role {
  font-size: 24rpx;
  color: $primary-color;
  background: rgba($primary-color, 0.1);
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
  margin-bottom: 40rpx;
}

.action-card {
  background: $white;
  border-radius: $radius;
  padding: 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: $shadow;
  
  &:active {
    opacity: 0.8;
  }
}

.action-icon {
  font-size: 60rpx;
  margin-bottom: 16rpx;
}

.action-title {
  font-size: 28rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 8rpx;
}

.action-desc {
  font-size: 22rpx;
  color: $text-light;
}

.info-card {
  background: $white;
  border-radius: $radius;
  box-shadow: $shadow;
  overflow: hidden;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 30rpx;
  border-bottom: 2rpx solid $border-color;
}

.info-title {
  font-size: 30rpx;
  font-weight: bold;
  color: $text-color;
}

.info-count {
  font-size: 28rpx;
  color: $primary-color;
  font-weight: bold;
}

.info-list {
  padding: 20rpx;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
}

.info-room {
  flex: 2;
  font-size: 26rpx;
  color: $text-color;
}

.info-time {
  flex: 2;
  font-size: 24rpx;
  color: $text-secondary;
  text-align: center;
}

.info-status {
  flex: 1;
  font-size: 22rpx;
  text-align: right;
  
  &.pending {
    color: $warning-color;
  }
  &.approved {
    color: $success-color;
  }
  &.rejected, &.cancelled {
    color: $error-color;
  }
  &.completed {
    color: $text-light;
  }
}

.info-empty {
  text-align: center;
  padding: 40rpx;
  color: $text-light;
}
</style>
