<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-red-600 mb-6">Nuestras Categorías</h1>

    <!-- Estado de carga -->
    <div v-if="categoryStore.isLoading" class="text-gray-500">
      Cargando categorías...
    </div>

    <!-- Error -->
    <div v-else-if="categoryStore.error" class="text-red-500 bg-red-100 p-4 rounded">
      Error: {{ categoryStore.error }}
    </div>

    <!-- Lista de categorías -->
    <div v-for="category in categoryStore.categories" :key="category.id"
      class="bg-white shadow-md rounded-lg p-4 mb-3 border-l-4 border-red-500 hover:shadow-lg transition cursor-pointer">
      <router-link :to="`/categoria/${category.slug}`" class="block">
        <h2 class="text-xl font-semibold text-gray-800">{{ category.name }}</h2>
        <p v-if="category.description" class="text-gray-600 text-sm">
          {{ category.description }}
        </p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCategoryStore } from '../stores/categoryStore'

const categoryStore = useCategoryStore()

onMounted(() => {
  categoryStore.fetchCategories()
})
</script>