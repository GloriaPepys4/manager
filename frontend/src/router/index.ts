import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import LoginView from '@/views/LoginView.vue'
import MainLayout from '@/components/Layout/MainLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import VehiclesView from '@/views/VehiclesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView
        },
        {
          path: 'vehicles',
          name: 'vehicles',
          component: VehiclesView
        },
        {
          path: 'fleets',
          name: 'fleets',
          component: () => import('@/views/FleetsView.vue')
        },
        {
          path: 'stations',
          name: 'stations',
          component: () => import('@/views/StationsView.vue')
        },
        {
          path: 'recharge',
          name: 'recharge',
          component: () => import('@/views/RechargeView.vue')
        },
        {
          path: 'orders',
          name: 'orders',
          component: () => import('@/views/OrdersView.vue')
        },
        {
          path: 'reconciliation',
          name: 'reconciliation',
          component: () => import('@/views/ReconciliationView.vue')
        },
        {
          path: 'import',
          name: 'import',
          component: () => import('@/views/ImportView.vue')
        }
      ]
    }
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth !== false && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
