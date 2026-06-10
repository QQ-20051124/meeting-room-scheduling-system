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

      <view class="form-item">
        <text class="form-label">用户类型</text>
        <picker 
          class="form-select"
          :range="roleOptions" 
          range-key="label"
          @change="onRoleChange"
          :value="roleIndex"
        >
          <view class="picker-display">{{ roleOptions[roleIndex].label }}</view>
        </picker>
      </view>

      <view class="form-item" v-if="selectedRole !== 'admin'">
        <text class="form-label">院系/部门</text>
        <input 
          class="form-input" 
          v-model="department" 
          placeholder="请输入院系或部门"
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
const department = ref('')
const roleIndex = ref(0)
const selectedRole = ref<'student' | 'teacher' | 'organization'>('student')

const roleOptions = [
  { label: '👨‍🎓 学生', value: 'student' },
  { label: '👨‍ 教师', value: 'teacher' },
  { label: '🏢 组织/社团', value: 'organization' }
]

function onRoleChange(e: any) {
  roleIndex.value = e.detail.value
  selectedRole.value = roleOptions[roleIndex.value].value as 'student' | 'teacher' | 'organization'
}

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
    role: selectedRole.value,
    phone: phone.value,
    email: email.value,
    department: department.value
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
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  width: 100%;
  background: $white;
  border-radius: $radius-lg;
  box-shadow: $shadow-lg;
  padding: 50rpx 40rpx;
}

.register-header {
  text-align: center;
  margin-bottom: 50rpx;
}

.register-title {
  display: block;
  font-size: 44rpx;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16rpx;
}

.register-sub {
  font-size: 28rpx;
  color: $text-light;
}

.login-link {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  color: $text-secondary;
}

.link {
  color: $primary-color;
  font-weight: 600;
  margin-left: 10rpx;
}

.picker-display {
  padding: 20rpx 0;
  font-size: 28rpx;
  color: $text-color;
}
</style>
