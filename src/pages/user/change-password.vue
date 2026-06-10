<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">修改密码</text>
      <view class="header-placeholder"></view>
    </view>

    <view class="password-content">
      <!-- 安全提示 -->
      <view class="security-tip">
        <view class="tip-icon-wrap">🔒</view>
        <view class="tip-content">
          <text class="tip-title">安全提醒</text>
          <text class="tip-desc">请确保密码长度不少于8位，包含字母和数字</text>
        </view>
      </view>

      <!-- 修改密码表单 -->
      <view class="password-form">
        <view class="form-item">
          <text class="form-label">原密码</text>
          <view class="input-wrap">
            <input 
              class="form-input" 
              v-model="oldPassword" 
              placeholder="请输入原密码"
              type="password"
            />
            <view class="eye-btn" @click="showOldPwd = !showOldPwd">
              <text>{{ showOldPwd ? '🙈' : '👁️' }}</text>
            </view>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">新密码</text>
          <view class="input-wrap">
            <input 
              class="form-input" 
              v-model="newPassword" 
              placeholder="请输入新密码"
              :type="showNewPwd ? 'text' : 'password'"
            />
            <view class="eye-btn" @click="showNewPwd = !showNewPwd">
              <text>{{ showNewPwd ? '🙈' : '👁️' }}</text>
            </view>
          </view>
          <view v-if="newPassword" class="pwd-strength">
            <text class="strength-label">密码强度：</text>
            <view class="strength-bars">
              <view :class="['bar', { active: strength >= 1, strong: strength >= 2 }]"></view>
              <view :class="['bar', { active: strength >= 2, strong: strength >= 3 }]"></view>
              <view :class="['bar', { active: strength >= 3 }]"></view>
            </view>
            <text class="strength-text">{{ strengthText }}</text>
          </view>
        </view>

        <view class="form-item">
          <text class="form-label">确认密码</text>
          <view class="input-wrap">
            <input 
              class="form-input" 
              v-model="confirmPassword" 
              placeholder="请再次输入新密码"
              :type="showConfirmPwd ? 'text' : 'password'"
            />
            <view class="eye-btn" @click="showConfirmPwd = !showConfirmPwd">
              <text>{{ showConfirmPwd ? '🙈' : '👁️' }}</text>
            </view>
          </view>
          <view v-if="confirmPassword && newPassword !== confirmPassword" class="error-hint">
            <text>两次输入的密码不一致</text>
          </view>
        </view>
      </view>

      <!-- 提交按钮 -->
      <view 
        :class="['submit-btn', { disabled: !canSubmit }]" 
        @click="handleSubmit"
      >
        <text>确认修改</text>
      </view>

      <!-- 找回密码 -->
      <view class="forgot-link" @click="goToForgot">
        <text>忘记密码？</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showOldPwd = ref(false)
const showNewPwd = ref(false)
const showConfirmPwd = ref(false)

const strength = computed(() => {
  let score = 0
  if (newPassword.value.length >= 8) score++
  if (newPassword.value.length >= 12) score++
  if (/[a-zA-Z]/.test(newPassword.value)) score++
  if (/[0-9]/.test(newPassword.value)) score++
  if (/[^a-zA-Z0-9]/.test(newPassword.value)) score++
  return Math.min(score, 3)
})

const strengthText = computed(() => {
  const texts = ['弱', '中等', '强']
  return texts[strength.value] || '弱'
})

const canSubmit = computed(() => {
  return oldPassword.value.trim() && 
         newPassword.value.trim() && 
         confirmPassword.value.trim() && 
         newPassword.value === confirmPassword.value &&
         newPassword.value.length >= 8
})

function goBack() {
  uni.navigateBack()
}

function goToForgot() {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

function handleSubmit() {
  if (!canSubmit.value) {
    uni.showToast({ title: '请检查输入内容', icon: 'none' })
    return
  }

  const success = userStore.changePassword(oldPassword.value, newPassword.value)

  if (success) {
    uni.showToast({ title: '修改成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } else {
    uni.showToast({ title: '原密码错误', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.container {
  min-height: 100vh;
  background: $bg-color;
}

/* ===== 顶部标题栏 ===== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx 40rpx;
  background: #ffffff;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.header-back {
  width: 72rpx;
  height: 72rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 50%;
  cursor: pointer;
}

.back-icon {
  font-size: 40rpx;
  color: $text-color;
}

.header-title {
  font-size: 36rpx;
  font-weight: 700;
  color: $text-color;
}

.header-placeholder {
  width: 72rpx;
}

/* ===== 密码内容 ===== */
.password-content {
  padding: 32rpx;
}

/* ===== 安全提示 ===== */
.security-tip {
  display: flex;
  gap: 20rpx;
  padding: 28rpx;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
  border-radius: 16rpx;
  margin-bottom: 32rpx;
}

.tip-icon-wrap {
  font-size: 48rpx;
}

.tip-content {
  flex: 1;
}

.tip-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 8rpx;
}

.tip-desc {
  font-size: 24rpx;
  color: $text-secondary;
}

/* ===== 密码表单 ===== */
.password-form {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: $shadow;
}

.form-item {
  margin-bottom: 32rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.form-label {
  display: block;
  font-size: 28rpx;
  color: $text-secondary;
  margin-bottom: 12rpx;
}

.input-wrap {
  position: relative;
}

.form-input {
  width: 100%;
  height: 88rpx;
  padding: 0 100rpx 0 28rpx;
  background: #f8fafc;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  font-size: 30rpx;
  box-sizing: border-box;
  
  &::placeholder {
    color: $text-light;
  }
}

.eye-btn {
  position: absolute;
  right: 24rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 32rpx;
  cursor: pointer;
}

/* ===== 密码强度 ===== */
.pwd-strength {
  margin-top: 12rpx;
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.strength-label {
  font-size: 24rpx;
  color: $text-secondary;
}

.strength-bars {
  display: flex;
  gap: 8rpx;
}

.bar {
  width: 60rpx;
  height: 8rpx;
  background: #e2e8f0;
  border-radius: 4rpx;
  transition: all 0.3s ease;
  
  &.active {
    background: #f59e0b;
  }
  
  &.strong {
    background: $success-color;
  }
}

.strength-text {
  font-size: 24rpx;
  color: $text-secondary;
}

/* ===== 错误提示 ===== */
.error-hint {
  margin-top: 12rpx;
  font-size: 24rpx;
  color: $error-color;
}

/* ===== 提交按钮 ===== */
.submit-btn {
  margin-top: 32rpx;
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 20rpx;
  font-size: 34rpx;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    opacity: 0.9;
  }
  
  &.disabled {
    background: #cbd5e1;
    cursor: not-allowed;
  }
}

/* ===== 找回密码 ===== */
.forgot-link {
  text-align: center;
  margin-top: 32rpx;
  font-size: 28rpx;
  color: #3b82f6;
  cursor: pointer;
}
</style>