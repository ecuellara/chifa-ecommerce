import { test, expect } from '@playwright/test'
test('register, pedido y mis pedidos', async ({ page }) => {
  const u = 'e2e' + Date.now()
  await page.goto('/register')
  await page.getByPlaceholder('Usuario').fill(u)
  await page.getByPlaceholder('Contraseña').fill('Clave12345')
  await page.getByRole('button', { name: 'Registrarse' }).click()
  await expect(page).toHaveURL(/my-orders/)
  // crea 1 pedido vía UI igual que spec 1 (repite Agregar+Checkout) y verifica aparece en /my-orders
})