<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon vehicle">
              <el-icon><Van /></el-icon>
            </div>
            <div class="stats-info">
              <h3>{{ stats.totalVehicles }}</h3>
              <p>车辆总数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon fleet">
              <el-icon><TruckFilled /></el-icon>
            </div>
            <div class="stats-info">
              <h3>{{ stats.totalFleets }}</h3>
              <p>车队总数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon order">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stats-info">
              <h3>{{ stats.todayOrders }}</h3>
              <p>今日订单</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon revenue">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stats-info">
              <h3>¥{{ stats.todayRevenue.toLocaleString() }}</h3>
              <p>今日收入</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表和表格 -->
    <el-row :gutter="20" class="content-row">
      <!-- 最近订单 -->
      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>最近订单</span>
              <el-button type="text" @click="$router.push('/orders')">查看全部</el-button>
            </div>
          </template>
          
          <el-table :data="recentOrders" style="width: 100%" size="small">
            <el-table-column prop="orderNo" label="订单号" width="120" />
            <el-table-column prop="fleetName" label="车队" width="100" />
            <el-table-column prop="amount" label="金额" width="80">
              <template #default="{ row }">
                ¥{{ row.amount.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="时间">
              <template #default="{ row }">
                {{ formatTime(row.createTime) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <!-- 平台数据统计 -->
      <el-col :span="12">
        <el-card class="content-card">
          <template #header>
            <div class="card-header">
              <span>平台数据统计</span>
            </div>
          </template>
          
          <el-table :data="platformStats" style="width: 100%" size="small">
            <el-table-column prop="platform" label="平台" width="120" />
            <el-table-column prop="todayOrders" label="今日订单" width="80" />
            <el-table-column prop="todayAmount" label="今日金额" width="100">
              <template #default="{ row }">
                ¥{{ row.todayAmount.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.status === '正常' ? 'success' : 'danger'" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="lastSync" label="最后同步">
              <template #default="{ row }">
                {{ formatTime(row.lastSync) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 统计数据
const stats = ref({
  totalVehicles: 0,
  totalFleets: 0,
  todayOrders: 0,
  todayRevenue: 0
})

// 最近订单
const recentOrders = ref([
  {
    orderNo: 'ORD20240106001',
    fleetName: '快运车队',
    amount: 156.80,
    status: '已完成',
    createTime: new Date()
  },
  {
    orderNo: 'ORD20240106002',
    fleetName: '城际运输',
    amount: 289.50,
    status: '进行中',
    createTime: new Date(Date.now() - 1000 * 60 * 30)
  },
  {
    orderNo: 'ORD20240106003',
    fleetName: '同城配送',
    amount: 98.20,
    status: '已完成',
    createTime: new Date(Date.now() - 1000 * 60 * 60)
  }
])

// 平台统计
const platformStats = ref([
  {
    platform: '滴滴货运',
    todayOrders: 45,
    todayAmount: 2580.50,
    status: '正常',
    lastSync: new Date(Date.now() - 1000 * 60 * 5)
  },
  {
    platform: '货拉拉',
    todayOrders: 38,
    todayAmount: 1950.80,
    status: '正常',
    lastSync: new Date(Date.now() - 1000 * 60 * 3)
  },
  {
    platform: '快狗打车',
    todayOrders: 22,
    todayAmount: 1280.30,
    status: '异常',
    lastSync: new Date(Date.now() - 1000 * 60 * 60 * 2)
  }
])

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '已取消':
      return 'danger'
    default:
      return 'info'
  }
}

// 格式化时间
const formatTime = (time: Date) => {
  return time.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载数据
const loadData = async () => {
  try {
    // 模拟数据加载
    stats.value = {
      totalVehicles: 156,
      totalFleets: 12,
      todayOrders: 105,
      todayRevenue: 5810.60
    }
  } catch (error) {
    ElMessage.error('数据加载失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  height: 120px;
}

.stats-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.stats-icon.vehicle {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-icon.fleet {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stats-icon.order {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stats-icon.revenue {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stats-info h3 {
  margin: 0 0 5px 0;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.stats-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.content-row {
  margin-bottom: 20px;
}

.content-card {
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-weight: 600;
  color: #333;
}
</style>