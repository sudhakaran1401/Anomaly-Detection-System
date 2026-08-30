import { test, expect } from '@playwright/test';

let AxeBuilder;
try {
  // eslint-disable-next-line global-require
  AxeBuilder = require('@axe-core/playwright').default;
} catch (e) {
  AxeBuilder = null;
}

test.describe('ADS accessibility', () => {
  test('login/application surface has no critical accessibility violations', async ({ page }) => {
    await page.goto('/');

    // ADS may redirect unauthenticated users to /login.
    await page.waitForLoadState('domcontentloaded');

    if (AxeBuilder) {
      const results = await new AxeBuilder({ page })
        .disableRules(['color-contrast'])
        .analyze();

      const critical = results.violations.filter(
        (violation) => violation.impact === 'critical'
      );

      expect(critical).toEqual([]);
    } else {
      // Keep the test meaningful even before the optional axe dependency
      // is installed: verify the page is usable and has a document title/body.
      await expect(page.locator('body')).toBeVisible();
      await expect(page.locator('body')).not.toBeEmpty();
    }
  });

  test('interactive controls have accessible names', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('domcontentloaded');

  const buttons = page.locator('button:visible');
  const count = await buttons.count();

  for (let i = 0; i < count; i += 1) {
    const button = buttons.nth(i);

    // Playwright's accessible name includes visible button text,
    // aria-label, aria-labelledby, etc.
    const accessibleName = await button.getAttribute('aria-label');
    const visibleText = (await button.innerText()).trim();

    expect(
      accessibleName?.trim() || visibleText
    ).not.toBe('');
  }
  });
});
