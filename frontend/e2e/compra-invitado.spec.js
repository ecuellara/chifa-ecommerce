import { test, expect } from '@playwright/test'
test('invitado compra y ve success', async ({ page, request }) => {
  const cats = await (await request.get('http://127.0.0.1:8000/api/categories/')).json()
  const cat = Array.isArray(cats) ? cats[0] : cats.results[0]
  await page.goto(`/categoria/${cat.slug}`)
  await page.getByRole('button', { name: 'Agregar' }).first().click()
  await page.goto('/cart')
  await expect(page.getByText(/^Total:/)).toBeVisible()
  await page.goto('/checkout')
  await page.getByPlaceholder('Nombre').fill('E2E Invitado')
  await page.getByPlaceholder('Teléfono').fill('999111222')
  const zonas = await (await request.get('http://127.0.0.1:8000/api/zones/')).json()
  const z = Array.isArray(zonas) ? zonas[0] : zonas.results[0]
  await page.locator('select').selectOption(String(z.id))
  await page.getByPlaceholder('Dirección').fill('Av Test 123')
  await page.getByRole('button', { name: 'Confirmar pedido' }).click()
  await expect(page).toHaveURL(/\/order\/\d+\/success/)
  await expect(page.getByText('¡Pedido confirmado!')).toBeVisible()
})