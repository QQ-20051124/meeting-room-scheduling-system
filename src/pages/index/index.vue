<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="header-title-bar">
      <text class="main-title">会议室调度系统</text>
    </view>
    
    <!-- 导航栏 -->
    <view class="top-nav">
      <!-- 左侧：导航链接 -->
      <view class="nav-left">
        <view 
          v-for="item in navLinks" 
          :key="item.key"
          :class="['nav-link', { active: currentNav === item.key }]"
          @click="navigateTo(item.path)"
        >
          <text class="nav-icon">{{ item.icon }}</text>
          <text class="nav-text">{{ item.label }}</text>
        </view>
      </view>
      
      <!-- 右侧：搜索、通知和用户信息 -->
      <view class="nav-right">
        <view class="search-box">
          <text class="search-icon">🔍</text>
          <input class="search-input" v-model="searchText" placeholder="搜索会议室..." />
        </view>
        <view class="notification" @click="goToNotification">
          <text class="notify-icon">🔔</text>
          <view v-if="notificationCount > 0" class="notify-badge">{{ notificationCount }}</view>
        </view>
        <view class="user-menu" @click="goToProfile">
          <view class="user-avatar">
            <text class="avatar-text">{{ getAvatarText(currentUser) }}</text>
          </view>
          <text class="user-name">{{ currentUser?.realName || currentUser?.username }}</text>
          <text class="user-arrow">▼</text>
        </view>
      </view>
    </view>

    <!-- 主体内容 -->
    <view class="main-body">
      <!-- 左侧会议室列表 -->
      <view class="sidebar">
        <view class="sidebar-header">
          <text class="sidebar-title">会议室列表</text>
          <text class="sidebar-count">共 {{ roomStore.rooms.length }} 间</text>
        </view>
        
        <!-- 筛选标签 - 横向排列 -->
        <view class="sidebar-filter">
          <view 
            v-for="tab in filterTabs" 
            :key="tab.key"
            :class="['filter-item', { active: activeFilter === tab.key }]"
            @click="activeFilter = tab.key"
          >
            <text class="filter-label">{{ tab.label }}</text>
            <text class="filter-count">{{ getFilterCount(tab.key) }}</text>
          </view>
        </view>
        
        <scroll-view class="room-list" scroll-y>
          <view 
            v-for="room in filteredRooms" 
            :key="room.id"
            :class="['room-item', { active: selectedRoom?.id === room.id }]"
            @click="selectRoom(room)"
          >
            <view class="room-item-header">
              <view :class="['room-status', room.status]">
                <text>{{ room.status === 'available' ? '可用' : '占用' }}</text>
              </view>
              <text class="room-code">{{ room.code }}</text>
            </view>
            <text class="room-name">{{ room.name }}</text>
            <text class="room-location">{{ room.location }}</text>
            <view class="room-meta">
              <view class="meta-item">
                <text class="meta-icon">👥</text>
                <text>{{ room.capacity }}人</text>
              </view>
              <view class="meta-item">
                <text class="meta-icon">📦</text>
                <text>{{ getEquipmentCount(room.equipment) }}项设备</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 中间主内容区 -->
      <view class="main-content">
        <view v-if="selectedRoom" class="room-detail">
          <!-- 会议室详情 -->
          <view class="detail-section">
            <view class="section-header">
              <text class="section-title">会议室详情</text>
            </view>
            <view class="detail-card">
              <view class="card-header">
                <view class="card-title-row">
                  <text class="room-title">{{ selectedRoom.name }}</text>
                  <view :class="['status-tag', selectedRoom.status]">
                    {{ selectedRoom.status === 'available' ? '可预约' : '占用中' }}
                  </view>
                </view>
                <text class="room-code-text">编号：{{ selectedRoom.code }}</text>
              </view>
              
              <view class="detail-grid">
                <view class="detail-item">
                  <text class="detail-icon">📍</text>
                  <view class="detail-info">
                    <text class="detail-label">位置</text>
                    <text class="detail-value">{{ selectedRoom.location }}</text>
                  </view>
                </view>
                <view class="detail-item">
                  <text class="detail-icon">👥</text>
                  <view class="detail-info">
                    <text class="detail-label">容纳人数</text>
                    <text class="detail-value">{{ selectedRoom.capacity }} 人</text>
                  </view>
                </view>
                <view class="detail-item">
                  <text class="detail-icon">📦</text>
                  <view class="detail-info">
                    <text class="detail-label">设备设施</text>
                    <text class="detail-value">{{ selectedRoom.equipment }}</text>
                  </view>
                </view>
                <view class="detail-item">
                  <text class="detail-icon">📝</text>
                  <view class="detail-info">
                    <text class="detail-label">描述</text>
                    <text class="detail-value">{{ selectedRoom.description || '暂无描述' }}</text>
                  </view>
                </view>
              </view>
            </view>
          </view>
          
          <!-- 快速预约 -->
          <view class="reservation-section">
            <view class="section-header">
              <text class="section-title">快速预约</text>
              <text class="section-hint">选择日期和时间进行预约</text>
            </view>
            <view class="reservation-form">
              <view class="form-row">
                <view class="form-group">
                  <text class="form-label">预约日期</text>
                  <picker mode="date" :value="reservationForm.date" @change="onDateChange">
                    <view class="form-picker">
                      <text class="picker-icon">📅</text>
                      <text>{{ reservationForm.date || '请选择日期' }}</text>
                    </view>
                  </picker>
                </view>
              </view>
              
              <view class="form-row">
                <view class="form-group">
                  <text class="form-label">开始时间</text>
                  <picker mode="time" :value="reservationForm.startTime" @change="onStartTimeChange">
                    <view class="form-picker">
                      <text class="picker-icon">🕐</text>
                      <text>{{ reservationForm.startTime || '选择开始时间' }}</text>
                    </view>
                  </picker>
                </view>
                <view class="form-group">
                  <text class="form-label">结束时间</text>
                  <picker mode="time" :value="reservationForm.endTime" @change="onEndTimeChange">
                    <view class="form-picker">
                      <text class="picker-icon">🕐</text>
                      <text>{{ reservationForm.endTime || '选择结束时间' }}</text>
                    </view>
                  </picker>
                </view>
              </view>
              
              <view class="form-row">
                <view class="form-group full">
                  <text class="form-label">预约事由</text>
                  <input class="form-input" v-model="reservationForm.reason" placeholder="请输入预约事由，如：部门例会、项目讨论等" />
                </view>
              </view>
              
              <view class="form-row">
                <view class="form-group half">
                  <text class="form-label">参会人数</text>
                  <picker mode="selector" :range="participantOptions" @change="onParticipantChange">
                    <view class="form-picker">
                      <text class="picker-icon">👥</text>
                      <text>{{ reservationForm.participantCount || '选择人数' }}</text>
                    </view>
                  </picker>
                </view>
              </view>
              
              <view class="form-actions">
                <view class="btn btn-secondary" @click="resetForm">重置</view>
                <view class="btn btn-primary" @click="submitReservation">立即预约</view>
              </view>
            </view>
          </view>
        </view>
        
        <view v-else class="empty-state">
          <view class="empty-icon-wrap">
            <text class="empty-icon">🏢</text>
          </view>
          <text class="empty-title">请选择会议室</text>
          <text class="empty-desc">从左侧列表中选择一个会议室，查看详情并进行预约</text>
        </view>
      </view>

      <!-- 右侧日程区 -->
      <view class="right-panel">
        <!-- 今日日程 -->
        <view class="panel-card schedule-card">
          <view class="panel-header">
            <text class="panel-title">📅 今日日程</text>
            <text class="panel-date">{{ today }}</text>
          </view>
          <scroll-view class="schedule-list" scroll-y>
            <view v-for="schedule in todaySchedule" :key="schedule.id" class="schedule-item">
              <view class="schedule-time-badge">{{ schedule.startTime }}</view>
              <view class="schedule-content">
                <text class="schedule-room-name">{{ schedule.roomName }}</text>
                <text class="schedule-topic">{{ schedule.meetingTopic }}</text>
                <view :class="['schedule-status', schedule.status]">
                  {{ getStatusText(schedule.status) }}
                </view>
              </view>
            </view>
            <view v-if="todaySchedule.length === 0" class="empty-schedule">
              <text class="empty-icon">📋</text>
              <text>今日暂无日程安排</text>
            </view>
          </scroll-view>
        </view>

        <!-- 我的预约统计 -->
        <view class="panel-card stats-card">
          <view class="panel-header">
            <text class="panel-title">📊 我的预约</text>
            <text class="panel-link" @click="goToReservationList">查看全部</text>
          </view>
          <view class="stats-grid">
            <view class="stat-item pending">
              <text class="stat-value">{{ pendingCount }}</text>
              <text class="stat-label">待审核</text>
            </view>
            <view class="stat-item approved">
              <text class="stat-value">{{ approvedCount }}</text>
              <text class="stat-label">已通过</text>
            </view>
            <view class="stat-item cancelled">
              <text class="stat-value">{{ cancelledCount }}</text>
              <text class="stat-label">已取消</text>
            </view>
          </view>
        </view>

        <!-- 快捷操作 -->
        <view class="panel-card quick-actions">
          <view class="panel-header">
            <text class="panel-title">⚡ 快捷操作</text>
          </view>
          <view class="action-grid">
            <view class="action-item" @click="goToQuickReserve">
              <text class="action-icon">⏱️</text>
              <text class="action-text">快速预约</text>
            </view>
            <view class="action-item" @click="goToRoomList">
              <text class="action-icon">🏢</text>
              <text class="action-text">全部会议室</text>
            </view>
            <view class="action-item" @click="goToHistory">
              <text class="action-icon">📜</text>
              <text class="action-text">预约历史</text>
            </view>
            <view class="action-item" @click="goToFeedback">
              <text class="action-icon">💬</text>
              <text class="action-text">意见反馈</text>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 自定义底部导航 -->
    <CustomTabbar current="home" />
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRoomStore } from '@/stores/room'
import CustomTabbar from '@/components/custom-tabbar/CustomTabbar.vue'
import { useReservationStore } from '@/stores/reservation'
import { getToday } from '@/utils/date'

