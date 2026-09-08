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
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLogged) return { path: '/login', query: { next: to.fullPath } }
  }
})

export default router