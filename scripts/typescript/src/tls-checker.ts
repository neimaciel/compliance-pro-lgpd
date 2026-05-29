#!/usr/bin/env node
/**
 * TLS Checker — validates TLS version and cipher suite of an HTTPS endpoint.
 *
 * LGPD Art. 46 — segurança técnica em trânsito.
 *
 * Usage:
 *   tsx src/tls-checker.ts --host example.com [--port 443] [--report report.json]
 *   tsx src/tls-checker.ts --hosts hosts.txt    # one host per line
 */
import tls from "node:tls";
import { readFileSync, writeFileSync } from "node:fs";
import { Command } from "commander";
import chalk from "chalk";

interface TlsReport {
  host: string;
  port: number;
  protocol: string | null;
  cipher: string | null;
  authorized: boolean;
  authorizationError: string | null;
  certIssuer: string | null;
  certValidFrom: string | null;
  certValidTo: string | null;
  daysToExpiry: number | null;
  findings: string[];
  passed: boolean;
}

const MIN_TLS = "TLSv1.2";

function inspect(host: string, port: number, timeoutMs = 10_000): Promise<TlsReport> {
  return new Promise((resolve) => {
    const socket = tls.connect({
      host,
      port,
      servername: host,
      timeout: timeoutMs,
      rejectUnauthorized: false,
    });

    let resolved = false;
    const done = (r: TlsReport) => {
      if (resolved) return;
      resolved = true;
      socket.destroy();
      resolve(r);
    };

    socket.once("secureConnect", () => {
      const protocol = socket.getProtocol();
      const cipher = socket.getCipher();
      const cert = socket.getPeerCertificate();
      const authError = socket.authorizationError ? String(socket.authorizationError) : null;
      const findings: string[] = [];

      if (!protocol) findings.push("Não foi possível detectar versão TLS");
      else if (protocol < MIN_TLS) findings.push(`TLS abaixo do mínimo (${protocol} < ${MIN_TLS})`);
      else if (protocol === "TLSv1.2") findings.push("TLS 1.2 OK, mas considere migrar para 1.3");

      if (cipher) {
        if (cipher.name.includes("RC4")) findings.push("Cipher inseguro (RC4)");
        if (cipher.name.includes("DES")) findings.push("Cipher inseguro (DES)");
        if (cipher.name.includes("NULL")) findings.push("Cipher NULL — nenhuma criptografia");
        if (!/(GCM|CHACHA20|POLY1305)/.test(cipher.name)) findings.push("Cipher sem AEAD (recomendado GCM/CHACHA20)");
      }

      const validTo = cert.valid_to ? new Date(cert.valid_to) : null;
      const daysToExpiry = validTo ? Math.floor((validTo.getTime() - Date.now()) / 86_400_000) : null;
      if (daysToExpiry !== null && daysToExpiry < 30) findings.push(`Certificado expira em ${daysToExpiry} dias`);

      if (authError) findings.push(`Erro de autorização: ${authError}`);

      done({
        host,
        port,
        protocol,
        cipher: cipher?.name ?? null,
        authorized: socket.authorized,
        authorizationError: authError,
        certIssuer: typeof cert.issuer === "object" ? cert.issuer.O ?? cert.issuer.CN ?? null : null,
        certValidFrom: cert.valid_from ?? null,
        certValidTo: cert.valid_to ?? null,
        daysToExpiry,
        findings,
        passed: findings.length === 0,
      });
    });

    socket.once("error", (err) => {
      done({
        host, port, protocol: null, cipher: null,
        authorized: false, authorizationError: err.message,
        certIssuer: null, certValidFrom: null, certValidTo: null, daysToExpiry: null,
        findings: [`Erro de conexão: ${err.message}`],
        passed: false,
      });
    });

    socket.once("timeout", () => {
      done({
        host, port, protocol: null, cipher: null,
        authorized: false, authorizationError: "timeout",
        certIssuer: null, certValidFrom: null, certValidTo: null, daysToExpiry: null,
        findings: ["Timeout"],
        passed: false,
      });
    });
  });
}

const program = new Command()
  .name("tls-check")
  .requiredOption("--host <host>", "Single host")
  .option("--hosts <file>", "File with one host per line")
  .option("--port <port>", "Port", "443")
  .option("-r, --report <path>", "JSON report")
  .option("--fail-on-violation", "Exit 2 on any failure")
  .parse();

const opts = program.opts();
const port = Number(opts.port);

let hosts: string[];
if (opts.hosts) {
  hosts = readFileSync(opts.hosts, "utf-8").split("\n").map((l) => l.trim()).filter(Boolean);
} else {
  hosts = [opts.host];
}

const results: TlsReport[] = [];
for (const h of hosts) {
  const r = await inspect(h, port);
  results.push(r);
  const status = r.passed ? chalk.green("✓") : chalk.red("✗");
  console.log(
    status,
    chalk.bold(h.padEnd(40)),
    chalk.cyan((r.protocol ?? "—").padEnd(10)),
    chalk.dim(r.cipher ?? "—"),
    r.daysToExpiry != null ? chalk.yellow(`${r.daysToExpiry}d`) : ""
  );
  for (const f of r.findings) console.log("    ", chalk.yellow(f));
}

console.log("");
console.log(chalk.bold(`Total: ${results.length} | Passed: ${results.filter((r) => r.passed).length} | Failed: ${results.filter((r) => !r.passed).length}`));

if (opts.report) {
  writeFileSync(opts.report, JSON.stringify({ ts: new Date().toISOString(), results }, null, 2));
  console.log(chalk.green(`Report: ${opts.report}`));
}

if (opts.failOnViolation && results.some((r) => !r.passed)) process.exit(2);
