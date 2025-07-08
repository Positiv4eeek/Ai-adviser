import { createRouter, createWebHistory } from 'vue-router'
import Home      from '@/views/Home.vue'
import Login     from '@/views/Login.vue'
import Register  from '@/views/Register.vue'
import Dashboard from '@/views/Dashboard.vue'
import Verify    from '@/views/Verify.vue'
import UploadCurriculum from '@/components/UploadCurriculum.vue'
import CurriculumList   from '@/views/CurriculumList.vue'

const routes = [
  { path: '/',         component: Home },
  { path: '/login',    component: Login },
  { path: '/register', component: Register },
  { path: '/verify',  component: Verify,    name: 'Verify' },
  { 
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } 
  },
  {
    path: '/upload-curriculum',
    component: UploadCurriculum,
    meta: { requiresAuth: true, requiresRole: 'admin' } 
  },
  {
    path: '/curriculum/list',
    component: CurriculumList,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) return next('/login')
  next()
})

export default router
