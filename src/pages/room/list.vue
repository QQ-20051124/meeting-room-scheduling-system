<template>
  <view class="container">
    <view class="search-bar">
      <input 
        class="search-input" 
        v-model="searchKeyword" 
        placeholder="搜索会议室名称或编号"
      />
      <text class="search-icon">🔍</text>
    </view>

    <view v-if="isAdmin" class="add-btn" @click="goToAddRoom">
      <text class="add-icon">+</text>
      <text class="add-text">添加会议室</text>
    </view>

    <view class="room-list">
      <view 
        v-for="room in filteredRooms" 
        :key="room.id" 
        class="room-card"
        @click="goToRoomDetail(room.id)"
      >
        <view class="room-header">
          <view class="room-code">{{ room.code }}</view>
          <view :class="['room-status', room.status]">{{ getStatusText(room.status) }}</view>
        </view>
        <text class="room-name">{{ room.name }}</text>
        <view class="room-info">
          <view class="info-item">
            <text class="info-icon">👥</text>
            <text class="info-text">{{ room.capacity }}人</text>
          </view>
          <view class="info-item">
            <text class="info-icon">📍</text>
            <text class="info-text">{{ room.location }}</text>
          </view>
        </view>
        <view class="room-equipment">
          <text class="equipment-icon">📦</text>
          <text class="equipment-text">{{ room.equipment }}</text>
        </view>
        <view v-if="isLoggedIn && room.status === 'available'" class="room-action">
          <view class="btn-primary" @click.stop="goToApply(room.id)">立即预约</view>
        </view>
      </view>
    </view>

    <view v-if="filteredRooms.length === 0" class="empty-state">
      <text class="empty-icon">🏢</text>
      <text class="empty-text">暂无会议室</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useUserStore } from '@/stores/user'

const roomStore = useRoomStore()
const userStore = useUserStore()
const searchKeyword = ref('')

const isLoggedIn = computed(() => userStore.isLoggedIn())
const isAdmin = computed(() => userStore.isAdmin())

const filteredRooms = computed(() => {
  if (!searchKeyword.value.trim()) {
    return roomStore.rooms
  }
  const keyword = searchKeyword.value.toLowerCase()
  return roomStore.rooms.filter(room => 
    room.name.toLowerCase().includes(keyword) || 
    room.code.toLowerCase().includes(keyword)
  )
})

function getStatusText(status: string): string {
  const map: Record<string, string> = {
    available: '可预约',
    unavailable: '不可用',
    maintenance: '维护中'
  }
  return map[status] || status
}

function goToAddRoom() {
  uni.navigateTo({ url: '/pages/room/add' })
}

function goToRoomDetail(id: string) {
  uni.navigateTo({ url: `/pages/room/edit?id=${id}` })
}

function goToApply(roomId: string) {
  uni.navigateTo({ url: `/pages/reservation/apply?roomId=${roomId}` })
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
  padding-bottom: 180rpx;
}

.search-bar {
  position: relative;
  margin-bottom: 20rpx;
}

.search-input {
  width: 100%;
  height: 80rpx;
  background: $white;
  border-radius: $radius;
  padding: 0 80rpx 0 30rpx;
  font-size: 28rpx;
  box-sizing: border-box;
  box-shadow: $shadow;
}

.search-icon {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 32rpx;
}

.add-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: $primary-color;
  color: $white;
  padding: 24rpx;
  border-radius: $radius;
  margin-bottom: 20rpx;
  
  &:active {
    background: $primary-dark;
  }
}

.add-icon {
  font-size: 36rpx;
  margin-right: 10rpx;
}

.add-text {
  font-size: 28rpx;
}

.room-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.room-card {
  background: $white;
  border-radius: $radius;
  padding: 30rpx;
  box-shadow: $shadow;
  
  &:active {
    opacity: 0.8;
  }
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.room-code {
  font-size: 24rpx;
  color: $primary-color;
  font-weight: bold;
}

.room-status {
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  
  &.available {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  &.unavailable {
    background: rgba($error-color, 0.1);
    color: $error-color;
  }
  &.maintenance {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
}

.room-name {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-color;
  margin-bottom: 16rpx;
}

.room-info {
  display: flex;
  gap: 30rpx;
  margin-bottom: 16rpx;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-icon {
  font-size: 28rpx;
  margin-right: 8rpx;
}

.info-text {
  font-size: 24rpx;
  color: $text-secondary;
}

.room-equipment {
  display: flex;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1rpx solid $border-color;
}

.equipment-icon {
  font-size: 24rpx;
  margin-right: 8rpx;
}

.equipment-text {
  font-size: 24rpx;
  color: $text-light;
}

.room-action {
  margin-top: 20rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: $text-light;
}
</style>
