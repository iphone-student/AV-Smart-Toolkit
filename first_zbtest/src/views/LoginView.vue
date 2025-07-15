<template>
  <div class="login-container">
      <div class="login-card">
        <h2 class="login-title">系统登录</h2>
        <el-form ref="formRef" :model="loginForm" :rules="rules" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <div class="login-links">
            <router-link to="/forgot-password">忘记密码</router-link>
            <router-link to="/register">注册账号</router-link>
          </div>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const loginForm = reactive({
  username: '',
  password: ''
});
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
};
const router = useRouter();

const handleLogin = () => {
  // 简单验证，实际项目中应使用el-form的validate方法
  if (loginForm.username && loginForm.password === '123') {
    router.push('/detection');
  } else {
    alert('用户名或密码错误');
  }
};
</script>

<style>
  .login-container {
    max-width: 100%;
  width: 100%;
  height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
  }

  .login-card {
    width: 400px;
    padding: 30px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .login-title {
    text-align: center;
    margin-bottom: 20px;
    color: #1890ff;
  }

  .login-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
  }

  .login-links a {
    color: #1890ff;
    text-decoration: none;
  }
  .login-button {
    margin: 0 auto;
    display: block;
  }
</style>

<style>
/* 覆盖全局媒体查询样式，确保登录页全屏显示 */
@media (min-width: 1024px) {
  body {
    display: block !important;
  }
  
  #app {
    display: block !important;
    padding: 0 !important;
    grid-template-columns: none !important;
  }
}
</style>
