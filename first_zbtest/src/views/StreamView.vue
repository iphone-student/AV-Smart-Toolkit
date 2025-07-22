<template>
  <el-tabs v-model="activeName" type="card">
    <el-tab-pane label="视频流接入" name="first">视频流接入</el-tab-pane>
  </el-tabs>
</template>
<script>
export default {
  data() {
      return {
        activeName: 'first'
      };
    }
};
</script>
<style scoped>
.card {
  line-height: 2;
}
</style>