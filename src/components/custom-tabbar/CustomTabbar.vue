<template>
  <view class="custom-tabbar">
    <view 
      v-for="item in tabList" 
      :key="item.key"
      :class="['tab-item', { active: currentTab === item.key }]"
      @click="switchTab(item.path)"
    >
      <text class="tab-icon">{{ item.icon }}</text>
      <text class="tab-text">{{ item.label }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  current: string
}>()

const currentTab = ref(props.current)

const tabList = [
  { key: 'home', label: '首页', icon: '🏠', path: '/pages/index/index' },
  { key: 'room', label: '会议室', icon: '🏢', path: '/pages/room/list' },
  { key: 'reservation', label: '我的预约', icon: '📅', path: '/pages/reservation/list' },
  { key: 'profile', label: '个人中心', icon: '👤', path: '/pages/user/profile' }
]

function switchTab(path: string) {
  uni.switchTab({ url: path })
}

onMounted(() => {
  currentTab.value = props.current
})
</script>

<style lang="scss" scoped>
.custom-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 140rpx;
  background: #ffffff;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.08);
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 999;
  display: flex;
  align-items: center;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.active {
    .tab-icon {
      transform: scale(1.1);
    }
    
    .tab-text {
      color: #4A90D9;
      font-weight: 700;
    }
  }
}

.tab-icon {
  font-size: 56rpx;
  margin-bottom: 8rpx;
  transition: transform 0.2s ease;
}

.tab-text {
  font-size: 36rpx;
  color: #8a8a8a;
  font-weight: 500;
  transition: color 0.2s ease;
}
</style>
