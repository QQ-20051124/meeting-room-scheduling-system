<template>
  <view class="container">
    <view class="login-card">
      <view class="login-header">
        <text class="login-title">用户登录</text>
        <text class="login-sub">欢迎使用会议室调度系统</text>
      </view>

      <view class="form-item">
        <text class="form-label">用户名</text>
        <input 
          class="form-input" 
          v-model="username" 
          placeholder="请输入用户名"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">密码</text>
        <input 
          class="form-input" 
          v-model="password" 
          placeholder="请输入密码"
          type="password"
        />
      </view>

      <view class="btn-primary" @click="handleLogin">登录</view>

      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link" @click="goToRegister">立即注册</text>
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
      uni.navigateBack()
    }, 1500)
  } else {
    uni.showToast({ title: '用户名或密码错误', icon: 'none' })
  }
}

function goToRegister() {
  uni.navigateTo({ url: '/pages/user/register' })
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 40rpx 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 600rpx;
  background: $white;
  border-radius: $radius;
  box-shadow: $shadow;
  padding: 40rpx;
}

.login-header {
  text-align: center;
  margin-bottom: 50rpx;
}

.login-title {
  display: block;
  font-size: $font-xl;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.login-sub {
  font-size: 26rpx;
  color: $text-light;
}

.register-link {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30rpx;
  font-size: 26rpx;
  color: $text-secondary;
}

.link {
  color: $primary-color;
  margin-left: 10rpx;
}
</style>
