<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <h2 class="forgot-password-title">忘记密码</h2>
      <el-form ref="forgotPasswordForm" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" placeholder="请输入注册邮箱"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-row :gutter="10">
            <el-col :span="16">
              <el-input v-model="form.code" placeholder="请输入验证码"></el-input>
            </el-col>
            <el-col :span="8">
              <el-button :disabled="countdown > 0" @click="sendCode" type="default">
                {{ countdown > 0 ? `${countdown}秒后重新发送` : '发送验证码' }}
              </el-button>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="form.newPassword" type="password" placeholder="请输入新密码"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请确认新密码"></el-input>
        </el-form-item>
        <div class="forgot-password-links">
          <router-link to="/login">返回登录</router-link>
        </div>
        <el-form-item>
          <el-button type="primary" @click="handleResetPassword" style="width: 100%">重置密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const form = reactive({
  email: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
});

const countdown = ref(0);
const router = useRouter();

const rules = reactive({
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (rule, value, callback) => {
        if (value !== form.newPassword) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      }, trigger: 'blur' }
  ]
});

const sendCode = () => {
  // 实际项目中应调用后端发送验证码API
  if (!form.email) {
    ElMessage.warning('请先输入邮箱');
    return;
  }

  countdown.value = 60;
  const timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(timer);
    }
  }, 1000);

  ElMessage.success('验证码已发送到邮箱');
};

const handleResetPassword = () => {
  // 实际项目中应调用后端重置密码API
  ElMessage.success('密码重置成功！即将跳转到登录页面');
  setTimeout(() => {
    router.push('/login');
  }, 1500);
};
</script>

<style scoped>
.forgot-password-container {
  max-width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.forgot-password-card {
  width: 450px;
  padding: 30px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.forgot-password-title {
  text-align: center;
  margin-bottom: 20px;
  color: #1890ff;
}

.forgot-password-links {
  text-align: right;
  margin-bottom: 20px;
}

.forgot-password-links a {
  color: #1890ff;
  text-decoration: none;
}
</style>