const userStore = useUserStore()
const roomStore = useRoomStore()
const reservationStore = useReservationStore()

const searchText = ref('')
const activeFilter = ref('all')
const selectedRoom = ref<Room | null>(null)
const currentNav = ref('home')
const today = ref(getToday())
const notificationCount = ref(2)

const participantOptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-15', '16-20', '20+']

const reservationForm = ref({
  date: getToday(),
  startTime: '',
  endTime: '',
  reason: '',
  participantCount: ''
})

const navLinks = [
  { key: 'home', label: '首页', icon: '🏠', path: '/pages/index/index' },
  { key: 'room', label: '会议室', icon: '🏢', path: '/pages/room/list' },
  { key: 'reservation', label: '我的预约', icon: '📅', path: '/pages/reservation/list' },
  { key: 'admin', label: '管理后台', icon: '⚙️', path: '/pages/admin/index' }
]

const filterTabs = [
  { key: 'all', label: '全部' },
  { key: 'available', label: '可用' },
  { key: 'occupied', label: '占用' }
]

const isLoggedIn = computed(() => userStore.isLoggedIn())
const isAdmin = computed(() => userStore.isAdmin())
const currentUser = computed(() => userStore.currentUser)

const filteredRooms = computed(() => {
  let rooms = roomStore.rooms
  
  if (activeFilter.value === 'available') {
    rooms = rooms.filter(r => r.status === 'available')
  } else if (activeFilter.value === 'occupied') {
    rooms = rooms.filter(r => r.status !== 'available')
  }
  
  return rooms
})

