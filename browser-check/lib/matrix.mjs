// Tryb matrix: viewport x motyw x trasa -> zrzut ekranu + błędy konsoli/sieci.
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { describeTarget, toLocator } from './locators.mjs';
import { maskText, maskUrl } from './mask.mjs';
import { ensureTheme, openPage, waitForReady } from './session.mjs';

function firstLine(error) {
  return String(error?.message ?? error).split('\n')[0].trim();
}

function stripTrailingSlash(pathname) {
  return pathname.length > 1 ? pathname.replace(/\/+$/, '') : pathname;
}

async function runStep(page, scenario, route, step) {
  const timeout = route.timeoutMs ?? 5000;
  switch (step.action) {
    case 'click':
      await toLocator(page, step.target).first().click({ timeout });
      break;
    case 'fill':
      await toLocator(page, step.target).first().fill(step.value, { timeout });
      break;
    case 'press':
      if (step.target) await toLocator(page, step.target).first().press(step.value, { timeout });
      else await page.keyboard.press(step.value);
      break;
    case 'wait':
      if (step.target) await toLocator(page, step.target).first().waitFor({ state: 'visible', timeout });
      else await page.waitForTimeout(step.ms);
      break;
  }
  await page.waitForTimeout(scenario.settleMs);
}

function describeStep(step, index) {
  const target = step.target ? ` ${describeTarget(step.target)}` : '';
  return `step ${index + 1} (${step.action}${target})`;
}

async function captureShot({ page, collector, scenario, outDir, route, viewport, theme }) {
  const startedAt = Date.now();
  const file = path.join(outDir, `${route.name}__${viewport.name}__${theme}.png`);
  const shot = {
    route: route.name,
    path: route.path,
    viewport: viewport.name,
    theme,
    ok: true,
    file,
    href: null,
    redirected: false,
    durationMs: 0,
    themeEvidence: null,
    consoleErrors: [],
    pageErrors: [],
    failedRequests: [],
    dialogs: [],
    warnings: [],
  };
  let failure = null;
  let navigated = false;
  collector.drain(); // zdarzenia spóźnione z poprzedniej strony nie należą do tego zrzutu

  try {
    await page.goto(new URL(route.path, scenario.baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await waitForReady(page, scenario, route);
    navigated = true;
    shot.themeEvidence = await ensureTheme(page, scenario, theme, route, viewport.name);
    for (const [index, step] of route.steps.entries()) {
      try {
        await runStep(page, scenario, route, step);
      } catch (error) {
        if (step.optional) {
          shot.warnings.push(`${describeStep(step, index)}: ${firstLine(error)}`);
        } else {
          throw new Error(`${describeStep(step, index)}: ${firstLine(error)}`);
        }
      }
    }
  } catch (error) {
    failure = firstLine(error); // zrzut stanu i tak powstaje jako dowód
  }

  try {
    shot.href = await page.evaluate(() => location.href);
  } catch {
    shot.href = page.url();
  }
  try {
    await page.screenshot({ path: file, fullPage: route.fullPage ?? false });
  } catch (error) {
    failure = failure ?? `screenshot: ${firstLine(error)}`;
  }

  // Przekierowanie ma sens tylko po udanej nawigacji; przy błędzie goto/waitForReady adres jest przypadkowy.
  if (navigated) {
    try {
      const expected = stripTrailingSlash(new URL(route.path, scenario.baseUrl).pathname);
      const actual = stripTrailingSlash(new URL(shot.href).pathname);
      shot.redirected = expected !== actual;
    } catch {
      shot.redirected = false;
    }
  }

  Object.assign(shot, collector.drain());
  // Do raportu i stdout trafiają tylko zamaskowane: adres i komunikaty mogą nieść dane osobowe (konsolę i sieć maskuje kolektor).
  shot.href = maskUrl(scenario, shot.href);
  shot.warnings = shot.warnings.map((text) => maskText(scenario, text));
  if (failure) {
    shot.ok = false;
    shot.error = maskText(scenario, failure);
  }
  shot.durationMs = Date.now() - startedAt;
  return shot;
}

function formatLine(shot) {
  const seconds = (shot.durationMs / 1000).toFixed(1);
  const relative = path.relative(process.cwd(), shot.file);
  const file = relative.startsWith('..') || path.isAbsolute(relative) ? shot.file : relative;
  let line =
    `SHOT ${shot.ok ? 'ok  ' : 'FAIL'} ${shot.route} ${shot.viewport}/${shot.theme} ${seconds}s  ${file}` +
    `  console:${shot.consoleErrors.length} net:${shot.failedRequests.length}`;
  if (shot.pageErrors.length > 0) line += ` pageerr:${shot.pageErrors.length}`;
  if (shot.dialogs.length > 0) line += ` dialogs:${shot.dialogs.length}`;
  if (shot.warnings.length > 0) line += ` warn:${shot.warnings.length}`;
  if (shot.redirected) {
    let pathname = shot.href;
    try {
      pathname = new URL(shot.href).pathname;
    } catch {
      // zostaw surowy href
    }
    line += `  REDIRECT -> ${pathname}`;
  }
  if (!shot.ok) line += `  ${shot.error}`;
  return line;
}

// `sink` (opcjonalne): tablica, do której trafiają zrzuty na bieżąco — dzięki temu wynik częściowy
// przetrwa wyjątek lub przerwanie przez limit czasu. Domyślnie tworzona jest nowa tablica.
export async function runMatrix({ browser, scenario, storageStatePath, outDir, log, sink = [] }) {
  const shots = sink;
  await mkdir(outDir, { recursive: true });
  viewports: for (const viewport of scenario.viewports) {
    if (!browser.isConnected()) break;
    const { context, page, collector, persistSession } = await openPage(browser, scenario, { viewport, storageStatePath });
    try {
      for (const theme of scenario.themes) {
        for (const route of scenario.matrix) {
          if (!browser.isConnected()) break viewports; // przeglądarka zamknięta (np. limit czasu)
          const shot = await captureShot({ page, collector, scenario, outDir, route, viewport, theme });
          shots.push(shot);
          log(formatLine(shot));
        }
      }
    } finally {
      await persistSession().catch(() => {}); // refresh token rotuje — kolejny kontekst potrzebuje aktualnych ciasteczek
      await context.close().catch(() => {});
    }
  }
  return shots;
}
