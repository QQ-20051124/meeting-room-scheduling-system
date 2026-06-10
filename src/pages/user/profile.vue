<template>
  <view class="profile-container">
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
        </view>
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
            <input class="search-input" placeholder="搜索..." />
          </view>
        </view>
      </view>

      <!-- 内容区域 -->
      <view class="content-area">
        <!-- 个人信息卡片 -->
        <view v-if="activeMenu === 'profile'" class="profile-section">
          <view class="profile-card">
            <view class="card-header">
              <view class="user-avatar-wrap">
                <view class="user-avatar" :style="{ background: currentUser?.avatar || '#2563EB' }">
                  <text class="avatar-text">{{ currentUser?.realName?.charAt(0) }}</text>
                </view>
                <view class="avatar-edit" @click="goToEdit">
                  <text class="edit-icon">✎</text>
                </view>
              </view>
              <view class="user-info">
                <text class="user-name">{{ currentUser?.realName }}</text>
                <text class="user-role">{{ getRoleText(currentUser?.role) }}</text>
                <view :class="['verify-badge', currentUser?.isVerified ? 'verified' : 'unverified']">
                  {{ currentUser?.isVerified ? '✓ 已认证' : '○ 未认证' }}
                </view>
              </view>
            </view>
            <view class="card-body">
              <view class="info-grid">
                <view class="info-item">
                  <text class="info-label">用户名</text>
                  <text class="info-value">{{ currentUser?.username }}</text>
                </view>
                <view class="info-item">
                  <text class="info-label">{{ getSchoolIdLabel(currentUser?.role) }}</text>
                  <text class="info-value">{{ currentUser?.schoolId || '-' }}</text>
                </view>
                <view class="info-item">
                  <text class="info-label">院系/部门</text>
                  <text class="info-value">{{ currentUser?.department || '-' }}</text>
                </view>
                <view class="info-item">
                  <text class="info-label">邮箱</text>
                  <text class="info-value">{{ currentUser?.email || '-' }}</text>
                </view>
                <view class="info-item">
                  <text class="info-label">手机号</text>
                  <text class="info-value">{{ currentUser?.phone || '-' }}</text>
                </view>
                <view class="info-item">
                  <text class="info-label">注册时间</text>
                  <text class="info-value">{{ currentUser?.createdAt || '-' }}</text>
                </view>
              </view>
            </view>
          </view>

          <view class="action-cards">
            <view class="action-card" @click="goToEdit">
              <view class="action-icon">✎</view>
              <view class="action-content">
                <text class="action-title">个人信息维护</text>
                <text class="action-desc">修改用户名、头像等个人信息</text>
              </view>
              <text class="action-arrow">→</text>
            </view>
            <view class="action-card" @click="goToChangePassword">
              <view class="action-icon">🔑</view>
              <view class="action-content">
                <text class="action-title">修改密码</text>
                <text class="action-desc">定期更换密码保证账户安全</text>
              </view>
              <text class="action-arrow">→</text>
            </view>
            <view class="action-card" @click="handleLogout">
              <view class="action-icon logout">◉</view>
              <view class="action-content">
                <text class="action-title">退出登录</text>
                <text class="action-desc">安全退出当前账号</text>
              </view>
              <text class="action-arrow">→</text>
            </view>
          </view>
        </view>

        <!-- 我的预约 -->
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
              <text class="th">会议主题</text>
              <text class="th">日期时间</text>
              <text class="th">参会人数</text>
              <text class="th">状态</text>
              <text class="th">操作</text>
            </view>
            <view v-for="res in filteredReservations" :key="res.id" class="table-row">
              <text class="td">{{ res.roomCode }} {{ res.roomName }}</text>
              <text class="td">{{ res.meetingTopic }}</text>
              <text class="td">{{ res.date }} {{ res.startTime }}-{{ res.endTime }}</text>
              <text class="td">{{ res.participantCount }}人</text>
              <view :class="['td status-cell', res.status]">{{ getStatusText(res.status) }}</view>
              <view class="td actions">
                <text v-if="res.status === 'pending'" class="action-btn cancel" @click="handleCancel(res.id)">取消预约</text>
                <text v-else-if="res.status === 'approved'" class="action-btn cancel" @click="handleCancel(res.id)">取消预约</text>
                <text v-else class="action-btn view">查看详情</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useReservationStore } from '@/stores/reservation'

const userStore = useUserStore()
const reservationStore = useReservationStore()

const activeMenu = ref('profile')
const activeReservationTab = ref('all')

const currentUser = computed(() => userStore.currentUser)
const reservations = computed(() => reservationStore.reservations)
const myReservations = computed(() => reservations.value.filter(r => r.applicant === currentUser.value?.realName))

const menuItems = computed(() => [
  { key: 'profile', label: '个人信息', icon: '◎' },
  { key: 'reservations', label: '我的预约', icon: '◯' }
])

const reservationTabs = computed(() => [
  { key: 'all', label: '全部', count: myReservations.value.length },
  { key: 'pending', label: '待审核', count: myReservations.value.filter(r => r.status === 'pending').length },
  { key: 'approved', label: '已通过', count: myReservations.value.filter(r => r.status === 'approved').length },
  { key: 'completed', label: '已完成', count: myReservations.value.filter(r => r.status === 'completed').length }
])

const currentPageTitle = computed(() => {
  const map: Record<string, string> = {
    profile: '个人中心',
    reservations: '我的预约'
  }
  return map[activeMenu.value] || '个人中心'
})

