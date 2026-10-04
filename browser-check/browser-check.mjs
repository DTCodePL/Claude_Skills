#!/usr/bin/env node
// browser-check — macierz zrzutów ekranu (viewport x motyw) i raport błędów konsoli/sieci.
// Użycie: node browser-check.mjs <scenario.json> [--out <dir>] [--only matrix|flows] [--headed] [--keep-auth]
import { randomBytes } from 'node:crypto';
import { existsSync, rmdirSync, rmSync } from 'node:fs';
import { mkdir, rm, rmdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { runMatrix } from './lib/matrix.mjs';
import { loadScenario, redact, redactDeep, ScenarioError } from './lib/scenario.mjs';
import {
  ensureTheme,
  findViewport,
  launchBrowser,
  login,
  openPage,
  storageStateFile,
  waitForReady,
} from './lib/session.mjs';

const TOOL_DIR = path.dirname(fileURLToPath(import.meta.url));
const FLOWS_MODULE = path.join(TOOL_DIR, 'lib', 'flows.mjs');
const USAGE = 'Użycie: node browser-check.mjs <scenario.json> [--out <dir>] [--only matrix|flows] [--headed] [--keep-auth]';

class UsageError extends Error {}

function pad(number, width = 2) {
  return String(number).padStart(width, '0');
}

/** RRRRMMDD-HHMMSS-mmm (czas lokalny). */
function timestamp(date) {
  return (
    `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}-` +
    `${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}-${pad(date.getMilliseconds(), 3)}`
  );
}

function firstLine(error) {
  return String(error?.message ?? error).split('\n')[0].trim();
}

function parseCommandLine() {
  let args;
  try {
    args = parseArgs({
      allowPositionals: true,
      options: {
        out: { type: 'string' },
        only: { type: 'string' },
        headed: { type: 'boolean', default: false },
        'keep-auth': { type: 'boolean', default: false },
      },
    });
  } catch (error) {
    throw new UsageError(firstLine(error));
  }
  if (args.positionals.length !== 1) throw new UsageError('Wymagany dokładnie jeden argument: ścieżka do scenariusza.');
  if (args.values.only !== undefined && !['matrix', 'flows'].includes(args.values.only)) {
    throw new UsageError('--only przyjmuje "matrix" albo "flows".');
  }
  return args;
}

/** Katalog wyników: domyślnie nowy, unikalny; jawny nie może być plikiem ani katalogiem z cudzym report.json. */
async function resolveOutDir(requested, startedAt) {
  if (requested === undefined) {
    return path.join(TOOL_DIR, 'out', `${timestamp(startedAt)}-${randomBytes(2).toString('hex')}`);
  }
  if (requested.trim() === '') throw new UsageError('--out nie może być pusty.');
  const outDir = path.resolve(requested);
  const info = await stat(outDir).catch(() => null);
  if (info && !info.isDirectory()) throw new UsageError(`--out wskazuje istniejący plik: ${outDir}`);
  if (info && (await stat(path.join(outDir, 'report.json')).catch(() => null))) {
    throw new UsageError(`--out zawiera już report.json (wynik wcześniejszego przebiegu): ${outDir}`);
  }
  return outDir;
}

/** Moduł flows (osobny plik): brak pliku = tryb pominięty; istniejący, ale wadliwy moduł to błąd. */
async function loadFlowsModule() {
  if (!existsSync(FLOWS_MODULE)) return null;
  const module = await import(pathToFileURL(FLOWS_MODULE).href);
  if (typeof module.runFlow !== 'function') throw new Error('lib/flows.mjs nie eksportuje funkcji runFlow');
  return module;
}

/** Przy SIGINT/SIGTERM plik stanu sesji (ciasteczka) nie może zostać na dysku. */
function installSignalCleanup(storageStatePath, keepAuth) {
  const handle = (signal, code) => () => {
    if (!keepAuth) {
      rmSync(storageStatePath, { force: true });
      try {
        rmdirSync(path.dirname(storageStatePath));
      } catch {
        // katalog nie istnieje albo nie jest pusty
      }
    }
    console.error(`Przerwano (${signal}).`);
    process.exit(code);
  };
  process.on('SIGINT', handle('SIGINT', 130));
  process.on('SIGTERM', handle('SIGTERM', 143));
}

async function main() {
  let args;
  let outDir;
  const startedAt = new Date();
  try {
    args = parseCommandLine();
    outDir = await resolveOutDir(args.values.out, startedAt);
  } catch (error) {
    if (!(error instanceof UsageError)) throw error;
    console.error(`${error.message}\n${USAGE}`);
    return 2;
  }

  let scenario;
  let flowsModule = null;
  const only = args.values.only ?? null;
  try {
    scenario = await loadScenario(path.resolve(args.positionals[0]));
    // Walidacja flows przed logowaniem i przeglądarką — błąd scenariusza nie może kosztować przebiegu.
    if (scenario.flows.length > 0 && only !== 'matrix') {
      flowsModule = await loadFlowsModule();
      if (flowsModule && typeof flowsModule.validateFlows === 'function') await flowsModule.validateFlows(scenario);
    }
  } catch (error) {
    if (error instanceof ScenarioError) {
      console.error(redact(error.secrets ? error : scenario, `Błąd scenariusza: ${error.message}`));
      return 2;
    }
    console.error(redact(scenario, `Błąd modułu flows: ${firstLine(error)}`));
    return 1;
  }

  const log = (line) => console.log(redact(scenario, line));
  try {
    await mkdir(outDir, { recursive: true });
  } catch (error) {
    console.error(redact(scenario, `Nie można utworzyć katalogu wyników "${outDir}": ${error.code ?? firstLine(error)}`));
    return 2;
  }

  const report = {
    startedAt: startedAt.toISOString(),
    finishedAt: null,
    durationMs: 0,
    baseUrl: scenario.baseUrl,
    ok: false,
    aborted: null,
    login: null,
    matrix: [],
    flows: [],
    flowsSkipped: false,
  };

  const storageStatePath = storageStateFile(outDir);
  let storageCreated = false;
  installSignalCleanup(storageStatePath, args.values['keep-auth']);

  let browser = null;
  const timer = setTimeout(() => {
    report.aborted = 'TIMEOUT';
    log(`ABORT timeout ${scenario.timeoutMs} ms`);
    if (browser) browser.close().catch(() => {});
  }, scenario.timeoutMs);

  async function runFlows() {
    if (!flowsModule) {
      log('FLOWS skipped: lib/flows.mjs not present');
      report.flowsSkipped = true;
      return;
    }
    for (const flow of scenario.flows) {
      if (report.aborted) break;
      let session = null;
      let result;
      try {
        const viewport = findViewport(scenario, flow.viewport ?? 'desktop');
        session = await openPage(browser, scenario, { viewport, storageStatePath: storageCreated ? storageStatePath : undefined });
        const { page, collector } = session;
        await page.goto(new URL(flow.startPath, scenario.baseUrl).href, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await waitForReady(page, scenario, { waitFor: flow.waitFor, timeoutMs: flow.timeoutMs });
        await ensureTheme(page, scenario, flow.theme ?? 'light', { waitFor: flow.waitFor }, viewport.name);
        collector.drain(); // zdarzenia z nawigacji harnessu nie należą do flow
        result = await flowsModule.runFlow({ page, flow, scenario, outDir, log, collector });
        if (!result || typeof result !== 'object') {
          result = { name: flow.name, status: 'ERROR', error: 'runFlow nie zwrócił wyniku' };
        }
        const late = collector.drain();
        for (const key of ['consoleErrors', 'pageErrors', 'failedRequests']) {
          if (late[key].length > 0) result[key] = [...(result[key] ?? []), ...late[key]];
        }
        await session.persistSession().catch(() => {});
      } catch (error) {
        result = { name: flow.name, status: 'ERROR', error: firstLine(error) };
        log(`FLOW ERROR ${flow.name} ${result.error}`);
      } finally {
        if (session) await session.context.close().catch(() => {});
      }
      report.flows.push(result);
    }
  }

  try {
    try {
      browser = await launchBrowser(scenario, { headed: args.values.headed });
    } catch (error) {
      report.aborted = 'BROWSER_LAUNCH_FAILED';
      report.error = firstLine(error);
      log(`ABORT cannot launch browser (channel ${scenario.browser.channel}): ${report.error}`);
    }

    let loginOk = true;
    if (browser && scenario.login && !report.aborted) {
      const result = await login(browser, scenario, outDir);
      report.login = {
        ok: result.ok,
        durationMs: result.durationMs,
        error: result.error ?? null,
        screenshot: result.screenshot ?? null,
      };
      if (result.ok) {
        storageCreated = true;
        log(`LOGIN ok ${(result.durationMs / 1000).toFixed(1)}s`);
      } else {
        loginOk = false;
        log(`LOGIN FAIL ${result.error}${result.screenshot ? `  ${path.relative(process.cwd(), result.screenshot)}` : ''}`);
      }
    }

    if (browser && loginOk && !report.aborted) {
      if (only !== 'flows' && scenario.matrix.length > 0) {
        await runMatrix({
          browser,
          scenario,
          storageStatePath: storageCreated ? storageStatePath : undefined,
          outDir,
          log,
          sink: report.matrix,
        });
      }
      if (only !== 'matrix' && scenario.flows.length > 0 && !report.aborted) {
        await runFlows();
      }
    }
  } catch (error) {
    if (!report.aborted) {
      report.aborted = 'ERROR';
      report.error = firstLine(error);
      log(`ABORT ${report.error}`);
    }
  } finally {
    clearTimeout(timer);
    if (browser) await browser.close().catch(() => {});
    if (!args.values['keep-auth']) {
      await rm(storageStatePath, { force: true }).catch(() => {});
      await rmdir(path.dirname(storageStatePath)).catch(() => {});
    }
  }

  const finishedAt = new Date();
  report.finishedAt = finishedAt.toISOString();
  report.durationMs = finishedAt - startedAt;
  const shotsOk = report.matrix.filter((shot) => shot.ok).length;
  // Błąd artefaktu (zrzut końcowy) liczy się jako nieudany flow, mimo statusu asercji.
  const flowsOk = report.flows.filter((flow) => flow.status === 'PASS' && !flow.artifactError).length;
  report.ok =
    report.aborted === null &&
    (report.login === null || report.login.ok) &&
    shotsOk === report.matrix.length &&
    flowsOk === report.flows.length;

  const reportPath = path.join(outDir, 'report.json');
  let reportWritten = true;
  try {
    // Redakcja wartości tekstowych PRZED serializacją — raport zostaje poprawnym JSON-em dla dowolnego sekretu.
    await writeFile(reportPath, JSON.stringify(redactDeep(scenario, report), null, 2), 'utf8');
  } catch (error) {
    reportWritten = false;
    console.error(redact(scenario, `Nie można zapisać raportu "${reportPath}": ${error.code ?? firstLine(error)}`));
  }
  log(
    `RESULT ${report.ok ? 'ok' : 'fail'}  shots ${shotsOk}/${report.matrix.length}  flows ${flowsOk}/${report.flows.length}  report: ${reportWritten ? reportPath : '(nie zapisano)'}`,
  );
  return report.ok && reportWritten ? 0 : 1;
}

process.exitCode = await main();
