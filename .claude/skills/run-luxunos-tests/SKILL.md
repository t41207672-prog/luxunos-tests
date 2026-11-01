---
name: run-luxunos-tests
description: Run, test, smoke-test and screenshot the luxunos-tests repo - its Playwright suite (tests/*.spec.js) and the minecraft-redstone song-to-circuit CLI (skills/minecraft-redstone/scripts/cancion_a_redstone.py). Use when asked to run the Playwright tests, run/verify the redstone script, take a screenshot, or check that a change to either works.
---

This repo has two runnable things: a **Playwright test suite** (`tests/`, driven by
`pnpm exec playwright test`) and the **`cancion_a_redstone.py` CLI** inside the
`minecraft-redstone` skill. Drive both through the harness in this directory:
`smoke.sh` (CLI) and `playwright.container.config.js` + `smoke.spec.js` (browser).
All paths are relative to the repo root.

## Prerequisites

Nothing to apt-get: the container already has Node 22, pnpm, python3 and Chromium
at `/opt/pw-browsers/chromium`. **Do not run `playwright install`** (see Gotchas).

## Setup

```bash
pnpm install
```

## Run (agent path)

**1. CLI smoke test** (redstone script - most changes to `skills/` land here):

```bash
bash .claude/skills/run-luxunos-tests/smoke.sh
# -> 7 "ok" lines, then: ALL OK (logs in /tmp/redstone-smoke)
```

It runs the example song, chords/percussion/solfège, `--mcfunction`/`--json` output,
`--transponer-auto`, and the two error paths (exit 1). Per-case logs and the generated
`musica.mcfunction` / `diseno.json` land in `/tmp/redstone-smoke/` (or pass a dir as `$1`).

Direct invocation for a single song:

```bash
cd skills/minecraft-redstone
python3 scripts/cancion_a_redstone.py -c "E4:2 E4:2 F4:2 G4:2 C4+E4+G4:4" --ticks-por-paso 2
python3 scripts/cancion_a_redstone.py assets/himno-de-la-alegria.txt --mcfunction /tmp/himno.mcfunction
```

**2. Browser smoke test + screenshot** (offline; proves Playwright/Chromium work):

```bash
pnpm exec playwright test -c .claude/skills/run-luxunos-tests/playwright.container.config.js --project=smoke
# -> 1 passed; prints "screenshot: .../test-results/smoke-.../smoke.png"
```

It renders the redstone plan into a page, asserts on it and writes
`test-results/smoke-offline-smoke-render-redstone-song-plan-smoke/smoke.png`. Open the PNG to check it.

## Test (the repo's real Playwright suite)

```bash
pnpm exec playwright test -c .claude/skills/run-luxunos-tests/playwright.container.config.js --project=chromium
```

The two tests in `tests/example.spec.js` load `https://playwright.dev`. In this sandbox
that host is **blocked by the network policy**, so both fail with
`net::ERR_TUNNEL_CONNECTION_FAILED` (a failure screenshot is still saved under
`test-results/`). They pass only when the environment allows `playwright.dev`.
Results: list output in the terminal, HTML report in `playwright-report/`.

## Run (human path)

`pnpm exec playwright test` with the repo's own `playwright.config.js` is what CI
(`.github/workflows/playwright.yml`) runs after `playwright install --with-deps`. It runs
chromium + firefox + webkit. It does not work in this container (see Gotchas).

## Gotchas

- **Browser build mismatch.** `@playwright/test` 1.64.1 wants
  `chromium_headless_shell-1248`; the container ships build **1243**. Plain
  `pnpm exec playwright test` fails with `Executable doesn't exist at
  /opt/pw-browsers/chromium_headless_shell-1248/...`. The container config fixes this by
  setting `launchOptions.executablePath` to `/opt/pw-browsers/chromium` (override it with
  `PW_CHROMIUM_PATH`). Don't `playwright install`: it downloads a browser the rest of the
  container won't find, and the download host is likely blocked anyway.
- **No Firefox/WebKit** in the container, so the container config keeps only `chromium`
  (+ `smoke`).
- **Config paths resolve relative to the config file.** The override config lives three
  levels down, so it re-anchors `testDir`, `outputDir` and the HTML report at the repo root.
  A spec outside `testDir` gives `Error: No tests found.`; that's why the smoke spec has its own
  `smoke` project with `testDir` set to this directory.
- **The base config's only reporter is `html`**, which prints just the failure summary.
  The container config adds `list` so each test and its error show in the terminal.
- **Every `playwright test` run empties `test-results/`**, including runs of the other project.
  Copy `smoke.png` somewhere else before running the suite again.
- **`--transponer-auto` tries +12, -12, +24, -24...**, so `C9` lands on `Do7` (Campana),
  not `Do8`.

## Troubleshooting

- **`page.goto: net::ERR_TUNNEL_CONNECTION_FAILED at https://playwright.dev/`**: the egress
  proxy denies `playwright.dev` (403; see `curl -sS "$HTTPS_PROXY/__agentproxy/status"`,
  `recentRelayFailures`). Add the host to the environment's allowed domains. Don't mock it.
- **`Executable doesn't exist at /opt/pw-browsers/chromium_headless_shell-1248/...`**: you ran
  without `-c .claude/skills/run-luxunos-tests/playwright.container.config.js`.
