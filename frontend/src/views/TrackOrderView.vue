<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold text-red-600 mb-6">Consultar pedido</h1>
    <div class="flex gap-2 mb-4">
      <input v-model="qid" placeholder="N° pedido" class="border p-2 rounded w-32" />
      <input v-model="qtel" placeholder="Teléfono" class="border p-2 rounded flex-1" />
      <button @click="buscar" class="bg-red-600 text-white px-4 rounded">Buscar</button>
    </div>
    <p v-if="error" class="text-red-500 bg-red-100 p-2 rounded mb-3">{{ error }}</p>
    <div v-if="order" class="bg-white shadow rounded p-4">
      <p class="font-bold">Pedido #{{ order.id }} — {{ order.estado }}</p>
      <div class="flex items-center mt-4 mb-2">
        <div v-for="(s, i) in steps" :key="s" class="flex items-center flex-1">
          <div :class="circleClass(i)" class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold">{{ i + 1 }}</div>
          <div v-if="i < steps.length - 1" :class="order.estado === 'cancelado' ? 'bg-red-300' : idx() >= i + 1 ? 'bg-green-500' : 'bg-gray-300'" class="h-1 flex-1 mx-1"></div>
        </div>
      </div>
      <div class="flex justify-between text-xs text-gray-600 mb-4">
        <span v-for="s in steps" :key="s" class="flex-1 text-center">{{ s }}</span>
      </div>
      <p>Total: S/. {{ order.total }} — {{ order.nombre }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/axios'

const qid = ref('')
const qtel = ref('')
const order = ref(null)
const error = ref('')
const steps = ['pendiente', 'confirmado', 'preparacion', 'camino', 'entregado']
const idx = () => steps.indexOf(order.value?.estado ?? 'pendiente')

const circleClass = (i) => {
  if (order.value?.estado === 'cancelado') return 'bg-red-500'
  return idx() >= i ? 'bg-green-500' : 'bg-gray-300'
}

const buscar = async () => {
  error.value = ''; order.value = null
  if (!qid.value || !qtel.value) { error.value = 'Indica N° y teléfono.'; return }
  try {
    const r = await api.get('orders/track/', { params: { id: qid.value, telefono: qtel.value } })
    order.value = r.data
  } catch (e) { error.value = 'No encontrado. Verifica N° y teléfono.' }
}
</script>