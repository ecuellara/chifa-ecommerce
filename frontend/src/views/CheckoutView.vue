<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold text-red-600 mb-6">Checkout</h1>

    <div v-if="cartStore.items.length === 0" class="text-gray-500">
      Tu carrito está vacío. <router-link to="/" class="underline text-red-600">Volver</router-link>
    </div>

    <div v-else class="space-y-4">
      <div class="flex gap-2">
        <button @click="tipo = 'delivery'" :class="tipo === 'delivery' ? 'bg-red-600 text-white' : 'bg-gray-200'" class="px-4 py-2 rounded">Delivery</button>
        <button @click="tipo = 'recojo'" :class="tipo === 'recojo' ? 'bg-red-600 text-white' : 'bg-gray-200'" class="px-4 py-2 rounded">Recojo</button>
      </div>

      <input v-model="nombre" placeholder="Nombre" class="w-full border p-2 rounded" />
      <input v-model="telefono" placeholder="Teléfono" class="w-full border p-2 rounded" />

      <div v-if="tipo === 'delivery'" class="space-y-2">
        <select v-model="zona_id" class="w-full border p-2 rounded">
          <option :value="null">Elige zona...</option>
          <option v-for="z in zonas" :key="z.id" :value="z.id">{{ z.name }} - S/. {{ z.cost }}</option>
        </select>
        <input v-model="direccion" placeholder="Dirección" class="w-full border p-2 rounded" />
        <input v-model="referencia" placeholder="Referencia (opcional)" class="w-full border p-2 rounded" />
      </div>

      <div class="space-y-1">
        <label><input type="radio" value="efectivo" v-model="metodo_pago" /> Efectivo</label><br />
        <label><input type="radio" value="yape" v-model="metodo_pago" /> Yape/Plin (placeholder)</label><br />
        <label><input type="radio" value="tarjeta" v-model="metodo_pago" /> Tarjeta (placeholder)</label>
      </div>

      <div class="border-t pt-3">
        <p>Subtotal: S/. {{ cartStore.subtotal.toFixed(2) }}</p>
        <p>Delivery: S/. {{ deliveryCost }}</p>
        <p class="font-bold">Total aprox: S/. {{ (cartStore.subtotal + Number(deliveryCost)).toFixed(2) }}</p>
        <p class="text-xs text-gray-500">Total final lo calcula el backend.</p>
      </div>

      <p v-if="error" class="text-red-500 bg-red-100 p-2 rounded">{{ error }}</p>

      <button @click="confirmar" :disabled="loading" class="bg-red-600 text-white px-6 py-3 rounded font-bold">
        {{ loading ? 'Enviando...' : 'Confirmar pedido' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/axios'
import { useCartStore } from '../stores/cartStore'
import { useAuthStore } from '../stores/authStore'

const cartStore = useCartStore()
const router = useRouter()
const authStore = useAuthStore()

const tipo = ref('delivery')
const nombre = ref('')
const telefono = ref('')
const zona_id = ref(null)
const direccion = ref('')
const referencia = ref('')
const metodo_pago = ref('efectivo')
const zonas = ref([])
const loading = ref(false)
const error = ref('')

const deliveryCost = computed(() => {
  if (tipo.value !== 'delivery' || !zona_id.value) return '0.00'
  const z = zonas.value.find((x) => x.id === zona_id.value)
  return z ? String(z.cost) : '0.00'
})

onMounted(async () => {  
  try {
    if (authStore.isLogged && authStore.username && !nombre.value) nombre.value = authStore.username
    const r = await api.get('zones/')
    zonas.value = Array.isArray(r.data) ? r.data : r.data.results || []
  } catch (e) { error.value = 'No se pudieron cargar zonas.' }
})

const confirmar = async () => {
  error.value = ''
  if (!nombre.value.trim() || !telefono.value.trim()) { error.value = 'Nombre y teléfono obligatorios.'; return }
  if (tipo.value === 'delivery' && !zona_id.value) { error.value = 'Elige zona.'; return }
  if (tipo.value === 'delivery' && !direccion.value.trim()) { error.value = 'Dirección obligatoria.'; return }

  loading.value = true
  try {
    const payload = {
      tipo_entrega: tipo.value,
      nombre: nombre.value, telefono: telefono.value,
      zona_id: tipo.value === 'delivery' ? zona_id.value : null,
      direccion: tipo.value === 'delivery' ? direccion.value : '',
      referencia: referencia.value,
      metodo_pago: metodo_pago.value,
      items: cartStore.items.map((it) => ({ product_id: it.id, qty: it.qty })),
    }
    const r = await api.post('orders/', payload)
    cartStore.clear()
    router.push(`/order/${r.data.id}/success`)
  } catch (e) {
    error.value = e.response?.data?.detail || JSON.stringify(e.response?.data) || 'Error al crear pedido.'
  } finally { loading.value = false }
}
</script>