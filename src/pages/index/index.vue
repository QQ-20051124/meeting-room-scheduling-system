<template>
  <view class="index-container">
    <!-- 顶部导航 -->
    <view class="top-nav">
      <view class="nav-left">
        <view class="logo">
          <text class="logo-icon">◉</text>
          <text class="logo-text">会议室调度系统</text>
        </view>
      </view>
      <view class="nav-center">
        <view class="search-box">
          <text class="search-icon">◉</text>
          <input class="search-input" v-model="searchText" placeholder="搜索会议室..." />
          <text class="search-btn" @click="handleSearch">搜索</text>
        </view>
      </view>
      <view class="nav-right">
        <view class="user-menu">
          <view class="user-avatar" :style="{ background: currentUser?.avatar || '#2563EB' }">
            <text class="avatar-text">{{ currentUser?.realName?.charAt(0) }}</text>
          </view>
          <view class="user-info">
            <text class="user-name">{{ currentUser?.realName }}</text>
            <text class="user-role">{{ getRoleText(currentUser?.role) }}</text>
          </view>
          <view class="menu-arrow">▼</view>
        </view>
      </view>
    </view>

    <!-- 主体内容 -->
    <view class="main-body">
      <!-- 左侧房间列表 -->
      <view class="rooms-sidebar">
        <view class="sidebar-header">
          <text class="sidebar-title">会议室列表</text>
          <view class="filter-tabs">
            <view 
              v-for="tab in filterTabs" 
              :key="tab.key"
              :class="['filter-tab', { active: activeFilter === tab.key }]"
              @click="activeFilter = tab.key"
            >
              {{ tab.label }}
              <view class="tab-count">{{ tab.count }}</view>
            </view>
          </view>
        </view>
        <scroll-view class="rooms-scroll" scroll-y>
          <view 
            v-for="room in filteredRooms" 
            :key="room.id"
            :class="['room-card', { selected: selectedRoom?.id === room.id }]"
            @click="selectRoom(room)"
          >
            <view class="room-image">
              <image :src="room.image" mode="aspectFill" />
              <view :class="['room-status-badge', room.status]">
                {{ getRoomStatusText(room.status) }}
              </view>
            </view>
            <view class="room-info">
              <text class="room-name">{{ room.name }}</text>
              <text class="room-location">{{ room.location }}</text>
              <view class="room-meta">
                <text class="meta-item">◉ {{ room.capacity }}人</text>
                <text class="meta-item">◉ {{ room.equipment.split('、').length }}项设备</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 中间详情区域 -->
      <view class="detail-section">
        <view v-if="selectedRoom" class="room-detail">
          <view class="detail-header">
            <text class="detail-title">{{ selectedRoom.name }}</text>
            <view :class="['status-tag', selectedRoom.status]">
              {{ getRoomStatusText(selectedRoom.status) }}
            </view>
          </view>
          <view class="detail-images">
            <image class="main-image" :src="selectedRoom.image" mode="aspectFill" />
            <view class="sub-images">
              <image v-for="(img, idx) in roomImages" :key="idx" :src="img" mode="aspectFill" />
            </view>
          </view>
          <view class="detail-info">
            <view class="info-row">
              <text class="info-label">位置</text>
              <text class="info-value">{{ selectedRoom.location }}</text>
            </view>
            <view class="info-row">
              <text class="info-label">容量</text>
              <text class="info-value">{{ selectedRoom.capacity }} 人</text>
            </view>
            <view class="info-row">
              <text class="info-label">设备</text>
              <view class="equipment-list">
                <view 
                  v-for="(device, idx) in selectedRoom.equipment.split('、')" 
                  :key="idx" 
                  class="equipment-tag"
                >{{ device }}</view>
              </view>
            </view>
            <view class="info-row">
              <text class="info-label">描述</text>
              <text class="info-value">{{ selectedRoom.description }}</text>
            </view>
          </view>
          <view class="quick-booking">
            <view class="booking-header">
              <text class="booking-title">快速预约</text>
            </view>
            <view class="booking-form">
              <view class="form-row">
                <view class="form-item">
                  <text class="form-label">日期</text>
                  <picker mode="date" :value="bookingDate" @change="onDateChange">
                    <view class="form-value">{{ bookingDate }}</view>
                  </picker>
                </view>
                <view class="form-item">
                  <text class="form-label">开始时间</text>
                  <picker mode="time" :value="startTime" @change="onStartTimeChange">
                    <view class="form-value">{{ startTime }}</view>
                  </picker>
                </view>
                <view class="form-item">
                  <text class="form-label">结束时间</text>
                  <picker mode="time" :value="endTime" @change="onEndTimeChange">
                    <view class="form-value">{{ endTime }}</view>
                  </picker>
                </view>
              </view>
              <view class="form-row">
                <view class="form-item full">
                  <text class="form-label">会议主题</text>
                  <input class="form-input" v-model="meetingTopic" placeholder="请输入会议主题" />
                </view>
              </view>
              <view class="form-row">
                <view class="form-item">
                  <text class="form-label">参会人数</text>
                  <input class="form-input" v-model="participantCount" type="number" placeholder="请输入人数" />
                </view>
                <view class="form-item">
                  <text class="form-label">联系人</text>
                  <input class="form-input" v-model="contactPerson" placeholder="请输入联系人" />
                </view>
              </view>
              <view class="form-row">
                <view class="form-item full">
                  <text class="form-label">备注</text>
                  <textarea class="form-textarea" v-model="remarks" placeholder="请输入备注信息（可选）" />
                </view>
              </view>
              <view class="booking-actions">
                <view class="btn-primary" @click="handleBooking">立即预约</view>
                <view class="btn-secondary" @click="clearBooking">重置</view>
              </view>
            </view>
          </view>
        </view>
        <view v-else class="empty-state">
          <text class="empty-icon">◉</text>
          <text class="empty-title">请选择会议室</text>
          <text class="empty-desc">从左侧列表中选择一个会议室查看详情并预约</text>
        </view>
      </view>

      <!-- 右侧日历和预约记录 -->
      <view class="right-panel">
        <view class="calendar-section">
          <view class="section-header">
            <text class="section-title">今日日程</text>
            <text class="section-date">{{ todayDate }}</text>
          </view>
          <view class="calendar-list">
            <view 
              v-for="item in todayReservations" 
              :key="item.id" 
              :class="['calendar-item', item.status]"
            >
              <view class="calendar-time">{{ item.startTime }} - {{ item.endTime }}</view>
              <view class="calendar-content">
                <text class="calendar-room">{{ item.roomName }}</text>
                <text class="calendar-topic">{{ item.meetingTopic }}</text>
              </view>
            </view>
            <view v-if="todayReservations.length === 0" class="empty-calendar">
              <text class="empty-text">今日暂无预约</text>
            </view>
          </view>
        </view>

        <view class="history-section">
          <view class="section-header">
            <text class="section-title">我的预约</text>
            <text class="section-more" @click="goToHistory">查看全部</text>
          </view>
          <view class="history-list">
            <view 
              v-for="item in myReservations" 
              :key="item.id" 
              class="history-item"
            >
              <view class="history-info">
                <text class="history-room">{{ item.roomName }}</text>
                <text class="history-date">{{ item.date }} {{ item.startTime }}-{{ item.endTime }}</text>
              </view>
              <view :class="['history-status', item.status]">{{ getStatusText(item.status) }}</view>
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
import type { Room, Reservation } from '@/types'

