<template>
  <div class="p-8 max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Crear cuenta</h1>
    <input v-model="u" placeholder="Usuario" class="w-full border p-2 rounded mb-2" />
    <input v-model="fn" placeholder="Nombre" class="w-full border p-2 rounded mb-2" />
    <input v-model="ln" placeholder="Apellido" class="w-full border p-2 rounded mb-2" />
    <input v-model="em" type="email" placeholder="Email" class="w-full border p-2 rounded mb-2" />
    <input v-model="ph" placeholder="Teléfono" class="w-full border p-2 rounded mb-2" />
    <input v-model="p" type="password" placeholder="Contraseña" class="w-full border p-2 rounded mb-2" />
    <p v-if="e" class="text-red-500 text-sm mb-2">{{ e }}</p>
    <button @click="doRegister" class="bg-red-600 text-white px-4 py-2 rounded w-full">Registrarse</button>
    <router-link to="/login" class="text-sm underline block mt-2">Iniciar sesión</router-link>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
const u = ref(''); const p = ref(''); const e = ref(''); const fn = ref(''); const ln = ref(''); const em = ref(''); const ph = ref('')
const auth = useAuthStore(); const route = useRoute(); const router = useRouter()
const doRegister = async () => {
  e.value = ''
  try { await auth.register({ username: u.value, password: p.value, first_name: fn.value, last_name: ln.value, email: em.value, phone: ph.value }); router.push(route.query.next || '/my-orders') }
  catch { e.value = 'Error al crear la cuenta.' }
}
</script>