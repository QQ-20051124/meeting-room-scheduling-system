<template>
  <view class="container">
    <!-- 顶部标题栏 -->
    <view class="page-header">
      <view class="header-content">
        <text class="page-title">🏢 会议室列表</text>
        <text class="page-subtitle">共 {{ roomStore.rooms.length }} 间会议室可供选择</text>
      </view>
      <view v-if="isAdmin" class="header-action" @click="goToAddRoom">
        <text class="action-icon">➕</text>
        <text class="action-text">添加会议室</text>
      </view>
    </view>

    <!-- 搜索栏 -->
    <view class="search-bar">
      <input 
        class="search-input" 
        v-model="searchKeyword" 
        placeholder="搜索会议室名称或编号"
      />
      <text class="search-icon">🔍</text>
    </view>

    <!-- 筛选标签 - 横向排列 -->
    <view class="filter-tabs">
      <view 
        v-for="tab in filterTabs" 
        :key="tab.key"
        :class="['filter-tab', { active: activeFilter === tab.key }]"
        @click="activeFilter = tab.key"
      >
        <text>{{ tab.label }}{{ tab.count }}</text>
      </view>
    </view>

    <!-- 4列网格布局 -->
    <view class="room-grid">
      <view 
        v-for="room in filteredRooms" 
        :key="room.id" 
        class="room-card"
        @click="goToRoomDetail(room.id)"
      >
        <view class="card-header">
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
      <text class="empty-hint">请联系管理员添加会议室</text>
    </view>
    
    <!-- 自定义底部导航 -->
    <CustomTabbar current="room" />
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useUserStore } from '@/stores/user'
import CustomTabbar from '@/components/custom-tabbar/CustomTabbar.vue'

const roomStore = useRoomStore()
const userStore = useUserStore()
const searchKeyword = ref('')
const activeFilter = ref('all')

const isLoggedIn = computed(() => userStore.isLoggedIn())
const isAdmin = computed(() => userStore.isAdmin())

const filterTabs = computed(() => [
  { key: 'all', label: '全部', count: roomStore.rooms.length },
  { key: 'available', label: '可用', count: roomStore.rooms.filter(r => r.status === 'available').length },
  { key: 'occupied', label: '占用', count: roomStore.rooms.filter(r => r.status !== 'available').length }
])

const filteredRooms = computed(() => {
  let rooms = roomStore.rooms
  
  // 状态筛选
  if (activeFilter.value === 'available') {
    rooms = rooms.filter(r => r.status === 'available')
  } else if (activeFilter.value === 'occupied') {
    rooms = rooms.filter(r => r.status !== 'available')
  }
  
  // 关键词搜索
  if (!searchKeyword.value.trim()) {
    return rooms
  }
  const keyword = searchKeyword.value.toLowerCase()
  return rooms.filter(room => 
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
  roomStore.loadRooms()
})
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.container {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 280rpx;
}

/* ===== 顶部标题栏 ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 40rpx;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.15);
}

.header-content {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 44rpx;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8rpx;
}

.page-subtitle {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.7);
}

.header-action {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx 28rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 32rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
}

.action-icon {
  font-size: 32rpx;
  color: #ffffff;
}

.action-text {
  font-size: 28rpx;
  color: #ffffff;
  font-weight: 500;
}

/* ===== 搜索栏 ===== */
.search-bar {
  position: relative;
  margin: 24rpx;
}

.search-input {
  width: 100%;
  height: 88rpx;
  background: #ffffff;
  border-radius: 16rpx;
  padding: 0 80rpx 0 32rpx;
  font-size: 30rpx;
  box-sizing: border-box;
  box-shadow: $shadow;
}

.search-icon {
  position: absolute;
  right: 32rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 36rpx;
}

/* ===== 筛选标签 ===== */
.filter-tabs {
  display: flex;
  padding: 0 24rpx;
  gap: 20rpx;
  margin-bottom: 24rpx;
}

.filter-tab {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 16rpx 60rpx;
  border-radius: 32rpx;
  font-size: 26rpx;
  color: #64748b;
  cursor: pointer;
  background: #ffffff;
  border: 2rpx solid #e2e8f0;
  transition: all 0.2s ease;
  font-weight: 600;
  white-space: nowrap;
  min-width: 220rpx;
  max-width: 220rpx;
  height: 80rpx;
  overflow: hidden;
  text-align: center;
  
  &:hover {
    border-color: #cbd5e0;
  }
  
  &.active {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: #ffffff;
    border-color: transparent;
    box-shadow: 0 4rpx 12rpx rgba(59, 130, 246, 0.3);
  }
}

.tab-count {
  font-size: 26rpx;
  opacity: 0.8;
}

/* ===== 4列网格布局 ===== */
.room-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24rpx;
  padding: 0 24rpx;
}

.room-card {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 28rpx;
  box-shadow: $shadow;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-4rpx);
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);
  }
  
  &:active {
    opacity: 0.8;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.room-code {
  font-size: 26rpx;
  color: #3b82f6;
  font-weight: 600;
}

.room-status {
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: 12rpx;
  font-weight: 500;
  
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
  font-weight: 600;
  color: $text-color;
  margin-bottom: 16rpx;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room-info {
  display: flex;
  gap: 20rpx;
  margin-bottom: 16rpx;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-icon {
  font-size: 24rpx;
  margin-right: 6rpx;
}

.info-text {
  font-size: 24rpx;
  color: $text-secondary;
}

.room-equipment {
  display: flex;
  align-items: center;
  padding-top: 16rpx;
  border-top: 2rpx solid $border-color;
  margin-bottom: 16rpx;
}

.equipment-icon {
  font-size: 22rpx;
  margin-right: 6rpx;
}

.equipment-text {
  font-size: 22rpx;
  color: $text-light;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room-action {
  .btn-primary {
    width: 100%;
    height: 72rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: #ffffff;
    border-radius: 12rpx;
    font-size: 28rpx;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      opacity: 0.9;
    }
  }
}

/* ===== 空状态 ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 0;
}

.empty-icon {
  font-size: 100rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 36rpx;
  color: $text-color;
  margin-bottom: 12rpx;
  font-weight: 500;
}

.empty-hint {
  font-size: 28rpx;
  color: $text-light;
}
</style>