const todaySchedule = computed(() => {
  if (!currentUser.value) return []
  return reservationStore.userReservations(currentUser.value.id)
    .filter(r => r.date === today.value)
    .sort((a, b) => a.startTime.localeCompare(b.startTime))
})

const pendingCount = computed(() => {
  if (!currentUser.value) return 0
  return reservationStore.userReservations(currentUser.value.id).filter(r => r.status === 'pending').length
})

const approvedCount = computed(() => {
  if (!currentUser.value) return 0
  return reservationStore.userReservations(currentUser.value.id).filter(r => r.status === 'approved').length
})

const cancelledCount = computed(() => {
  if (!currentUser.value) return 0
  return reservationStore.userReservations(currentUser.value.id).filter(r => r.status === 'cancelled').length
})

function getAvatarText(user: User | null | undefined): string {
  if (!user) return '?'
  const name = user.realName || user.username || '?'
  return name.charAt(0).toUpperCase()
}

function getFilterCount(key: string): number {
  if (key === 'all') return roomStore.rooms.length
  if (key === 'available') return roomStore.rooms.filter(r => r.status === 'available').length
  return roomStore.rooms.filter(r => r.status !== 'available').length
}

function getEquipmentCount(equipment: string): number {
  return equipment.split('、').length
}

function getStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

