// @ts-check
// Container override for the repo's playwright.config.js.
// The project pins @playwright/test 1.64.1 (wants chromium build 1248), but this
// container ships chromium 1243 at /opt/pw-browsers/chromium and has no Firefox/
// WebKit. This config reuses everything from the base config, keeps only the
// chromium project, and points it at the preinstalled binary.
//
// Run from the repo root:
//   pnpm exec playwright test -c .claude/skills/run-luxunos-tests/playwright.container.config.js --project=smoke
//   pnpm exec playwright test -c .claude/skills/run-luxunos-tests/playwright.container.config.js --project=chromium
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, devices } from '@playwright/test';
import base from '../../../playwright.config.js';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const executablePath = process.env.PW_CHROMIUM_PATH || '/opt/pw-browsers/chromium';

export default defineConfig({
  ...base,
  // Paths in a config resolve relative to the config file, so re-anchor them at the repo root.
  testDir: path.join(repoRoot, 'tests'),
  outputDir: path.join(repoRoot, 'test-results'),
  reporter: [['list'], ['html', { outputFolder: path.join(repoRoot, 'playwright-report'), open: 'never' }]],
  use: { ...base.use, screenshot: 'on' },
  projects: [
    // The repo's real tests (tests/*.spec.js). They hit https://playwright.dev.
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], launchOptions: { executablePath } },
    },
    // Offline smoke test that lives next to this config (no network needed).
    {
      name: 'smoke',
      testDir: path.dirname(fileURLToPath(import.meta.url)),
      use: { ...devices['Desktop Chrome'], launchOptions: { executablePath } },
    },
  ],
});
