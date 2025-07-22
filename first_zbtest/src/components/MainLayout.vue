<template>
  <el-container style="height: 100vh;">
    <el-aside :width="'var(--sidebar-width)'" style="background-color: #001529;">
      <el-menu
        default-active="/detection"
        class="el-menu-vertical-demo"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><PieChart /></el-icon>
          <span>平台可视化展示</span>
        </el-menu-item>
        <el-menu-item index="/detection">
          <el-icon><Picture /></el-icon>
          <span>目标检测</span>
        </el-menu-item>
          <el-menu-item index="/live">
          <el-icon><Picture /></el-icon>
          <span>实时画面</span>
        </el-menu-item>
          <el-sub-menu index="/video">
            <template #title>
              <el-icon><Picture /></el-icon>
              <span>视频接入</span>
            </template>
            <el-menu-item index="/video/camera">摄像头</el-menu-item>
            <el-menu-item index="/video/stream">视频流</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/alarm">
          <el-icon><Picture /></el-icon>
          <span>告警记录</span>
        </el-menu-item>
          <el-menu-item index="/dataPush">
          <el-icon><Picture /></el-icon>
          <span>数据推送</span>
        </el-menu-item>
          <el-menu-item index="/algorithm">
          <el-icon><Picture /></el-icon>
          <span>算法仓库</span>
        </el-menu-item>
          <el-menu-item index="/database">
          <el-icon><Picture /></el-icon>
          <span>底库管理</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container style="flex-direction: column; height: 100%;">
      <el-header style="background-color: var(--header-bg-color); border-bottom: 1px solid var(--header-border-color); padding: var(--header-padding); height: 10%; min-height: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; height: 100%;">
          <div></div>
          <div style="display: flex; justify-content: flex-end; align-items: center; width: 100%; padding: 0 20px;">
            <el-dropdown>
              <span class="el-dropdown-link" style="display: flex; align-items: center; cursor: pointer; padding: var(--user-info-padding); border-radius: var(--border-radius); transition: background-color var(--transition-speed); margin-left: auto;">
                <el-avatar icon="User" style="margin-right: var(--avatar-margin-right);"></el-avatar>
                <span>管理员</span>
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { PieChart, Picture, Setting, User, ArrowDown } from '@element-plus/icons-vue';
</script>

<style scoped>
.el-header {
  height: 10% !important;
  min-height: auto !important;
}

.el-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  line-height: 200px;
  margin: 0;
  padding: 0;
}

.el-aside {
  width: var(--sidebar-width);
  height: 100vh;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 100%;
  height: 100%;
  min-height: auto;
}

.el-main { padding: 0; padding-left: 0; flex: 1 !important; box-sizing: border-box; margin: 0; width: 100%; min-width: 0; }

@media (max-width: 768px) {
  .el-aside {
    width: var(--sidebar-mobile-width) !important;
  }
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 60px;
  }
  .el-menu-item span {
    display: none;
  }
}
</style>