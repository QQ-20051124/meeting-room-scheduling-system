<template>
  <view class="stats-view">
    <view class="stats-header">
      <view class="header-title"> 数据统计</view>
      <view class="header-period">{{ periodText }}</view>
    </view>

    <view class="stats-cards">
      <view class="stat-card primary">
        <view class="stat-icon"></view>
        <view class="stat-info">
          <view class="stat-value">{{ totalRooms }}</view>
          <view class="stat-label">总会议室数</view>
        </view>
      </view>

      <view class="stat-card success">
        <view class="stat-icon">✅</view>
        <view class="stat-info">
          <view class="stat-value">{{ todayReservations }}</view>
          <view class="stat-label">今日预约</view>
        </view>
      </view>

      <view class="stat-card warning">
        <view class="stat-icon">⏳</view>
        <view class="stat-info">
          <view class="stat-value">{{ pendingCount }}</view>
          <view class="stat-label">待审核</view>
        </view>
      </view>

      <view class="stat-card info">
        <view class="stat-icon"></view>
        <view class="stat-info">
          <view class="stat-value">{{ totalUsers }}</view>
          <view class="stat-label">总用户数</view>
        </view>
      </view>
    </view>

    <view class="stats-section">
      <view class="section-title">按用户类型统计</view>
      <view class="role-stats">
        <view class="role-item">
          <view class="role-label">👨‍🎓 学生</view>
          <view class="role-bar">
            <view class="role-fill student" :style="{ width: studentPercent + '%' }"></view>
          </view>
          <view class="role-value">{{ studentCount }} ({{ studentPercent }}%)</view>
        </view>
        <view class="role-item">
          <view class="role-label">👨‍ 教师</view>
          <view class="role-bar">
            <view class="role-fill teacher" :style="{ width: teacherPercent + '%' }"></view>
          </view>
          <view class="role-value">{{ teacherCount }} ({{ teacherPercent }}%)</view>
        </view>
        <view class="role-item">
          <view class="role-label">🏢 组织</view>
          <view class="role-bar">
            <view class="role-fill org" :style="{ width: orgPercent + '%' }"></view>
          </view>
          <view class="role-value">{{ orgCount }} ({{ orgPercent }}%)</view>
        </view>
      </view>
    </view>

    <view class="stats-section">
      <view class="section-title">会议室使用率</view>
      <view class="room-usage-list">
        <view class="room-usage-item" v-for="room in roomUsage" :key="room.id">
          <view class="room-name">{{ room.name }}</view>
          <view class="usage-bar">
            <view class="usage-fill" :style="{ width: room.usagePercent + '%' }"></view>
          </view>
          <view class="usage-value">{{ room.usageCount }}次 ({{ room.usagePercent }}%)</view>
        </view>
      </view>
    </view>

    <view class="stats-section" v-if="recentReservations.length > 0">
      <view class="section-title">最近预约</view>
      <view class="recent-list">
        <view class="recent-item" v-for="res in recentReservations.slice(0, 5)" :key="res.id">
          <view class="recent-info">
            <view class="recent-room">{{ res.roomName }}</view>
            <view class="recent-topic">{{ res.meetingTopic }}</view>
          </view>
          <view class="recent-meta">
            <view class="recent-date">{{ res.date }}</view>
            <view :class="['recent-status', res.status]">{{ getStatusText(res.status) }}</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Reservation, User, Room } from '@/types'
import { getToday } from '@/utils/date'

interface Props {
  reservations?: Reservation[]
  users?: User[]
  rooms?: Room[]
}

const props = withDefaults(defineProps<Props>(), {
  reservations: () => [],
  users: () => [],
  rooms: () => []
})

const periodText = computed(() => {
  const today = new Date()
  return `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate()}日`
})

const totalRooms = computed(() => props.rooms.length)

const todayReservations = computed(() => {
  const today = getToday()
  return props.reservations.filter(r => r.date === today).length
})

const pendingCount = computed(() => {
  return props.reservations.filter(r => r.status === 'pending').length
})

const totalUsers = computed(() => props.users.length)

const studentCount = computed(() => props.users.filter(u => u.role === 'student').length)
const teacherCount = computed(() => props.users.filter(u => u.role === 'teacher').length)
const orgCount = computed(() => props.users.filter(u => u.role === 'organization').length)

const studentPercent = computed(() => totalUsers.value > 0 ? Math.round(studentCount.value / totalUsers.value * 100) : 0)
const teacherPercent = computed(() => totalUsers.value > 0 ? Math.round(teacherCount.value / totalUsers.value * 100) : 0)
const orgPercent = computed(() => totalUsers.value > 0 ? Math.round(orgCount.value / totalUsers.value * 100) : 0)

