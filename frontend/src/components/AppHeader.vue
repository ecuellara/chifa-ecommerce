<template>
  <header class="bg-red-700 text-white">
    <nav class="max-w-4xl mx-auto px-4 py-3 flex items-center gap-4 flex-wrap">
      <router-link to="/" class="font-bold text-lg">Chifa</router-link>
      <router-link to="/cart" class="underline">
        Carrito<span v-if="cart.totalItems"> ({{ cart.totalItems }})</span>
      </router-link>
      <router-link to="/track" class="underline">Consultar pedido</router-link>
      <span class="flex-1"></span>
      <template v-if="auth.isLogged">
        <router-link to="/my-orders" class="underline">Mis pedidos</router-link>
        <router-link v-if="auth.isStaff" to="/staff" class="underline">Panel</router-link>
        <span class="text-sm opacity-80">{{ auth.username }}</span>
        <button @click="salir" class="underline text-sm">Salir</button>
      </template>
      <template v-else>
        <router-link to="/login" class="underline">Entrar</router-link>
        <router-link to="/register" class="underline">Registro</router-link>
      </template>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cartStore'
import { useAuthStore } from '../stores/authStore'

const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()

const salir = () => {
  auth.logout()
  router.push('/')
}
</script>
