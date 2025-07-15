import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import MainLayout from '../components/MainLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import DetectionView from '../views/DetectionView.vue'
import SettingsView from '../views/SettingsView.vue'
import AlgorithmView from '../views/AlgorithmView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPasswordView
    },
    {
      path: '/main',
      name: 'main',
      component: MainLayout,
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          component: DashboardView
        },
        {
          path: '/detection',
          name: 'detection',
          component: DetectionView
        },
        {
          path: '/algorithm',
          name: 'algorithm',
          component: AlgorithmView
        },
        {
          path: '/settings',
          name: 'settings',
          component: SettingsView
        }
      ]
    }
  ],
})

export default router
