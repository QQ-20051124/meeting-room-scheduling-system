<template>
  <view class="admin-container">
    <!-- 左侧侧边栏 -->
    <view class="sidebar">
      <view class="sidebar-header">
        <view class="logo">
          <text class="logo-icon">◉</text>
          <text class="logo-text">会议室调度系统</text>
        </view>
      </view>
      
      <view class="sidebar-menu">
        <view 
          v-for="item in menuItems" 
          :key="item.key"
          :class="['menu-item', { active: activeMenu === item.key }]"
          @click="activeMenu = item.key"
        >
          <text class="menu-icon">{{ item.icon }}</text>
          <text class="menu-text">{{ item.label }}</text>
          <view v-if="item.badge" class="menu-badge">{{ item.badge }}</view>
        </view>
      </view>

      <view class="sidebar-footer">
        <view class="user-info">
          <view class="user-avatar" :style="{ background: currentUser?.avatar || '#2563EB' }">
            <text class="avatar-text">{{ currentUser?.realName?.charAt(0) }}</text>
          </view>
          <view class="user-detail">
            <text class="user-name">{{ currentUser?.realName }}</text>
            <text class="user-role">{{ getRoleText(currentUser?.role) }}</text>
          </view>
        </view>
        <view class="logout-btn" @click="handleLogout">退出登录</view>
      </view>
    </view>

    <!-- 主内容区域 -->
    <view class="main-content">
      <!-- 顶部导航 -->
      <view class="top-header">
        <view class="header-left">
          <text class="page-title">{{ currentPageTitle }}</text>
        </view>
        <view class="header-right">
          <view class="search-box">
            <text class="search-icon">◉</text>
            <input class="search-input" v-model="searchText" placeholder="搜索会议室、预约..." />
          </view>
          <view class="header-actions">
            <view class="action-item">
              <text class="action-icon">🔔</text>
              <view class="action-badge">0</view>
            </view>
          </view>
        </view>
      </view>

      <!-- 内容区域 -->
      <view class="content-area">
        <!-- 仪表盘 -->
        <view v-if="activeMenu === 'dashboard'" class="dashboard-section">
          <view class="stats-grid">
            <view class="stat-card stat-primary">
              <view class="stat-icon">▣</view>
              <view class="stat-content">
                <text class="stat-value">{{ rooms.length }}</text>
                <text class="stat-label">会议室总数</text>
              </view>
            </view>
            <view class="stat-card stat-success">
              <view class="stat-icon">✓</view>
              <view class="stat-content">
                <text class="stat-value">{{ availableRooms }}</text>
                <text class="stat-label">可用</text>
              </view>
            </view>
            <view class="stat-card stat-warning">
              <view class="stat-icon">⚙</view>
              <view class="stat-content">
                <text class="stat-value">{{ maintenanceRooms }}</text>
                <text class="stat-label">维护中</text>
              </view>
            </view>
            <view class="stat-card stat-error">
              <view class="stat-icon">●</view>
              <view class="stat-content">
                <text class="stat-value">{{ pendingReservations.length }}</text>
                <text class="stat-label">待审核</text>
              </view>
            </view>
          </view>

          <view class="quick-actions">
            <view class="quick-btn primary" @click="goToAddRoom">
              <text class="quick-icon">+</text>
              <text class="quick-text">新增会议室</text>
            </view>
            <view class="quick-btn" @click="goToPending">
              <text class="quick-icon">✓</text>
              <text class="quick-text">审核预约</text>
            </view>
            <view class="quick-btn" @click="goToAutoAssign">
              <text class="quick-icon">◯</text>
              <text class="quick-text">智能分配</text>
            </view>
          </view>

          <view class="recent-reservations">
            <view class="section-header">
              <text class="section-title">最近预约</text>
              <text class="section-more">查看全部</text>
            </view>
            <view class="reservation-list">
              <view v-for="res in recentReservations" :key="res.id" class="reservation-item">
                <view class="res-info">
                  <text class="res-room">{{ res.roomCode }} {{ res.roomName }}</text>
                  <text class="res-topic">{{ res.meetingTopic }}</text>
                </view>
                <view class="res-time">{{ res.date }} {{ res.startTime }} - {{ res.endTime }}</view>
                <view :class="['res-status', res.status]">{{ getStatusText(res.status) }}</view>
              </view>
            </view>
          </view>
        </view>

        <!-- 会议室管理 -->
        <view v-if="activeMenu === 'rooms'" class="rooms-section">
          <view class="section-toolbar">
            <view class="search-filter">
              <input class="filter-input" v-model="roomSearch" placeholder="搜索会议室名称或位置" />
              <picker class="filter-select" :range="statusOptions" @change="onStatusChange">
                <text>{{ statusOptions[statusIndex] }}</text>
              </picker>
            </view>
            <view class="toolbar-actions">
              <view class="btn-primary" @click="goToAddRoom">+ 新增会议室</view>
            </view>
          </view>
          <view class="room-table">
            <view class="table-header">
              <text class="th">ID</text>
              <text class="th">名称</text>
              <text class="th">位置</text>
              <text class="th">楼层</text>
              <text class="th">容量</text>
              <text class="th">设备</text>
              <text class="th">状态</text>
              <text class="th">预约次数</text>
              <text class="th">操作</text>
            </view>
            <view v-for="room in filteredRooms" :key="room.id" class="table-row">
              <text class="td">{{ room.id }}</text>
              <text class="td">{{ room.name }}</text>
              <text class="td">{{ room.location }}</text>
              <text class="td">{{ getFloor(room.location) }}</text>
              <text class="td">{{ room.capacity }}人</text>
              <view class="td devices">
                <view v-for="(device, idx) in room.equipment.split('、')" :key="idx" class="device-tag">{{ device }}</view>
              </view>
              <view :class="['td status-cell', room.status]">{{ getRoomStatusText(room.status) }}</view>
              <text class="td">0</text>
              <view class="td actions">
                <text class="action-btn edit">编辑</text>
                <text class="action-btn delete">删除</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 预约管理 -->
        <view v-if="activeMenu === 'reservations'" class="reservations-section">
          <view class="tabs">
            <view 
              v-for="tab in reservationTabs" 
              :key="tab.key"
              :class="['tab-item', { active: activeReservationTab === tab.key }]"
              @click="activeReservationTab = tab.key"
            >
              {{ tab.label }}
              <view v-if="tab.count" class="tab-badge">{{ tab.count }}</view>
            </view>
          </view>
          <view class="reservation-table">
            <view class="table-header">
              <text class="th">会议室</text>
              <text class="th">申请人</text>
              <text class="th">会议主题</text>
              <text class="th">日期时间</text>
              <text class="th">参会人数</text>
              <text class="th">状态</text>
              <text class="th">操作</text>
            </view>
            <view v-for="res in filteredReservations" :key="res.id" class="table-row">
              <text class="td">{{ res.roomCode }} {{ res.roomName }}</text>
              <text class="td">{{ res.applicant }}</text>
              <text class="td">{{ res.meetingTopic }}</text>
              <text class="td">{{ res.date }} {{ res.startTime }}-{{ res.endTime }}</text>
              <text class="td">{{ res.participantCount }}人</text>
              <view :class="['td status-cell', res.status]">{{ getStatusText(res.status) }}</view>
              <view class="td actions" v-if="res.status === 'pending'">
                <text class="action-btn approve" @click="handleApprove(res.id)">通过</text>
                <text class="action-btn reject" @click="handleReject(res.id)">拒绝</text>
              </view>
              <view class="td actions" v-else>
                <text class="action-btn cancel" @click="handleCancel(res.id)">取消</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 用户管理 -->
        <view v-if="activeMenu === 'users'" class="users-section">
          <view class="section-toolbar">
            <view class="search-filter">
              <input class="filter-input" v-model="userSearch" placeholder="搜索用户名或姓名" />
              <picker class="filter-select" :range="roleOptions" @change="onUserRoleChange">
                <text>{{ roleOptions[userRoleIndex] }}</text>
              </picker>
            </view>
          </view>
          <view class="user-table">
            <view class="table-header">
              <text class="th">头像</text>
              <text class="th">用户名</text>
              <text class="th">真实姓名</text>
              <text class="th">角色</text>
              <text class="th">学号/工号</text>
              <text class="th">院系</text>
              <text class="th">认证状态</text>
              <text class="th">注册时间</text>
            </view>
            <view v-for="user in users" :key="user.id" class="table-row">
              <view class="td avatar-cell">
                <view class="small-avatar" :style="{ background: user.avatar || '#2563EB' }">
                  <text class="avatar-text">{{ user.realName?.charAt(0) }}</text>
                </view>
              </view>
              <text class="td">{{ user.username }}</text>
              <text class="td">{{ user.realName }}</text>
              <view :class="['td role-cell', user.role]">{{ getRoleText(user.role) }}</view>
              <text class="td">{{ user.schoolId }}</text>
              <text class="td">{{ user.department || '-' }}</text>
              <view :class="['td verify-cell', user.isVerified ? 'verified' : 'unverified']">
                {{ user.isVerified ? '已认证' : '未认证' }}
              </view>
              <text class="td">{{ user.createdAt }}</text>
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

