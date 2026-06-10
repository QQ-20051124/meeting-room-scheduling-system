<template>
  <view class="edit-container">
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
          <text class="back-btn" @click="goBack">← 返回</text>
          <text class="page-title">编辑个人信息</text>
        </view>
      </view>

      <!-- 内容区域 -->
      <view class="content-area">
        <view class="edit-card">
          <!-- 头像选择 -->
          <view class="section">
            <text class="section-title">头像设置</text>
            <view class="avatar-section">
              <view class="current-avatar">
                <view class="avatar-preview" :style="{ background: selectedAvatar || '#2563EB' }">
                  <text class="avatar-text">{{ currentUser?.realName?.charAt(0) }}</text>
                </view>
                <text class="avatar-label">当前头像</text>
              </view>
              <view class="avatar-options">
                <text class="options-title">选择头像颜色</text>
                <view class="color-grid">
                  <view 
                    v-for="color in avatarColors" 
                    :key="color"
                    :class="['color-item', { selected: selectedAvatar === color }]"
                    :style="{ background: color }"
                    @click="selectedAvatar = color"
                  >
                    <text v-if="selectedAvatar === color" class="check-icon">✓</text>
                  </view>
                </view>
              </view>
            </view>
          </view>

          <!-- 个人信息 -->
          <view class="section">
            <text class="section-title">基本信息</text>
            <view class="form-grid">
              <view class="form-item">
                <text class="form-label">用户名</text>
                <input class="form-input" v-model="username" placeholder="请输入用户名" />
              </view>
              <view class="form-item">
                <text class="form-label">真实姓名</text>
                <input class="form-input" v-model="realName" placeholder="请输入真实姓名" />
              </view>
              <view class="form-item">
                <text class="form-label">邮箱</text>
                <input class="form-input" v-model="email" placeholder="请输入邮箱" />
              </view>
              <view class="form-item">
                <text class="form-label">手机号</text>
                <input class="form-input" v-model="phone" placeholder="请输入手机号" />
              </view>
              <view class="form-item">
                <text class="form-label">院系/部门</text>
                <input class="form-input" v-model="department" placeholder="请输入院系或部门" />
              </view>
            </view>
          </view>

          <!-- 身份认证 -->
          <view class="section">
            <text class="section-title">身份认证</text>
            <view class="verify-section">
              <view class="verify-status">
                <text class="verify-label">认证状态</text>
                <view :class="['verify-badge', currentUser?.isVerified ? 'verified' : 'unverified']">
                  {{ currentUser?.isVerified ? '✓ 已认证' : '○ 未认证' }}
                </view>
              </view>
              <view class="school-id-section">
                <view class="form-item">
                  <text class="form-label">{{ getSchoolIdLabel(currentUser?.role) }}
                    <text class="required">*</text>
                  </text>
                  <input 
                    class="form-input" 
                    v-model="schoolId" 
                    :placeholder="getSchoolIdPlaceholder(currentUser?.role)"
                  />
                </view>
                <text class="school-id-tip">{{ getSchoolIdTip(currentUser?.role) }}</text>
              </view>
              <view v-if="!currentUser?.isVerified" class="verify-btn-wrap">
                <view class="btn-primary" @click="handleVerify">提交认证</view>
              </view>
            </view>
          </view>

          <!-- 保存按钮 -->
          <view class="form-actions">
            <view class="btn-secondary" @click="resetForm">重置</view>
            <view class="btn-primary" @click="handleSave">保存修改</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const activeMenu = ref('profile')
const selectedAvatar = ref('')
const username = ref('')
const realName = ref('')
const email = ref('')
const phone = ref('')
const department = ref('')
const schoolId = ref('')

const currentUser = computed(() => userStore.currentUser)

const menuItems = computed(() => [
  { key: 'profile', label: '个人信息', icon: '◎' },
  { key: 'reservations', label: '我的预约', icon: '◯' }
])

const avatarColors = [
  '#2563EB', '#16A34A', '#F59E0B', '#EF4444', 
  '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16',
  '#F97316', '#6366F1', '#EC4899', '#14B8A6'
]

function getSchoolIdLabel(role?: string): string {
  const map: Record<string, string> = {
    admin: '管理员编号',
    teacher: '教工号',
    student: '学号',
    organization: '组织编号'
  }
  return map[role || ''] || '身份编号'
}

function getSchoolIdPlaceholder(role?: string): string {
  const map: Record<string, string> = {
    admin: '请输入管理员编号',
    teacher: '请输入教工号',
    student: '请输入学号',
    organization: '请输入组织编号'
  }
  return map[role || ''] || '请输入身份编号'
}

function getSchoolIdTip(role?: string): string {
  const map: Record<string, string> = {
    admin: '管理员编号由系统分配',
    teacher: '教工号由学校人事部门分配',
    student: '学号为您的学生注册号',
    organization: '组织编号由社团联合会分配'
  }
  return map[role || ''] || '请填写您的身份编号完成实名认证'
}

