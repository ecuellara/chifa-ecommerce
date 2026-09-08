<template>
  <div class="p-8 max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Iniciar sesión</h1>
    <input v-model="u" placeholder="Usuario" class="w-full border p-2 rounded mb-2" />
    <input v-model="p" type="password" placeholder="Contraseña" class="w-full border p-2 rounded mb-2" />
    <p v-if="e" class="text-red-500 text-sm mb-2">{{ e }}</p>
    <button @click="doLogin" class="bg-red-600 text-white px-4 py-2 rounded w-full">Entrar</button>
    <router-link to="/register" class="text-sm underline block mt-2">Crear cuenta</router-link>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
const u = ref(''); const p = ref(''); const e = ref('')
const auth = useAuthStore(); const route = useRoute(); const router = useRouter()
const doLogin = async () => {
  e.value = ''
  try { await auth.login(u.value, p.value); router.push(route.query.next || '/my-orders') }
  catch { e.value = 'Credenciales inválidas.' }
}
</script>