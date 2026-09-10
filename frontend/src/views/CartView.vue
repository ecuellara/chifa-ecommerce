<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-red-600 mb-6">Tu carrito ({{ cartStore.totalItems }})</h1>

    <div v-if="cartStore.items.length === 0" class="text-gray-500">
      Carrito vacío.
      <router-link to="/" class="text-red-600 underline ml-2">Ver categorías</router-link>
    </div>

    <div v-else>
      <div
        v-for="item in cartStore.items"
        :key="item.id"
        class="bg-white shadow rounded-lg p-4 mb-3 flex items-center gap-4"
      >
        <img v-if="item.image" :src="item.image" :alt="item.name" loading="lazy" decoding="async" class="w-16 h-16 object-cover rounded" />
        <div class="flex-1">
          <h2 class="font-semibold">{{ item.name }}</h2>
          <p class="text-red-600 font-bold">S/. {{ item.price }} c/u</p>
          <p class="text-sm text-gray-600">Subtotal: S/. {{ (item.price * item.qty).toFixed(2) }}</p>
        </div>
        <div class="flex items-center gap-2">
          <button @click="cartStore.updateQty(item.id, item.qty - 1)" class="px-3 py-1 bg-gray-200 rounded">-</button>
          <span class="w-6 text-center font-bold">{{ item.qty }}</span>
          <button @click="cartStore.updateQty(item.id, item.qty + 1)" class="px-3 py-1 bg-gray-200 rounded">+</button>
        </div>
        <button @click="cartStore.removeItem(item.id)" class="text-sm text-red-500 underline">Quitar</button>
      </div>

      <div class="mt-6 border-t pt-4 flex justify-between items-center gap-3 flex-wrap">
        <p class="text-xl font-bold">Total: S/. {{ cartStore.subtotal.toFixed(2) }}</p>
        <div class="flex gap-3 items-center">
          <button @click="cartStore.clear()" class="text-sm text-gray-500 underline">Vaciar carrito</button>
          <router-link to="/checkout" class="bg-red-600 text-white px-6 py-3 rounded font-bold">Ir a pagar</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../stores/cartStore'
const cartStore = useCartStore()
</script>