const roomStore = useRoomStore()
const reservationStore = useReservationStore()
const userStore = useUserStore()

const currentUser = computed(() => userStore.currentUser)
const rooms = computed(() => roomStore.rooms)
const reservations = computed(() => reservationStore.reservations)

const searchText = ref('')
const activeFilter = ref('all')
const selectedRoom = ref<Room | null>(null)

const bookingDate = ref('')
const startTime = ref('09:00')
const endTime = ref('10:00')
const meetingTopic = ref('')
const participantCount = ref('')
const contactPerson = ref('')
const remarks = ref('')

const todayDate = computed(() => {
  const now = new Date()
  return `${now.getMonth() + 1}月${now.getDate()}日`
})

const roomImages = ['/static/room1.jpg', '/static/room2.jpg', '/static/room3.jpg']

const filterTabs = computed(() => [
  { key: 'all', label: '全部', count: rooms.value.length },
  { key: 'available', label: '可用', count: rooms.value.filter(r => r.status === 'available').length },
  { key: 'unavailable', label: '占用', count: rooms.value.filter(r => r.status !== 'available').length }
])

const filteredRooms = computed(() => {
  let result = rooms.value
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(r => 
      r.name.toLowerCase().includes(search) || 
      r.location.toLowerCase().includes(search)
    )
  }
  if (activeFilter.value !== 'all') {
    if (activeFilter.value === 'available') {
      result = result.filter(r => r.status === 'available')
    } else {
      result = result.filter(r => r.status !== 'available')
    }
  }
  return result
})

