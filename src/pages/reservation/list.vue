<template>
  <view class="container">
    <!-- 未登录状态 -->
    <view v-if="!isLoggedIn" class="not-login-section">
      <view class="not-login-card">
        <view class="not-login-icon">◯</view>
        <text class="not-login-title">请先登录</text>
        <text class="not-login-desc">登录后可查看您的预约记录</text>
        <view class="btn-primary mt-lg" @click="goToLogin">立即登录</view>
      </view>
    </view>

    <!-- 登录后内容 -->
    <view v-else class="reservation-content">
      <!-- 标签页 -->
      <view class="tabs-wrapper">
        <view class="tabs">
          <view 
            v-for="tab in tabs" 
            :key="tab.value"
            :class="['tab-item', { active: activeTab === tab.value }]"
            @click="activeTab = tab.value"
          >
            {{ tab.label }}
            <view v-if="getTabCount(tab.value) > 0" class="tab-badge">{{ getTabCount(tab.value) }}</view>
          </view>
        </view>
      </view>

      <!-- 预约列表 -->
      <view class="reservation-list">
        <view 
          v-for="res in filteredReservations" 
          :key="res.id" 
          class="reservation-card"
        >
          <!-- 卡片头部 -->
          <view class="card-header">
            <view class="room-info">
              <text class="room-code">{{ res.roomCode }}</text>
              <text class="room-name">{{ res.roomName }}</text>
            </view>
            <view :class="['status-tag', res.status]">{{ getStatusText(res.status) }}</view>
          </view>
          
          <!-- 会议主题 -->
          <view class="meeting-info">
            <text class="meeting-icon">◆</text>
            <text class="meeting-title">{{ res.meetingTopic }}</text>
          </view>
          
          <!-- 时间地点 -->
          <view class="time-location">
            <view class="time-item">
              <text class="time-icon">●</text>
              <text class="time-text">{{ res.date }} {{ res.startTime }} - {{ res.endTime }}</text>
            </view>
            <view class="time-item">
              <text class="time-icon">○</text>
              <text class="time-text">{{ res.participantCount }}人</text>
            </view>
          </view>
          
          <!-- 操作按钮 -->
          <view class="card-actions">
            <view 
              v-if="res.status === 'pending'" 
              class="btn-outline"
              @click="handleCancel(res.id)"
            >
              取消预约
            </view>
            <view 
              v-if="res.status === 'approved' && canCancel(res)" 
              class="btn-danger"
              @click="handleCancel(res.id)"
            >
              取消预约
            </view>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view v-if="filteredReservations.length === 0" class="empty-state">
        <view class="empty-icon">◉</view>
        <text class="empty-title">暂无{{ tabs.find(t => t.value === activeTab)?.label }}记录</text>
        <text class="empty-desc">{{ activeTab === 'all' ? '快去预约一个会议室吧' : '换个标签看看' }}</text>
        <view v-if="activeTab === 'all'" class="btn-secondary mt-lg" @click="goToApply">立即预约</view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'
import { getToday, isBefore, isTimeBefore } from '@/utils/date'

const reservationStore = useReservationStore()
const userStore = useUserStore()

const isLoggedIn = ref(false)
const activeTab = ref('all')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '待审核', value: 'pending' },
  { label: '已通过', value: 'approved' },
  { label: '已完成', value: 'completed' }
]

const userReservations = computed(() => {
  if (!userStore.currentUser) return []
  return reservationStore.userReservations(userStore.currentUser.id)
})

const filteredReservations = computed(() => {
  if (activeTab.value === 'all') {
    return userReservations.value
  }
  return userReservations.value.filter(r => r.status === activeTab.value)
})

function getTabCount(tabValue: string): number {
  if (tabValue === 'all') return userReservations.value.length
  return userReservations.value.filter(r => r.status === tabValue).length
}

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

function canCancel(res: any): boolean {
  const today = getToday()
  if (isBefore(res.date, today)) return false
  if (res.date === today && isTimeBefore(res.startTime, new Date().toTimeString().slice(0, 5))) {
    return false
  }
  return true
}

function handleCancel(id: string) {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消该预约吗？',
    success: (res) => {
      if (res.confirm) {
        reservationStore.cancelReservation(id)
        uni.showToast({ title: '已取消', icon: 'success' })
      }
    }
  })
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}

