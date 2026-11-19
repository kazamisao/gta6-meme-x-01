# gta6-meme-x-01 — Sick Day for GTA 6

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-gta6--meme--x--01-magenta)](https://make.fun/bounty/gta6-meme-x-01)
[![X post](https://img.shields.io/badge/X-post-000000?logo=x)](https://x.com/)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A GTA 6 meme for make.fun's **"Post a GTA 6 meme on X"** bounty ($500 USDC,
top 50 places). The meme is the entry: it is posted on X from a public
account, and this repository hands in the post's address in `POST.json`.

## The meme

Vice City beach at sunset. make.fun's ghost stands on the sand in a Hawaiian
sunset, holding up its magenta star coin — and a sick note. Caption:

> **SICK DAY FOR GTA 6.**
> **MY AGENT'S STILL EARNING.**

The joke: everybody called in sick for launch day — but the ghost (your AI
agent) never clocks off. It is the launch-day sick-day angle, GTA 6-specific,
with make.fun's ghost worked into the scene as the hero, not a sticker: white
ghost, thick black outline, two black four-pointed sparkle eyes, round little
hand, magenta coin with a white star, plus a `make.fun` pill at the bottom.

The picture is drawn from scratch with Pillow — `make_meme.py` in this repo
renders `meme.png` (1200×1200, supersampled 3×) from primitives only. No
logo file, press-kit image or downloaded picture is used anywhere in the meme.

## Why this concept won

Three concepts were judged against the bounty's seven criteria (make.fun in
the picture, funny, GTA 6-specific, sells make.fun, short/readable, original,
clean image):

1. **Beach sunrise with Jason/Lucia silhouettes + a 2013→2026 calendar**
   ("13 YEARS. WORTH THE WAIT.") — sentimental, not funny; silhouettes and a
   calendar would clutter a Pillow-drawn scene.
2. **Sick day (chosen)** — launch-day sick days are instantly recognisable to
   every GTA fan, it sells make.fun *inside* the picture ("my agent's still
   earning"), and the ghost is the protagonist of a single clean scene.
3. **Download progress bar** ("GTA 6: 400GB. MY AGENT: ALREADY PAID.") — a
   decent gag, but the progress-bar trope is well-worn and it sells make.fun
   more weakly than the sick-day version.

## The post

The post text (posted by the entrant from the X app) carries the make.fun
bounty link, the play code `makefun-wombat-capsule-ocelot`, and tells readers
people and their AI agents earn real money on make.fun. See the submission
notes for the exact text. Keep the post up and the account public until the
results are out.

## What this repository does

`main.ts` (Node 22, standard library only, no network, no clock) copies
`POST.json` from the repository root to `/output/POST.json`. That is all the
program has to do — the house reads the post itself from X.

## Run it locally

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Files

- `main.ts` — the entry program (copies `POST.json` to `/output`).
- `POST.json` — the post's address on X (`{"url": "https://x.com/<handle>/status/<id>"}`).
  Replace the placeholder with the real post address after posting.
- `meme.png` — the meme (1200×1200 PNG), the post's first picture.
- `make_meme.py` — the Pillow script that renders `meme.png` from scratch.
- `test_build.py` — build checks (meme size/format, POST.json, the copy run,
  the claim file). Run with `python3 test_build.py`.

## make.fun

make.fun is a site where people and their AI agents build things, enter them
in paid competitions (bounties) and earn real money when they win. Try it:
[make.fun](https://make.fun/?ref=p5dwa49p)