const todayReservations = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return reservations.value.filter(r => r.date === today).slice(0, 5)
})

const myReservations = computed(() => {
  return reservations.value.filter(r => r.applicant === currentUser.value?.realName).slice(0, 5)
})

function getRoleText(role?: string): string {
  const map: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生',
    organization: '组织'
  }
  return map[role || ''] || ''
}

function getRoomStatusText(status: string): string {
  const map: Record<string, string> = {
    available: '可用',
    unavailable: '不可用',
    maintenance: '维护中'
  }
  return map[status] || status
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

function selectRoom(room: Room) {
  selectedRoom.value = room
}

function handleSearch() {
  activeFilter.value = 'all'
}

function onDateChange(e: any) {
  bookingDate.value = e.detail.value
}

function onStartTimeChange(e: any) {
  startTime.value = e.detail.value
}

function onEndTimeChange(e: any) {
  endTime.value = e.detail.value
}

function handleBooking() {
  if (!selectedRoom.value) {
    uni.showToast({ title: '请先选择会议室', icon: 'none' })
    return
  }
  if (!bookingDate.value) {
    uni.showToast({ title: '请选择日期', icon: 'none' })
    return
  }
  if (!meetingTopic.value.trim()) {
    uni.showToast({ title: '请输入会议主题', icon: 'none' })
    return
  }

  const reservation: Omit<Reservation, 'id'> = {
    roomId: selectedRoom.value.id,
    roomCode: selectedRoom.value.code,
    roomName: selectedRoom.value.name,
    applicant: currentUser.value?.realName || '',
    meetingTopic: meetingTopic.value,
    date: bookingDate.value,
    startTime: startTime.value,
    endTime: endTime.value,
    participantCount: parseInt(participantCount.value) || 0,
    contactPerson: contactPerson.value || currentUser.value?.realName || '',
    remarks: remarks.value,
    status: 'pending',
    createdAt: new Date().toISOString()
  }

  reservationStore.addReservation(reservation)
  uni.showToast({ title: '预约提交成功，等待审核', icon: 'success' })
  clearBooking()
}

function clearBooking() {
  bookingDate.value = ''
  startTime.value = '09:00'
  endTime.value = '10:00'
  meetingTopic.value = ''
  participantCount.value = ''
  contactPerson.value = ''
  remarks.value = ''
}

function goToHistory() {
  uni.navigateTo({ url: '/pages/reservation/list' })
}

onMounted(() => {
  const now = new Date()
  bookingDate.value = now.toISOString().split('T')[0]
  
  if (rooms.value.length > 0) {
    selectedRoom.value = rooms.value[0]
  }
  
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
.index-container {
  min-height: 100vh;
  background: $bg-page;
  display: flex;
  flex-direction: column;
}

/* ===== 顶部导航 ===== */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  background: $bg-card;
  border-bottom: 1rpx solid $border-light;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  flex: 1;
}

.logo {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.logo-icon {
  font-size: 40rpx;
  color: $primary-color;
}

.logo-text {
  font-size: $font-lg;
  font-weight: 700;
  color: $text-title;
}

.nav-center {
  flex: 2;
  display: flex;
  justify-content: center;
}

.search-box {
  display: flex;
  align-items: center;
  background: $bg-page;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  padding: 0 $spacing-md;
  height: 64rpx;
  width: 600rpx;
}

.search-icon {
  font-size: 28rpx;
  color: $text-muted;
  margin-right: $spacing-sm;
}

.search-input {
  flex: 1;
  height: 100%;
  font-size: $font-sm;
  background: transparent;
}

.search-btn {
  padding: 0 $spacing-md;
  color: $primary-color;
  font-size: $font-sm;
  font-weight: 500;
  cursor: pointer;
}

.nav-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  border-radius: $radius-lg;
  cursor: pointer;
  
  &:hover {
    background: $bg-hover;
  }
}

.user-avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 24rpx;
  font-weight: 600;
  color: $white;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: $font-sm;
  font-weight: 500;
  color: $text-title;
}

.user-role {
  font-size: $font-xs;
  color: $text-muted;
}

.menu-arrow {
  font-size: $font-xs;
  color: $text-muted;
}

/* ===== 主体内容 ===== */
.main-body {
  flex: 1;
  display: flex;
  padding: $spacing-lg;
  gap: $spacing-lg;
}

/* ===== 左侧房间列表 ===== */
.rooms-sidebar {
  width: 480rpx;
  background: $bg-card;
  border-radius: $radius-xl;
  overflow: hidden;
  box-shadow: $shadow-sm;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: $spacing-md;
  border-bottom: 1rpx solid $border-light;
}

.sidebar-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-title;
  display: block;
  margin-bottom: $spacing-md;
}