function selectRoom(room: Room) {
  selectedRoom.value = room
}

function navigateTo(path: string) {
  if (path === '/pages/admin/index' && !isAdmin.value) {
    uni.showToast({ title: '权限不足', icon: 'none' })
    return
  }
  currentNav.value = navLinks.find(n => n.path === path)?.key || 'home'
  
  const tabPaths = ['/pages/index/index', '/pages/room/list', '/pages/reservation/list', '/pages/user/profile']
  
  if (tabPaths.includes(path)) {
    uni.switchTab({ url: path })
  } else {
    uni.navigateTo({ url: path })
  }
}

function goToProfile() {
  uni.switchTab({ url: '/pages/user/profile' })
}

function goToNotification() {
  uni.showToast({ title: '暂无新通知', icon: 'none' })
}

function goToReservationList() {
  uni.switchTab({ url: '/pages/reservation/list' })
}

function goToRoomList() {
  uni.switchTab({ url: '/pages/room/list' })
}

function goToQuickReserve() {
  if (!selectedRoom.value) {
    uni.showToast({ title: '请先选择会议室', icon: 'none' })
    return
  }
  uni.navigateTo({ url: `/pages/reservation/apply?roomId=${selectedRoom.value.id}` })
}

function goToHistory() {
  uni.switchTab({ url: '/pages/reservation/list' })
}

function goToFeedback() {
  uni.navigateTo({ url: '/pages/user/feedback' })
}

function onDateChange(e: any) {
  reservationForm.value.date = e.detail.value
}

function onStartTimeChange(e: any) {
  reservationForm.value.startTime = e.detail.value
}

function onEndTimeChange(e: any) {
  reservationForm.value.endTime = e.detail.value
}

function onParticipantChange(e: any) {
  reservationForm.value.participantCount = participantOptions[e.detail.value]
}

function resetForm() {
  reservationForm.value = {
    date: getToday(),
    startTime: '',
    endTime: '',
    reason: '',
    participantCount: ''
  }
}

function submitReservation() {
  if (!selectedRoom.value) {
    uni.showToast({ title: '请选择会议室', icon: 'none' })
    return
  }
  if (!reservationForm.value.startTime || !reservationForm.value.endTime) {
    uni.showToast({ title: '请选择时间', icon: 'none' })
    return
  }
  if (!reservationForm.value.reason.trim()) {
    uni.showToast({ title: '请输入预约事由', icon: 'none' })
    return
  }
  
  reservationStore.addReservation({
    roomId: selectedRoom.value.id,
    userId: currentUser.value!.id,
    roomCode: selectedRoom.value.code,
    roomName: selectedRoom.value.name,
    date: reservationForm.value.date,
    startTime: reservationForm.value.startTime,
    endTime: reservationForm.value.endTime,
    meetingTopic: reservationForm.value.reason,
    participantCount: parseInt(reservationForm.value.participantCount) || 1,
    applicant: currentUser.value!.realName || currentUser.value!.username,
    status: 'pending'
  })
  
  uni.showToast({ title: '预约提交成功', icon: 'success' })
  
  resetForm()
}

