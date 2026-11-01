// @ts-check
// Offline smoke test: proves the container's Playwright + chromium wiring works
// without touching the network (playwright.dev is blocked in some sandboxes).
// It renders the redstone song plan produced by the minecraft-redstone skill's
// script into a page, checks it, and saves a screenshot.
//
// Run from the repo root:
//   pnpm exec playwright test -c .claude/skills/run-luxunos-tests/playwright.container.config.js --project=smoke
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const skill = path.join(repoRoot, 'skills/minecraft-redstone');

test('offline smoke: render redstone song plan', async ({ page }, testInfo) => {
  const plan = execFileSync(
    'python3',
    ['scripts/cancion_a_redstone.py', 'assets/himno-de-la-alegria.txt', '--ticks-por-paso', '2'],
    { cwd: skill, encoding: 'utf8' },
  );
  const escaped = plan.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  await page.setContent(
    `<!doctype html><meta charset="utf-8"><title>Redstone smoke</title>
     <body style="font:13px monospace;background:#111;color:#eee;padding:16px">
     <h1>Smoke test</h1><pre id="plan">${escaped}</pre></body>`,
  );
  await expect(page).toHaveTitle('Redstone smoke');
  await expect(page.locator('#plan')).toContainText('CIRCUITO MUSICAL CON PALANCA');
  await expect(page.locator('#plan')).toContainText('30 bloques musicales');
  const shot = testInfo.outputPath('smoke.png');
  await page.screenshot({ path: shot, fullPage: true });
  console.log(`screenshot: ${shot}`);
});
