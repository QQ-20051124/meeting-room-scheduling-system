<template>
  <view class="container">
    <!-- 顶部背景 -->
    <view class="profile-bg">
      <view class="bg-gradient"></view>
    </view>

    <!-- 用户信息卡片 -->
    <view class="profile-card">
      <view class="avatar-section">
        <view class="avatar" @click="changeAvatar">
          <text class="avatar-text">{{ getAvatarText(currentUser) }}</text>
          <view class="avatar-edit">
            <text class="edit-icon">📷</text>
          </view>
        </view>
        <view class="user-info">
          <text class="user-name">{{ currentUser?.realName || currentUser?.username || '未登录' }}</text>
          <view :class="['auth-badge', { certified: isCertified, uncertified: !isCertified }]">
            <text>{{ isCertified ? '✓ 已认证' : '⚠️ 未认证' }}</text>
          </view>
        </view>
        <view v-if="!isLoggedIn" class="login-btn" @click="goToLogin">
          <text>登录 / 注册</text>
        </view>
      </view>

      <!-- 未认证用户红色边框提示 -->
      <view v-if="isLoggedIn && !isCertified" class="certification-prompt">
        <view class="prompt-icon">🔒</view>
        <view class="prompt-content">
          <text class="prompt-title">请完成身份认证</text>
          <text class="prompt-desc">认证后可享受完整预约功能</text>
        </view>
        <view class="prompt-action" @click="goToCertify">
          <text>立即认证</text>
        </view>
      </view>
    </view>

    <!-- 身份认证入口 -->
    <view v-if="isLoggedIn" class="section-card">
      <view class="section-header">
        <text class="section-title">👤 身份认证</text>
        <view :class="['section-status', { completed: isCertified }]">
          <text>{{ isCertified ? '已完成' : '待认证' }}</text>
        </view>
      </view>
      <view class="certify-info" @click="goToCertify">
        <view class="certify-icon">
          <text>{{ isCertified ? '✅' : '📝' }}</text>
        </view>
        <view class="certify-detail">
          <text class="certify-title">{{ isCertified ? '认证信息' : '点击进行身份认证' }}</text>
          <text class="certify-desc">{{ isCertified ? `学号/教工号: ${currentUser?.schoolId}` : '需要学号或教工号进行认证' }}</text>
        </view>
        <text class="certify-arrow">›</text>
      </view>
    </view>

    <!-- 个人信息编辑 -->
    <view v-if="isLoggedIn" class="section-card">
      <view class="section-header">
        <text class="section-title">👤 个人信息</text>
      </view>
      <view class="info-list">
        <view class="info-item" @click="editField('realName')">
          <text class="info-label">真实姓名</text>
          <view class="info-value-wrap">
            <text class="info-value">{{ currentUser?.realName || '未设置' }}</text>
            <text class="info-arrow">›</text>
          </view>
        </view>
        <view class="info-item" @click="editField('username')">
          <text class="info-label">用户名</text>
          <view class="info-value-wrap">
            <text class="info-value">{{ currentUser?.username || '未设置' }}</text>
            <text class="info-arrow">›</text>
          </view>
        </view>
        <view class="info-item" @click="editField('phone')">
          <text class="info-label">手机号码</text>
          <view class="info-value-wrap">
            <text class="info-value">{{ currentUser?.phone || '未设置' }}</text>
            <text class="info-arrow">›</text>
          </view>
        </view>
        <view class="info-item" @click="editField('email')">
          <text class="info-label">邮箱地址</text>
          <view class="info-value-wrap">
            <text class="info-value">{{ currentUser?.email || '未设置' }}</text>
            <text class="info-arrow">›</text>
          </view>
        </view>
        <view class="info-item">
          <text class="info-label">用户角色</text>
          <view class="info-value-wrap">
            <text class="info-value">{{ getUserRole(currentUser?.role) }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 安全设置 -->
    <view v-if="isLoggedIn" class="section-card">
      <view class="section-header">
        <text class="section-title">🔐 安全设置</text>
      </view>
      <view class="setting-list">
        <view class="setting-item" @click="goToChangePassword">
          <view class="setting-icon">🔑</view>
          <text class="setting-text">修改密码</text>
          <text class="setting-arrow">›</text>
        </view>
        <view class="setting-item" @click="goToSecurity">
          <view class="setting-icon">🛡️</view>
          <text class="setting-text">账号安全</text>
          <text class="setting-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 快捷操作 -->
    <view v-if="isLoggedIn" class="section-card">
      <view class="section-header">
        <text class="section-title">⚡ 快捷操作</text>
      </view>
      <view class="action-grid">
        <view class="action-item" @click="goToMyReservation">
          <view class="action-icon-wrap">
            <text class="action-icon">📅</text>
          </view>
          <text class="action-text">我的预约</text>
        </view>
        <view class="action-item" @click="goToFavorite">
          <view class="action-icon-wrap">
            <text class="action-icon">❤️</text>
          </view>
          <text class="action-text">收藏列表</text>
        </view>
        <view class="action-item" @click="goToHistory">
          <view class="action-icon-wrap">
            <text class="action-icon">📜</text>
          </view>
          <text class="action-text">预约历史</text>
        </view>
        <view class="action-item" @click="goToFeedback">
          <view class="action-icon-wrap">
            <text class="action-icon">💬</text>
          </view>
          <text class="action-text">意见反馈</text>
        </view>
      </view>
    </view>

    <!-- 系统信息 -->
    <view v-if="isLoggedIn" class="section-card">
      <view class="setting-list">
        <view class="setting-item" @click="goToAbout">
          <view class="setting-icon">ℹ️</view>
          <text class="setting-text">关于系统</text>
          <text class="setting-arrow">›</text>
        </view>
        <view class="setting-item logout" @click="handleLogout">
          <view class="setting-icon">🚪</view>
          <text class="setting-text">退出登录</text>
          <text class="setting-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 未登录状态 -->
    <view v-if="!isLoggedIn" class="guest-section">
      <view class="guest-card" @click="goToLogin">
        <view class="guest-icon">👤</view>
        <text class="guest-text">登录后可使用完整功能</text>
        <text class="guest-arrow">›</text>
      </view>
      <view class="guest-card" @click="goToRegister">
        <view class="guest-icon">📝</view>
        <text class="guest-text">注册新账号</text>
        <text class="guest-arrow">›</text>
      </view>
    </view>
    
    <!-- 自定义底部导航 -->
    <CustomTabbar current="profile" />
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import CustomTabbar from '@/components/custom-tabbar/CustomTabbar.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const currentUser = computed(() => userStore.currentUser)
const isLoggedIn = computed(() => userStore.isLoggedIn())
const isCertified = computed(() => userStore.isCertified())

function getAvatarText(user: User | null | undefined): string {
  if (!user) return '?'
  const name = user.realName || user.username || '?'
  return name.charAt(0).toUpperCase()
}

function getUserRole(role?: string): string {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生',
    organization: '组织'
  }
  return roleMap[role || ''] || '普通用户'
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}