function goToApply() {
  uni.navigateTo({ url: '/pages/reservation/apply' })
}

onMounted(() => {
  userStore.loadUser()
  isLoggedIn.value = userStore.isLoggedIn()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: 180rpx;
}

/* ===== 未登录状态 ===== */
.not-login-section {
  padding: $spacing-xl;
}

.not-login-card {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-2xl;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: $shadow-lg;
}

.not-login-icon {
  width: 140rpx;
  height: 140rpx;
  border-radius: 50%;
  background: rgba($primary-color, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 70rpx;
  color: $primary-color;
  margin-bottom: $spacing-lg;
}

.not-login-title {
  font-size: $font-xl;
  font-weight: 600;
  color: $text-title;
  margin-bottom: $spacing-xs;
}

.not-login-desc {
  font-size: $font-sm;
  color: $text-muted;
  margin-bottom: $spacing-xl;
}

/* ===== 标签页 ===== */
.tabs-wrapper {
  padding: $spacing-lg;
  padding-bottom: 0;
}

.tabs {
  display: flex;
  background: $bg-card;
  border-radius: $radius-xl;
  padding: 8rpx;
  box-shadow: $shadow-sm;
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-sm;
  font-size: $font-sm;
  color: $text-secondary;
  border-radius: $radius-lg;
  transition: all 0.2s ease;
  position: relative;
  
  &.active {
    background: linear-gradient(135deg, $primary-color, $primary-dark);
    color: $white;
    
    .tab-badge {
      background: rgba(255, 255, 255, 0.3);
      color: $white;
    }
  }
}

.tab-badge {
  position: absolute;
  top: 8rpx;
  right: 16rpx;
  min-width: 32rpx;
  height: 32rpx;
  padding: 0 8rpx;
  border-radius: $radius-full;
  font-size: $font-xs;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba($primary-color, 0.1);
  color: $primary-color;
}

/* ===== 预约列表 ===== */
.reservation-list {
  padding: $spacing-lg;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.reservation-card {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-md;
  box-shadow: $shadow-sm;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}

.room-info {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.room-code {
  font-size: $font-xs;
  font-weight: 700;
  color: $primary-color;
}

.room-name {
  font-size: $font-md;
  font-weight: 600;
  color: $text-title;
}

.status-tag {
  font-size: $font-xs;
  padding: 6rpx 16rpx;
  border-radius: $radius-full;
  font-weight: 500;
  
  &.pending {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
  &.approved {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  &.rejected, &.cancelled {
    background: rgba($error-color, 0.1);
    color: $error-color;
  }
  &.completed {
    background: $bg-hover;
    color: $text-muted;
  }
}

.meeting-info {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  margin-bottom: $spacing-sm;
}

.meeting-icon {
  font-size: $font-sm;
  color: $primary-color;
}

.meeting-title {
  font-size: $font-base;
  color: $text-primary;
}

.time-location {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  margin-bottom: $spacing-md;
}

.time-item {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.time-icon {
  font-size: $font-xs;
  color: $text-light;
}

.time-text {
  font-size: $font-sm;
  color: $text-secondary;
}

.card-actions {
  display: flex;
  gap: $spacing-sm;
  padding-top: $spacing-sm;
  border-top: 1rpx solid $border-light;
}

.btn-outline {
  padding: $spacing-sm $spacing-md;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $text-primary;
  
  &:active {
    background: $bg-hover;
  }
}

.btn-danger {
  padding: $spacing-sm $spacing-md;
  background: rgba($error-color, 0.1);
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $error-color;
  
  &:active {
    background: rgba($error-color, 0.15);
  }
}

/* ===== 空状态 ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-3xl;
}

.empty-icon {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: $bg-hover;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
  color: $text-light;
  margin-bottom: $spacing-lg;
}

.empty-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.empty-desc {
  font-size: $font-sm;
  color: $text-muted;
}

.btn-primary, .btn-secondary {
  padding: $spacing-sm $spacing-xl;
  border-radius: $radius-lg;
  font-size: $font-base;
  font-weight: 500;
  
  &:active {
    opacity: 0.9;
  }
}

.btn-primary {
  background: linear-gradient(135deg, $primary-color, $primary-dark);
  color: $white;
}

.btn-secondary {
  background: $bg-card;
  color: $text-primary;
  border: 1rpx solid $border-color;
}

.mt-lg {
  margin-top: $spacing-lg;
}
</style>