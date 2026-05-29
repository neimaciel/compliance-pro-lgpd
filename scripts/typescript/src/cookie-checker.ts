#!/usr/bin/env node
/**
 * Cookie Checker — audits a website for cookie/tracker compliance with LGPD.
 *
 * Loads a URL via Playwright (headless), inspects cookies set BEFORE any consent
 * is given, and flags non-essential trackers loaded without user opt-in.
 *
 * LGPD Art. 7 I (consentimento) + Art. 8 (livre, informado, inequívoco, específico).
 *
 * Usage:
 *   tsx src/cookie-checker.ts --url https://example.com --report report.json
 */
import { chromium, type Cookie } from "playwright";
import { Command } from "commander";
import chalk from "chalk";
import { writeFileSync } from "node:fs";

interface ThirdPartyCategory {
  pattern: RegExp;
  category: "analytics" | "advertising" | "social" | "session" | "functional";
  vendor: string;
  consentRequired: boolean;
}

const KNOWN_TRACKERS: ThirdPartyCategory[] = [
  { pattern: /google-analytics\.com|googletagmanager\.com|_ga|_gid|_gat/i, category: "analytics", vendor: "Google Analytics", consentRequired: true },
  { pattern: /doubleclick\.net|adservice\.google/i, category: "advertising", vendor: "Google Ads", consentRequired: true },
  { pattern: /facebook\.com|fbcdn|_fbp|_fbc/i, category: "advertising", vendor: "Meta Pixel", consentRequired: true },
  { pattern: /linkedin\.com|li_/i, category: "advertising", vendor: "LinkedIn Insight", consentRequired: true },
  { pattern: /tiktok\.com|ttp_/i, category: "advertising", vendor: "TikTok Pixel", consentRequired: true },
  { pattern: /hotjar\.com|_hj/i, category: "analytics", vendor: "Hotjar", consentRequired: true },
  { pattern: /clarity\.ms/i, category: "analytics", vendor: "Microsoft Clarity", consentRequired: true },
  { pattern: /amplitude\.com/i, category: "analytics", vendor: "Amplitude", consentRequired: true },
  { pattern: /mixpanel\.com/i, category: "analytics", vendor: "Mixpanel", consentRequired: true },
  { pattern: /segment\.io|segment\.com/i, category: "analytics", vendor: "Segment", consentRequired: true },
  { pattern: /intercom\.io|intercom-cdn/i, category: "functional", vendor: "Intercom", consentRequired: true },
  { pattern: /(^|\.)cloudflare\.com$/i, category: "session", vendor: "Cloudflare", consentRequired: false },
  { pattern: /__Secure|__Host|sessionid|sess_|XSRF|csrftoken/i, category: "session", vendor: "Session", consentRequired: false },
];

function classify(cookie: Cookie) {
  for (const t of KNOWN_TRACKERS) {
    if (t.pattern.test(cookie.name) || t.pattern.test(cookie.domain)) return t;
  }
  return null;
}

interface Finding {
  type: "cookie" | "request";
  name: string;
  domain: string;
  vendor: string;
  category: string;
  consentRequired: boolean;
  setBeforeConsent: boolean;
  legalRef: string;
  notes: string;
}

const program = new Command()
  .name("cookie-check")
  .description("LGPD cookie compliance audit")
  .requiredOption("-u, --url <url>", "URL to audit")
  .option("-r, --report <path>", "Write JSON report")
  .option("--timeout <ms>", "Page timeout", "30000")
  .option("--fail-on-violation", "Exit non-zero if violations found")
  .parse();

const opts = program.opts();

const browser = await chromium.launch();
const context = await browser.newContext({ acceptDownloads: false });
const page = await context.newPage();

const requestUrls: string[] = [];
page.on("request", (req) => requestUrls.push(req.url()));

console.log(chalk.cyan(`Auditing ${opts.url}…`));
await page.goto(opts.url, { waitUntil: "networkidle", timeout: Number(opts.timeout) });

const cookies = await context.cookies();
const findings: Finding[] = [];

for (const c of cookies) {
  const klass = classify(c);
  if (!klass) {
    findings.push({
      type: "cookie",
      name: c.name,
      domain: c.domain,
      vendor: "Unknown",
      category: "unclassified",
      consentRequired: true, // err on safe side
      setBeforeConsent: true,
      legalRef: "LGPD Art. 8 — verificar finalidade e base legal",
      notes: "Cookie não reconhecido — investigar finalidade e classificar manualmente",
    });
    continue;
  }
  if (klass.consentRequired) {
    findings.push({
      type: "cookie",
      name: c.name,
      domain: c.domain,
      vendor: klass.vendor,
      category: klass.category,
      consentRequired: true,
      setBeforeConsent: true,
      legalRef: "LGPD Art. 7 I + Art. 8 — exige consent prévio",
      notes: `Tracker ${klass.vendor} carregado SEM consentimento (página acabou de carregar)`,
    });
  }
}

// Inspect third-party requests
const violatingRequests = new Set<string>();
for (const url of requestUrls) {
  for (const t of KNOWN_TRACKERS) {
    if (!t.consentRequired) continue;
    if (t.pattern.test(url)) {
      const host = new URL(url).host;
      const key = `${t.vendor}:${host}`;
      if (!violatingRequests.has(key)) {
        violatingRequests.add(key);
        findings.push({
          type: "request",
          name: host,
          domain: host,
          vendor: t.vendor,
          category: t.category,
          consentRequired: true,
          setBeforeConsent: true,
          legalRef: "LGPD Art. 7 I + Art. 8",
          notes: `Requisição para ${t.vendor} antes de consent — CMP deve bloquear`,
        });
      }
    }
  }
}

await browser.close();

// Report
console.log("");
console.log(chalk.bold(`Cookies set:    ${cookies.length}`));
console.log(chalk.bold(`Findings:       ${findings.length}`));
const violations = findings.filter((f) => f.consentRequired && f.setBeforeConsent);
console.log(chalk.bold(`Violations:     ${violations.length}`));

for (const v of violations) {
  console.log(
    chalk.red("✗"),
    chalk.bold(v.vendor.padEnd(20)),
    chalk.dim(v.type),
    chalk.yellow(v.name),
    chalk.gray(`(${v.category})`)
  );
}

if (violations.length === 0 && cookies.length > 0) {
  console.log(chalk.green("\n✓ Nenhuma violação detectada antes de consent."));
}

if (opts.report) {
  writeFileSync(
    opts.report,
    JSON.stringify(
      {
        url: opts.url,
        timestamp: new Date().toISOString(),
        cookies: cookies.length,
        findings,
        summary: {
          total: findings.length,
          violations: violations.length,
          byVendor: violations.reduce<Record<string, number>>((acc, f) => {
            acc[f.vendor] = (acc[f.vendor] || 0) + 1;
            return acc;
          }, {}),
        },
      },
      null,
      2
    )
  );
  console.log(chalk.green(`\nReport written: ${opts.report}`));
}

if (opts.failOnViolation && violations.length > 0) {
  process.exit(2);
}
