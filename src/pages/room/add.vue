<template>
  <view class="container">
    <!-- 返回按钮 -->
    <view class="back-header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
        <text class="back-text">返回</text>
      </view>
    </view>
    
    <view class="form-card">
      <view class="form-item">
        <text class="form-label">会议室编号 *</text>
        <input 
          class="form-input" 
          v-model="room.code" 
          placeholder="请输入会议室编号"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">会议室名称 *</text>
        <input 
          class="form-input" 
          v-model="room.name" 
          placeholder="请输入会议室名称"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">容纳人数 *</text>
        <input 
          class="form-input" 
          v-model="room.capacity" 
          placeholder="请输入容纳人数"
          type="number"
        />
      </view>

      <view class="form-item">
        <text class="form-label">地点 *</text>
        <input 
          class="form-input" 
          v-model="room.location" 
          placeholder="请输入会议室地点"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">设备情况</text>
        <textarea 
          class="form-textarea" 
          v-model="room.equipment" 
          placeholder="请输入设备情况，如：投影仪、白板、音响等"
        />
      </view>

      <view class="form-item">
        <text class="form-label">状态 *</text>
        <picker :value="statusIndex" :range="statusOptions" @change="onStatusChange">
          <view class="form-select">
            {{ statusOptions[statusIndex] }}
          </view>
        </picker>
      </view>

      <view class="btn-primary" @click="handleSubmit">添加会议室</view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoomStore } from '@/stores/room'

const roomStore = useRoomStore()

const room = reactive({
  code: '',
  name: '',
  capacity: 0,
  location: '',
  equipment: '',
  status: 'available'
})

const statusOptions = ['可预约', '不可用', '维护中']
const statusValues: Record<string, 'available' | 'unavailable' | 'maintenance'> = {
  '可预约': 'available',
  '不可用': 'unavailable',
  '维护中': 'maintenance'
}
const statusIndex = ref(0)

function onStatusChange(e: any) {
  statusIndex.value = e.detail.value
  room.status = statusValues[statusOptions[e.detail.value]]
}

function goBack() {
  uni.navigateBack()
}

function handleSubmit() {
  if (!room.code.trim()) {
    uni.showToast({ title: '请输入会议室编号', icon: 'none' })
    return
  }
  if (!room.name.trim()) {
    uni.showToast({ title: '请输入会议室名称', icon: 'none' })
    return
  }
  if (!room.capacity || room.capacity <= 0) {
    uni.showToast({ title: '请输入有效的容纳人数', icon: 'none' })
    return
  }
  if (!room.location.trim()) {
    uni.showToast({ title: '请输入会议室地点', icon: 'none' })
    return
  }

  roomStore.addRoom({
    code: room.code,
    name: room.name,
    capacity: room.capacity,
    location: room.location,
    equipment: room.equipment || '无',
    status: room.status
  })

  uni.showToast({ title: '添加成功', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}
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
</style>