const activeMenu = ref('dashboard')
const activeReservationTab = ref('all')
const searchText = ref('')
const roomSearch = ref('')
const userSearch = ref('')
const statusIndex = ref(0)
const userRoleIndex = ref(0)

const currentUser = computed(() => userStore.currentUser)
const rooms = computed(() => roomStore.rooms)
const pendingReservations = computed(() => reservationStore.pendingReservations)
const allReservations = computed(() => reservationStore.reservations)
const users = computed(() => roomStore.mockUsers)

const statusOptions = ['全部状态', '可用', '不可用', '维护中']
const roleOptions = ['全部角色', '管理员', '教师', '学生', '组织']
const reservationTabs = computed(() => [
  { key: 'all', label: '全部', count: allReservations.value.length },
  { key: 'pending', label: '待审核', count: pendingReservations.value.length },
  { key: 'approved', label: '已通过', count: allReservations.value.filter(r => r.status === 'approved').length },
  { key: 'completed', label: '已完成', count: allReservations.value.filter(r => r.status === 'completed').length }
])

const menuItems = computed(() => [
  { key: 'dashboard', label: '仪表盘', icon: '◎', badge: null },
  { key: 'rooms', label: '会议室管理', icon: '▣', badge: null },
  { key: 'reservations', label: '预约管理', icon: '◯', badge: pendingReservations.value.length > 0 ? pendingReservations.value.length : null },
  { key: 'users', label: '用户管理', icon: '◇', badge: null }
])

