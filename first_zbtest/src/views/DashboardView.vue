<template>
  <el-container class="dashboard">

      <!-- 左侧设备树 -->
      <el-aside width="260px" class="sidebar">
        <el-input placeholder="搜索设备..." v-model="search" size="big" />
        <el-tree :data="treeData" :props="defaultProps" />
      </el-aside>

      <!-- 中间监控内容 -->
      <el-main class="main-panel">
        <!-- 视频区域 -->
        <div class="video-grid">
          <div class="video-box" v-for="n in 4" :key="n">
            <div class="video-feed">实时监控 {{ n }}</div>
          </div>
        </div>

        <!-- 下方统计 -->
        <div class="stats">
          <div class="stat-box">
            <div>设备统计</div>
            <el-progress :percentage="50" status="success" />
          </div>
          <div class="stat-box">
            <div>今日告警数</div>
            <div class="alarm-number">9</div>
          </div>
          <div class="stat-box">
            <div>告警趋势图</div>
            <div ref="chartRef" class="chart" />
          </div>
        </div>
      </el-main>

      <!-- 右侧告警记录 -->
      <el-aside width="350px" class="alarm-panel">
        <div class="alarm-title">告警记录</div>
            <el-timeline-item v-for="(item, index) in alarmList" :key="index" :timestamp="item.time">
              <div>{{ item.device }}</div></el-timeline-item>
      </el-aside>
    </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const search = ref('')
const treeData = [
  {
    label: '实验室区域设备',
    children: [{ label: '001' }, { label: '002' }, { label: '003' }]
  },
  {
    label: '核心区域设备',
    children: [{ label: '004' }, { label: '005' }, { label: '006' }]
  }
]
const defaultProps = {
  children: 'children',
  label: 'label'
}

const alarmList = ref([
  { device: '设备 001', time: '2024-01-14 17:22:10', img: 'https://via.placeholder.com/100' },
  { device: '设备 002', time: '2024-01-14 17:22:02', img: 'https://via.placeholder.com/100' },
  // 可继续添加
])

const currentTime = ref('')
function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleString()
}
setInterval(updateTime, 1000)
updateTime()

// ECharts 示例
const chartRef = ref()
onMounted(() => {
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    xAxis: {
      type: 'category',
      data: ['1.12', '1.13', '1.14', '1.15', '1.16', '1.17', '1.18']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [5, 9, 12, 7, 14, 8, 10],
        type: 'line'
      }
    ]
  })
})
</script>

<style scoped>
.dashboard {
  line-height: 2;
  height: 90vh;
  background: #001c30;
  color: #fff;
  font-family: 'Microsoft YaHei';
}

.header {
  height: 50px;
  background: #003366;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.title {
  font-size: 15px;
  font-weight: bold;
}
.time-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sidebar {
  background: #01203a;
  border-right: 1px solid #0a2f4e;
  padding: 0 12px !important;
  margin: 0;
}

.sidebar .el-input {
  margin-top: 0 !important;
}
.sidebar .el-input {
  
  margin-top: 0 !important;
  padding: 0 0px;
}
.sidebar .el-input__wrapper {
  margin-top: 0 !important;
}

.sidebar .el-tree {
  margin-top: 0 !important;
}

.main-panel {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #000;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
.video-box {
  background: #000;
  height: 200px;
  position: relative;
}
.video-feed {
  position: absolute;
  bottom: 5px;
  left: 5px;
  color: #00ffff;
}

.stats {
  display: flex;
  gap: 10px;
}
.stat-box {
  flex: 1;
  background: #012d4c;
  padding: 10px;
}
.chart {
  width: 100%;
  height: 150px;
}

.alarm-panel {
  background: #01203a;
  padding: 15px;
  height: 100%;
  color: white;
}

.alarm-panel .el-timeline {
  display: flex;
  overflow-x: auto;
  padding-bottom: 10px;
}

.alarm-panel .el-timeline-item {
  flex: none;
  margin-right: 20px;
  white-space: nowrap;
}
.alarm-title {
  font-size: 13px;
  margin-bottom: 0px;
}
.alarm-img {
  width: 10%;
  margin-top: 1px;
  border-radius: 1px;
}
</style>
