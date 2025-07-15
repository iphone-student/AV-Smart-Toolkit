<template>
  <div class="settings-container">
    <h1 class="page-title">系统设置</h1>
    <el-card>
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="账户设置">
          <el-form ref="accountForm" :model="accountForm" label-width="120px">
            <el-form-item label="用户名">
              <el-input v-model="accountForm.username" disabled></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="accountForm.email"></el-input>
            </el-form-item>
            <el-form-item label="手机号码">
              <el-input v-model="accountForm.phone"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveAccountSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="安全设置">
          <el-form ref="securityForm" :model="securityForm" label-width="120px">
            <el-form-item label="当前密码">
              <el-input v-model="securityForm.currentPassword" type="password"></el-input>
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="securityForm.newPassword" type="password"></el-input>
            </el-form-item>
            <el-form-item label="确认新密码">
              <el-input v-model="securityForm.confirmPassword" type="password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="通知设置">
          <el-form ref="notificationForm" :model="notificationForm" label-width="120px">
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationForm.emailNotification"></el-switch>
            </el-form-item>
            <el-form-item label="短信通知">
              <el-switch v-model="notificationForm.smsNotification"></el-switch>
            </el-form-item>
            <el-form-item label="检测结果通知">
              <el-switch v-model="notificationForm.detectionNotification"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';

const activeTab = ref('0');

const accountForm = reactive({
  username: 'admin',
  email: 'admin@example.com',
  phone: ''
});

const securityForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const notificationForm = reactive({
  emailNotification: true,
  smsNotification: false,
  detectionNotification: true
});

const saveAccountSettings = () => {
  // 实际项目中应调用后端API保存设置
  ElMessage.success('账户设置保存成功');
};

const changePassword = () => {
  // 实际项目中应调用后端API修改密码
  if (securityForm.newPassword !== securityForm.confirmPassword) {
    ElMessage.error('两次输入密码不一致');
    return;
  }
  ElMessage.success('密码修改成功');
};

const saveNotificationSettings = () => {
  // 实际项目中应调用后端API保存设置
  ElMessage.success('通知设置保存成功');
};
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}
</style>