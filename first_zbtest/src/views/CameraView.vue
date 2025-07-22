<template>
  <el-tabs v-model="activeName" type="card">
    <el-tab-pane name="first">
      <template #label>
        <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
          <span>摄像头</span>
          <el-button size="small" type="primary" @click="drawerVisible = true" style="margin-left: 580px;">导入摄像头</el-button>
        </div>
      </template>
      <el-drawer
        v-model="drawerVisible"
        style="margin-top: 2"
        title="导入摄像头"
        direction="rtl"
        size="30%"
      >
        <div>导入摄像头的表单内容将在这里添加</div>
      </el-drawer>
      <div>
        <el-table :data="tableData" style="width: 100%" >
          <el-table-column prop="name" label="描述" width="160" align="center"></el-table-column>
          <el-table-column prop="ip" label="IP地址" width="160" align="center"></el-table-column>
          <el-table-column prop="port" label="流地址" width="160"></el-table-column>
          <el-table-column prop="useAlgorithm" label="启用算法" width="160"></el-table-column>
          <el-table-column prop="status" label="状态" width="160"></el-table-column>
          <el-table-column prop="codeFormat" label="编码格式" width="160"></el-table-column>
          <el-table-column prop="operation" label="操作" width="160"></el-table-column>
        </el-table>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
export default {
  data() {
      return {
        tableData: [
          {
            name: '摄像头1',
            ip: '192.168.1.1',
            port: 'rtsp://192.168.1.1:554/Streaming/Channels/101',
            useAlgorithm: '是',
            status: '正常',
            codeFormat: 'H264',
            operation: '编辑  删除  启用  禁用'
          },
          {
            name: '摄像头2',
            ip: '192.168.1.2',
            port: 'rtsp://192.168.1.1:554/Streaming/Channels/102',
            useAlgorithm: '是',
            status: '正常',
            codeFormat: 'H264',
            operation: '编辑  删除  启用  禁用'
          }
          
        ],
        activeName: 'first',
        drawerVisible: false
      };
    }
};
</script>
<style scoped>
.card {
  line-height: 2;
}
</style>