const filteredReservations = computed(() => {
  if (activeReservationTab.value === 'all') return myReservations.value
  return myReservations.value.filter(r => r.status === activeReservationTab.value)
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

function getSchoolIdLabel(role?: string): string {
  const map: Record<string, string> = {
    admin: '管理员编号',
    teacher: '教工号',
    student: '学号',
    organization: '组织编号'
  }
  return map[role || ''] || '身份编号'
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

function goToEdit() {
  uni.navigateTo({ url: '/pages/user/edit' })
}

function goToChangePassword() {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

function handleCancel(id: string) {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消此预约吗？',
    success: (res) => {
      if (res.confirm) {
        reservationStore.cancelReservation(id)
        uni.showToast({ title: '已取消', icon: 'success' })
      }
    }
  })
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
.profile-container {
  display: flex;
  min-height: 100vh;
  background: $bg-page;
}

/* ===== 侧边栏 ===== */
.sidebar {
  width: 280rpx;
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
  font-size: $font-base;
  color: rgba(255, 255, 255, 0.9);
}

/* ===== 主内容区域 ===== */
.main-content {
  flex: 1;
  margin-left: 280rpx;
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
}

.search-box {
  display: flex;
  align-items: center;
  background: $bg-page;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  padding: 0 $spacing-md;
  height: 64rpx;
  width: 300rpx;
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

/* ===== 内容区域 ===== */
.content-area {
  flex: 1;
  padding: $spacing-lg;
  overflow: auto;
}

/* ===== 个人信息卡片 ===== */
.profile-section {
  display: flex;
  gap: $spacing-lg;
}

.profile-card {
  flex: 1;
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-xl;
  box-shadow: $shadow-sm;
}

.card-header {
  display: flex;
  gap: $spacing-lg;
  padding-bottom: $spacing-xl;
  border-bottom: 1rpx solid $border-light;
}

.user-avatar-wrap {
  position: relative;
}

.user-avatar {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow;
}

.avatar-text {
  font-size: 56rpx;
  font-weight: 700;
  color: $white;
}

.avatar-edit {
  position: absolute;
  bottom: 8rpx;
  right: 8rpx;
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: $primary-color;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  
  &:hover {
    background: $primary-dark;
  }
}

.edit-icon {
  font-size: 24rpx;
  color: $white;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: $spacing-sm;
}

.user-name {
  font-size: $font-2xl;
  font-weight: 700;
  color: $text-title;
}

.user-role {
  font-size: $font-base;
  color: $text-secondary;
}

.verify-badge {
  display: inline-flex;
  align-items: center;
  padding: 8rpx 20rpx;
  border-radius: $radius-full;
  font-size: $font-xs;
  width: fit-content;
  
  &.verified {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  
  &.unverified {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
}

.card-body {
  padding-top: $spacing-xl;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-lg;
}

.info-item {
  background: $bg-page;
  padding: $spacing-md;
  border-radius: $radius-lg;
}

.info-label {
  font-size: $font-xs;
  color: $text-muted;
  display: block;
  margin-bottom: $spacing-xs;
}

.info-value {
  font-size: $font-base;
  color: $text-title;
  font-weight: 500;
}

/* ===== 操作卡片 ===== */
.action-cards {
  width: 400rpx;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.action-card {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-lg;
  background: $bg-card;
  border-radius: $radius-xl;
  cursor: pointer;
  box-shadow: $shadow-sm;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateX(8rpx);
    box-shadow: $shadow;
  }
}

.action-icon {
  width: 64rpx;
  height: 64rpx;
  border-radius: $radius-lg;
  background: rgba($primary-color, 0.1);
  color: $primary-color;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  
  &.logout {
    background: rgba($error-color, 0.1);
    color: $error-color;
  }
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: $font-base;
  font-weight: 600;
  color: $text-title;
  display: block;
}

.action-desc {
  font-size: $font-xs;
  color: $text-muted;
}

.action-arrow {
  font-size: $font-lg;
  color: $text-muted;
}

/* ===== 预约列表 ===== */
.reservations-section {
  max-width: 1400rpx;
}

.tabs {
  display: flex;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;
  background: $bg-card;
  padding: $spacing-xs;
  border-radius: $radius-xl;
  width: fit-content;
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

.reservation-table {
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

.th:first-child, .td:first-child { flex: 1.2; }
.th:last-child, .td:last-child { flex: 1; }

.td {
  color: $text-primary;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.status-cell {
    padding: 8rpx 20rpx;
    border-radius: $radius-full;
    font-size: $font-xs;
    font-weight: 500;
    
    &.pending { background: rgba($warning-color, 0.1); color: $warning-color; }
    &.approved { background: rgba($success-color, 0.1); color: $success-color; }
    &.rejected, &.cancelled { background: rgba($error-color, 0.1); color: $error-color; }
    &.completed { background: $bg-hover; color: $text-muted; }
  }
}

.actions {
  display: flex;
  justify-content: center;
  gap: $spacing-sm;
}

.action-btn {
  padding: 8rpx 20rpx;
  border-radius: $radius-md;
  font-size: $font-xs;
  cursor: pointer;
  
  &.cancel { background: rgba($warning-color, 0.1); color: $warning-color; }
  &.view { background: rgba($primary-color, 0.1); color: $primary-color; }
  
  &:hover {
    opacity: 0.8;
  }
}
</style>