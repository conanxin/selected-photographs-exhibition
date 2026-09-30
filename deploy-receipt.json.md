# Deploy receipt — SPFC v0.3 (real scans)

Date: 2026-09-27.

## What completed locally

- Workspace: `/mnt/d/CodexData/spfc-exhibition` (existed-or-created per START_HERE.md).
- Source download: `selectedphotographsfromchina_jp2.zip` from archive.org — 96,919,838 bytes, sha256 `fe5cbd3e7ba19aa9862550a10671ecfd7f6cd6e8c2ccae233c4b61dae9b7ca5b`.
- `python3 start.py --prepare-only --zip /tmp/spfc_jp2.zip` — 6/6 candidate scan leaves decoded + 10 evidence pages.
- `ingest-receipt.json` written; `assets/assets.js` regenerated with 6 works + 10 evidence pages.
- `human_verified_count` left at 0; `review_status` left as `PENDING_VISUAL_REVIEW`.
- `visual-review.md` written with Agent visual review of all six candidate scans (mapping, photographer name reconciliation, page observations).
- Publish directory `/home/conanxin/spfc-public-release/selected-photographs-exhibition/` synced: `index.html` + `assets/` only (17 asset files). No source code, ZIP, or notes.

## Visual review summary (full text in `visual-review.md`)

| Book page | Photo on leaf | Author on caption | Page number visible | Status |
|---|---|---|---|---|
| 3  | 9  | Chou Chun-yen | (n/a) | photo+caption match |
| 38 | 44 | (caption on leaf 45 verso) | (n/a) | photo on 44, caption on 45 |
| 39 | 45 | Cheng Chen-sun | 39 | photo+caption match |
| 40 | 46+47 (spread) | Jen Chen-pei | 40 (leaf 46), 41 (leaf 47) | spread image |
| 52 | 58 | Chang Chen (NOT Chiang) | 52 | photo+caption match |
| 90 | 96 | Chou Chia-kuo (NOT kue) | 90 | photo+caption match |

Reconciliation: works.json's variant field matches printed text in all three name conflicts (Chou Chun-yen, Chang Chen, Chou Chia-kuo). The primary field is not always what's on the page — left unchanged because the user is the human-verified source.

Still unresolved: Chinese characters on the medical-team sign (p. 90) only partially legible at scan resolution. p. 40 is a 2-page spread image.

## Vercel deploy status: BLOCKED on user login

- Vercel CLI installed (60.1.3, Node 22.23.2).
- No existing session in `~/.vercel`.
- OAuth device-code URL produced by `vercel login --non-interactive`:
  **https://vercel.com/oauth/device?user_code=SDRP-LBCS**
  (note: device code rotates each run; if it has expired by the time you visit, re-run the login command below)
- To re-trigger: `cd /home/conanxin/spfc-public-release && bash publish.sh` (the script will detect no auth and re-issue a fresh login URL)
- Or manually: `cd /home/conanxin/spfc-public-release/selected-photographs-exhibition && npx --yes vercel@latest deploy . --prod --yes --scope conanxins-projects`

## Required action from user
Open https://vercel.com/oauth/device?user_code=SDRP-LBCS in a browser, complete the OAuth grant, then re-run the publish. I will then capture the actual production URL Vercel returns, verify anonymous access with a no-auth fetch, and report back with a real link.

## What will happen after user authorization
1. `vercel deploy` against `/home/conanxin/spfc-public-release/selected-photographs-exhibition/` to scope `conanxins-projects`.
2. Capture the returned `https://…vercel.app` URL.
3. Anonymous HTTP probe: ensure response is the HTML, not a Vercel login page.
4. If deployment protection blocks public access, walk through disabling it on *this* project only.
5. Final receipt returned with `PUBLIC_URL`, `REAL_PAGES_LOADED=6/6`, `AGENT_VISUALLY_REVIEWED=6/6`, anonymous-access pass.
6. Notion sync (if write connection is available).