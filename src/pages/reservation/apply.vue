<template>
  <view class="container">
    <!-- 返回按钮 -->
    <view class="back-header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
        <text class="back-text">返回</text>
      </view>
    </view>
    
    <view v-if="!isLoggedIn" class="not-login">
      <text class="not-login-text">请先登录</text>
      <view class="btn-primary mt-30" @click="goToLogin">立即登录</view>
    </view>

    <view v-else class="form-card">
      <view class="form-item">
        <text class="form-label">选择会议室 *</text>
        <picker mode="selector" :range="roomOptions" @change="onRoomChange">
          <view class="form-select">
            {{ selectedRoom?.name || '请选择会议室' }}
          </view>
        </picker>
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
        <text class="form-label">会议主题 *</text>
        <input 
          class="form-input" 
          v-model="form.meetingTopic" 
          placeholder="请输入会议主题"
          type="text"
        />
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

      <view class="btn-primary" @click="handleSubmit">提交预约申请</view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useReservationStore } from '@/stores/reservation'
import { useUserStore } from '@/stores/user'
import { getToday, isValidTimeRange } from '@/utils/date'

const roomStore = useRoomStore()
const reservationStore = useReservationStore()
const userStore = useUserStore()

const form = reactive({
  roomId: '',
  date: getToday(),
  startTime: '',
  endTime: '',
  meetingTopic: '',
  participantCount: 0
})

const isLoggedIn = ref(false)

const availableRooms = computed(() => {
  return roomStore.rooms.filter(r => r.status === 'available')
})

const roomOptions = computed(() => {
  return availableRooms.value.map(r => `${r.code} - ${r.name}`)
})

const selectedRoom = computed(() => {
  if (!form.roomId) return null
  return roomStore.getRoomById(form.roomId)
})

function goBack() {
  uni.navigateBack()
}

function onRoomChange(e: any) {
  const index = e.detail.value
  form.roomId = availableRooms.value[index]?.id || ''
}

function onDateChange(e: any) {
  form.date = e.detail.value
}

function onStartTimeChange(e: any) {
  form.startTime = e.detail.value
}

function onEndTimeChange(e: any) {
  form.endTime = e.detail.value
}

function handleSubmit() {
  if (!form.roomId) {
    uni.showToast({ title: '请选择会议室', icon: 'none' })
    return
  }
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
  if (!form.meetingTopic.trim()) {
    uni.showToast({ title: '请输入会议主题', icon: 'none' })
    return
  }
  if (!form.participantCount || form.participantCount <= 0) {
    uni.showToast({ title: '请输入有效的参会人数', icon: 'none' })
    return
  }

  const room = selectedRoom.value
  if (room && form.participantCount > room.capacity) {
    uni.showToast({ title: '参会人数超过会议室容量', icon: 'none' })
    return
  }

  if (!reservationStore.isRoomAvailable(form.roomId, form.date, form.startTime, form.endTime)) {
    uni.showModal({
      title: '时段冲突',
      content: '该会议室在所选时段已被预约，是否加入等待队列？',
      success: (res) => {
        if (res.confirm) {
          addToQueue()
        }
      }
    })
    return
  }

  reservationStore.addReservation({
    userId: userStore.currentUser!.id,
    roomId: form.roomId,
    roomCode: room?.code || '',
    roomName: room?.name || '',
    date: form.date,
    startTime: form.startTime,
    endTime: form.endTime,
    meetingTopic: form.meetingTopic,
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
    meetingTopic: form.meetingTopic,
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

onMounted(() => {
  userStore.loadUser()
  isLoggedIn.value = userStore.isLoggedIn()

  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = (currentPage as any).$page?.options || {}
  
  if (options.roomId) {
    form.roomId = options.roomId
  }
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
}

.back-header {
  margin-bottom: 20rpx;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx 24rpx;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 24rpx;
  cursor: pointer;
  width: fit-content;
  
  &:active {
    background: rgba(59, 130, 246, 0.2);
  }
}

.back-icon {
  font-size: 36rpx;
  color: #3b82f6;
  font-weight: 600;
}

.back-text {
  font-size: 30rpx;
  color: #3b82f6;
  font-weight: 500;
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
</style>