function goToRegister() {
  uni.navigateTo({ url: '/pages/user/register' })
}

function goToCertify() {
  uni.navigateTo({ url: '/pages/user/certify' })
}

function goToChangePassword() {
  uni.navigateTo({ url: '/pages/user/change-password' })
}

function goToSecurity() {
  uni.navigateTo({ url: '/pages/user/security' })
}

function goToMyReservation() {
  uni.switchTab({ url: '/pages/reservation/list' })
}

function goToFavorite() {
  uni.navigateTo({ url: '/pages/user/favorite' })
}

function goToHistory() {
  uni.switchTab({ url: '/pages/reservation/list' })
}

function goToFeedback() {
  uni.navigateTo({ url: '/pages/user/feedback' })
}

function goToAbout() {
  uni.showModal({
    title: '关于系统',
    content: '会议室调度系统 v1.0\n\n一款便捷的会议室预约管理系统，支持预约申请、审核管理、资源统计等功能。',
    showCancel: false
  })
}

function changeAvatar() {
  uni.showActionSheet({
    itemList: ['拍照', '从相册选择'],
    success: (res) => {
      uni.showToast({ title: '头像修改功能开发中', icon: 'none' })
    }
  })
}

function editField(field: string) {
  const fieldNames: Record<string, string> = {
    realName: '真实姓名',
    username: '用户名',
    phone: '手机号码',
    email: '邮箱地址'
  }
  uni.showModal({
    title: `修改${fieldNames[field] || field}`,
    editable: true,
    placeholderText: `请输入新的${fieldNames[field] || field}`,
    success: (res) => {
      if (res.confirm && res.content) {
        userStore.updateUserField(field, res.content)
        uni.showToast({ title: '修改成功', icon: 'success' })
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
        uni.showToast({ title: '退出成功', icon: 'success' })
        setTimeout(() => {
          uni.reLaunch({ url: '/pages/user/login' })
        }, 1500)
      }
    }
  })
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.container {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 280rpx;
}

/* ===== 顶部背景 ===== */
.profile-bg {
  position: relative;
  height: 320rpx;
  overflow: hidden;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 50%, #3b82f6 100%);
}

/* ===== 用户信息卡片 ===== */
.profile-card {
  background: #ffffff;
  border-radius: 24rpx;
  margin: -160rpx 24rpx 24rpx;
  padding: 160rpx 32rpx 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  position: relative;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 24rpx;
  margin-bottom: 24rpx;
}

.avatar {
  position: relative;
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 6rpx solid #ffffff;
  box-shadow: 0 8rpx 24rpx rgba(59, 130, 246, 0.3);
}

.avatar-text {
  font-size: 56rpx;
  color: #ffffff;
  font-weight: 700;
}

.avatar-edit {
  position: absolute;
  bottom: -8rpx;
  right: -8rpx;
  width: 56rpx;
  height: 56rpx;
  background: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.edit-icon {
  font-size: 28rpx;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 40rpx;
  font-weight: 700;
  color: $text-color;
  display: block;
  margin-bottom: 12rpx;
}

.auth-badge {
  display: inline-flex;
  padding: 8rpx 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  font-weight: 500;
  
  &.certified {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  
  &.uncertified {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
}

.login-btn {
  padding: 16rpx 32rpx;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 24rpx;
  color: #ffffff;
  font-size: 28rpx;
  font-weight: 500;
}

/* ===== 未认证提示 ===== */
.certification-prompt {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 24rpx;
  background: rgba(239, 68, 68, 0.08);
  border: 2rpx solid rgba(239, 68, 68, 0.3);
  border-radius: 16rpx;
  margin-top: 16rpx;
}

.prompt-icon {
  font-size: 40rpx;
  flex-shrink: 0;
}

.prompt-content {
  flex: 1;
}

.prompt-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $error-color;
  display: block;
  margin-bottom: 6rpx;
}

.prompt-desc {
  font-size: 24rpx;
  color: $text-secondary;
}

.prompt-action {
  padding: 12rpx 24rpx;
  background: $error-color;
  border-radius: 20rpx;
  color: #ffffff;
  font-size: 26rpx;
  font-weight: 500;
}

/* ===== 区块卡片 ===== */
.section-card {
  background: #ffffff;
  border-radius: 20rpx;
  margin: 0 24rpx 24rpx;
  padding: 24rpx;
  box-shadow: $shadow;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding-bottom: 20rpx;
  border-bottom: 2rpx solid $border-color;
}

.section-title {
  font-size: 34rpx;
  font-weight: 700;
  color: $text-color;
}

.section-status {
  font-size: 26rpx;
  padding: 8rpx 20rpx;
  border-radius: 12rpx;
  background: rgba($warning-color, 0.1);
  color: $warning-color;
  
  &.completed {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
}

/* ===== 认证信息 ===== */
.certify-info {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 16rpx;
  background: #f8fafc;
  border-radius: 16rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f1f5f9;
  }
}

.certify-icon {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
}

.certify-detail {
  flex: 1;
}

.certify-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-color;
  display: block;
  margin-bottom: 6rpx;
}

.certify-desc {
  font-size: 24rpx;
  color: $text-secondary;
}

.certify-arrow {
  font-size: 40rpx;
  color: $text-light;
}

/* ===== 信息列表 ===== */
.info-list {
  display: flex;
  flex-direction: column;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 2rpx solid #f1f5f9;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:active {
    opacity: 0.7;
  }
}

.info-label {
  font-size: 30rpx;
  color: $text-secondary;
}

.info-value-wrap {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.info-value {
  font-size: 30rpx;
  color: $text-color;
  font-weight: 500;
}

.info-arrow {
  font-size: 36rpx;
  color: $text-light;
}

/* ===== 设置列表 ===== */
.setting-list {
  display: flex;
  flex-direction: column;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 28rpx 0;
  border-bottom: 2rpx solid #f1f5f9;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: #fafafa;
  }
  
  &.logout {
    .setting-text {
      color: $error-color;
    }
  }
}

.setting-icon {
  font-size: 36rpx;
}

.setting-text {
  flex: 1;
  font-size: 32rpx;
  color: $text-color;
}

.setting-arrow {
  font-size: 40rpx;
  color: $text-light;
}

/* ===== 快捷操作 ===== */
.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 16rpx;
  background: #f8fafc;
  border-radius: 16rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f1f5f9;
    transform: translateY(-4rpx);
  }
}

.action-icon-wrap {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12rpx;
}

.action-icon {
  font-size: 36rpx;
}

.action-text {
  font-size: 24rpx;
  color: $text-color;
}

/* ===== 未登录状态 ===== */
.guest-section {
  padding: 32rpx 24rpx;
}

.guest-card {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 32rpx;
  background: #ffffff;
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  box-shadow: $shadow;
  cursor: pointer;
  
  &:active {
    opacity: 0.7;
  }
}

.guest-icon {
  font-size: 48rpx;
}

.guest-text {
  flex: 1;
  font-size: 32rpx;
  color: $text-color;
}

.guest-arrow {
  font-size: 40rpx;
  color: $text-light;
}
</style>