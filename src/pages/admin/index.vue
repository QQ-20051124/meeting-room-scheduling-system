<template>
  <view class="container">
    <view v-if="!isAdmin" class="not-admin">
      <text class="not-admin-icon">🔒</text>
      <text class="not-admin-text">您不是管理员</text>
    </view>

    <view v-else class="admin-content">
      <view class="admin-header">
        <text class="admin-title">后台管理</text>
        <text class="admin-sub">系统管理中心</text>
      </view>

      <view class="admin-stats">
        <view class="stat-card">
          <text class="stat-value">{{ rooms.length }}</text>
          <text class="stat-label">会议室总数</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{ pendingReservations.length }}</text>
          <text class="stat-label">待审核预约</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{ queue.length }}</text>
          <text class="stat-label">等待队列</text>
        </view>
      </view>

      <view class="menu-list">
        <view class="menu-item" @click="goToRoomList">
          <text class="menu-icon">🏢</text>
          <view class="menu-info">
            <text class="menu-title">会议室管理</text>
            <text class="menu-desc">添加、删除、修改会议室</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goToPending">
          <text class="menu-icon">📋</text>
          <view class="menu-info">
            <text class="menu-title">预约审核</text>
            <text class="menu-desc">审核待处理的预约申请</text>
          </view>
          <view v-if="pendingReservations.length > 0" class="menu-badge">{{ pendingReservations.length }}</view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goToRecords">
          <text class="menu-icon">📊</text>
          <view class="menu-info">
            <text class="menu-title">后台记录</text>
            <text class="menu-desc">查看所有预约记录</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-item" @click="goToQueue">
          <text class="menu-icon">⏳</text>
          <view class="menu-info">
            <text class="menu-title">等待队列</text>
            <text class="menu-desc">管理预约等待列表</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>

      <view v-if="activeSection === 'pending'" class="pending-section">
        <view class="section-header">
          <text class="section-title">待审核预约</text>
          <text class="section-back" @click="activeSection = ''">返回</text>
        </view>
        <view class="pending-list">
          <view 
            v-for="res in pendingReservations" 
            :key="res.id" 
            class="pending-card"
          >
            <view class="pending-header">
              <text class="pending-room">{{ res.roomCode }} - {{ res.roomName }}</text>
            </view>
            <view class="pending-info">
              <text class="pending-applicant">申请人：{{ res.applicant }}</text>
              <text class="pending-topic">主题：{{ res.meetingTopic }}</text>
              <text class="pending-date">📅 {{ res.date }}</text>
              <text class="pending-time">🕐 {{ res.startTime }} - {{ res.endTime }}</text>
              <text class="pending-participants">👥 {{ res.participantCount }}人</text>
            </view>
            <view class="pending-actions">
              <view class="btn-success" @click="handleApprove(res.id)">通过</view>
              <view class="btn-reject" @click="handleReject(res.id)">拒绝</view>
            </view>
          </view>
        </view>
        <view v-if="pendingReservations.length === 0" class="empty-state">
          <text class="empty-text">暂无待审核预约</text>
        </view>
      </view>

      <view v-if="activeSection === 'records'" class="records-section">
        <view class="section-header">
          <text class="section-title">后台记录</text>
          <text class="section-back" @click="activeSection = ''">返回</text>
        </view>
        <view class="records-list">
          <view 
            v-for="res in allReservations" 
            :key="res.id" 
            class="record-card"
          >
            <view class="record-header">
              <text class="record-room">{{ res.roomCode }} - {{ res.roomName }}</text>
              <view :class="['record-status', res.status]">{{ getStatusText(res.status) }}</view>
            </view>
            <view class="record-info">
              <text>申请人：{{ res.applicant }}</text>
              <text>主题：{{ res.meetingTopic }}</text>
              <text>日期：{{ res.date }}</text>
              <text>时间：{{ res.startTime }} - {{ res.endTime }}</text>
              <text>人数：{{ res.participantCount }}人</text>
              <text>申请时间：{{ res.createdAt }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'

const roomStore = useRoomStore()
const reservationStore = useReservationStore()
const userStore = useUserStore()

const isAdmin = ref(false)
const activeSection = ref('')

const rooms = computed(() => roomStore.rooms)
const pendingReservations = computed(() => reservationStore.pendingReservations)
const queue = computed(() => reservationStore.queue)
const allReservations = computed(() => reservationStore.reservations)

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

function goToRoomList() {
  uni.switchTab({ url: '/pages/room/list' })
}

function goToPending() {
  activeSection.value = 'pending'
}

function goToRecords() {
  activeSection.value = 'records'
}

function goToQueue() {
  uni.navigateTo({ url: '/pages/queue/list' })
}

function handleApprove(id: string) {
  reservationStore.approveReservation(id)
  uni.showToast({ title: '已通过', icon: 'success' })
}

function handleReject(id: string) {
  reservationStore.rejectReservation(id)
  uni.showToast({ title: '已拒绝', icon: 'success' })
}

onMounted(() => {
  userStore.loadUser()
  isAdmin.value = userStore.isAdmin()
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

.admin-content {
  padding-top: 10rpx;
}

.admin-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.admin-title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 10rpx;
}

.admin-sub {
  font-size: 26rpx;
  color: $text-light;
}

.admin-stats {
  display: flex;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.stat-card {
  flex: 1;
  background: $white;
  border-radius: $radius;
  padding: 24rpx;
  text-align: center;
  box-shadow: $shadow;
}

.stat-value {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: $primary-color;
}

.stat-label {
  font-size: 22rpx;
  color: $text-light;
}

.menu-list {
  background: $white;
  border-radius: $radius;
  overflow: hidden;
  margin-bottom: 30rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid $border-color;
  position: relative;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:active {
    background: $bg-color;
  }
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.menu-info {
  flex: 1;
}

.menu-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 6rpx;
}

.menu-desc {
  font-size: 22rpx;
  color: $text-light;
}

.menu-arrow {
  font-size: 36rpx;
  color: $text-light;
}

.menu-badge {
  position: absolute;
  right: 80rpx;
  background: $error-color;
  color: $white;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 20rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-color;
}

.section-back {
  font-size: 26rpx;
  color: $primary-color;
}

.pending-list, .records-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.pending-card, .record-card {
  background: $white;
  border-radius: $radius;
  padding: 24rpx;
  box-shadow: $shadow;
}

.pending-header, .record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.pending-room, .record-room {
  font-size: 28rpx;
  font-weight: bold;
  color: $text-color;
}

.record-status {
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

.pending-info, .record-info {
  font-size: 24rpx;
  color: $text-secondary;
  line-height: 1.8;
}

.pending-actions {
  display: flex;
  gap: 20rpx;
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid $border-color;
}

.btn-success {
  flex: 1;
  background: $success-color;
  color: $white;
  text-align: center;
  padding: 20rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  
  &:active {
    background: darken($success-color, 10%);
  }
}

.btn-reject {
  flex: 1;
  background: $error-color;
  color: $white;
  text-align: center;
  padding: 20rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  
  &:active {
    background: darken($error-color, 10%);
  }
}

.empty-state {
  text-align: center;
  padding: 40rpx;
}

.empty-text {
  font-size: 28rpx;
  color: $text-light;
}
</style>
