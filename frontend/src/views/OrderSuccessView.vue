<template>
  <div class="p-8 max-w-2xl mx-auto text-center">
    <div v-if="loading" class="text-gray-500">Cargando pedido...</div>
    <div v-else-if="error" class="text-red-500 bg-red-100 p-4 rounded">{{ error }}</div>
    <div v-else-if="order">
      <h1 class="text-3xl font-bold text-green-600 mb-2">¡Pedido confirmado!</h1>
      <p class="text-lg">Pedido #{{ order.id }} — {{ order.estado }}</p>
      <router-link :to="'/track'" class="text-sm underline text-red-600">Consultar / guardar N° para seguimiento</router-link>
      <p class="mt-2">{{ order.nombre }} ({{ order.telefono }})</p>
      <p v-if="order.tipo_entrega === 'delivery'">Delivery: {{ order.direccion }} — {{ order.zona_name }}</p>
      <p v-else>Recojo en tienda</p>
      <div class="mt-4 text-left bg-white shadow rounded p-4">
        <div v-for="(it, i) in order.items" :key="i" class="flex justify-between text-sm">
          <span>{{ it.qty }} x {{ it.product_name }}</span>
          <span>S/. {{ it.subtotal }}</span>
        </div>
        <div class="border-t mt-2 pt-2">
          <p>Subtotal: S/. {{ order.subtotal }}</p>
          <p>Delivery: S/. {{ order.delivery_cost }}</p>
          <p class="font-bold text-lg">Total: S/. {{ order.total }}</p>
        </div>
      </div>
      <router-link to="/" class="inline-block mt-6 bg-red-600 text-white px-6 py-3 rounded font-bold">Volver al inicio</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/axios'

const route = useRoute()
const order = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const r = await api.get(`orders/${route.params.id}/`)
    order.value = r.data
  } catch (e) { error.value = 'No se encontró el pedido.' }
  finally { loading.value = false }
})
</script>