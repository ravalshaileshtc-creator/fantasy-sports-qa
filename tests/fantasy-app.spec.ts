import { test, expect } from '@playwright/test';

test('home page', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('body')).toBeVisible();
});

test('contest page', async ({ page }) => {
  await page.goto('/contests');
  await expect(page.locator('body')).toBeVisible();
});

test('rewards page', async ({ page }) => {
  await page.goto('/rewards');
  await expect(page.locator('body')).toBeVisible();
});

test('wallet page', async ({ page }) => {
  await page.goto('/wallet');
  await expect(page.locator('body')).toBeVisible();
});

test('mobile responsive', async ({ page }) => {
  await page.setViewportSize({
    width: 390,
    height: 844
  });

  await page.goto('/');

  await page.screenshot({
    path: 'mobile-home.png',
    fullPage: true
  });
});
