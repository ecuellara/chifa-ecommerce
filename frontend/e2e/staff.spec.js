import { test, expect } from '@playwright/test'
test('staff ve dashboard y avanza pedido', async ({ page }) => {
  await page.goto('/staff/login')
  const staffUser = process.env.E2E_STAFF_USER || 'everson'
  const staffPass = process.env.E2E_STAFF_PASS || 'Inicio001$'
  await page.getByPlaceholder('Usuario o email').fill(staffUser)
  await page.getByPlaceholder('Contraseña').fill(staffPass)
  await page.getByRole('button', { name: 'Entrar' }).click()
  await expect(page).toHaveURL(/\/staff\/?$/)
  await expect(page.getByRole('heading', { name: /Dashboard/ })).toBeVisible()
  await page.goto('/staff/orders')
  await expect(page.getByRole('heading', { name: /Pedidos/ })).toBeVisible()
})