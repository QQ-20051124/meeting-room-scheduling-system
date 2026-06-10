<template>
  <view class="container">
    <!-- 返回按钮 -->
    <view class="back-header">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
        <text class="back-text">返回</text>
      </view>
    </view>
    
    <view v-if="room" class="form-card">
      <view class="form-item">
        <text class="form-label">会议室编号</text>
        <input 
          class="form-input" 
          v-model="room.code" 
          placeholder="请输入会议室编号"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">会议室名称</text>
        <input 
          class="form-input" 
          v-model="room.name" 
          placeholder="请输入会议室名称"
          type="text"
        />
      </view>

      <view class="form-item">
        <text class="form-label">容纳人数</text>
        <input 
          class="form-input" 
          v-model="room.capacity" 
          placeholder="请输入容纳人数"
          type="number"
        />
      </view>

      <view class="form-item">
        <text class="form-label">地点</text>
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
          placeholder="请输入设备情况"
        />
      </view>

      <view class="form-item">
        <text class="form-label">状态</text>
        <picker :value="statusIndex" :range="statusOptions" @change="onStatusChange">
          <view class="form-select">
            {{ statusOptions[statusIndex] }}
          </view>
        </picker>
      </view>

      <view class="btn-primary" @click="handleUpdate">保存修改</view>

      <view v-if="isAdmin" class="btn-danger mt-20" @click="handleDelete">删除会议室</view>
    </view>

    <view v-else class="empty-state">
      <text class="empty-text">会议室不存在</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoomStore } from '@/stores/room'
import { useUserStore } from '@/stores/user'

const roomStore = useRoomStore()
const userStore = useUserStore()

const room = reactive({
  id: '',
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
const isAdmin = ref(false)

function onStatusChange(e: any) {
  statusIndex.value = e.detail.value
  room.status = statusValues[statusOptions[e.detail.value]]
}

function goBack() {
  uni.navigateBack()
}

function handleUpdate() {
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

  roomStore.updateRoom(room.id, {
    code: room.code,
    name: room.name,
    capacity: room.capacity,
    location: room.location,
    equipment: room.equipment || '无',
    status: room.status
  })

  uni.showToast({ title: '修改成功', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}

function handleDelete() {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除该会议室吗？',
    success: (res) => {
      if (res.confirm) {
        roomStore.deleteRoom(room.id)
        uni.showToast({ title: '删除成功', icon: 'success' })
        setTimeout(() => {
          uni.navigateBack()
        }, 1500)
      }
    }
  })
}

onMounted(() => {
  userStore.loadUser()
  isAdmin.value = userStore.isAdmin()
  
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = (currentPage as any).$page?.options || {}
  
  if (options.id) {
    const foundRoom = roomStore.getRoomById(options.id)
    if (foundRoom) {
      Object.assign(room, foundRoom)
      const keys = Object.keys(statusValues)
      statusIndex.value = keys.indexOf(foundRoom.status)
    }
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

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400rpx;
}

.empty-text {
  font-size: 28rpx;
  color: $text-light;
}
</style>
