<template>
  <div class="p-8 max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-4">Acceso personal</h1>
    <input v-model="u" placeholder="Usuario o email" class="w-full border p-2 rounded mb-2" />
    <input v-model="p" type="password" placeholder="Contraseña" class="w-full border p-2 rounded mb-2" />
    <p v-if="e" class="text-red-500 text-sm mb-2">{{ e }}</p>
    <button @click="doLogin" class="bg-black text-white px-4 py-2 rounded w-full">Entrar</button>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
const u = ref(''); const p = ref(''); const e = ref('')
const auth = useAuthStore(); const router = useRouter()
const doLogin = async () => {
  e.value = ''
  try {
    await auth.login(u.value, p.value)
    if (!auth.isStaff) { e.value = 'Sin permiso de personal.'; auth.logout(); return }
    router.push('/staff')
  } catch { e.value = 'Credenciales inválidas.' }
}
</script>