const availableRooms = computed(() => rooms.value.filter(r => r.status === 'available').length)
const maintenanceRooms = computed(() => rooms.value.filter(r => r.status === 'maintenance').length)
const recentReservations = computed(() => allReservations.value.slice(0, 5))

const currentPageTitle = computed(() => {
  const map: Record<string, string> = {
    dashboard: '仪表盘',
    rooms: '会议室管理',
    reservations: '预约管理',
    users: '用户管理'
  }
  return map[activeMenu.value] || '仪表盘'
})

const filteredRooms = computed(() => {
  let result = rooms.value
  if (roomSearch.value) {
    const search = roomSearch.value.toLowerCase()
    result = result.filter(r => 
      r.name.toLowerCase().includes(search) || 
      r.location.toLowerCase().includes(search)
    )
  }
  if (statusIndex.value > 0) {
    const statusMap: Record<number, string> = { 1: 'available', 2: 'unavailable', 3: 'maintenance' }
    result = result.filter(r => r.status === statusMap[statusIndex.value])
  }
  return result
})

const filteredReservations = computed(() => {
  if (activeReservationTab.value === 'all') return allReservations.value
  return allReservations.value.filter(r => r.status === activeReservationTab.value)
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

function getRoomStatusText(status: string): string {
  const map: Record<string, string> = {
    available: '可用',
    unavailable: '不可用',
    maintenance: '维护中'
  }
  return map[status] || status
}

function getFloor(location: string): string {
  const match = location.match(/(\d+)F/)
  return match ? match[1] + 'F' : '-'
}

function onStatusChange(e: any) {
  statusIndex.value = e.detail.value
}

function onUserRoleChange(e: any) {
  userRoleIndex.value = e.detail.value
}

function goToAddRoom() {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

function goToPending() {
  activeMenu.value = 'reservations'
  activeReservationTab.value = 'pending'
}

function goToAutoAssign() {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

function handleApprove(id: string) {
  reservationStore.approveReservation(id)
  uni.showToast({ title: '已通过', icon: 'success' })
}

function handleReject(id: string) {
  reservationStore.rejectReservation(id)
  uni.showToast({ title: '已拒绝', icon: 'success' })
}

function handleCancel(id: string) {
  reservationStore.cancelReservation(id)
  uni.showToast({ title: '已取消', icon: 'success' })
}

function handleLogout() {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.redirectTo({ url: '/pages/user/login' })
      }
    }
  })
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
.admin-container {
  display: flex;
  min-height: 100vh;
  background: $bg-page;
}

/* ===== 侧边栏 ===== */
.sidebar {
  width: 320rpx;
  background: #1E293B;
  color: $white;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
}

.sidebar-header {
  padding: $spacing-xl $spacing-lg;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.1);
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
  color: $white;
}