const roomUsage = computed(() => {
  return props.rooms.map(room => {
    const usageCount = props.reservations.filter(r => r.roomId === room.id).length
    const maxUsage = Math.max(...props.rooms.map(r => props.reservations.filter(res => res.roomId === r.id).length), 1)
    const usagePercent = Math.round((usageCount / maxUsage) * 100)
    return {
      id: room.id,
      name: room.name,
      usageCount,
      usagePercent
    }
  }).sort((a, b) => b.usageCount - a.usageCount)
})

const recentReservations = computed(() => {
  return [...props.reservations].sort((a, b) => {
    const dateA = new Date(a.createdAt + 'T' + a.startTime).getTime()
    const dateB = new Date(b.createdAt + 'T' + b.startTime).getTime()
    return dateB - dateA
  })
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
</script>

<style lang="scss" scoped>
.stats-view {
  background: $white;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  box-shadow: $shadow;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.header-title {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-color;
}

.header-period {
  font-size: 24rpx;
  color: $text-light;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  border-radius: $radius;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  
  &.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    
    .stat-icon, .stat-value, .stat-label {
      color: $white;
    }
  }
  
  &.success {
    background: linear-gradient(135deg, #0ba360, #3cba92);
    
    .stat-icon, .stat-value, .stat-label {
      color: $white;
    }
  }
  
  &.warning {
    background: linear-gradient(135deg, #f093fb, #f5576c);
    
    .stat-icon, .stat-value, .stat-label {
      color: $white;
    }
  }
  
  &.info {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    
    .stat-icon, .stat-value, .stat-label {
      color: $white;
    }
  }
}

.stat-icon {
  font-size: 48rpx;
  margin-right: $spacing-md;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: $text-color;
  line-height: 1;
}

.stat-label {
  font-size: 22rpx;
  color: $text-secondary;
  margin-top: 8rpx;
}

.stats-section {
  margin-bottom: $spacing-lg;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: $spacing-md;
  padding-left: $spacing-xs;
  border-left: 4rpx solid $primary-color;
}

.role-stats {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.role-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.role-label {
  min-width: 140rpx;
  font-size: 26rpx;
  color: $text-color;
}

.role-bar {
  flex: 1;
  height: 20rpx;
  background: #e9ecef;
  border-radius: $radius-full;
  overflow: hidden;
}

.role-fill {
  height: 100%;
  border-radius: $radius-full;
  transition: width 0.3s ease;
  
  &.student {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
  }
  
  &.teacher {
    background: linear-gradient(90deg, #0ba360, #3cba92);
  }
  
  &.org {
    background: linear-gradient(90deg, #f093fb, #f5576c);
  }
}

.role-value {
  min-width: 120rpx;
  font-size: 24rpx;
  color: $text-secondary;
  text-align: right;
}

.room-usage-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.room-usage-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.room-name {
  min-width: 160rpx;
  font-size: 26rpx;
  color: $text-color;
  font-weight: 600;
}

.usage-bar {
  flex: 1;
  height: 16rpx;
  background: #e9ecef;
  border-radius: $radius-full;
  overflow: hidden;
}

.usage-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: $radius-full;
  transition: width 0.3s ease;
}

.usage-value {
  min-width: 140rpx;
  font-size: 24rpx;
  color: $text-secondary;
  text-align: right;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md;
  background: #f8f9fa;
  border-radius: $radius;
  border-left: 4rpx solid $primary-color;
}

.recent-info {
  flex: 1;
  
  .recent-room {
    font-size: 26rpx;
    font-weight: bold;
    color: $text-color;
  }
  
  .recent-topic {
    font-size: 24rpx;
    color: $text-secondary;
    margin-top: 4rpx;
  }
}

.recent-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8rpx;
  
  .recent-date {
    font-size: 24rpx;
    color: $text-light;
  }
  
  .recent-status {
    font-size: 22rpx;
    padding: 6rpx 16rpx;
    border-radius: $radius-full;
    font-weight: 600;
    
    &.pending {
      background: rgba(#F59E0B, 0.1);
      color: #F59E0B;
    }
    
    &.approved {
      background: rgba(#10B981, 0.1);
      color: #10B981;
    }
    
    &.rejected {
      background: rgba(#EF4444, 0.1);
      color: #EF4444;
    }
    
    &.completed {
      background: rgba(#3B82F6, 0.1);
      color: #3B82F6;
    }
    
    &.cancelled {
      background: rgba(#6B7280, 0.1);
      color: #6B7280;
    }
  }
}
</style>