function goBack() {
  uni.navigateBack()
}

function resetForm() {
  if (currentUser.value) {
    selectedAvatar.value = currentUser.value.avatar || '#2563EB'
    username.value = currentUser.value.username
    realName.value = currentUser.value.realName
    email.value = currentUser.value.email || ''
    phone.value = currentUser.value.phone || ''
    department.value = currentUser.value.department || ''
    schoolId.value = currentUser.value.schoolId || ''
  }
}

function handleSave() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }
  if (!realName.value.trim()) {
    uni.showToast({ title: '请输入真实姓名', icon: 'none' })
    return
  }

  userStore.updateUser({
    avatar: selectedAvatar.value,
    username: username.value,
    realName: realName.value,
    email: email.value,
    phone: phone.value,
    department: department.value,
    schoolId: schoolId.value
  })

  uni.showToast({ title: '保存成功', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}

function handleVerify() {
  if (!schoolId.value.trim()) {
    uni.showToast({ title: `请输入${getSchoolIdLabel(currentUser.value?.role)}`, icon: 'none' })
    return
  }

  userStore.updateUser({
    schoolId: schoolId.value,
    isVerified: true
  })

  uni.showToast({ title: '认证成功', icon: 'success' })
}

onMounted(() => {
  userStore.loadUser()
  resetForm()
})
</script>

<style lang="scss" scoped>
.edit-container {
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
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.back-btn {
  font-size: $font-base;
  color: $primary-color;
  cursor: pointer;
  
  &:hover {
    text-decoration: underline;
  }
}

.page-title {
  font-size: $font-xl;
  font-weight: 700;
  color: $text-title;
}

/* ===== 内容区域 ===== */
.content-area {
  flex: 1;
  padding: $spacing-lg;
  overflow: auto;
  display: flex;
  justify-content: center;
}

.edit-card {
  width: 800rpx;
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-xl;
  box-shadow: $shadow-sm;
}

.section {
  margin-bottom: $spacing-xl;
  
  &:last-of-type {
    margin-bottom: $spacing-lg;
  }
}

.section-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-title;
  display: block;
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-md;
  border-bottom: 1rpx solid $border-light;
}

/* ===== 头像选择 ===== */
.avatar-section {
  display: flex;
  gap: $spacing-xl;
}

.current-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-sm;
}

.avatar-preview {
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

.avatar-label {
  font-size: $font-sm;
  color: $text-muted;
}

.avatar-options {
  flex: 1;
}

.options-title {
  font-size: $font-base;
  font-weight: 500;
  color: $text-secondary;
  display: block;
  margin-bottom: $spacing-md;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: $spacing-md;
}

.color-item {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    transform: scale(1.1);
  }
  
  &.selected {
    transform: scale(1.15);
    box-shadow: 0 0 0 4rpx rgba($primary-color, 0.3);
  }
}

.check-icon {
  font-size: 28rpx;
  color: $white;
  font-weight: bold;
}

/* ===== 表单 ===== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-lg;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  
  &:last-child {
    grid-column: span 2;
  }
}

.form-label {
  font-size: $font-sm;
  color: $text-secondary;
  
  .required {
    color: $error-color;
  }
}

.form-input {
  padding: $spacing-md;
  border: 1rpx solid $border-color;
  border-radius: $radius-lg;
  font-size: $font-base;
  background: $bg-page;
  
  &:focus {
    border-color: $primary-color;
    outline: none;
  }
}

/* ===== 认证区域 ===== */
.verify-section {
  background: $bg-page;
  border-radius: $radius-lg;
  padding: $spacing-lg;
}

.verify-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-lg;
  border-bottom: 1rpx solid $border-light;
}

.verify-label {
  font-size: $font-base;
  font-weight: 500;
  color: $text-title;
}

.verify-badge {
  padding: 8rpx 24rpx;
  border-radius: $radius-full;
  font-size: $font-sm;
  
  &.verified {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  
  &.unverified {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
}

.school-id-section {
  margin-bottom: $spacing-lg;
}

.school-id-tip {
  font-size: $font-xs;
  color: $text-muted;
  display: block;
  margin-top: $spacing-xs;
}

.verify-btn-wrap {
  text-align: center;
}

/* ===== 表单按钮 ===== */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
  padding-top: $spacing-lg;
  border-top: 1rpx solid $border-light;
}

.btn-primary {
  padding: $spacing-md $spacing-xl;
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
  padding: $spacing-md $spacing-xl;
  border-radius: $radius-lg;
  background: $bg-page;
  color: $text-secondary;
  font-size: $font-base;
  text-align: center;
  cursor: pointer;
  border: 1rpx solid $border-color;
  
  &:hover {
    background: $bg-hover;
  }
}
</style>