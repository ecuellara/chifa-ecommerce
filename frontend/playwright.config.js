import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:5173', trace: 'on-first-retry', channel: 'chrome' },
  webServer: undefined, // tú ya corres dev 5173 + Django 8000 a mano
})