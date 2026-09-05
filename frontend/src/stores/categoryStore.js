import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/axios'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchCategories = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.get('categories/')
      categories.value = response.data
    } catch (err) {
      error.value = err.message || 'Error al cargar categorías'
      console.error('Error fetching categories:', err)
    } finally {
      isLoading.value = false
    }
  }

  return { categories, isLoading, error, fetchCategories }
})