import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '../stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/cart', name: 'cart', component: () => import('../views/CartView.vue') },
    { path: '/categoria/:slug', name: 'category', component: () => import('../views/ProductListView.vue') },
    { path: '/checkout', name: 'checkout', component: () => import('../views/CheckoutView.vue') },
    { path: '/order/:id/success', name: 'order-success', component: () => import('../views/OrderSuccessView.vue') },
    { path: '/track', name: 'track', component: () => import('../views/TrackOrderView.vue') },
    { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
    { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
    { path: '/my-orders', name: 'my-orders', component: () => import('../views/MyOrdersView.vue'), meta: { requiresAuth: true } },
    { path: '/staff/login', name: 'staff-login', component: () => import('../views/staff/StaffLoginView.vue') },
    {
      path: '/staff', component: () => import('../views/staff/AdminLayout.vue'), meta: { requiresStaff: true },
      children: [
        { path: '', name: 'staff-home', component: () => import('../views/staff/StaffDashboardView.vue') },
        { path: 'orders', name: 'staff-orders', component: () => import('../views/staff/StaffOrdersView.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLogged) return { path: '/login', query: { next: to.fullPath } }
  }
  if (to.meta.requiresStaff) {
    const auth = useAuthStore()
    if (!auth.isLogged) return { path: '/staff/login' }
    try { await auth.fetchMe() } catch {}
    if (!auth.isStaff) return { path: '/' }
  }
})

export default router