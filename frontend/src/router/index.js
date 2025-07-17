import { createRouter, createWebHistory } from 'vue-router'
import Home           from '@/views/Home.vue'
import Login          from '@/views/Login.vue'
import Register       from '@/views/Register.vue'
import Dashboard      from '@/views/Dashboard.vue'
import Verify         from '@/views/Verify.vue'
import UploadCurriculum from '@/components/UploadCurriculum.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'

const routes = [
  { path: '/',         component: Home },
  { path: '/login',    component: Login, meta: { guestOnly: true } },
  { path: '/register', component: Register, meta: { guestOnly: true } },
  { path: '/verify',   component: Verify, name: 'Verify', meta: { guestOnly: true } },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/curriculum/upload',
    component: UploadCurriculum,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
  {
    path: '/admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _, next) => {
  const token = localStorage.getItem('token')
  const userRaw = localStorage.getItem('user')
  let user = null

  try {
    user = userRaw ? JSON.parse(userRaw) : null
  } catch (e) {
    user = null
  }

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  if (to.meta.requiresRole) {
    if (!user || user.role !== to.meta.requiresRole) {
      return next('/')
    }
  }

  if (to.meta.guestOnly && token) {
    return next('/dashboard')
  }

  next()
})

export default router
