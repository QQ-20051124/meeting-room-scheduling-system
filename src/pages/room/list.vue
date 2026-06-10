<template>
  <view class="container">
    <!-- 搜索区域 -->
    <view class="search-section">
      <view class="search-box">
        <text class="search-icon">◉</text>
        <input 
          class="search-input" 
          v-model="searchKeyword" 
          placeholder="搜索会议室名称或编号"
        />
        <view v-if="searchKeyword" class="clear-btn" @click="searchKeyword = ''">✕</view>
      </view>
    </view>

    <!-- 添加按钮 -->
    <view v-if="isAdmin" class="add-section">
      <view class="add-card" @click="goToAddRoom">
        <view class="add-icon-wrap">
          <text class="add-icon">+</text>
        </view>
        <text class="add-text">添加会议室</text>
      </view>
    </view>

    <!-- 会议室列表 -->
    <view class="room-grid">
      <view
        v-for="room in filteredRooms"
        :key="room.id"
        class="room-card"
        @click="goToRoomDetail(room.id)"
      >
        <!-- 卡片顶部状态 -->
        <view class="card-header">
          <view class="room-code">{{ room.code }}</view>
          <view :class="['status-badge', getRoomDisplayStatus(room)]">
            {{ getStatusText(getRoomDisplayStatus(room)) }}
          </view>
        </view>
        
        <!-- 会议室名称 -->
        <text class="room-name">{{ room.name }}</text>
        
        <!-- 会议室信息 -->
        <view class="room-meta">
          <view class="meta-item">
            <text class="meta-icon">●</text>
            <text class="meta-text">{{ room.location }}</text>
          </view>
          <view class="meta-item">
            <text class="meta-icon">○</text>
            <text class="meta-text">{{ room.capacity }}人</text>
          </view>
        </view>
        
        <!-- 设备标签 -->
        <view class="equipment-tags">
          <view v-for="(eq, index) in room.equipment.split('、').slice(0, 3)" :key="index" class="equipment-tag">
            {{ eq }}
          </view>
        </view>
        
        <!-- 预约按钮 -->
        <view v-if="isLoggedIn && room.status === 'available'" class="card-action">
          <view class="btn-primary" @click.stop="goToApply(room.id)">立即预约</view>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-if="filteredRooms.length === 0" class="empty-state">
      <view class="empty-icon">◯</view>
      <text class="empty-title">暂无会议室</text>
      <text class="empty-desc">{{ searchKeyword ? '未找到匹配的会议室' : '管理员还未添加会议室' }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useUserStore } from '@/stores/user'
import { useReservationStore } from '@/stores/reservation'
import { getToday } from '@/utils/date'

const roomStore = useRoomStore()
const userStore = useUserStore()
const reservationStore = useReservationStore()
const searchKeyword = ref('')
const today = getToday()

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
    available: '空闲',
    booked: '已预约',
    unavailable: '不可用',
    maintenance: '维护中'
  }
  return map[status] || status
}

function isRoomBookedToday(roomId: string): boolean {
  return reservationStore.reservations.some(r =>
    r.roomId === roomId &&
    r.date === today &&
    ['pending', 'approved'].includes(r.status)
  )
}

function getRoomDisplayStatus(room: any): string {
  if (room.status !== 'available') return room.status
  return isRoomBookedToday(room.id) ? 'booked' : 'available'
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
  background: $bg-page;
  padding: $spacing-lg;
  padding-bottom: 180rpx;
}

/* ===== 搜索区域 ===== */
.search-section {
  margin-bottom: $spacing-md;
}

.search-box {
  display: flex;
  align-items: center;
  background: $bg-card;
  border-radius: $radius-xl;
  padding: 0 $spacing-md;
  box-shadow: $shadow-sm;
  border: 1rpx solid $border-color;
}

.search-icon {
  font-size: $font-md;
  color: $text-light;
  margin-right: $spacing-sm;
}

.search-input {
  flex: 1;
  height: 88rpx;
  font-size: $font-base;
  color: $text-primary;
}

.clear-btn {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: $bg-hover;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $font-sm;
  color: $text-muted;
}

/* ===== 添加按钮 ===== */
.add-section {
  margin-bottom: $spacing-md;
}

.add-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  background: linear-gradient(135deg, $primary-color, $primary-dark);
  border-radius: $radius-xl;
  padding: $spacing-lg;
  box-shadow: $shadow-sm;
  transition: all 0.2s ease;
  
  &:active {
    transform: scale(0.98);
    box-shadow: $shadow;
  }
}

.add-icon-wrap {
  width: 56rpx;
  height: 56rpx;
  border-radius: $radius-lg;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-icon {
  font-size: $font-xl;
  color: $white;
}

.add-text {
  font-size: $font-base;
  font-weight: 600;
  color: $white;
}

/* ===== 会议室网格 ===== */
.room-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-md;
}

/* ===== 会议室卡片 ===== */
.room-card {
  background: $bg-card;
  border-radius: $radius-xl;
  padding: $spacing-md;
  box-shadow: $shadow-sm;
  transition: all 0.2s ease;
  
  &:active {
    transform: translateY(-4rpx);
    box-shadow: $shadow;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}

.room-code {
  font-size: $font-xs;
  font-weight: 700;
  color: $primary-color;
}

.status-badge {
  font-size: $font-xs;
  padding: 6rpx 16rpx;
  border-radius: $radius-full;
  font-weight: 500;
  
  &.available {
    background: rgba($success-color, 0.1);
    color: $success-color;
  }
  &.booked {
    background: rgba($error-color, 0.1);
    color: $error-color;
  }
  &.unavailable {
    background: $bg-hover;
    color: $text-muted;
  }
  &.maintenance {
    background: rgba($warning-color, 0.1);
    color: $warning-color;
  }
}

.room-name {
  font-size: $font-md;
  font-weight: 600;
  color: $text-title;
  margin-bottom: $spacing-sm;
  display: block;
}

.room-meta {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  margin-bottom: $spacing-sm;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-icon {
  font-size: $font-sm;
  color: $text-light;
  margin-right: 8rpx;
}

.meta-text {
  font-size: $font-xs;
  color: $text-secondary;
}

.equipment-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-bottom: $spacing-sm;
}

.equipment-tag {
  font-size: $font-xs;
  padding: 6rpx 12rpx;
  background: rgba($primary-color, 0.08);
  color: $primary-color;
  border-radius: $radius-sm;
}

.card-action {
  margin-top: $spacing-xs;
}

.btn-primary {
  width: 100%;
  text-align: center;
  padding: $spacing-sm;
  background: linear-gradient(135deg, $primary-color, $primary-dark);
  color: $white;
  border-radius: $radius-lg;
  font-size: $font-sm;
  font-weight: 500;
  
  &:active {
    opacity: 0.9;
  }
}

/* ===== 空状态 ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-3xl 0;
}

.empty-icon {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: $bg-hover;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
  color: $text-light;
  margin-bottom: $spacing-lg;
}

.empty-title {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.empty-desc {
  font-size: $font-sm;
  color: $text-muted;
}
</style>