onMounted(() => {
  userStore.loadUser()
  roomStore.loadRooms()
  if (roomStore.rooms.length > 0) {
    selectedRoom.value = roomStore.rooms[0]
  }
})
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.container {
  min-height: 100vh;
  background: $bg-color;
  display: flex;
  flex-direction: column;
}

/* ===== 顶部标题栏 ===== */
.header-title-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40rpx 0;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.15);
}

.main-title {
  font-size: 56rpx;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 12rpx;
  text-shadow: 
    0 4rpx 8rpx rgba(0, 0, 0, 0.4),
    0 0 40rpx rgba(255, 255, 255, 0.3),
    0 0 80rpx rgba(100, 181, 246, 0.2);
}

/* ===== 导航栏 ===== */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40rpx;
  height: 90rpx;
  background: #ffffff;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  gap: 48rpx;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 12rpx 24rpx;
  border-radius: 24rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  
  &:hover {
    background: rgba(59, 130, 246, 0.08);
  }
  
  &.active {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    
    .nav-icon, .nav-text {
      color: #ffffff;
    }
  }
}

.nav-icon {
  font-size: 32rpx;
}

.nav-text {
  font-size: 30rpx;
  color: #475569;
  font-weight: 500;
}

.nav-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16rpx;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10rpx;
  padding: 10rpx 16rpx;
  background: #f1f5f9;
  border-radius: 20rpx;
  width: 260rpx;
  border: 2rpx solid #e2e8f0;
}

.search-icon {
  font-size: 28rpx;
  color: #94a3b8;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  background: transparent;
  border: none;
  color: #334155;
  
  &::placeholder {
    color: #94a3b8;
  }
}

.notification {
  position: relative;
  cursor: pointer;
  padding: 14rpx;
}

.notify-icon {
  font-size: 40rpx;
  color: #64748b;
}

.notify-badge {
  position: absolute;
  top: 4rpx;
  right: 4rpx;
  min-width: 32rpx;
  height: 32rpx;
  background: #ef4444;
  color: #ffffff;
  border-radius: 16rpx;
  font-size: 22rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 8rpx;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 10rpx 18rpx;
  background: rgba(59, 130, 246, 0.08);
  border-radius: 28rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(59, 130, 246, 0.12);
  }
}

.user-avatar {
  width: 68rpx;
  height: 68rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3rpx solid rgba(255, 255, 255, 0.4);
}

.avatar-text {
  font-size: 30rpx;
  color: #ffffff;
  font-weight: 600;
}

.user-name {
  font-size: 28rpx;
  color: #334155;
  font-weight: 500;
}

.user-arrow {
  color: #64748b;
  font-size: 24rpx;
}

/* ===== 主体内容 ===== */
.main-body {
  flex: 1;
  display: flex;
  padding: 24rpx;
  gap: 24rpx;
  overflow-y: auto;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

/* ===== 左侧边栏 ===== */
.sidebar {
  width: 460rpx;
  background: #ffffff;
  border-radius: 20rpx;
  box-shadow: $shadow;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 32rpx;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border-bottom: 2rpx solid $border-color;
}

.sidebar-title {
  font-size: 34rpx;
  font-weight: 700;
  color: $text-color;
}

.sidebar-count {
  font-size: 26rpx;
  color: $text-light;
}

.sidebar-filter {
  display: flex;
  padding: 24rpx 28rpx;
  gap: 16rpx;
  border-bottom: 2rpx solid $border-color;
  background: #fafafa;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx 32rpx;
  border-radius: 28rpx;
  font-size: 28rpx;
  color: #64748b;
  background: #ffffff;
  border: 2rpx solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #cbd5e1;
  }
  
  &.active {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-color: #3b82f6;
    color: #ffffff;
    
    .filter-count {
      background: rgba(255, 255, 255, 0.2);
    }
  }
}

.filter-label {
  font-weight: 500;
}

.filter-count {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  background: #e2e8f0;
  border-radius: 12rpx;
}

