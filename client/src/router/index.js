import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import DashboardView from '@/views/DashboardView.vue'
import CreateWorkView from '@/views/CreateWorkView.vue'
import JoinWorkView from '@/views/JoinWorkView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/dashboard/create',
      name: 'create_work',
      component: CreateWorkView
    },
    {
      path: '/dashboard/join',
      name: 'join_work',
      component: JoinWorkView
    }
  ]
})

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'chalk -> . . .'
})

export default router
