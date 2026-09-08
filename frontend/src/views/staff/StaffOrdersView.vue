<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Pedidos</h1>
    <div class="flex gap-2 mb-3">
      <select v-model="filtro" @change="cargar" class="border p-2 rounded">
        <option value="">Todos</option>
        <option v-for="s in estados" :key="s" :value="s">{{ s }}</option>
      </select>
      <button @click="cargar" class="border px-3 rounded">Recargar</button>
      <span class="text-xs text-gray-500 self-center">Auto cada 30s</span>
    </div>
    <p v-if="error" class="text-red-500 bg-red-100 p-2 rounded mb-3">{{ error }}</p>
    <div v-for="o in orders" :key="o.id" class="bg-white shadow rounded p-3 mb-2">
      <div class="flex justify-between">
        <span class="font-bold">#{{ o.id }} — {{ o.nombre }} — S/. {{ o.total }}</span>
        <span class="text-sm">{{ o.estado }} ({{ o.tipo_entrega }})</span>
      </div>
      <p class="text-xs text-gray-600">{{ o.telefono }} — {{ o.direccion || 'recojo' }} · {{ o.metodo_pago }}</p>
      <div class="flex gap-2 mt-2 flex-wrap">
        <button
          v-for="nxt in siguientes(o.estado)"
          :key="nxt"
          @click="avanzar(o, nxt)"
          class="text-xs bg-black text-white px-3 py-1 rounded"
        >
          → {{ nxt }}
        </button>
      </div>
    </div>
    <p v-if="!orders.length" class="text-gray-500">Sin pedidos.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../../services/axios'

const estados = ['pendiente', 'confirmado', 'preparacion', 'camino', 'entregado', 'cancelado']
const TRANS = {
  pendiente: ['confirmado', 'cancelado'],
  confirmado: ['preparacion', 'cancelado'],
  preparacion: ['camino', 'cancelado'],
  camino: ['entregado'],
  entregado: [],
  cancelado: [],
}
const filtro = ref('')
const orders = ref([])
const error = ref('')
let timer = null

const siguientes = (est) => TRANS[est] || []

const cargar = async () => {
  error.value = ''
  try {
    const r = await api.get('staff/orders/', { params: filtro.value ? { estado: filtro.value } : {} })
    orders.value = r.data
  } catch { error.value = 'No se pudo cargar (¿eres staff?).' }
}

const avanzar = async (o, nuevo) => {
  try {
    const r = await api.patch(`staff/orders/${o.id}/`, { estado: nuevo })
    const i = orders.value.findIndex((x) => x.id === o.id)
    if (i >= 0) orders.value[i] = r.data
  } catch (e) {
    error.value = e.response?.data?.estado || 'Transición inválida.'
  }
}

onMounted(() => {
  cargar()
  timer = setInterval(cargar, 30000)
})
onUnmounted(() => clearInterval(timer))
</script>
