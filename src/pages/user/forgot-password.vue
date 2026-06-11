<template>
  <view class="container">
    <!-- 背景装饰 -->
    <view class="bg-decoration">
      <view class="bg-circle bg-circle-1"></view>
      <view class="bg-circle bg-circle-2"></view>
      <view class="bg-circle bg-circle-3"></view>
      <view class="bg-circle bg-circle-4"></view>
    </view>
    
    <view class="forgot-card">
      <!-- 头部 -->
      <view class="forgot-header">
        <view class="back-btn" @click="goBack">
          <text class="back-icon">←</text>
        </view>
        <view class="header-content">
          <view class="icon-wrap">
            <text class="icon">🔐</text>
          </view>
          <text class="title">忘记密码</text>
          <text class="subtitle">请输入您的账号信息，我们将发送验证码到您的邮箱</text>
        </view>
      </view>

      <!-- 表单 -->
      <view class="form">
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

        <!-- 邮箱输入 -->
        <view class="form-item">
          <view class="input-wrap">
            <text class="input-icon">📧</text>
            <input 
              class="form-input" 
              v-model="email" 
              placeholder="请输入邮箱"
              type="text"
            />
          </view>
        </view>

        <!-- 验证码输入 -->
        <view class="form-item">
          <view class="input-wrap captcha-wrap">
            <text class="input-icon">✏️</text>
            <input 
              class="form-input" 
              v-model="captcha" 
              placeholder="请输入验证码"
              type="text"
            />
            <view 
              class="captcha-btn" 
              :class="{ disabled: !canSendCaptcha }"
              @click="sendCaptcha"
            >
              <text class="captcha-text">{{ captchaText }}</text>
            </view>
          </view>
        </view>

        <!-- 新密码输入 -->
        <view class="form-item">
          <view class="input-wrap">
            <text class="input-icon">🔑</text>
            <input 
              class="form-input" 
              v-model="newPassword" 
              placeholder="请输入新密码"
              type="password"
            />
          </view>
        </view>

        <!-- 确认密码输入 -->
        <view class="form-item">
          <view class="input-wrap">
            <text class="input-icon">🔑</text>
            <input 
              class="form-input" 
              v-model="confirmPassword" 
              placeholder="请确认新密码"
              type="password"
            />
          </view>
        </view>
      </view>

      <!-- 提交按钮 -->
      <view class="btn-primary" @click="handleSubmit">
        <text class="btn-text">重置密码</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const captcha = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const canSendCaptcha = ref(true)
const captchaText = ref('获取验证码')

function goBack() {
  uni.navigateBack()
}

function sendCaptcha() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }
  if (!email.value.trim()) {
    uni.showToast({ title: '请输入邮箱', icon: 'none' })
    return
  }
  
  // 模拟发送验证码
  canSendCaptcha.value = false
  captchaText.value = '60s'
  
  let count = 60
  const timer = setInterval(() => {
    count--
    captchaText.value = `${count}s`
    if (count <= 0) {
      clearInterval(timer)
      canSendCaptcha.value = true
      captchaText.value = '获取验证码'
    }
  }, 1000)
  
  uni.showToast({ title: '验证码已发送', icon: 'success' })
}

function handleSubmit() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }
  if (!email.value.trim()) {
    uni.showToast({ title: '请输入邮箱', icon: 'none' })
    return
  }
  if (!captcha.value.trim()) {
    uni.showToast({ title: '请输入验证码', icon: 'none' })
    return
  }
  if (!newPassword.value.trim()) {
    uni.showToast({ title: '请输入新密码', icon: 'none' })
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    uni.showToast({ title: '两次密码不一致', icon: 'none' })
    return
  }
  
  // 模拟重置密码成功
  uni.showToast({ title: '密码重置成功', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
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

.forgot-card {
  width: 100%;
  max-width: 680rpx;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24rpx;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.2);
  padding: 40rpx 50rpx;
  position: relative;
  z-index: 10;
}

.forgot-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 40rpx;
}

.back-btn {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  
  &:active {
    opacity: 0.7;
  }
}

.back-icon {
  font-size: 40rpx;
  color: $text-color;
}

.header-content {
  flex: 1;
  text-align: center;
}

.icon-wrap {
  width: 80rpx;
  height: 80rpx;
  margin: 0 auto 20rpx;
  background: linear-gradient(135deg, $primary-color 0%, $primary-dark 100%);
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  font-size: 40rpx;
}

.title {
  display: block;
  font-size: 36rpx;
  font-weight: 700;
  color: $text-color;
  margin-bottom: 10rpx;
}

.subtitle {
  font-size: 24rpx;
  color: $text-light;
  line-height: 1.6;
}

/* 表单 */
.form {
  margin-bottom: 30rpx;
}

.form-item {
  margin-bottom: 24rpx;
}

.input-wrap {
  display: flex;
  align-items: center;
  background: $bg-color;
  border-radius: $radius;
  padding: 0 24rpx;
  border: 2rpx solid $border-color;
  
  &.captcha-wrap {
    padding-right: 10rpx;
  }
  
  &:focus-within {
    border-color: $primary-color;
    background: $white;
  }
}

.input-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
  color: $text-light;
}

.form-input {
  flex: 1;
  height: 88rpx;
  font-size: 28rpx;
  color: $text-color;
  background: transparent;
}

.captcha-btn {
  width: 160rpx;
  height: 64rpx;
  background: $primary-color;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.disabled {
    background: $text-light;
  }
  
  &:active:not(.disabled) {
    opacity: 0.8;
  }
}

.captcha-text {
  font-size: 24rpx;
  color: $white;
}

/* 提交按钮 */
.btn-primary {
  width: calc(100% - 4rpx);
  height: 90rpx;
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
  font-size: 32rpx;
  font-weight: 600;
}
</style>
