import { createRouter, createWebHistory } from 'vue-router'

import StartHomeView from '@/views/start/StartHomeView.vue'
import StartLoginView from '@/views/start/StartLoginView.vue'
import StartSignupView from '@/views/start/StartSignupView.vue'
import UserDashboardView from '@/views/user/UserDashboardView.vue'
import UserCreateView from '@/views/user/UserCreateView.vue'
import UserJoinView from '@/views/user/UserJoinView.vue'
import WorkMembersView from '@/views/work/WorkMembersView.vue'
import WorkExamsView from '@/views/work/WorkExamsView.vue'
import WorkSettingsView from '@/views/work/WorkSettingsView.vue'
import WorkCreateView from '@/views/work/WorkCreateView.vue'
import ManageStartView from '@/views/manage/ManageStartView.vue'
import ManageSessionsView from '@/views/manage/ManageSessionsView.vue'
import ManageQuestionsView from '@/views/manage/ManageQuestionsView.vue'
import ManageSettingsView from '@/views/manage/ManageSettingsView.vue'
import ExamWriteView from '@/views/exam/ExamWriteView.vue'
import ExamAccessView from '@/views/exam/ExamAccessView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: StartHomeView
    },
    {
      path: '/login',
      component: StartLoginView
    },
    {
      path: '/signup',
      component: StartSignupView
    },
    {
      path: '/dashboard',
      component: UserDashboardView
    },
    {
      path: '/dashboard/join',
      component: UserJoinView
    },
    {
      path: '/dashboard/create',
      component: UserCreateView
    },
    {
      path: '/:work_admin_username/:urn/members',
      component: WorkMembersView
    },
    {
      path: '/:work_admin_username/:urn/exams',
      component: WorkExamsView
    },
    {
      path: '/:work_admin_username/:urn/settings',
      component: WorkSettingsView
    },
    {
      path: '/:work_admin_username/:urn/create',
      component: WorkCreateView
    },
    {
      path: '/:work_admin_username/:urn/:id/start',
      component: ManageStartView
    },
    {
      path: '/:work_admin_username/:urn/:id/sessions',
      component: ManageSessionsView
    },
    {
      path: '/:work_admin_username/:urn/:id/questions',
      component: ManageQuestionsView
    },
    {
      path: '/:work_admin_username/:urn/:id/settings',
      component: ManageSettingsView
    },
    {
      path: '/:work_admin_username/:urn/:id/write',
      component: ExamWriteView
    },
    {
      path: '/:work_admin_username/:urn/:id/access',
      component: ExamAccessView
    }
  ]
})

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'chalk -> . . .'
})

export default router
