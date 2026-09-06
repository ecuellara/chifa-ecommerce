import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'chifa_cart_v1'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  // 1. Cargar al arrancar: lee texto y convierte a array
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) items.value = JSON.parse(raw)
  } catch (e) {
    console.warn('Carrito corrupto, se reinicia', e)
    items.value = []
  }

  // 2. Persistir cada cambio
  watch(items, (val) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
  }, { deep: true })

  const totalItems = computed(() =>
    items.value.reduce((acc, it) => acc + it.qty, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((acc, it) => acc + Number(it.price) * it.qty, 0)
  )

  function addItem(product, qty = 1) {
    const found = items.value.find((it) => it.id === product.id)
    if (found) {
      found.qty += qty
    } else {
      items.value.push({
        id: product.id,
        name: product.name,
        price: Number(product.price),
        image: product.image,
        qty,
      })
    }
  }

  function updateQty(id, qty) {
    const found = items.value.find((it) => it.id === id)
    if (!found) return
    if (qty <= 0) removeItem(id)
    else found.qty = qty
  }

  function removeItem(id) {
    items.value = items.value.filter((it) => it.id !== id)
  }

  function clear() {
    items.value = []
  }

  return { items, totalItems, subtotal, addItem, updateQty, removeItem, clear }
})