<template>
  <view class="container">
    <!-- 背景装饰 -->
    <view class="bg-decoration">
      <view class="bg-circle bg-circle-1"></view>
      <view class="bg-circle bg-circle-2"></view>
      <view class="bg-circle bg-circle-3"></view>
      <view class="bg-circle bg-circle-4"></view>
    </view>
    
    <view class="login-card">
      <!-- 头部Logo和标题 -->
      <view class="login-header">
        <view class="logo">
          <text class="logo-icon">🏢</text>
        </view>
        <text class="login-title">会议室调度系统</text>
        <text class="login-sub">高效预约，轻松管理</text>
      </view>

      <!-- 身份选择 -->
      <view class="role-section">
        <text class="section-title">选择身份</text>
        <view class="role-options">
          <view 
            class="role-option" 
            :class="{ active: role === 'user' }"
            @click="role = 'user'"
          >
            <text class="role-icon">👤</text>
            <text class="role-name">普通用户</text>
            <text class="role-desc">预约会议室</text>
          </view>
          <view 
            class="role-option" 
            :class="{ active: role === 'admin' }"
            @click="role = 'admin'"
          >
            <text class="role-icon">🔧</text>
            <text class="role-name">管理员</text>
            <text class="role-desc">管理系统</text>
          </view>
        </view>
      </view>

      <!-- 用户名输入 -->
      <view class="form-item">
        <view class="input-wrap">
          <text class="input-icon">👤</text>
          <input 
            class="form-input" 
            v-model="username" 
            placeholder="请输入用户名"
            type="text"
          />
        </view>
      </view>

      <!-- 密码输入 -->
      <view class="form-item">
        <view class="input-wrap">
          <text class="input-icon">🔑</text>
          <input 
            class="form-input" 
            v-model="password" 
            placeholder="请输入密码"
            type="password"
          />
        </view>
      </view>

      <!-- 记住我 -->
      <view class="remember-me">
        <view class="checkbox" :class="{ checked: rememberMe }" @click="rememberMe = !rememberMe">
          <text v-if="rememberMe" class="check-icon">✓</text>
        </view>
        <text class="remember-text">记住我</text>
      </view>

      <!-- 登录按钮 -->
      <view class="btn-primary" @click="handleLogin">
        <text class="btn-text">登 录</text>
      </view>

      <!-- 辅助链接 -->
      <view class="helper-links">
        <text class="helper-link" @click="goToForgotPassword">忘记密码？</text>
        <text class="divider">|</text>
        <text class="helper-link" @click="goToRegister">立即注册</text>
      </view>

      <!-- 测试账号提示 -->
      <view class="test-info">
        <text class="test-label">测试账号</text>
        <text class="test-account">普通用户: user / 123456</text>
        <text class="test-account">管理员: admin / 123456</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const username = ref('')
const password = ref('')
const role = ref('user')
const rememberMe = ref(false)

function handleLogin() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }
  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' })
    return
  }

  const success = userStore.login(username.value, password.value)
  if (success) {
    uni.showToast({ title: '登录成功', icon: 'success' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 1500)
  } else {
    uni.showToast({ title: '用户名或密码错误', icon: 'none' })
  }
}

function goToRegister() {
  uni.navigateTo({ url: '/pages/user/register' })
}

function goToForgotPassword() {
  uni.navigateTo({ url: '/pages/user/forgot-password' })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 60rpx 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  
  &-1 {
    width: 500rpx;
    height: 500rpx;
    background: rgba(255, 255, 255, 0.15);
    top: -150rpx;
    right: -100rpx;
  }
  
  &-2 {
    width: 400rpx;
    height: 400rpx;
    background: rgba(255, 255, 255, 0.1);
    bottom: -100rpx;
    left: -80rpx;
  }
  
  &-3 {
    width: 250rpx;
    height: 250rpx;
    background: rgba(255, 255, 255, 0.08);
    top: 30%;
    right: 25%;
  }
  
  &-4 {
    width: 180rpx;
    height: 180rpx;
    background: rgba(255, 255, 255, 0.05);
    bottom: 30%;
    right: 10%;
  }
}

