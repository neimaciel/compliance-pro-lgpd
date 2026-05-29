#!/usr/bin/env node
/**
 * compliance-pro-lgpd — TypeScript audit orchestrator.
 */
import { Command } from "commander";

const program = new Command()
  .name("compliance-pro")
  .description("LGPD audit toolkit (TypeScript)")
  .version("1.0.0");

program.command("cookie", "Audit cookies/trackers", { executableFile: "./cookie-checker.js" });
program.command("tls", "Audit TLS endpoint", { executableFile: "./tls-checker.js" });
program.command("dep", "Audit npm dependencies", { executableFile: "./dependency-scanner.js" });

program.parse(process.argv);