.filter-tabs {
  display: flex;
  gap: $spacing-sm;
}

.filter-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-xs;
  padding: $spacing-sm;
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $text-secondary;
  cursor: pointer;
  background: $bg-page;
  
  &.active {
    background: $primary-color;
    color: $white;
    
    .tab-count {
      background: rgba(255,255,255,0.2);
      color: $white;
    }
  }
}

.tab-count {
  min-width: 32rpx;
  height: 32rpx;
  padding: 0 8rpx;
  border-radius: $radius-full;
  background: $bg-hover;
  font-size: $font-xs;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rooms-scroll {
  flex: 1;
  padding: $spacing-md;
  overflow: auto;
}

.room-card {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-md;
  border-radius: $radius-lg;
  cursor: pointer;
  margin-bottom: $spacing-sm;
  background: $bg-page;
  border: 2rpx solid transparent;
  
  &:hover {
    background: $bg-hover;
  }
  
  &.selected {
    border-color: $primary-color;
    background: rgba($primary-color, 0.05);
  }
}

.room-image {
  position: relative;
  width: 120rpx;
  height: 80rpx;
  border-radius: $radius-md;
  overflow: hidden;
  flex-shrink: 0;
}

.room-image image {
  width: 100%;
  height: 100%;
}

.room-status-badge {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  padding: 4rpx 12rpx;
  border-radius: $radius-md;
  font-size: $font-xs;
  
  &.available { background: rgba($success-color, 0.9); color: $white; }
  &.unavailable { background: rgba($error-color, 0.9); color: $white; }
  &.maintenance { background: rgba($warning-color, 0.9); color: $white; }
}

.room-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.room-name {
  font-size: $font-base;
  font-weight: 600;
  color: $text-title;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room-location {
  font-size: $font-xs;
  color: $text-muted;
  margin-bottom: $spacing-xs;
}

.room-meta {
  display: flex;
  gap: $spacing-md;
}

.meta-item {
  font-size: $font-xs;
  color: $text-secondary;
}

/* ===== 中间详情区域 ===== */
.detail-section {
  flex: 2;
  background: $bg-card;
  border-radius: $radius-xl;
  overflow: hidden;
  box-shadow: $shadow-sm;
  display: flex;
  flex-direction: column;
}

.room-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1rpx solid $border-light;
}

.detail-title {
  font-size: $font-xl;
  font-weight: 700;
  color: $text-title;
}

.status-tag {
  padding: 8rpx 24rpx;
  border-radius: $radius-full;
  font-size: $font-xs;
  
  &.available { background: rgba($success-color, 0.1); color: $success-color; }
  &.unavailable { background: rgba($error-color, 0.1); color: $error-color; }
  &.maintenance { background: rgba($warning-color, 0.1); color: $warning-color; }
}

.detail-images {
  padding: $spacing-lg;
}

.main-image {
  width: 100%;
  height: 300rpx;
  border-radius: $radius-lg;
  margin-bottom: $spacing-md;
}

.sub-images {
  display: flex;
  gap: $spacing-sm;
}

.sub-images image {
  width: calc(33.33% - 16rpx);
  height: 120rpx;
  border-radius: $radius-md;
}

.detail-info {
  padding: 0 $spacing-lg $spacing-lg;
  border-bottom: 1rpx solid $border-light;
}

.info-row {
  display: flex;
  padding: $spacing-sm 0;
  
  &:not(:last-child) {
    border-bottom: 1rpx solid $border-light;
  }
}

.info-label {
  width: 120rpx;
  font-size: $font-sm;
  color: $text-muted;
  flex-shrink: 0;
}

.info-value {
  flex: 1;
  font-size: $font-sm;
  color: $text-primary;
}

.equipment-list {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.equipment-tag {
  padding: 6rpx 16rpx;
  border-radius: $radius-md;
  background: rgba($primary-color, 0.08);
  color: $primary-color;
  font-size: $font-xs;
}

.quick-booking {
  flex: 1;
  padding: $spacing-lg;
  background: $bg-page;
}

.booking-header {
  margin-bottom: $spacing-md;
}

.booking-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-title;
}

.booking-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-row {
  display: flex;
  gap: $spacing-md;
}

.form-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
  
  &.full {
    flex: 100%;
  }
}

