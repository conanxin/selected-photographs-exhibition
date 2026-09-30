# v0.8-rc1 — Publication Release Candidate

Release date: 2026-09-30
TASK_ID: `SPFC_P8_PUBLICATION_RELEASE_CANDIDATE`
Issue: [#7 — P8: publication release candidate](https://github.com/conanxin/selected-photographs-exhibition/issues/7)
Notion: [13｜P8 Publication Release Candidate](https://app.notion.com/p/3eb34a28189a81f9bc90f39b75d742d7)
Production: https://selected-photographs-exhibition.vercel.app

---

## Public-facing changes

- **Version label updated to `v0.8-rc1`** in `<p id="asset-state">`, runtime `updateStatus()`, footer, and `STATUS.json`.
- **Editorial copy finalised** in the public `About` (`#about`) section. Stale future-tense / draft / prototype language was scrubbed; "回到来源" now reads as the project's standing rights / provenance statement.
- **Archive index copy** (`#archive-index`) tightened: filter labels and counts use canonical values (96 / 18 / 18 / 68), and the sub-note clarifies that `printed credit` vs `catalog credit` conflicts on p.3 / p.52 / p.90 are intentionally preserved (both spellings).
- **Title and language label** (`v0.7 → v0.8-rc1`) updated in footer alongside the 2026.09.30 release date.

---

## Accessibility

- **Skip link**: `<a class="skip-link" href="#top">跳到主要内容</a>` at document top; target `<main id="top" tabindex="-1">` is focusable. First `Tab` from a fresh load focuses the skip link; `Enter` jumps past the header to `#main`.
- **Image semantics** for all 18 exhibition scan images:
  - `alt="原书扫描页：<工作题名>；项目对应书内第<page>页"` — non-empty, project-controlled wording; no AI-generated visual description; no fabricated subject details; no obsolete draft phrases.
  - `loading="lazy"` and `decoding="async"` set on every wall image.
- **HTML semantics**: every archive row that corresponds to an exhibited work is a real `<button>` with `aria-label="打发展览作品：<printed_title_en>"`; text-only catalog rows remain `<div>`, not clickable.

---

## Metadata (for crawlers and link previews)

The HTML head now exposes publication metadata without adding any OG image:

- `<title>Selected Photographs from China — 被选择的中国</title>`
- `<meta name="description" content="基于1977年《Selected Photographs from China》的当代网页再策展：18件真实扫描作品、6个章节与96项全书档案索引，并公开区分Agent review与Human verification。">`
- `<link rel="canonical" href="https://selected-photographs-exhibition.vercel.app/">`
- Open Graph: `og:type=website`, `og:title`, `og:description`, `og:url` (all canonical URL).
- Twitter: `twitter:card=summary`, `twitter:title`, `twitter:description`.
- **OG image is intentionally absent** in this release candidate. The rights handling of historical scan images as social-card art has not been finalised, and any automated OG image would have to defer to that decision.

---

## Rights / provenance

The public `About` section explicitly states:

1. This is a contemporary re-curation built on the 1977 book *Selected Photographs from China* (Foreign Languages Press).
2. Chinese-language titles in the interface are project working translations, **not** claimed original-book Chinese titles.
3. Web display is **scan derivatives of the book's printed images**, not original negatives or full-bleed prints.
4. All 18 currently exhibited works are wired to real scan pages.
5. **Agent review** and **Human verification** are distinct evidence tiers (公开区分).
6. Internet Archive accessibility does **not** automatically equal public domain or open licence.
7. The repository's **MIT License** applies to code and documentation; the historical scan images are **not** claimed to be MIT-licensed.

No specific licence inference is made for individual scan images.

---

## Evidence model unchanged

- **No new works, no fourth batch, no Human Verification P2.** This release is publication polish only.
- **18 exhibited works**, **6 chapters**, **96 catalog entries** (18 selected link fields + 78 text-only), **68 colour-marked + 28 unmarked**, **4/18 Human verified** — all preserved as P1/P6 invariants.
- **Human verified exact set `[3, 40–41, 52, 90]`** preserved.
- **p.90 canonical direction** preserved: printed/main author `Chou Chia-kuo`, catalog OCR variant `Chou Chia-kue` (both spellings intentionally).
- **p.100** remains Agent confirmed, Human verification `Pending`.
- **§7 credit variants** preserved on p.3 (`Chou Chun-yen` / `Chou Chun-jen`), p.52 (`Chang Chen` / `Chiang Chen`), p.90 (`Chou Chia-kuo` / `Chou Chia-kue`).

---

## P7 interaction integrity preserved

All archive interaction fixes from v0.7 (P7) remain in effect:

- Shared `[data-work] → showWork(Number, trigger)` delegated handler (no stale `openDetail()` reference).
- Archive filter uses the correct `p.selected_for_exhibition` field (no `p.p.…` typo).
- Selected archive rows are real `<button>` elements with `aria-label` for screen readers.
- Focus returns to the originating trigger element after the detail dialog closes (subject to `trigger.isConnected`).
- Detail dialog: keyboard activation (Enter / Space), Esc close, and tab keyboard navigation (click / ArrowRight / ArrowLeft / Home / End) all still work.

---

## Performance

- 18 wall images use `loading="lazy"` and `decoding="async"`.
- No duplicate image requests, no 404s, no JS exceptions on a fresh load.
- Page weight: ~98 KB HTML + lazy scan assets; no extra framework dependencies added.

Lightweight performance QA only — no Lighthouse score is the gate for `v0.8-rc1`.

---

## Known limitations

- **14 works still Agent-level**: p.2, p.6, p.10, p.18, p.23, p.38, p.39, p.54, p.59, p.79, p.83, p.87, p.98, p.100. Human Verification P2 has not started; it is a separate task.
- **Capture dates mostly unknown** for Agent-level works. OCR-confirmed prints do not consistently include shoot dates; we do not guess.
- **Chinese-character photographer names are not guessed**; `author` is left as the English / pinyin form confirmed in OCR.
- **No OG image** yet, by deliberate decision. The right to use historical scan derivatives as social-card art is an open question for the project.
- **Single publication URL** (no mirror / no CDN). Vercel alias `selected-photographs-exhibition.vercel.app` is the canonical public address.
- **No automatic social-share pre-generation**: when sharing the URL to a platform that does not accept our static metadata, the platform's own preview generator will fetch the canonical URL and our OG/Twitter tags.

---

## Deployment

| Stage | Build / Deployment ID | Notes |
|---|---|---|
| Validator gate | 152/152 PASS | local `scripts/validate_catalog.py` |
| Static metadata check | grep PASS | meta description, canonical, OG, Twitter, title all present |
| Push to `main` | (latest commit at close) | non-force-push |
| Vercel deployment | Git integration check PASS · `H8YaFKmAsFvbFtcnMCXckFrgLvB5` | aliased to `selected-photographs-exhibition.vercel.app` |
| Production browser QA | 42/42 PASS | Remote Windows Chromium/Puppeteer; desktop 1440×1000 + mobile 390×844 |
| Production assets | 18/18 scan images | canonical `assets.js` synced from `ingest-receipt.json`; 0 asset 404s |
| Production errors | 0 console / 0 page / 0 asset 404 | favicon request suppressed with data-URI icon |
| Production metadata | description / canonical / OG / Twitter exact | live DOM verified |

---

## How to read this release

This is a publication release candidate. The substantive content (18 works / 6 chapters / 96 catalog entries / 4 Human verified) has been stable since v0.7. The change in `v0.8-rc1` is about the **public-facing surface**: how the project presents itself to a casual visitor, to search engines, and to accessibility tooling — without re-opening the evidence layer.