.login-card {
  width: 100%;
  max-width: 680rpx;
  background: rgba(255, 255, 255, 0.95);
  border-radius: $radius-lg;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.2);
  padding: 60rpx 50rpx;
  position: relative;
  z-index: 10;
  backdrop-filter: blur(20rpx);
}

.login-header {
  text-align: center;
  margin-bottom: 50rpx;
}

.logo {
  width: 120rpx;
  height: 120rpx;
  margin: 0 auto 25rpx;
  background: linear-gradient(135deg, $primary-color 0%, $primary-dark 100%);
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 32rpx rgba(74, 144, 217, 0.3);
}

.logo-icon {
  font-size: 60rpx;
}

.login-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $text-color;
  margin-bottom: 12rpx;
  letter-spacing: 2rpx;
}

.login-sub {
  font-size: 28rpx;
  color: $text-light;
}

/* 身份选择 */
.role-section {
  margin-bottom: 40rpx;
}

.section-title {
  display: block;
  font-size: 28rpx;
  color: $text-secondary;
  margin-bottom: 20rpx;
}

.role-options {
  display: flex;
  gap: 20rpx;
}

.role-option {
  flex: 1;
  padding: 28rpx 20rpx;
  background: $bg-color;
  border-radius: $radius;
  border: 2rpx solid transparent;
  text-align: center;
  transition: all 0.3s ease;
  
  &.active {
    background: rgba($primary-color, 0.08);
    border-color: $primary-color;
  }
  
  &:active {
    transform: scale(0.98);
  }
}

.role-icon {
  display: block;
  font-size: 48rpx;
  margin-bottom: 12rpx;
}

.role-name {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 6rpx;
}

.role-desc {
  display: block;
  font-size: 24rpx;
  color: $text-light;
}

/* 表单 */
.form-item {
  margin-bottom: 28rpx;
}

.input-wrap {
  display: flex;
  align-items: center;
  background: $bg-color;
  border-radius: $radius;
  padding: 0 24rpx;
  border: 2rpx solid $border-color;
  
  &:focus-within {
    border-color: $primary-color;
    background: $white;
  }
}

.input-icon {
  font-size: 36rpx;
  margin-right: 20rpx;
  color: $text-light;
}

.form-input {
  flex: 1;
  height: 90rpx;
  font-size: 30rpx;
  color: $text-color;
  background: transparent;
}

/* 记住我 */
.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
}

.checkbox {
  width: 36rpx;
  height: 36rpx;
  border: 2rpx solid $border-color;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
  
  &.checked {
    background: $primary-color;
    border-color: $primary-color;
  }
}

.check-icon {
  font-size: 24rpx;
  color: $white;
}

.remember-text {
  font-size: 26rpx;
  color: $text-secondary;
}

/* 登录按钮 */
.btn-primary {
  width: calc(100% - 4rpx);
  height: 96rpx;
  background: linear-gradient(135deg, $primary-color 0%, $primary-dark 100%);
  color: $white;
  border-radius: $radius;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-sizing: border-box;
  
  &:active {
    opacity: 0.9;
  }
}

.btn-text {
  font-size: 34rpx;
  font-weight: 600;
  letter-spacing: 8rpx;
}

/* 辅助链接 */
.helper-links {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 36rpx;
  font-size: 28rpx;
  color: $text-secondary;
}

.helper-link {
  color: $primary-color;
  
  &:active {
    opacity: 0.7;
  }
}

.divider {
  margin: 0 24rpx;
  color: $border-color;
}

/* 测试账号 */
.test-info {
  margin-top: 40rpx;
  padding-top: 30rpx;
  border-top: 2rpx dashed $border-color;
  text-align: center;
}

.test-label {
  display: block;
  font-size: 24rpx;
  color: $text-light;
  margin-bottom: 12rpx;
}

.test-account {
  display: block;
  font-size: 24rpx;
  color: $text-secondary;
  margin-bottom: 6rpx;
}
</style>