.form-label {
  font-size: $font-sm;
  color: $text-secondary;
}

.form-value {
  padding: $spacing-sm;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $text-primary;
  background: $bg-card;
}

.form-input {
  padding: $spacing-sm;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-sm;
  background: $bg-card;
}

.form-textarea {
  padding: $spacing-sm;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-sm;
  background: $bg-card;
  height: 120rpx;
}

.booking-actions {
  display: flex;
  gap: $spacing-md;
  margin-top: $spacing-lg;
}

.btn-primary {
  flex: 2;
  padding: $spacing-md;
  border-radius: $radius-lg;
  background: linear-gradient(135deg, $primary-color, $primary-dark);
  color: $white;
  font-size: $font-base;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  
  &:hover {
    opacity: 0.9;
  }
}

.btn-secondary {
  flex: 1;
  padding: $spacing-md;
  border-radius: $radius-lg;
  background: $bg-card;
  color: $text-secondary;
  font-size: $font-base;
  text-align: center;
  cursor: pointer;
  border: 1rpx solid $border-color;
  
  &:hover {
    background: $bg-hover;
  }
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $spacing-md;
}

.empty-icon {
  font-size: 120rpx;
  color: $border-color;
}

.empty-title {
  font-size: $font-xl;
  font-weight: 600;
  color: $text-title;
}

.empty-desc {
  font-size: $font-sm;
  color: $text-muted;
}

/* ===== 右侧面板 ===== */
.right-panel {
  width: 420rpx;
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.calendar-section, .history-section {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-md;
  box-shadow: $shadow-sm;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.section-title {
  font-size: $font-base;
  font-weight: 600;
  color: $text-title;
}

.section-date {
  font-size: $font-xs;
  color: $text-muted;
}

.section-more {
  font-size: $font-xs;
  color: $primary-color;
  cursor: pointer;
}

.calendar-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.calendar-item {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-sm;
  border-radius: $radius-lg;
  background: $bg-page;
  
  &.pending { border-left: 4rpx solid $warning-color; }
  &.approved { border-left: 4rpx solid $success-color; }
  &.completed { border-left: 4rpx solid $text-muted; }
}

.calendar-time {
  font-size: $font-xs;
  color: $text-muted;
  white-space: nowrap;
}

.calendar-content {
  flex: 1;
  min-width: 0;
}

.calendar-room {
  font-size: $font-sm;
  font-weight: 500;
  color: $text-title;
  display: block;
}

.calendar-topic {
  font-size: $font-xs;
  color: $text-muted;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.empty-calendar {
  padding: $spacing-lg;
  text-align: center;
}

.empty-text {
  font-size: $font-sm;
  color: $text-muted;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-sm;
  border-radius: $radius-lg;
  background: $bg-page;
}

.history-info {
  flex: 1;
  min-width: 0;
}

.history-room {
  font-size: $font-sm;
  font-weight: 500;
  color: $text-title;
  display: block;
}

.history-date {
  font-size: $font-xs;
  color: $text-muted;
}

.history-status {
  padding: 6rpx 16rpx;
  border-radius: $radius-md;
  font-size: $font-xs;
  
  &.pending { background: rgba($warning-color, 0.1); color: $warning-color; }
  &.approved { background: rgba($success-color, 0.1); color: $success-color; }
  &.completed { background: $bg-hover; color: $text-muted; }
}
</style>