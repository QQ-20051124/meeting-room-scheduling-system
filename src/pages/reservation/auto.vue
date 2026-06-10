<template>
  <view class="container">
    <view v-if="!isLoggedIn" class="not-login">
      <text class="not-login-text">请先登录</text>
      <view class="btn-primary mt-30" @click="goToLogin">立即登录</view>
    </view>

    <view v-else class="form-card">
      <view class="auto-title">
        <text class="title-icon">🤖</text>
        <text class="title-text">会议室自动分配</text>
      </view>

      <view class="form-item">
        <text class="form-label">预约日期 *</text>
        <picker mode="date" :value="form.date" @change="onDateChange">
          <view class="form-select">
            {{ form.date || '请选择日期' }}
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="form-label">开始时间 *</text>
        <picker mode="time" :value="form.startTime" @change="onStartTimeChange">
          <view class="form-select">
            {{ form.startTime || '请选择开始时间' }}
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="form-label">结束时间 *</text>
        <picker mode="time" :value="form.endTime" @change="onEndTimeChange">
          <view class="form-select">
            {{ form.endTime || '请选择结束时间' }}
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="form-label">参会人数 *</text>
        <input 
          class="form-input" 
          v-model="form.participantCount" 
          placeholder="请输入参会人数"
          type="number"
        />
      </view>

      <view class="btn-primary" @click="handleAutoAssign">自动匹配会议室</view>

      <view v-if="matchedRooms.length > 0" class="matched-section">
        <text class="matched-title">匹配结果</text>
        <view class="matched-list">
          <view 
            v-for="room in matchedRooms" 
            :key="room.id" 
            class="matched-item"
            @click="selectRoom(room)"
          >
            <view class="matched-header">
              <text class="matched-code">{{ room.code }}</text>
              <text class="matched-name">{{ room.name }}</text>
            </view>
            <view class="matched-info">
              <text>👥 {{ room.capacity }}人</text>
              <text>📍 {{ room.location }}</text>
            </view>
            <view class="matched-equipment">{{ room.equipment }}</view>
            <view class="matched-btn">选择此会议室</view>
          </view>
        </view>
      </view>

      <view v-if="noRoomsFound" class="no-rooms">
        <text class="no-rooms-icon">😔</text>
        <text class="no-rooms-text">暂无合适的会议室</text>
        <view class="btn-secondary mt-20" @click="addToQueue">加入等待队列</view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'
import { getToday, isValidTimeRange } from '@/utils/date'

const roomStore = useRoomStore()
const reservationStore = useReservationStore()
const userStore = useUserStore()

const form = reactive({
  date: getToday(),
  startTime: '',
  endTime: '',
  participantCount: 0
})

const isLoggedIn = ref(false)
const matchedRooms = ref<any[]>([])
const noRoomsFound = ref(false)

function onDateChange(e: any) {
  form.date = e.detail.value
}

function onStartTimeChange(e: any) {
  form.startTime = e.detail.value
}

function onEndTimeChange(e: any) {
  form.endTime = e.detail.value
}

function handleAutoAssign() {
  if (!form.date) {
    uni.showToast({ title: '请选择预约日期', icon: 'none' })
    return
  }
  if (!form.startTime) {
    uni.showToast({ title: '请选择开始时间', icon: 'none' })
    return
  }
  if (!form.endTime) {
    uni.showToast({ title: '请选择结束时间', icon: 'none' })
    return
  }
  if (!isValidTimeRange(form.startTime, form.endTime)) {
    uni.showToast({ title: '结束时间必须晚于开始时间', icon: 'none' })
    return
  }
  if (!form.participantCount || form.participantCount <= 0) {
    uni.showToast({ title: '请输入有效的参会人数', icon: 'none' })
    return
  }

  matchedRooms.value = []
  noRoomsFound.value = false

  const availableRooms = roomStore.getAvailableRooms(form.date, form.startTime, form.endTime, form.participantCount)
  
  const filteredRooms = availableRooms.filter(room => {
    return reservationStore.isRoomAvailable(room.id, form.date, form.startTime, form.endTime)
  })

  if (filteredRooms.length > 0) {
    matchedRooms.value = filteredRooms
  } else {
    noRoomsFound.value = true
  }
}

function selectRoom(room: any) {
  reservationStore.addReservation({
    userId: userStore.currentUser!.id,
    roomId: room.id,
    roomCode: room.code,
    roomName: room.name,
    date: form.date,
    startTime: form.startTime,
    endTime: form.endTime,
    meetingTopic: '自动分配会议',
    participantCount: form.participantCount,
    applicant: userStore.currentUser!.realName,
    status: 'pending'
  })

  uni.showToast({ title: '预约申请已提交', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}

function addToQueue() {
  reservationStore.addToQueue({
    userId: userStore.currentUser!.id,
    date: form.date,
    startTime: form.startTime,
    endTime: form.endTime,
    meetingTopic: '自动分配会议',
    participantCount: form.participantCount,
    applicant: userStore.currentUser!.realName
  })

  uni.showToast({ title: '已加入等待队列', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}

function goToLogin() {
  uni.navigateTo({ url: '/pages/user/login' })
}

userStore.loadUser()
isLoggedIn.value = userStore.isLoggedIn()
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
}

.form-card {
  background: $white;
  border-radius: $radius;
  padding: 30rpx;
  box-shadow: $shadow;
}

.not-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.not-login-text {
  font-size: 32rpx;
  color: $text-secondary;
}

.auto-title {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40rpx;
}

.title-icon {
  font-size: 48rpx;
  margin-right: 16rpx;
}

.title-text {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
}

.matched-section {
  margin-top: $spacing-xl;
  padding-top: $spacing-md;
  border-top: 2rpx solid $border-color;
}

.matched-title {
  font-size: $font-md;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.matched-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.matched-item {
  background: $bg-card;
  border-radius: $radius;
  padding: 24rpx;
}

.matched-header {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}

.matched-code {
  font-size: 24rpx;
  color: $primary-color;
  font-weight: bold;
  margin-right: 10rpx;
}

.matched-name {
  font-size: $font-base;
  font-weight: 600;
  color: $text-primary;
}

.matched-info {
  display: flex;
  gap: 30rpx;
  margin-bottom: 12rpx;
  font-size: 24rpx;
  color: $text-secondary;
}

.matched-equipment {
  font-size: 24rpx;
  color: $text-light;
  margin-bottom: 16rpx;
}

.matched-btn {
  background: $primary-color;
  color: $white;
  text-align: center;
  padding: 16rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  
  &:active {
    background: $primary-dark;
  }
}

.no-rooms {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
  margin-top: 40rpx;
  background: $bg-card;
  border-radius: $radius;
}

.no-rooms-icon {
  font-size: 60rpx;
  margin-bottom: 16rpx;
}

.no-rooms-text {
  font-size: 28rpx;
  color: $text-secondary;
}
</style>
