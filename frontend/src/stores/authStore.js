import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/axios'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('chifa_access') || '')
  const refresh = ref(localStorage.getItem('chifa_refresh') || '')
  const username = ref(localStorage.getItem('chifa_user') || '')

  const isLogged = ref(!!access.value)

  function saveTokens(a, r, u) {
    access.value = a || ''; refresh.value = r || ''; username.value = u || ''
    isLogged.value = !!a
    if (a) localStorage.setItem('chifa_access', a); else localStorage.removeItem('chifa_access')
    if (r) localStorage.setItem('chifa_refresh', r); else localStorage.removeItem('chifa_refresh')
    if (u) localStorage.setItem('chifa_user', u); else localStorage.removeItem('chifa_user')
  }

  async function login(usernameIn, password) {
    const r = await api.post('auth/login/', { username: usernameIn, password })
    saveTokens(r.data.access, r.data.refresh, usernameIn)
  }

  async function register(usernameIn, password) {
    await api.post('auth/register/', { username: usernameIn, password })
    await login(usernameIn, password)
  }

  function logout() { saveTokens('', '', '') }

  return { access, refresh, username, isLogged, login, register, logout, saveTokens }
})