<template>
  <div class="flex min-h-screen">
    <aside class="w-52 bg-neutral-900 text-white p-4 space-y-2">
      <p class="font-bold mb-4">Chifa Staff</p>
      <router-link to="/staff" class="block underline">Dashboard</router-link>
      <router-link to="/staff/orders" class="block underline">Pedidos</router-link>
      <router-link to="/" class="block underline opacity-70">Ver tienda</router-link>
      <button @click="auth.logout(); $router.push('/staff/login')" class="text-sm opacity-70">Salir</button>
    </aside>
    <main class="flex-1 p-6"><router-view /></main>
  </div>
</template>
<script setup>
import { useAuthStore } from '../../stores/authStore'
const auth = useAuthStore()
</script>