<template>
  <view class="calendar-view">
    <view class="calendar-header">
      <view class="calendar-nav" @click="prevMonth">
        <text class="nav-arrow">‹</text>
      </view>
      <view class="calendar-title">{{ currentYear }}年{{ currentMonth }}月</view>
      <view class="calendar-nav" @click="nextMonth">
        <text class="nav-arrow">›</text>
      </view>
    </view>

    <view class="calendar-weekdays">
      <view class="weekday" v-for="day in weekDays" :key="day">{{ day }}</view>
    </view>

    <view class="calendar-days">
      <view 
        class="day-cell" 
        v-for="(day, index) in calendarDays" 
        :key="index"
        :class="{
          'day-prev': day.isPrevMonth,
          'day-next': day.isNextMonth,
          'day-today': day.isToday,
          'day-selected': day.isSelected,
          'day-has-events': day.hasEvents
        }"
        @click="selectDay(day)"
      >
        <view class="day-number">{{ day.day }}</view>
        <view v-if="day.hasEvents" class="event-dot"></view>
      </view>
    </view>

    <view class="selected-date-info" v-if="selectedDate">
      <view class="info-title">
        <text>{{ selectedDate.year }}年{{ selectedDate.month }}月{{ selectedDate.day }}日</text>
        <text class="info-weekday">{{ selectedDate.weekday }}</text>
      </view>
      <view class="events-list">
        <view v-if="eventsOnSelectedDay.length === 0" class="no-events">
          <text>暂无预约</text>
        </view>
        <view v-else class="event-item" v-for="event in eventsOnSelectedDay" :key="event.id">
          <view class="event-time">{{ event.startTime }} - {{ event.endTime }}</view>
          <view class="event-info">
            <view class="event-room">{{ event.roomName }}</view>
            <view class="event-topic">{{ event.meetingTopic }}</view>
            <view class="event-applicant">{{ event.applicant }}</view>
          </view>
          <view :class="['event-status', event.status]">
            {{ getStatusText(event.status) }}
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Reservation } from '@/types'

interface Props {
  reservations?: Reservation[]
  onDaySelect?: (date: string) => void
}

const props = withDefaults(defineProps<Props>(), {
  reservations: () => []
})

const emit = defineEmits<{
  daySelect: [date: string]
}>()

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const currentDate = new Date()
const currentYear = ref(currentDate.getFullYear())
const currentMonth = ref(currentDate.getMonth() + 1)

const selectedDate = ref<{
  year: number
  month: number
  day: number
  weekday: string
} | null>(null)

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month - 1, 1)
  const lastDay = new Date(year, month, 0)
  const prevMonthLastDay = new Date(year, month - 1, 0)
  const startWeekday = firstDay.getDay()
  
  const days: any[] = []
  const today = new Date()
  
  // 添加上个月的天数
  for (let i = startWeekday - 1; i >= 0; i--) {
    const day = prevMonthLastDay.getDate() - i
    days.push({
      day,
      isPrevMonth: true,
      isToday: false,
      isSelected: false,
      hasEvents: false,
      date: new Date(year, month - 2, day)
    })
  }
  
  // 添加当月的天数
  for (let day = 1; day <= lastDay.getDate(); day++) {
    const date = new Date(year, month - 1, day)
    const isToday = date.toDateString() === today.toDateString()
    const isSelected = selectedDate.value && 
      selectedDate.value.year === year && 
      selectedDate.value.month === month && 
      selectedDate.value.day === day
    
    const dateStr = formatDate(date)
    const hasEvents = props.reservations.some(r => r.date === dateStr)
    
    days.push({
      day,
      isPrevMonth: false,
      isNextMonth: false,
      isToday,
      isSelected,
      hasEvents,
      date,
      weekday: weekDays[date.getDay()]
    })
  }
  
  // 添加下个月的天数
  const remaining = 42 - days.length
  for (let day = 1; day <= remaining; day++) {
    days.push({
      day,
      isPrevMonth: false,
      isNextMonth: true,
      isToday: false,
      isSelected: false,
      hasEvents: false,
      date: new Date(year, month, day)
    })
  }
  
  return days
})

