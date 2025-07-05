import { createRouter, createWebHistory } from 'vue-router'
import Home      from '@/views/Home.vue'
import Login     from '@/views/Login.vue'
import Register  from '@/views/Register.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  { path: '/',         component: Home },
  { path: '/login',    component: Login },
  { path: '/register', component: Register },
  { 
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } 
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
