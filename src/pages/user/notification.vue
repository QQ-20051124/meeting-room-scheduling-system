<template>
  <view class="container">
    <!-- 自定义导航栏 -->
    <view class="nav-bar">
      <view class="nav-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="nav-title">消息通知</text>
      <view class="nav-right">
        <text class="clear-btn" @click="clearAll">清空</text>
      </view>
    </view>

    <!-- 通知列表 -->
    <scroll-view class="notification-list" scroll-y>
      <view v-if="notifications.length === 0" class="empty-state">
        <text class="empty-icon">📭</text>
        <text class="empty-text">暂无新通知</text>
        <text class="empty-hint">有新消息会在这里显示</text>
      </view>
      
      <view 
        v-for="item in notifications" 
        :key="item.id" 
        class="notification-item"
        :class="{ read: item.read }"
        @click="markAsRead(item)"
      >
        <view class="notify-icon-wrap" :class="item.type">
          <text class="notify-icon">{{ getIcon(item.type) }}</text>
        </view>
        <view class="notify-content">
          <text class="notify-title">{{ item.title }}</text>
          <text class="notify-desc">{{ item.description }}</text>
          <text class="notify-time">{{ item.time }}</text>
        </view>
        <view v-if="!item.read" class="unread-dot"></view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Notification {
  id: number
  type: string
  title: string
  description: string
  time: string
  read: boolean
}

const notifications = ref<Notification[]>([
  {
    id: 1,
    type: 'approval',
    title: '预约审核通过',
    description: '您预约的「大会议室」已通过审核，请按时参加会议',
    time: '10分钟前',
    read: false
  },
  {
    id: 2,
    type: 'system',
    title: '系统维护通知',
    description: '系统将于今晚22:00-00:00进行维护升级，期间无法预约',
    time: '1小时前',
    read: false
  },
  {
    id: 3,
    type: 'conflict',
    title: '预约冲突提醒',
    description: '您预约的「小会议室」与其他会议时间冲突，已自动调整',
    time: '2小时前',
    read: true
  },
  {
    id: 4,
    type: 'queue',
    title: '等待队列通知',
    description: '您在「中会议室」等待队列中已排至第一位',
    time: '3小时前',
    read: true
  },
  {
    id: 5,
    type: 'reminder',
    title: '会议即将开始',
    description: '您预约的「大会议室」会议将在30分钟后开始',
    time: '昨天',
    read: true
  }
])

function goBack() {
  uni.navigateBack()
}

function getIcon(type: string) {
  const icons: Record<string, string> = {
    approval: '✅',
    rejection: '❌',
    conflict: '⚠️',
    queue: '🔄',
    reminder: '⏰',
    system: '📢',
    maintenance: '🔧',
    cancellation: '🚫'
  }
  return icons[type] || '📄'
}

function markAsRead(item: Notification) {
  if (!item.read) {
    item.read = true
  }
}

function clearAll() {
  uni.showModal({
    title: '确认清空',
    content: '确定要清空所有通知吗？',
    success: (res) => {
      if (res.confirm) {
        notifications.value = []
        uni.showToast({ title: '已清空', icon: 'success' })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: $bg-color;
}

/* 导航栏 */
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 88rpx;
  padding: 0 30rpx;
  background: $white;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.nav-back {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:active {
    opacity: 0.7;
  }
}

.back-icon {
  font-size: 40rpx;
  color: $text-color;
}

.nav-title {
  font-size: 34rpx;
  font-weight: 600;
  color: $text-color;
}

.nav-right {
  width: 60rpx;
  text-align: right;
}

.clear-btn {
  font-size: 28rpx;
  color: $primary-color;
  
  &:active {
    opacity: 0.7;
  }
}

/* 通知列表 */
.notification-list {
  height: calc(100vh - 88rpx);
  padding: 20rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 30rpx;
}

.empty-text {
  font-size: 32rpx;
  color: $text-color;
  margin-bottom: 10rpx;
}

.empty-hint {
  font-size: 26rpx;
  color: $text-light;
}

/* 通知项 */
.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 30rpx;
  background: $white;
  border-radius: $radius;
  margin-bottom: 20rpx;
  
  &.read {
    opacity: 0.6;
  }
  
  &:active {
    background: $bg-color;
  }
}

.notify-icon-wrap {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
  
  &.approval {
    background: rgba($success-color, 0.1);
  }
  
  &.rejection, &.cancellation {
    background: rgba($error-color, 0.1);
  }
  
  &.conflict {
    background: rgba($warning-color, 0.1);
  }
  
  &.queue {
    background: rgba($primary-color, 0.1);
  }
  
  &.reminder {
    background: rgba(#FF9500, 0.1);
  }
  
  &.system, &.maintenance {
    background: rgba(#999999, 0.1);
  }
}

.notify-icon {
  font-size: 36rpx;
}

.notify-content {
  flex: 1;
  min-width: 0;
}

.notify-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 8rpx;
}

.notify-desc {
  display: block;
  font-size: 26rpx;
  color: $text-secondary;
  margin-bottom: 12rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notify-time {
  font-size: 24rpx;
  color: $text-light;
}

.unread-dot {
  width: 16rpx;
  height: 16rpx;
  background: $error-color;
  border-radius: 50%;
  margin-top: 10rpx;
}
</style>