.room-list {
  flex: 1;
  padding: 20rpx;
}

.room-item {
  padding: 24rpx;
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fafafa;
  border: 2rpx solid transparent;
  
  &:hover {
    background: #f1f5f9;
    transform: translateX(4rpx);
  }
  
  &.active {
    background: rgba(59, 130, 246, 0.08);
    border-color: #3b82f6;
    box-shadow: 0 4rpx 12rpx rgba(59, 130, 246, 0.15);
  }
}

.room-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.room-status {
  padding: 6rpx 16rpx;
  border-radius: 8rpx;
  font-size: 22rpx;
  font-weight: 600;
  
  &.available {
    background: rgba(82, 196, 26, 0.1);
    color: $success-color;
  }
  &.maintenance, &.unavailable {
    background: rgba(239, 68, 68, 0.1);
    color: $error-color;
  }
}

.room-code {
  font-size: 24rpx;
  color: $text-light;
}

.room-name {
  font-size: 32rpx;
  font-weight: 600;
  color: $text-color;
  display: block;
  margin-bottom: 8rpx;
}

.room-location {
  font-size: 24rpx;
  color: $text-secondary;
  display: block;
  margin-bottom: 16rpx;
}

.room-meta {
  display: flex;
  gap: 24rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
  font-size: 22rpx;
  color: $text-light;
}

.meta-icon {
  font-size: 20rpx;
}