const eventsOnSelectedDay = computed(() => {
  if (!selectedDate.value) return []
  const dateStr = formatDate(selectedDate.value.date!)
  return props.reservations.filter(r => r.date === dateStr)
})

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function prevMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function selectDay(dayInfo: any) {
  selectedDate.value = {
    year: dayInfo.date.getFullYear(),
    month: dayInfo.date.getMonth() + 1,
    day: dayInfo.date.getDate(),
    weekday: dayInfo.weekday || weekDays[dayInfo.date.getDay()]
  }
  
  const dateStr = formatDate(dayInfo.date)
  emit('daySelect', dateStr)
}

function getStatusText(status: string): string {
  const map: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}
</script>

<style lang="scss" scoped>
.calendar-view {
  background: $white;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  box-shadow: $shadow;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.calendar-nav {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: $radius-full;
  
  &:active {
    opacity: 0.8;
  }
}

.nav-arrow {
  font-size: 40rpx;
  color: $white;
  font-weight: bold;
}

.calendar-title {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-color;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10rpx;
  margin-bottom: 10rpx;
}

.weekday {
  text-align: center;
  font-size: 24rpx;
  color: $text-light;
  font-weight: 600;
  padding: 10rpx 0;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10rpx;
}

.day-cell {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: $radius;
  position: relative;
  transition: all 0.3s ease;
  
  &:active {
    transform: scale(0.9);
  }
  
  &.day-today {
    background: linear-gradient(135deg, #667eea, #764ba2);
    
    .day-number {
      color: $white;
      font-weight: bold;
    }
  }
  
  &.day-selected {
    background: linear-gradient(135deg, #0ba360, #3cba92);
    
    .day-number {
      color: $white;
    }
  }
  
  &.day-has-events {
    &::after {
      content: '';
      position: absolute;
      bottom: 8rpx;
      width: 12rpx;
      height: 12rpx;
      background: #ef4444;
      border-radius: 50%;
    }
  }
}

.day-number {
  font-size: 28rpx;
  color: $text-color;
}

.event-dot {
  position: absolute;
  bottom: 8rpx;
  width: 12rpx;
  height: 12rpx;
  background: #ef4444;
  border-radius: 50%;
}

.selected-date-info {
  margin-top: $spacing-lg;
  padding-top: $spacing-lg;
  border-top: 2rpx solid $border-color;
}

.info-title {
  display: flex;
  flex-direction: column;
  margin-bottom: $spacing-md;
  
  text {
    font-size: 30rpx;
    font-weight: bold;
    color: $text-color;
  }
  
  .info-weekday {
    font-size: 26rpx;
    color: $text-light;
    margin-top: 8rpx;
  }
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.no-events {
  text-align: center;
  padding: 40rpx;
  color: $text-light;
  font-size: 28rpx;
}

.event-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background: #f8f9fa;
  border-radius: $radius;
  border-left: 4rpx solid $primary-color;
}

.event-time {
  font-size: 24rpx;
  color: $text-light;
  min-width: 120rpx;
}

.event-info {
  flex: 1;
  margin-left: $spacing-sm;
  
  .event-room {
    font-size: 26rpx;
    font-weight: bold;
    color: $text-color;
  }
  
  .event-topic {
    font-size: 24rpx;
    color: $text-secondary;
    margin-top: 4rpx;
  }
  
  .event-applicant {
    font-size: 22rpx;
    color: $text-light;
    margin-top: 4rpx;
  }
}

.event-status {
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: $radius-full;
  font-weight: 600;
  
  &.pending {
    background: rgba(#F59E0B, 0.1);
    color: #F59E0B;
  }
  
  &.approved {
    background: rgba(#10B981, 0.1);
    color: #10B981;
  }
  
  &.rejected {
    background: rgba(#EF4444, 0.1);
    color: #EF4444;
  }
  
  &.completed {
    background: rgba(#3B82F6, 0.1);
    color: #3B82F6;
  }
  
  &.cancelled {
    background: rgba(#6B7280, 0.1);
    color: #6B7280;
  }
}
</style>
