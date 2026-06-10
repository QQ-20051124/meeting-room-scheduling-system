<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">意见反馈</text>
      <view class="header-placeholder"></view>
    </view>

    <view class="feedback-content">
      <!-- 反馈类型 -->
      <view class="feedback-section">
        <text class="section-label">反馈类型</text>
        <view class="type-grid">
          <view 
            v-for="type in feedbackTypes" 
            :key="type.value"
            :class="['type-item', { active: selectedType === type.value }]"
            @click="selectedType = type.value"
          >
            <text class="type-icon">{{ type.icon }}</text>
            <text class="type-label">{{ type.label }}</text>
          </view>
        </view>
      </view>

      <!-- 反馈内容 -->
      <view class="feedback-section">
        <text class="section-label">反馈内容</text>
        <textarea 
          class="feedback-textarea" 
          v-model="feedbackContent"
          placeholder="请详细描述您的问题或建议..."
          :maxlength="500"
        />
        <view class="char-count">
          <text>{{ feedbackContent.length }}/500</text>
        </view>
      </view>

      <!-- 联系方式 -->
      <view class="feedback-section">
        <text class="section-label">联系方式（选填）</text>
        <input 
          class="contact-input" 
          v-model="contactInfo"
          placeholder="您的邮箱或手机号，便于我们联系您"
        />
      </view>

      <!-- 提交按钮 -->
      <view 
        :class="['submit-btn', { disabled: !canSubmit }]" 
        @click="handleSubmit"
      >
        <text>提交反馈</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const feedbackTypes = [
  { value: 'bug', label: 'Bug反馈', icon: '🐛' },
  { value: 'feature', label: '功能建议', icon: '💡' },
  { value: 'ui', label: '界面优化', icon: '🎨' },
  { value: 'other', label: '其他', icon: '📝' }
]

const selectedType = ref('bug')
const feedbackContent = ref('')
const contactInfo = ref('')

const canSubmit = computed(() => {
  return feedbackContent.value.trim().length >= 10
})

function goBack() {
  uni.navigateBack()
}

function handleSubmit() {
  if (!canSubmit.value) {
    uni.showToast({ title: '请详细描述您的反馈', icon: 'none' })
    return
  }

  uni.showToast({ title: '反馈已提交', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.container {
  min-height: 100vh;
  background: $bg-color;
}

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

.feedback-content {
  padding: 32rpx;
}

.feedback-section {
  margin-bottom: 32rpx;
}

.section-label {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 16rpx;
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16rpx;
}

.type-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 16rpx;
  background: #ffffff;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.active {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
    
    .type-label {
      color: #3b82f6;
      font-weight: 600;
    }
  }
}

.type-icon {
  font-size: 48rpx;
  margin-bottom: 12rpx;
}

.type-label {
  font-size: 24rpx;
  color: $text-secondary;
}

.feedback-textarea {
  width: 100%;
  height: 300rpx;
  padding: 24rpx;
  background: #ffffff;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  font-size: 30rpx;
  box-sizing: border-box;
  
  &::placeholder {
    color: $text-light;
  }
}

.char-count {
  text-align: right;
  font-size: 24rpx;
  color: $text-light;
  margin-top: 8rpx;
}

.contact-input {
  width: 100%;
  height: 88rpx;
  padding: 0 24rpx;
  background: #ffffff;
  border: 2rpx solid $border-color;
  border-radius: 16rpx;
  font-size: 30rpx;
  box-sizing: border-box;
  
  &::placeholder {
    color: $text-light;
  }
}

.submit-btn {
  margin-top: 40rpx;
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
  
  &.disabled {
    background: #cbd5e1;
    cursor: not-allowed;
  }
}
</style>
