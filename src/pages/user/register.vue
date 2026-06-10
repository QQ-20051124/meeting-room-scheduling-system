<template>
  <view class="container">
    <view class="register-card">
      <view class="register-header">
        <text class="register-title">用户注册</text>
        <text class="register-sub">创建您的账号</text>
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

      <view class="form-item">
        <text class="form-label">确认密码</text>
        <input 
          class="form-input" 
          v-model="confirmPassword" 
          placeholder="请再次输入密码"
          type="password"
        />
      </view>

      <view class="form-item">
        <text class="form-label">真实姓名</text>
        <input 
          class="form-input" 
          v-model="realName" 
          placeholder="请输入真实姓名"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">手机号码</text>
        <input 
          class="form-input" 
          v-model="phone" 
          placeholder="请输入手机号码"
          type="number"
        />
      </view>

      <view class="form-item">
        <text class="form-label">邮箱</text>
        <input 
          class="form-input" 
          v-model="email" 
          placeholder="请输入邮箱地址"
          type="text"
        />
      </view>

      <view class="btn-primary" @click="handleRegister">注册</view>

      <view class="login-link">
        <text>已有账号？</text>
        <text class="link" @click="goToLogin">立即登录</text>
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
const confirmPassword = ref('')
const realName = ref('')
const phone = ref('')
const email = ref('')

function handleRegister() {
  if (!username.value.trim()) {
    uni.showToast({ title: '请输入用户名', icon: 'none' })
    return
  }
  if (!password.value.trim()) {
    uni.showToast({ title: '请输入密码', icon: 'none' })
    return
  }
  if (password.value !== confirmPassword.value) {
    uni.showToast({ title: '两次输入的密码不一致', icon: 'none' })
    return
  }
  if (!realName.value.trim()) {
    uni.showToast({ title: '请输入真实姓名', icon: 'none' })
    return
  }

  const success = userStore.register({
    username: username.value,
    password: password.value,
    realName: realName.value,
    role: 'user',
    phone: phone.value,
    email: email.value
  })

  if (success) {
    uni.showToast({ title: '注册成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } else {
    uni.showToast({ title: '用户名已存在', icon: 'none' })
  }
}

function goToLogin() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 40rpx 30rpx;
  padding-bottom: 100rpx;
}

.register-card {
  width: 100%;
  background: $white;
  border-radius: $radius;
  box-shadow: $shadow;
  padding: 40rpx;
}

.register-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.register-title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 10rpx;
}

.register-sub {
  font-size: 26rpx;
  color: $text-light;
}

.login-link {
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
