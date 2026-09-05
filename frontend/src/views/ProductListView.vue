<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-red-600 mb-6">
      {{ categoryName || 'Productos' }}
    </h1>

    <div v-if="isLoading" class="text-gray-500">Cargando productos...</div>

    <div v-else-if="error" class="text-red-500 bg-red-100 p-4 rounded">
      Error: {{ error }}
    </div>

    <div v-else>
      <div
        v-for="product in products"
        :key="product.id"
        class="bg-white shadow-md rounded-lg p-4 mb-3 border-l-4 border-yellow-500 flex items-center"
      >
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
          class="w-20 h-20 object-cover rounded mr-4"
        />
        <div>
          <h2 class="text-xl font-semibold text-gray-800">{{ product.name }}</h2>
          <p v-if="product.description" class="text-gray-600 text-sm">
            {{ product.description }}
          </p>
          <p class="text-red-600 font-bold mt-1">S/. {{ product.price }}</p>
        </div>
      </div>

      <p v-if="products.length === 0" class="text-gray-400">
        No hay productos en esta categoría.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/axios'

const route = useRoute()
const products = ref([])
const categoryName = ref('')
const isLoading = ref(false)
const error = ref(null)

const fetchProducts = async () => {
  const slug = route.params.slug
  if (!slug) return

  isLoading.value = true
  error.value = null
  try {
    const response = await api.get(`products/?category=${slug}`)
    products.value = response.data
    if (products.value.length > 0) {
      categoryName.value = products.value[0].category_name
    } else {
      // Si no hay productos, podríamos obtener el nombre de la categoría de otra forma,
      // pero por ahora dejamos el nombre por defecto o vacío.
    }
  } catch (err) {
    error.value = err.message || 'Error al cargar productos'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchProducts()
})
</script>