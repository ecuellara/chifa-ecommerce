import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/axios'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('chifa_access') || '')
  const refresh = ref(localStorage.getItem('chifa_refresh') || '')
  const username = ref(localStorage.getItem('chifa_user') || '')
  const firstName = ref(localStorage.getItem('chifa_first') || '')
  const lastName = ref(localStorage.getItem('chifa_last') || '')
  const email = ref(localStorage.getItem('chifa_email') || '')
  const phone = ref(localStorage.getItem('chifa_phone') || '')
  const isLogged = ref(!!access.value)

  function persistProfile(p) {
    firstName.value = p.first_name || ''; lastName.value = p.last_name || ''
    email.value = p.email || ''; phone.value = p.phone || ''
    username.value = p.username || username.value
    localStorage.setItem('chifa_first', firstName.value)
    localStorage.setItem('chifa_last', lastName.value)
    localStorage.setItem('chifa_email', email.value)
    localStorage.setItem('chifa_phone', phone.value)
    localStorage.setItem('chifa_user', username.value)
  }

  function saveTokens(a, r, u) {
    access.value = a || ''; refresh.value = r || ''
    isLogged.value = !!a
    if (a) localStorage.setItem('chifa_access', a); else localStorage.removeItem('chifa_access')
    if (r) localStorage.setItem('chifa_refresh', r); else localStorage.removeItem('chifa_refresh')
    if (u) { username.value = u; localStorage.setItem('chifa_user', u) }
  }

  async function fetchMe() {
    if (!access.value) return
    try { const r = await api.get('auth/me/'); persistProfile(r.data) } catch {}
  }

  async function login(identifier, password) {
    const r = await api.post('auth/login/', { username: identifier, password })
    saveTokens(r.data.access, r.data.refresh, identifier.includes('@') ? '' : identifier)
    await fetchMe()
    if (!username.value) username.value = identifier
  }

  async function register(payload) {
    await api.post('auth/register/', payload)
    await login(payload.username, payload.password)
  }

  function logout() {
    saveTokens('', '', ''); persistProfile({})
    ;['chifa_access','chifa_refresh','chifa_user','chifa_first','chifa_last','chifa_email','chifa_phone'].forEach(k=>localStorage.removeItem(k))
    firstName.value=''; lastName.value=''; email.value=''; phone.value=''; username.value=''
  }

  if (access.value) fetchMe()
  return { access, refresh, username, firstName, lastName, email, phone, isLogged, login, register, logout, fetchMe }
})