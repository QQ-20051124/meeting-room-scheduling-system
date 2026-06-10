<template>
  <view class="container">
    <view v-if="!isAdmin" class="not-admin">
      <text class="not-admin-icon">🔒</text>
      <text class="not-admin-text">仅管理员可查看</text>
    </view>

    <view v-else class="queue-content">
      <view class="queue-header">
        <text class="queue-title">等待队列</text>
        <text class="queue-count">共 {{ queue.length }} 人等待</text>
      </view>

      <view class="queue-list">
        <view 
          v-for="item in queue" 
          :key="item.id" 
          class="queue-card"
        >
          <view class="queue-rank">
            <text class="rank-num">{{ item.priority }}</text>
            <text class="rank-label">号</text>
          </view>
          <view class="queue-info">
            <view class="queue-applicant">申请人：{{ item.applicant }}</view>
            <view class="queue-topic">主题：{{ item.meetingTopic }}</view>
            <view class="queue-date">📅 {{ item.date }}</view>
            <view class="queue-time">🕐 {{ item.startTime }} - {{ item.endTime }}</view>
            <view class="queue-participants">👥 {{ item.participantCount }}人</view>
          </view>
          <view class="queue-actions">
            <view class="action-btn" @click="handleRemove(item.id)">移除</view>
          </view>
        </view>
      </view>

      <view v-if="queue.length === 0" class="empty-state">
        <text class="empty-icon">✅</text>
        <text class="empty-text">等待队列为空</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'

const reservationStore = useReservationStore()
const userStore = useUserStore()

const isAdmin = computed(() => userStore.isAdmin())
const queue = computed(() => {
  const q = [...reservationStore.queue]
  q.sort((a, b) => a.priority - b.priority)
  return q
})

function handleRemove(id: string) {
  uni.showModal({
    title: '确认移除',
    content: '确定要从等待队列中移除该申请吗？',
    success: (res) => {
      if (res.confirm) {
        reservationStore.removeFromQueue(id)
        uni.showToast({ title: '已移除', icon: 'success' })
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
}

.not-admin {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.not-admin-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.not-admin-text {
  font-size: 28rpx;
  color: $text-light;
}

.queue-content {
  padding-top: 10rpx;
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.queue-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
}

.queue-count {
  font-size: 26rpx;
  color: $primary-color;
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.queue-card {
  display: flex;
  background: $white;
  border-radius: $radius;
  padding: 24rpx;
  box-shadow: $shadow;
}

.queue-rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80rpx;
  height: 80rpx;
  background: $primary-color;
  border-radius: 50%;
  margin-right: 24rpx;
}

.rank-num {
  font-size: 28rpx;
  font-weight: bold;
  color: $white;
}

.rank-label {
  font-size: 18rpx;
  color: rgba(255, 255, 255, 0.8);
}

.queue-info {
  flex: 1;
}

.queue-applicant {
  font-size: $font-base;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.queue-topic {
  font-size: 26rpx;
  color: $text-secondary;
  margin-bottom: 8rpx;
}

.queue-date, .queue-time, .queue-participants {
  font-size: 24rpx;
  color: $text-light;
  margin-bottom: 4rpx;
}

.queue-actions {
  display: flex;
  align-items: center;
}

.action-btn {
  padding: 12rpx 24rpx;
  background: $error-color;
  color: $white;
  border-radius: 8rpx;
  font-size: 24rpx;
  
  &:active {
    background: darken($error-color, 10%);
  }
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
