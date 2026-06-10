<template>
  <view class="container">
    <view v-if="!isLoggedIn" class="not-login">
      <text class="not-login-icon">👤</text>
      <text class="not-login-text">请先登录</text>
      <view class="btn-primary mt-30" @click="goToLogin">立即登录</view>
    </view>

    <view v-else class="reservation-content">
      <view class="tabs">
        <view 
          v-for="tab in tabs" 
          :key="tab.value"
          :class="['tab-item', { active: activeTab === tab.value }]"
          @click="activeTab = tab.value"
        >
          {{ tab.label }}
        </view>
      </view>

      <view class="reservation-list">
        <view 
          v-for="res in filteredReservations" 
          :key="res.id" 
          class="reservation-card"
        >
          <view class="res-header">
            <view class="res-room">
              <text class="room-code">{{ res.roomCode }}</text>
              <text class="room-name">{{ res.roomName }}</text>
            </view>
            <view :class="['res-status', res.status]">{{ getStatusText(res.status) }}</view>
          </view>

          <view class="res-date">📅 {{ res.date }}</view>
          <view class="res-time">🕐 {{ res.startTime }} - {{ res.endTime }}</view>
          <view class="res-topic">📋 {{ res.meetingTopic }}</view>
          <view class="res-participants">👥 {{ res.participantCount }}人</view>

          <view class="res-actions">
            <view 
              v-if="res.status === 'pending'" 
              class="btn-secondary"
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

      <view v-if="filteredReservations.length === 0" class="empty-state">
        <text class="empty-icon">📅</text>
        <text class="empty-text">暂无{{ tabs.find(t => t.value === activeTab)?.label }}记录</text>
      </view>
    </view>
    
    <!-- 自定义底部导航 -->
    <CustomTabbar current="reservation" />
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'
import { getToday, isBefore, isTimeBefore } from '@/utils/date'
import CustomTabbar from '@/components/custom-tabbar/CustomTabbar.vue'

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

onMounted(() => {
  userStore.loadUser()
  isLoggedIn.value = userStore.isLoggedIn()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
  padding-bottom: 280rpx;
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

.reservation-content {
  padding-top: 10rpx;
}

.tabs {
  display: flex;
  background: $white;
  border-radius: $radius;
  padding: 10rpx;
  margin-bottom: 20rpx;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 20rpx;
  font-size: 26rpx;
  color: $text-secondary;
  border-radius: 8rpx;
  
  &.active {
    background: $primary-color;
    color: $white;
  }
}

.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.reservation-card {
  background: $white;
  border-radius: $radius;
  padding: 30rpx;
  box-shadow: $shadow;
}

.res-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.res-room {
  display: flex;
  align-items: center;
}

.room-code {
  font-size: 24rpx;
  color: $primary-color;
  font-weight: bold;
  margin-right: 10rpx;
}

.room-name {
  font-size: 28rpx;
  color: $text-color;
  font-weight: bold;
}

.res-status {
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  
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
    background: rgba($text-light, 0.1);
    color: $text-light;
  }
}

.res-date, .res-time, .res-topic, .res-participants {
  font-size: 26rpx;
  color: $text-secondary;
  margin-bottom: 10rpx;
}

.res-actions {
  margin-top: 20rpx;
  display: flex;
  gap: 20rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: $text-light;
}
</style>