/* ===== 中间主内容区 ===== */
.main-content {
  flex: 4;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.detail-section, .reservation-section {
  background: #ffffff;
  border-radius: 20rpx;
  box-shadow: $shadow;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 32rpx;
  background: #f8fafc;
  border-bottom: 2rpx solid $border-color;
}

.section-title {
  font-size: 34rpx;
  font-weight: 700;
  color: $text-color;
}

.section-hint {
  font-size: 26rpx;
  color: $text-light;
}

.detail-card {
  padding: 32rpx;
}

.card-header {
  margin-bottom: 32rpx;
}

.card-title-row {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 8rpx;
}

.room-title {
  font-size: 44rpx;
  font-weight: 700;
  color: $text-color;
}

.status-tag {
  padding: 10rpx 28rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  font-weight: 600;
  
  &.available {
    background: rgba(82, 196, 26, 0.1);
    color: $success-color;
  }
  &.occupied, &.maintenance, &.unavailable {
    background: rgba(239, 68, 68, 0.1);
    color: $error-color;
  }
}

.room-code-text {
  font-size: 28rpx;
  color: $text-light;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
}

.detail-item {
  display: flex;
  gap: 16rpx;
  padding: 24rpx;
  background: #f8fafc;
  border-radius: 16rpx;
}

.detail-icon {
  font-size: 40rpx;
  flex-shrink: 0;
}

.detail-info {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 24rpx;
  color: $text-light;
  margin-bottom: 4rpx;
}

.detail-value {
  font-size: 28rpx;
  color: $text-color;
  font-weight: 500;
}

/* ===== 预约表单 ===== */
.reservation-form {
  padding: 32rpx;
}

.form-row {
  display: flex;
  gap: 24rpx;
  margin-bottom: 24rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.form-group {
  flex: 1;
  
  &.full {
    flex: 2;
  }
  
  &.half {
    flex: 1;
  }
}

.form-label {
  font-size: 28rpx;
  color: $text-secondary;
  margin-bottom: 12rpx;
  display: block;
}

.form-input {
  width: 100%;
  height: 80rpx;
  padding: 0 24rpx;
  background: #f8fafc;
  border: 2rpx solid $border-color;
  border-radius: 12rpx;
  font-size: 28rpx;
  
  &::placeholder {
    color: $text-light;
  }
}

.form-picker {
  width: 100%;
  height: 80rpx;
  padding: 0 24rpx;
  background: #f8fafc;
  border: 2rpx solid $border-color;
  border-radius: 12rpx;
  font-size: 28rpx;
  display: flex;
  align-items: center;
  gap: 12rpx;
  color: $text-color;
}

.picker-icon {
  font-size: 28rpx;
}

.form-actions {
  display: flex;
  gap: 24rpx;
  margin-top: 32rpx;
}

.btn {
  flex: 1;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
  font-size: 32rpx;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary {
  background: #f1f5f9;
  color: $text-secondary;
  border: 2rpx solid $border-color;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
}

/* ===== 空状态 ===== */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border-radius: 20rpx;
  box-shadow: $shadow;
  padding: 100rpx;
}

.empty-icon-wrap {
  width: 160rpx;
  height: 160rpx;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
}

.empty-icon {
  font-size: 80rpx;
}

.empty-title {
  font-size: 36rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 16rpx;
}

.empty-desc {
  font-size: 28rpx;
  color: $text-light;
  text-align: center;
}

/* ===== 右侧面板 ===== */
.right-panel {
  width: 440rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.panel-card {
  background: #ffffff;
  border-radius: 20rpx;
  box-shadow: $shadow;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border-bottom: 2rpx solid $border-color;
  background: #f8fafc;
}

.panel-title {
  font-size: 30rpx;
  font-weight: 700;
  color: $text-color;
}

.panel-date {
  font-size: 24rpx;
  color: $text-light;
}

.panel-link {
  font-size: 26rpx;
  color: #3b82f6;
  cursor: pointer;
}

/* ===== 日程列表 ===== */
.schedule-list {
  padding: 20rpx;
  max-height: 420rpx;
}

.schedule-item {
  display: flex;
  gap: 16rpx;
  padding: 20rpx;
  border-radius: 12rpx;
  margin-bottom: 16rpx;
  background: #f8fafc;
}

.schedule-time-badge {
  padding: 8rpx 16rpx;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
  border-radius: 8rpx;
  font-size: 24rpx;
  font-weight: 600;
  flex-shrink: 0;
}

.schedule-content {
  flex: 1;
}

.schedule-room-name {
  font-size: 28rpx;
  font-weight: 600;
  color: $text-color;
  display: block;
  margin-bottom: 8rpx;
}

.schedule-topic {
  font-size: 24rpx;
  color: $text-secondary;
  display: block;
  margin-bottom: 8rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.schedule-status {
  display: inline-block;
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
  font-size: 22rpx;
  
  &.pending {
    background: rgba(250, 173, 20, 0.1);
    color: $warning-color;
  }
  &.approved {
    background: rgba(82, 196, 26, 0.1);
    color: $success-color;
  }
  &.rejected, &.cancelled {
    background: rgba(239, 68, 68, 0.1);
    color: $error-color;
  }
}

.empty-schedule {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
  color: $text-light;
  font-size: 26rpx;
  
  .empty-icon {
    font-size: 48rpx;
    margin-bottom: 12rpx;
  }
}

/* ===== 统计卡片 ===== */
.stats-grid {
  display: flex;
  padding: 24rpx;
  gap: 16rpx;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 24rpx 16rpx;
  border-radius: 16rpx;
  
  &.pending {
    background: rgba(250, 173, 20, 0.1);
    
    .stat-value {
      color: $warning-color;
    }
  }
  
  &.approved {
    background: rgba(82, 196, 26, 0.1);
    
    .stat-value {
      color: $success-color;
    }
  }
  
  &.cancelled {
    background: rgba(148, 163, 184, 0.1);
    
    .stat-value {
      color: $text-secondary;
    }
  }
}

.stat-value {
  font-size: 48rpx;
  font-weight: 700;
  display: block;
}

.stat-label {
  font-size: 24rpx;
  color: $text-secondary;
  margin-top: 8rpx;
  display: block;
}

/* ===== 快捷操作 ===== */
.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  padding: 20rpx;
  gap: 16rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx;
  background: #f8fafc;
  border-radius: 12rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: #e2e8f0;
    transform: translateY(-4rpx);
  }
}

.action-icon {
  font-size: 44rpx;
  margin-bottom: 12rpx;
}

.action-text {
  font-size: 26rpx;
  color: $text-color;
}
</style>