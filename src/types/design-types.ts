/**
 * 8.4.4 关键数据结构设计
 * 根据设计文档创建的数据类型定义
 */

/**
 * (1) 预约实体结构
 */
interface Reservation {
  date: string;                  // 预约日期
  startTime: string;             // 起始时间
  endTime: string;               // 结束时间
  roomId: string;                // 目标会议室ID
  status: 'pending' | 'approved' | 'rejected';  // 预约状态
  userId: string;                // 申请人ID
  userType: 'admin' | 'teacher' | 'student';    // 用户类型
}

/**
 * (2) 预约二级索引结构 (优化冲突检索)
 * 第一层key: 预约日期；第二层key: 会议室ID；值: 当日预约数组
 * 
 * 设计价值: 不用遍历系统全部预约记录，直接通过日期 + 会议室ID精准定位待校验数据集，
 * 大幅缩减循环次数。
 */
type RoomDateIndex = Record<string, Record<string, Reservation[]>>;

/**
 * (3) 排队队列项结构
 */
interface QueueItem {
  id: string;                    // 队列项唯一标识
  userId: string;                // 用户ID
  date: string;                  // 预约日期
  startTime: string;             // 起始时间
  endTime: string;               // 结束时间
  participantCount: number;      // 参会人数
  priorityScore: number;         // 综合优先级分值，越小越优先
  createTime: string;            // 入队时间，用于计算等待时长加分
}

/**
 * (4) 优先队列 (小根堆) 结构
 * 基于数组实现标准堆结构，封装入队、出队、取堆顶方法，
 * 自动维护优先级有序，无需每次全局排序。
 */
class PriorityQueue<T> {
  private heap: T[] = [];
  private compare: (a: T, b: T) => number;

  constructor(compareFn: (a: T, b: T) => number) {
    this.compare = compareFn;
  }

  // 入队
  enqueue(item: T): void {
    this.heap.push(item);
    this.bubbleUp(this.heap.length - 1);
  }

  // 出队（获取优先级最高的元素）
  dequeue(): T | undefined {
    if (this.isEmpty()) return undefined;
    
    const top = this.heap[0];
    const last = this.heap.pop();
    
    if (this.heap.length > 0 && last) {
      this.heap[0] = last;
      this.bubbleDown(0);
    }
    
    return top;
  }

  // 取堆顶元素（不删除）
  peek(): T | undefined {
    return this.heap[0];
  }

  // 判断是否为空
  isEmpty(): boolean {
    return this.heap.length === 0;
  }

  // 获取队列大小
  size(): number {
    return this.heap.length;
  }

  // 上浮调整
  private bubbleUp(index: number): void {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      
      if (this.compare(this.heap[index], this.heap[parentIndex]) >= 0) {
        break;
      }
      
      this.swap(index, parentIndex);
      index = parentIndex;
    }
  }

  // 下沉调整
  private bubbleDown(index: number): void {
    const length = this.heap.length;
    
    while (true) {
      let smallest = index;
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      
      if (leftChild < length && this.compare(this.heap[leftChild], this.heap[smallest]) < 0) {
        smallest = leftChild;
      }
      
      if (rightChild < length && this.compare(this.heap[rightChild], this.heap[smallest]) < 0) {
        smallest = rightChild;
      }
      
      if (smallest === index) break;
      
      this.swap(index, smallest);
      index = smallest;
    }
  }

  // 交换元素
  private swap(i: number, j: number): void {
    const temp = this.heap[i];
    this.heap[i] = this.heap[j];
    this.heap[j] = temp;
  }
}

export type { Reservation, RoomDateIndex, QueueItem };
export { PriorityQueue };
