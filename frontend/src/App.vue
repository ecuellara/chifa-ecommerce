<template>
  <div id="app" class="min-h-screen flex flex-col">
    <AppHeader v-if="!$route.path.startsWith('/staff')" />
    <router-view class="flex-1" />
    <AppFooter v-if="!$route.path.startsWith('/staff')" />
  </div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>