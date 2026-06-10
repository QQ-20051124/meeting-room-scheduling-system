<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">身份认证</text>
      <view class="header-placeholder"></view>
    </view>

    <view class="certify-content">
      <!-- 认证说明 -->
      <view class="certify-intro">
        <view class="intro-icon">📝</view>
        <text class="intro-title">完成身份认证</text>
        <text class="intro-desc">请输入您的学号或教工号进行身份认证，认证后可享受完整的预约功能</text>
      </view>

      <!-- 认证表单 -->
      <view class="certify-form">
        <view class="form-section">
          <view class="section-title">认证信息</view>
          
          <view class="form-item">
            <text class="form-label">认证类型</text>
            <view class="type-selector">
              <view 
                v-for="type in certTypes" 
                :key="type.key"
                :class="['type-item', { active: certType === type.key }]"
                @click="certType = type.key"
              >
                <text>{{ type.label }}</text>
              </view>
            </view>
          </view>

          <view class="form-item">
            <text class="form-label">{{ certType === 'student' ? '学号' : certType === 'teacher' ? '教工号' : '组织编号' }}</text>
            <input 
              class="form-input" 
              v-model="schoolId" 
              placeholder="请输入学号/教工号/组织编号"
              type="text"
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
            <text class="form-label">联系电话</text>
            <input 
              class="form-input" 
              v-model="phone" 
              placeholder="请输入联系电话"
              type="number"
            />
          </view>

          <view class="form-item">
            <text class="form-label">邮箱地址</text>
            <input 
              class="form-input" 
              v-model="email" 
              placeholder="请输入邮箱地址"
              type="text"
            />
          </view>
        </view>

        <!-- 认证协议 -->
        <view class="agreement-section">
          <view class="checkbox" :class="{ checked: agreed }" @click="agreed = !agreed">
            <text v-if="agreed">✓</text>
          </view>
          <text class="agreement-text">我已阅读并同意</text>
          <text class="agreement-link">《用户服务协议》</text>
          <text class="agreement-text">和</text>
          <text class="agreement-link">《隐私政策》</text>
        </view>
      </view>

      <!-- 提交按钮 -->
      <view 
        :class="['submit-btn', { disabled: !canSubmit }]" 
        @click="handleSubmit"
      >
        <text>{{ isCertified ? '重新认证' : '提交认证' }}</text>
      </view>

      <!-- 认证提示 -->
      <view class="tip-section">
        <text class="tip-icon">💡</text>
        <text class="tip-text">认证信息将严格保密，仅用于身份验证</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const certType = ref('student')
const schoolId = ref('')
const realName = ref('')
const phone = ref('')
const email = ref('')
const agreed = ref(false)

const certTypes = [
  { key: 'student', label: '学生' },
  { key: 'teacher', label: '教师' },
  { key: 'organization', label: '组织' }
]

const isCertified = computed(() => userStore.isCertified())

const canSubmit = computed(() => {
  return schoolId.value.trim() && 
         realName.value.trim() && 
         phone.value.trim() && 
         agreed.value
})

function goBack() {
  uni.navigateBack()
}

function handleSubmit() {
  if (!canSubmit.value) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' })
    return
  }

  const success = userStore.certify({
    schoolId: schoolId.value,
    realName: realName.value,
    phone: phone.value,
    email: email.value,
    role: certType.value
  })

  if (success) {
    uni.showToast({ title: '认证成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } else {
    uni.showToast({ title: '认证失败，请重试', icon: 'none' })
  }
}

onMounted(() => {
  userStore.loadUser()
  if (userStore.currentUser) {
    realName.value = userStore.currentUser.realName || ''
    phone.value = userStore.currentUser.phone || ''
    email.value = userStore.currentUser.email || ''
    if (userStore.currentUser.schoolId) {
      schoolId.value = userStore.currentUser.schoolId
    }
    if (userStore.currentUser.role) {
      certType.value = userStore.currentUser.role
    }
  }
})
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

/* ===== 认证内容 ===== */
.certify-content {
  padding: 32rpx;
}

/* ===== 认证说明 ===== */
.certify-intro {
  text-align: center;
  margin-bottom: 40rpx;
}

.intro-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.intro-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $text-color;
  margin-bottom: 16rpx;
}

.intro-desc {
  font-size: 28rpx;
  color: $text-secondary;
  line-height: 1.6;
}

/* ===== 认证表单 ===== */
.certify-form {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: $shadow;
}

.form-section {
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 24rpx;
}

.form-item {
  margin-bottom: 28rpx;
  
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

.form-input {
  width: 100%;
  height: 88rpx;
  padding: 0 28rpx;
  background: #f8fafc;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  font-size: 30rpx;
  box-sizing: border-box;
  
  &::placeholder {
    color: $text-light;
  }
}

/* ===== 类型选择器 ===== */
.type-selector {
  display: flex;
  gap: 20rpx;
}

.type-item {
  flex: 1;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  font-size: 28rpx;
  color: $text-secondary;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.active {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    border-color: #3b82f6;
    color: #ffffff;
  }
}

/* ===== 协议部分 ===== */
.agreement-section {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding-top: 16rpx;
}

.checkbox {
  width: 40rpx;
  height: 40rpx;
  border: 2rpx solid #cbd5e1;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  color: #ffffff;
  cursor: pointer;
  
  &.checked {
    background: #3b82f6;
    border-color: #3b82f6;
  }
}

.agreement-text {
  font-size: 24rpx;
  color: $text-secondary;
}

.agreement-link {
  font-size: 24rpx;
  color: #3b82f6;
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

/* ===== 提示信息 ===== */
.tip-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  margin-top: 32rpx;
}

.tip-icon {
  font-size: 28rpx;
}

.tip-text {
  font-size: 24rpx;
  color: $text-light;
}
</style>