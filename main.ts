// gta6-meme-x-01 entry: copies POST.json from the repository root to /output.
// The entry is the X post itself — the house reads the post from X, so this
// program does nothing else. Node 22, standard library only: no network,
// no clock, no files outside the repository.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(botDir, "POST.json");
const destination = join(outputDir, "POST.json");

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(source, destination);
} catch (error) {
  console.error(`could not copy ${source} to ${destination}: ${(error as Error).message}`);
  process.exit(1);
}
