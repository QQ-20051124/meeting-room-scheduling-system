/**
 * 预约通知工具
 * 用于发送预约成功、审核结果、冲突提醒等通知
 */

interface NotificationOptions {
  title: string
  content: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

/**
 * 显示通知
 */
export function showNotification(options: NotificationOptions) {
  const { title, content, type = 'info', duration = 3000 } = options
  
  // 使用 uni.showToast 显示通知
  uni.showToast({
    title: `${title}: ${content}`,
    icon: type === 'success' ? 'success' : type === 'error' ? 'error' : 'none',
    duration
  })
}

/**
 * 预约成功通知
 */
export function notifyReservationSuccess(roomName: string, date: string, time: string) {
  showNotification({
    title: '✅ 预约成功',
    content: `您已成功预约 ${roomName} (${date} ${time})`,
    type: 'success'
  })
}

/**
 * 预约审核通过通知
 */
export function notifyApproval(roomName: string, date: string, time: string) {
  showNotification({
    title: '✅ 审核通过',
    content: `您的预约已审核通过：${roomName} (${date} ${time})`,
    type: 'success'
  })
}

/**
 * 预约审核拒绝通知
 */
export function notifyRejection(roomName: string, reason: string) {
  showNotification({
    title: '❌ 审核拒绝',
    content: `您的预约被拒绝：${roomName}\n原因：${reason}`,
    type: 'error'
  })
}

/**
 * 冲突提醒通知
 */
export function notifyConflict(roomName: string, date: string, time: string, conflictReason: string) {
  showNotification({
    title: '⚠️ 时间冲突',
    content: `${roomName} 在 ${date} ${time} 已有预约\n${conflictReason}`,
    type: 'warning'
  })
}

/**
 * 预约取消通知
 */
export function notifyCancellation(roomName: string, date: string) {
  showNotification({
    title: 'ℹ️ 预约已取消',
    content: `您取消了 ${roomName} 的预约 (${date})`,
    type: 'info'
  })
}

/**
 * 等待队列补位通知
 */
export function notifyQueueTurn(userId: string, roomName: string, date: string, time: string) {
  showNotification({
    title: '🎉 轮到您了',
    content: `您排队的 ${roomName} (${date} ${time}) 现在可用，请尽快确认！`,
    type: 'success',
    duration: 5000
  })
}

/**
 * 会议室维护通知
 */
export function notifyMaintenance(roomName: string, reason: string) {
  showNotification({
    title: '🔧 维护通知',
    content: `${roomName} 正在进行维护：${reason}`,
    type: 'warning'
  })
}

/**
 * 预约提醒（会议开始前）
 */
export function notifyReminder(roomName: string, date: string, time: string, topic: string) {
  showNotification({
    title: ' 会议提醒',
    content: `您有一个即将开始的会议\n主题：${topic}\n地点：${roomName}\n时间：${date} ${time}`,
    type: 'info',
    duration: 5000
  })
}

/**
 * 显示确认对话框
 */
export function showConfirm(options: {
  title: string
  content: string
  onConfirm?: () => void
  onCancel?: () => void
}) {
  uni.showModal({
    title: options.title,
    content: options.content,
    success: (res) => {
      if (res.confirm && options.onConfirm) {
        options.onConfirm()
      } else if (res.cancel && options.onCancel) {
        options.onCancel()
      }
    }
  })
}
