<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Mis pedidos</h1>
    <div v-if="!list.length" class="text-gray-500">Sin pedidos.</div>
    <div v-for="o in list" :key="o.id" class="border p-3 rounded mb-2 flex justify-between">
      <span>#{{ o.id }} — S/. {{ o.total }} — {{ o.estado }}</span>
      <router-link :to="`/order/${o.id}/success`" class="underline text-red-600">Ver</router-link>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/axios'
const list = ref([])
onMounted(async () => { const r = await api.get('my-orders/'); list.value = r.data })
</script>