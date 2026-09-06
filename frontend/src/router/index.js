import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/homeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/cart', name: 'cart', component: () => import('../views/CartView.vue') },
    { path: '/categoria/:slug', name: 'category', component: () => import('../views/ProductListView.vue') },
    { path: '/checkout', name: 'checkout', component: () => import('../views/CheckoutView.vue') },
    { path: '/order/:id/success', name: 'order-success', component: () => import('../views/OrderSuccessView.vue') },
    { path: '/track', name: 'track', component: () => import('../views/TrackOrderView.vue') },
  ],
})

export default router