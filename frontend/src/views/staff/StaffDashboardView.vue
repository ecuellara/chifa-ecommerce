<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Dashboard hoy ({{ stats.fecha }})</h1>
    <p v-if="error" class="text-red-500 bg-red-100 p-2 rounded mb-3">{{ error }}</p>
    <div class="grid grid-cols-3 gap-3 mb-4">
      <div class="bg-white shadow rounded p-4"><p class="text-sm text-gray-500">Pedidos</p><p class="text-2xl font-bold">{{ stats.n_hoy }}</p></div>
      <div class="bg-white shadow rounded p-4"><p class="text-sm text-gray-500">Ventas</p><p class="text-2xl font-bold">S/. {{ stats.ventas_hoy }}</p></div>
      <div class="bg-white shadow rounded p-4"><p class="text-sm text-gray-500">Ticket</p><p class="text-2xl font-bold">S/. {{ stats.ticket_hoy }}</p></div>
    </div>
    <div class="bg-white shadow rounded p-4">
      <p class="font-bold mb-2">Por estado</p>
      <div v-for="e in stats.por_estado" :key="e.estado" class="flex justify-between text-sm">
        <span>{{ e.estado }}</span><span>{{ e.n }}</span>
      </div>
    </div>
    <router-link to="/staff/orders" class="underline text-sm mt-3 inline-block">Ir a pedidos</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/axios'

const stats = ref({ fecha: '', n_hoy: 0, ventas_hoy: '0', ticket_hoy: '0', por_estado: [] })
const error = ref('')

onMounted(async () => {
  try {
    const r = await api.get('staff/stats/')
    stats.value = r.data
  } catch { error.value = 'No se pudo cargar stats (¿eres staff?).' }
})
</script>
