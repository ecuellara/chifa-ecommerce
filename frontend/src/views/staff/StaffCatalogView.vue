<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Catálogo</h1>
    <div class="flex gap-2 mb-4">
      <button @click="tab = 'products'" :class="tab === 'products' ? 'bg-black text-white' : 'border'" class="px-3 py-1 rounded">Productos</button>
      <button @click="tab = 'categories'" :class="tab === 'categories' ? 'bg-black text-white' : 'border'" class="px-3 py-1 rounded">Categorías</button>
      <button @click="tab = 'zones'" :class="tab === 'zones' ? 'bg-black text-white' : 'border'" class="px-3 py-1 rounded">Zonas</button>
    </div>
    <p v-if="error" class="text-red-500 bg-red-100 p-2 rounded mb-3">{{ error }}</p>

    <div v-if="tab === 'products'">
      <div v-for="p in products" :key="p.id" class="bg-white shadow rounded p-3 mb-2 flex justify-between items-center gap-3">
        <div>
          <p class="font-bold">{{ p.name }} — S/. {{ p.price }}</p>
          <p class="text-xs text-gray-500">{{ p.is_active ? 'activo' : 'inactivo' }}{{ p.is_featured ? ' · destacado' : '' }}</p>
        </div>
        <div class="flex gap-2 items-center">
          <input v-model.number="edits[p.id]" type="number" step="0.01" class="border p-1 rounded w-24" placeholder="precio" />
          <button @click="savePrice(p)" class="text-xs border px-2 py-1 rounded">Precio</button>
          <button @click="toggle(p, 'products')" class="text-xs border px-2 py-1 rounded">{{ p.is_active ? 'Desactivar' : 'Activar' }}</button>
        </div>
      </div>
    </div>

    <div v-if="tab === 'categories'">
      <div v-for="c in categories" :key="c.id" class="bg-white shadow rounded p-3 mb-2 flex justify-between">
        <span>{{ c.name }} ({{ c.is_active ? 'activa' : 'inactiva' }})</span>
        <button @click="toggle(c, 'categories')" class="text-xs border px-2 py-1 rounded">Activar/Desactivar</button>
      </div>
    </div>

    <div v-if="tab === 'zones'">
      <div v-for="z in zones" :key="z.id" class="bg-white shadow rounded p-3 mb-2 flex justify-between items-center gap-3">
        <span>{{ z.name }} — S/. {{ z.cost }}{{ z.free_over ? ` (gratis desde ${z.free_over})` : '' }}</span>
        <div class="flex gap-2 items-center">
          <input v-model.number="zEdits[z.id]" type="number" step="0.01" class="border p-1 rounded w-24" placeholder="costo" />
          <button @click="saveCost(z)" class="text-xs border px-2 py-1 rounded">Costo</button>
          <button @click="toggle(z, 'zones')" class="text-xs border px-2 py-1 rounded">{{ z.is_active ? 'Desactivar' : 'Activar' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/axios'

const tab = ref('products')
const products = ref([])
const categories = ref([])
const zones = ref([])
const edits = ref({})
const zEdits = ref({})
const error = ref('')

const cargar = async () => {
  error.value = ''
  try {
    const [p, c, z] = await Promise.all([
      api.get('staff/products/'),
      api.get('staff/categories/'),
      api.get('staff/zones/'),
    ])
    products.value = p.data
    categories.value = c.data
    zones.value = z.data
  } catch { error.value = 'No se pudo cargar (¿eres staff?).' }
}

const toggle = async (item, kind) => {
  const url = kind === 'products' ? `staff/products/${item.id}/` : kind === 'categories' ? `staff/categories/${item.id}/` : `staff/zones/${item.id}/`
  try {
    const r = await api.patch(url, { is_active: !item.is_active })
    Object.assign(item, r.data)
  } catch { error.value = 'No se pudo cambiar estado.' }
}

const savePrice = async (p) => {
  const v = edits.value[p.id]
  if (v == null || v < 0) { error.value = 'Precio inválido.'; return }
  try {
    const r = await api.patch(`staff/products/${p.id}/`, { price: v })
    Object.assign(p, r.data)
  } catch { error.value = 'No se pudo guardar precio.' }
}

const saveCost = async (z) => {
  const v = zEdits.value[z.id]
  if (v == null || v < 0) { error.value = 'Costo inválido.'; return }
  try {
    const r = await api.patch(`staff/zones/${z.id}/`, { cost: v })
    Object.assign(z, r.data)
  } catch { error.value = 'No se pudo guardar costo.' }
}

onMounted(cargar)
</script>