.sidebar-menu {
  flex: 1;
  padding: $spacing-md;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  border-radius: $radius-lg;
  margin-bottom: $spacing-xs;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba($primary-color, 0.2);
  }
  
  &.active {
    background: $primary-color;
    
    .menu-icon {
      color: $white;
    }
  }
}

.menu-icon {
  font-size: 32rpx;
  color: rgba(255, 255, 255, 0.6);
  margin-right: $spacing-sm;
}

.menu-text {
  flex: 1;
  font-size: $font-base;
  color: rgba(255, 255, 255, 0.9);
}

.menu-badge {
  min-width: 36rpx;
  height: 36rpx;
  padding: 0 12rpx;
  border-radius: $radius-full;
  background: $error-color;
  font-size: $font-xs;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-footer {
  padding: $spacing-md $spacing-lg;
  border-top: 1rpx solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-md;
}

.user-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 28rpx;
  font-weight: 600;
  color: $white;
}

.user-detail {
  flex: 1;
}

.user-name {
  font-size: $font-base;
  font-weight: 500;
  color: $white;
  display: block;
}

.user-role {
  font-size: $font-xs;
  color: rgba(255, 255, 255, 0.6);
}

.logout-btn {
  width: 100%;
  text-align: center;
  padding: $spacing-sm;
  border-radius: $radius-lg;
  background: rgba(239, 68, 68, 0.2);
  color: $error-color;
  font-size: $font-sm;
  cursor: pointer;
  
  &:hover {
    background: rgba(239, 68, 68, 0.3);
  }
}

/* ===== 主内容区域 ===== */
.main-content {
  flex: 1;
  margin-left: 320rpx;
  display: flex;
  flex-direction: column;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  background: $bg-card;
  border-bottom: 1rpx solid $border-light;
}

