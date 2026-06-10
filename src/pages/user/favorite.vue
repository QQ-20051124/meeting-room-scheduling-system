<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-back" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="header-title">我的收藏</text>
      <view class="header-placeholder"></view>
    </view>

    <view class="favorite-content">
      <view v-if="favorites.length === 0" class="empty-state">
        <text class="empty-icon">❤️</text>
        <text class="empty-title">暂无收藏</text>
        <text class="empty-desc">收藏喜欢的会议室，方便快速预约</text>
        <view class="empty-action" @click="goToRoomList">
          <text>去看看</text>
        </view>
      </view>

      <view v-else class="favorite-list">
        <view 
          v-for="room in favorites" 
          :key="room.id" 
          class="favorite-card"
          @click="goToRoomDetail(room.id)"
        >
          <view class="card-header">
            <text class="room-code">{{ room.code }}</text>
            <view :class="['room-status', room.status]">
              <text>{{ room.status === 'available' ? '可用' : '占用' }}</text>
            </view>
          </view>
          <text class="room-name">{{ room.name }}</text>
          <view class="room-info">
            <view class="info-item">
              <text class="info-icon">📍</text>
              <text class="info-text">{{ room.location }}</text>
            </view>
            <view class="info-item">
              <text class="info-icon">👥</text>
              <text class="info-text">{{ room.capacity }}人</text>
            </view>
          </view>
          <view class="room-equipment">
            <text class="equipment-icon">📦</text>
            <text class="equipment-text">{{ room.equipment }}</text>
          </view>
          <view class="card-action">
            <view class="btn-primary" @click.stop="goToApply(room.id)">立即预约</view>
            <view class="btn-secondary" @click.stop="removeFavorite(room.id)">取消收藏</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useUserStore } from '@/stores/user'

const roomStore = useRoomStore()
const userStore = useUserStore()

const favorites = computed(() => {
  const favoriteIds = userStore.currentUser?.favoriteRooms || []
  return roomStore.rooms.filter(r => favoriteIds.includes(r.id))
})

function goBack() {
  uni.navigateBack()
}

function goToRoomList() {
  uni.switchTab({ url: '/pages/room/list' })
}

function goToRoomDetail(id: string) {
  uni.navigateTo({ url: `/pages/room/edit?id=${id}` })
}

function goToApply(roomId: string) {
  uni.navigateTo({ url: `/pages/reservation/apply?roomId=${roomId}` })
}

function removeFavorite(roomId: string) {
  userStore.removeFavoriteRoom(roomId)
  uni.showToast({ title: '已取消收藏', icon: 'success' })
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

.favorite-content {
  padding: 32rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 24rpx;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 12rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: $text-secondary;
  margin-bottom: 40rpx;
}

.empty-action {
  padding: 20rpx 48rpx;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 32rpx;
  color: #ffffff;
  font-size: 30rpx;
  font-weight: 500;
  cursor: pointer;
}

.favorite-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.favorite-card {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 28rpx;
  box-shadow: $shadow;
  cursor: pointer;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.room-code {
  font-size: 36rpx;
  font-weight: 700;
  color: #3b82f6;
}

.room-status {
  padding: 8rpx 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
  font-weight: 500;
  
  &.available {
    background: rgba(34, 197, 94, 0.1);
    color: #22c55e;
  }
  
  &.occupied {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
}

.room-name {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: $text-color;
  margin-bottom: 16rpx;
}

.room-info {
  display: flex;
  gap: 32rpx;
  margin-bottom: 16rpx;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.info-icon {
  font-size: 28rpx;
}

.info-text {
  font-size: 26rpx;
  color: $text-secondary;
}

.room-equipment {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 16rpx;
  background: #f8fafc;
  border-radius: 8rpx;
  margin-bottom: 20rpx;
}

.equipment-icon {
  font-size: 24rpx;
}

.equipment-text {
  font-size: 24rpx;
  color: $text-secondary;
}

.card-action {
  display: flex;
  gap: 20rpx;
}

.btn-primary {
  flex: 1;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 16rpx;
  color: #ffffff;
  font-size: 28rpx;
  font-weight: 500;
  cursor: pointer;
}

.btn-secondary {
  flex: 1;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 16rpx;
  color: $text-secondary;
  font-size: 28rpx;
  font-weight: 500;
  cursor: pointer;
}
</style>
