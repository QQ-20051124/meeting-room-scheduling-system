<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">账号安全</text>
      <view class="header-placeholder"></view>
    </view>

    <view class="security-content">
      <!-- 安全状态 -->
      <view class="security-status">
        <view class="status-icon">🛡️</view>
        <view class="status-info">
          <text class="status-title">账号安全</text>
          <text class="status-desc">您的账号已开启多重保护</text>
        </view>
        <view class="status-score">
          <text class="score-value">80</text>
          <text class="score-label">安全分</text>
        </view>
      </view>

      <!-- 安全设置列表 -->
      <view class="security-list">
        <view class="security-item" @click="goToChangePassword">
          <view class="item-icon">🔑</view>
          <view class="item-info">
            <text class="item-title">修改密码</text>
            <text class="item-desc">建议定期更换密码</text>
          </view>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="security-item" @click="goToBindPhone">
          <view class="item-icon">📱</view>
          <view class="item-info">
            <text class="item-title">绑定手机</text>
            <text class="item-desc">{{ currentUser?.phone || '未绑定' }}</text>
          </view>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="security-item" @click="goToBindEmail">
          <view class="item-icon">📧</view>
          <view class="item-info">
            <text class="item-title">绑定邮箱</text>
            <text class="item-desc">{{ currentUser?.email || '未绑定' }}</text>
          </view>
          <text class="item-arrow">›</text>
        </view>
        
        <view class="security-item" @click="goToSession">
          <view class="item-icon">📱</view>
          <view class="item-info">
            <text class="item-title">登录设备</text>
            <text class="item-desc">查看当前登录设备</text>
          </view>
          <text class="item-arrow">›</text>
        </view>
      </view>

      <!-- 登录记录 -->
      <view class="section-card">
        <view class="section-header">
          <text class="section-title">最近登录</text>
        </view>
        <view class="login-record">
          <view class="record-item">
            <view class="record-icon">🖥️</view>
            <view class="record-info">
              <text class="record-title">当前设备</text>
              <text class="record-desc">Windows 浏览器 | 刚刚</text>
            </view>
          </view>
          <view class="record-item">
            <view class="record-icon">📱</view>
            <view class="record-info">
              <text class="record-title">移动端</text>
              <text class="record-desc">微信小程序 | 2024-01-15</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)

function goBack() {
  uni.navigateBack()
}

function goToChangePassword() {
  uni.navigateTo({ url: '/pages/user/change-password' })
}

function goToBindPhone() {
  uni.showToast({ title: '手机绑定功能开发中', icon: 'none' })
}

function goToBindEmail() {
  uni.showToast({ title: '邮箱绑定功能开发中', icon: 'none' })
}

function goToSession() {
  uni.showToast({ title: '登录设备管理功能开发中', icon: 'none' })
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

.security-content {
  padding: 32rpx;
}

.security-status {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 32rpx;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
  border-radius: 20rpx;
  margin-bottom: 32rpx;
}

.status-icon {
  font-size: 64rpx;
}

.status-info {
  flex: 1;
}

.status-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 8rpx;
}

.status-desc {
  font-size: 26rpx;
  color: $text-secondary;
}

.status-score {
  text-align: center;
  padding: 16rpx 24rpx;
  background: rgba(34, 197, 94, 0.15);
  border-radius: 16rpx;
}

.score-value {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: #22c55e;
}

.score-label {
  font-size: 22rpx;
  color: #22c55e;
}

.security-list {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 16rpx;
  margin-bottom: 32rpx;
  box-shadow: $shadow;
}

.security-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 28rpx 24rpx;
  border-bottom: 2rpx solid $border-color;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: rgba(0, 0, 0, 0.02);
  }
}

.item-icon {
  font-size: 40rpx;
}

.item-info {
  flex: 1;
}

.item-title {
  display: block;
  font-size: 30rpx;
  font-weight: 500;
  color: $text-color;
  margin-bottom: 6rpx;
}

.item-desc {
  font-size: 24rpx;
  color: $text-secondary;
}

.item-arrow {
  font-size: 36rpx;
  color: $text-light;
}

.section-card {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: $shadow;
}

.section-header {
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $text-color;
}

.login-record {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 20rpx;
  background: #f8fafc;
  border-radius: 12rpx;
}

.record-icon {
  font-size: 36rpx;
}

.record-info {
  flex: 1;
}

.record-title {
  display: block;
  font-size: 28rpx;
  font-weight: 500;
  color: $text-color;
  margin-bottom: 4rpx;
}

.record-desc {
  font-size: 24rpx;
  color: $text-secondary;
}
</style>
