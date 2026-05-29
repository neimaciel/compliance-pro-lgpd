#!/usr/bin/env node
/**
 * Dependency Scanner — flags npm dependencies known to send telemetry / data to third parties.
 *
 * LGPD context: dependências enviam dados a terceiros sem você saber → tratamento sem base legal +
 * possível transferência internacional (Cap. V LGPD) não documentada.
 *
 * Usage:
 *   tsx src/dependency-scanner.ts --pkg path/to/package.json --report report.json
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { Command } from "commander";
import chalk from "chalk";

interface ConcernCategory {
  category: "telemetry" | "analytics" | "tracking" | "third-party-call" | "untrusted-cdn";
  description: string;
  legalNote: string;
}

const CONCERNS: Record<string, ConcernCategory> = {
  "next": { category: "telemetry", description: "Next.js telemetry (anônima, mas habilitada por padrão)", legalNote: "Desabilitar com NEXT_TELEMETRY_DISABLED=1" },
  "react-scripts": { category: "telemetry", description: "Pode coletar telemetria de build", legalNote: "Verificar configuração" },
  "google-analytics": { category: "analytics", description: "Google Analytics — requer consent (Art. 8)", legalNote: "Bloquear até opt-in" },
  "@vercel/analytics": { category: "analytics", description: "Vercel Analytics — coleta IP/UA", legalNote: "Requer base legal + transparência" },
  "@google-cloud/logging": { category: "third-party-call", description: "Envia logs ao GCP — transferência internacional", legalNote: "TIA + SCC obrigatórios" },
  "@sentry/node": { category: "third-party-call", description: "Sentry — envia stacktraces (pode conter PII)", legalNote: "Configurar sanitização + DPA + TIA" },
  "@sentry/react": { category: "third-party-call", description: "Sentry browser SDK", legalNote: "Idem; cuidar de PII em URLs e form data" },
  "@datadog/browser-rum": { category: "third-party-call", description: "Datadog RUM — captura sessões", legalNote: "Pode capturar PII; configurar redaction" },
  "logrocket": { category: "tracking", description: "LogRocket — gravação de sessão", legalNote: "Requer consent + DPA" },
  "fullstory": { category: "tracking", description: "FullStory — gravação de sessão", legalNote: "Idem" },
  "hotjar": { category: "tracking", description: "Hotjar — heatmaps/recordings", legalNote: "Idem" },
  "mixpanel-browser": { category: "analytics", description: "Mixpanel", legalNote: "Consent + DPA + TIA" },
  "amplitude-js": { category: "analytics", description: "Amplitude", legalNote: "Idem" },
  "@amplitude/analytics-browser": { category: "analytics", description: "Amplitude v2", legalNote: "Idem" },
  "posthog-js": { category: "analytics", description: "PostHog (self-host ou cloud)", legalNote: "Se cloud → TIA; se self-host → OK" },
  "react-ga": { category: "analytics", description: "Google Analytics wrapper", legalNote: "Consent obrigatório" },
  "react-ga4": { category: "analytics", description: "GA4 wrapper", legalNote: "Idem" },
  "facebook-pixel": { category: "analytics", description: "Meta Pixel — requer consent", legalNote: "Idem" },
  "fbevents": { category: "tracking", description: "Meta CAPI events", legalNote: "Verificar fluxo server-side" },
  "react-native-firebase": { category: "telemetry", description: "Firebase pode coletar dados de uso", legalNote: "Configurar consent + minimização" },
};

const program = new Command()
  .name("dep-scan")
  .requiredOption("-p, --pkg <path>", "Path to package.json")
  .option("-r, --report <path>", "JSON report")
  .option("--fail-on-finding", "Exit 2 if any concern found")
  .parse();

const opts = program.opts();
const pkgPath = resolve(opts.pkg);
if (!existsSync(pkgPath)) {
  console.error(chalk.red(`Not found: ${pkgPath}`));
  process.exit(1);
}

const pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
const deps = { ...(pkg.dependencies ?? {}), ...(pkg.devDependencies ?? {}) };

const findings: Array<{ name: string; version: string; concern: ConcernCategory }> = [];
for (const [name, version] of Object.entries(deps)) {
  if (CONCERNS[name]) {
    findings.push({ name, version: String(version), concern: CONCERNS[name] });
  }
}

console.log(chalk.bold(`Dependencies scanned: ${Object.keys(deps).length}`));
console.log(chalk.bold(`LGPD concerns found:  ${findings.length}\n`));

const catColor: Record<string, (s: string) => string> = {
  telemetry: chalk.yellow,
  analytics: chalk.magenta,
  tracking: chalk.red,
  "third-party-call": chalk.cyan,
  "untrusted-cdn": chalk.red,
};

for (const f of findings) {
  console.log(
    catColor[f.concern.category]?.(`[${f.concern.category}]`.padEnd(20)) ?? `[${f.concern.category}]`,
    chalk.bold(f.name.padEnd(40)),
    chalk.dim(f.version)
  );
  console.log("   ", f.concern.description);
  console.log("   ", chalk.gray(f.concern.legalNote));
  console.log("");
}

if (opts.report) {
  writeFileSync(
    opts.report,
    JSON.stringify({ ts: new Date().toISOString(), pkgPath, total: Object.keys(deps).length, findings }, null, 2)
  );
  console.log(chalk.green(`Report: ${opts.report}`));
}

if (opts.failOnFinding && findings.length > 0) process.exit(2);