.header-left {
  .page-title {
    font-size: $font-xl;
    font-weight: 700;
    color: $text-title;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.search-box {
  display: flex;
  align-items: center;
  background: $bg-page;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  padding: 0 $spacing-md;
  height: 64rpx;
  width: 400rpx;
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

.header-actions {
  display: flex;
  gap: $spacing-md;
}

.action-item {
  position: relative;
  width: 64rpx;
  height: 64rpx;
  border-radius: $radius-lg;
  background: $bg-page;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  
  &:hover {
    background: $bg-hover;
  }
}

.action-icon {
  font-size: 32rpx;
}

.action-badge {
  position: absolute;
  top: -8rpx;
  right: -8rpx;
  min-width: 32rpx;
  height: 32rpx;
  padding: 0 8rpx;
  border-radius: $radius-full;
  background: $error-color;
  font-size: $font-xs;
  color: $white;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== 内容区域 ===== */
.content-area {
  flex: 1;
  padding: $spacing-lg;
  overflow: auto;
}

/* ===== 仪表盘 ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
}

.stat-card {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-lg;
  display: flex;
  align-items: center;
  gap: $spacing-md;
  box-shadow: $shadow-sm;
  
  &.stat-primary {
    background: linear-gradient(135deg, $primary-color, $primary-dark);
    .stat-icon { background: rgba(255,255,255,0.2); color: $white; }
    .stat-value, .stat-label { color: $white; }
    .stat-label { opacity: 0.9; }
  }
  &.stat-success .stat-icon { background: rgba($success-color, 0.1); color: $success-color; }
  &.stat-warning .stat-icon { background: rgba($warning-color, 0.1); color: $warning-color; }
  &.stat-error .stat-icon { background: rgba($error-color, 0.1); color: $error-color; }
}

.stat-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: $radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: $font-2xl;
  font-weight: 700;
  color: $text-title;
  display: block;
}

.stat-label {
  font-size: $font-sm;
  color: $text-muted;
}

.quick-actions {
  display: flex;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
}

.quick-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  padding: $spacing-lg;
  border-radius: $radius-xl;
  background: $bg-card;
  box-shadow: $shadow-sm;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-4rpx);
    box-shadow: $shadow;
  }
  
  &.primary {
    background: linear-gradient(135deg, $primary-color, $primary-dark);
    
    .quick-icon, .quick-text {
      color: $white;
    }
  }
}

.quick-icon {
  font-size: 32rpx;
  color: $primary-color;
}

.quick-text {
  font-size: $font-base;
  font-weight: 500;
  color: $text-primary;
}

.recent-reservations {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-lg;
  box-shadow: $shadow-sm;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.section-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-title;
}

.section-more {
  font-size: $font-sm;
  color: $primary-color;
  cursor: pointer;
}

.reservation-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.reservation-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  border-radius: $radius-lg;
  background: $bg-page;
  
  &:hover {
    background: $bg-hover;
  }
}

.res-info {
  flex: 1;
}

.res-room {
  font-size: $font-base;
  font-weight: 500;
  color: $text-title;
  display: block;
}

.res-topic {
  font-size: $font-sm;
  color: $text-muted;
}

.res-time {
  font-size: $font-sm;
  color: $text-secondary;
  margin: 0 $spacing-lg;
}

.res-status {
  font-size: $font-xs;
  padding: 8rpx 20rpx;
  border-radius: $radius-full;
  
  &.pending { background: rgba($warning-color, 0.1); color: $warning-color; }
  &.approved { background: rgba($success-color, 0.1); color: $success-color; }
  &.completed { background: $bg-hover; color: $text-muted; }
}

/* ===== 工具栏 ===== */
.section-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.search-filter {
  display: flex;
  gap: $spacing-md;
}

.filter-input {
  width: 300rpx;
  height: 64rpx;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  padding: 0 $spacing-md;
  font-size: $font-sm;
}

.filter-select {
  height: 64rpx;
  padding: 0 $spacing-md;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $text-secondary;
}

.toolbar-actions {
  display: flex;
  gap: $spacing-md;
}

.btn-primary {
  padding: $spacing-sm $spacing-lg;
  border-radius: $radius-lg;
  background: linear-gradient(135deg, $primary-color, $primary-dark);
  color: $white;
  font-size: $font-sm;
  font-weight: 500;
  cursor: pointer;
  
  &:hover {
    opacity: 0.9;
  }
}

/* ===== 表格 ===== */
.room-table, .reservation-table, .user-table {
  background: $bg-card;
  border-radius: $radius-xl;
  overflow: hidden;
  box-shadow: $shadow-sm;
}

.table-header {
  display: flex;
  background: $bg-hover;
  padding: $spacing-md;
  font-weight: 600;
  font-size: $font-sm;
  color: $text-secondary;
}

.table-row {
  display: flex;
  padding: $spacing-md;
  border-bottom: 1rpx solid $border-light;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: $bg-page;
  }
}

.th, .td {
  flex: 1;
  text-align: center;
  font-size: $font-sm;
}

.th:first-child, .td:first-child { flex: 0.5; }
.th:last-child, .td:last-child { flex: 1.2; }

.td {
  color: $text-primary;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.devices {
    flex-wrap: wrap;
    gap: 8rpx;
  }
  
  &.status-cell {
    padding: 8rpx 20rpx;
    border-radius: $radius-full;
    font-size: $font-xs;
    font-weight: 500;
    
    &.available { background: rgba($success-color, 0.1); color: $success-color; }
    &.unavailable { background: rgba($error-color, 0.1); color: $error-color; }
    &.maintenance { background: rgba($warning-color, 0.1); color: $warning-color; }
    &.pending { background: rgba($warning-color, 0.1); color: $warning-color; }
    &.approved { background: rgba($success-color, 0.1); color: $success-color; }
    &.rejected, &.cancelled { background: rgba($error-color, 0.1); color: $error-color; }
    &.completed { background: $bg-hover; color: $text-muted; }
  }
  
  &.role-cell {
    padding: 8rpx 20rpx;
    border-radius: $radius-full;
    font-size: $font-xs;
    
    &.admin { background: rgba($accent-color, 0.1); color: $accent-color; }
    &.teacher { background: rgba($success-color, 0.1); color: $success-color; }
    &.student { background: rgba($primary-color, 0.1); color: $primary-color; }
    &.organization { background: rgba($warning-color, 0.1); color: $warning-color; }
  }
  
  &.verify-cell {
    padding: 8rpx 20rpx;
    border-radius: $radius-full;
    font-size: $font-xs;
    
    &.verified { background: rgba($success-color, 0.1); color: $success-color; }
    &.unverified { background: rgba($warning-color, 0.1); color: $warning-color; }
  }
  
  &.avatar-cell {
    justify-content: flex-start;
    padding-left: $spacing-md;
  }
}

.device-tag {
  padding: 4rpx 12rpx;
  border-radius: $radius-md;
  background: rgba($primary-color, 0.08);
  color: $primary-color;
  font-size: $font-xs;
}

.actions {
  display: flex;
  gap: $spacing-sm;
}

.action-btn {
  padding: 8rpx 20rpx;
  border-radius: $radius-md;
  font-size: $font-xs;
  cursor: pointer;
  
  &.edit { background: rgba($primary-color, 0.1); color: $primary-color; }
  &.delete { background: rgba($error-color, 0.1); color: $error-color; }
  &.approve { background: rgba($success-color, 0.1); color: $success-color; }
  &.reject { background: rgba($error-color, 0.1); color: $error-color; }
  &.cancel { background: rgba($warning-color, 0.1); color: $warning-color; }
  
  &:hover {
    opacity: 0.8;
  }
}

.small-avatar {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .avatar-text {
    font-size: 20rpx;
  }
}

/* ===== 标签页 ===== */
.tabs {
  display: flex;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;
  background: $bg-card;
  padding: $spacing-xs;
  border-radius: $radius-xl;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-md $spacing-lg;
  border-radius: $radius-lg;
  font-size: $font-sm;
  color: $text-secondary;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.active {
    background: $primary-color;
    color: $white;
  }
}

.tab-badge {
  min-width: 32rpx;
  height: 32rpx;
  padding: 0 8rpx;
  border-radius: $radius-full;
  background: rgba(255,255,255,0.2);
  font-size: $font-xs;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>