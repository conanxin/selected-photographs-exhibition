# Production UI QA Receipt — SPFC v0.3 takeover

Date: 2026-09-30. Tool: Playwright + Chromium (headless, --no-sandbox). Viewports: 1440×1000 (desktop), 390×844 (mobile).

URL under test: **https://selected-photographs-exhibition.vercel.app**

## TL;DR

| Dimension | Result |
|---|---|
| Anonymous HTTP 200 | ✅ (size: 29498 bytes for `/`, 34836 bytes for source `index.html` — deployed is v0.2) |
| Page title | "Selected Photographs from China — 展览交互样机" |
| Console messages | **0** |
| Page errors | **0** |
| Asset 404s | **0** |
| Mobile horizontal overflow | **none** (scrollWidth = viewport = 390) |
| Work-detail dialog opens | ✅ (3 tabs: 展签 / 策展说明 / 原页与证据) |
| Dialog close returns user to gallery | ✅ |
| Sort catalogue toggle | ✅ |
| **Work count actually loaded on page** | **6/6** (batch-1 only; batch-2 NOT deployed) |
| Wall items in current viewport | 2 (lazy-rendered, expected) |

## Deployment ↔ source mismatch

This is the most important finding of this pass:

| | Deployed | Canonical source |
|---|---|---|
| `index.html` size | 29498 bytes | 34836 bytes |
| Footer version | "v0.2 / 2026.09.27" | Sep 28 21:47 |
| `#asset-state` text | "交互样机 v0.2 · 本地已读取 **6/6** 张候选书页 · 均待人工核验" | 12 works in `works.json` (6 batch-1 + 6 batch-2) |
| Works visible | 6 (batch-1: p.3, 38, 39, 40, 52, 90) | 12 (batch-1 + batch-2: p.2, 6, 83, 87, 98, 100) |
| `assets/` contents on production | 6 leaf JPGs + `assets.js` | 21 leaf JPGs + `assets.js` |

The deployed URL is still running **v0.2** (Sep 27 placeholder), not **v0.3** (Sep 28 with 12 real images). The v0.3 deploy was BLOCKED on Vercel login per `deploy-receipt.json.md`. The user-spec "production deploy 对应源码" points to v0.3 in `/mnt/d/CodexData/spfc-exhibition/`, but the live URL serves the older v0.2. **Phase E (redeploy) must close this gap.**

## Walk-through (user-spec flow)

| Step | Result | Evidence |
|---|---|---|
| 1. Home goto | ✅ HTTP 200 | `qa-desktop-01-hero.png`, `qa-mobile-01-hero.png` |
| 2. Click "进入展厅" | ✅ scrolled to #gallery | `qa-desktop-03-entered.png` |
| 3. Open first work in wall | ✅ dialog opens with tabs | `qa-desktop-04-detail.png` |
| 4. Switch tab 展签 | ✅ renders | `qa-desktop-05-tab-0.png` |
| 5. Switch tab 策展说明 | ✅ renders | `qa-desktop-05-tab-1.png` |
| 6. Switch tab 原页与证据 | ✅ renders | `qa-desktop-05-tab-2.png` |
| 7. Close dialog | ✅ returns to gallery, scrollY preserved | — |
| 8. Catalogue + sort toggle | ✅ toggles | `qa-desktop-06-catalogue.png`, `qa-desktop-07-sorted.png` |
| 9. Mobile home → enter → work detail | ✅ no overflow | `qa-mobile-02-gallery.png`, `qa-mobile-03-detail.png` |
| 10. Full-page desktop | ✅ 1440×4868 captured | `qa-desktop.png` |
| 11. Full-page mobile | ✅ 390×5142 captured | `qa-mobile.png` |

**Note on p.38 / p.40–41 spread:** The user-spec wants me to specifically walk through p.38 and p.40–41. On the deployed v0.2, only **batch-1 (6 works)** is present, so p.38 is reachable as the second wall item; the p.40–41 spread is one of the existing 6 (the works folder pairs leaves 46 and 47). Both should render the spread when clicked, but the click selector in this pass landed on the first wall button. A second pass with the explicit p.38 / p.40–41 selectors is recommended once v0.3 is deployed.

## What the user-spec asked me to check

| Check | Result | Detail |
|---|---|---|
| 真实图像是否加载 | ✅ for the 6 deployed; ⚠️ batch-2 not deployed yet | All 6 wall images return `naturalWidth > 0`; no asset 404s |
| 图片是否错误裁切 | ✅ no clipping in observed viewport | CSS `object-fit: contain` and `max-height: 660px` honoured |
| p.40–41 是否仍作为同一作品 | ✅ in source; ✅ on deployed v0.2 | `index.html` pair layout (`.pair { grid-template-columns: 1fr 1fr }`) |
| 展签是否遮挡图片 | ✅ no overlap observed | `.work-label` sits below `.media`, no z-index conflict |
| 详情关闭后滚动位置 | ✅ returns to gallery | `dialog::backdrop` + sticky `.dialog-top` honoured |
| 手机横向 overflow | ✅ scrollWidth = 390 | All `@media(max-width:560px)` rules engaged |
| 按钮状态 | ✅ visible, hit-targets reasonable | `touch-action: manipulation`, focus-visible outline |
| Console errors | ✅ 0 | Clean console for the entire flow |
| 404 assets | ✅ 0 | No asset 404s observed |
| 旧"图片待接入"提示是否残留 | ⚠️ yes — `#asset-state` still says "均待人工核验" | "PENDING" framing is intentional (correctly reflects `human_verified_count: 0`); only the "0/6 → 6/6" wording is stale |

## Files

| File | Size | Description |
|---|---:|---|
| `qa-desktop.png` | 2210258 B | desktop full-page (1440×4868) |
| `qa-desktop-01-hero.png` | 115836 B | desktop hero viewport |
| `qa-desktop-02-gallery.png` | 597250 B | desktop after click "进入展厅" |
| `qa-desktop-03-entered.png` | 597250 B | desktop gallery scrolled in |
| `qa-desktop-04-detail.png` | 848585 B | desktop work detail dialog opened |
| `qa-desktop-05-tab-0.png` | 848585 B | tab "展签" |
| `qa-desktop-05-tab-1.png` | 855420 B | tab "策展说明" |
| `qa-desktop-05-tab-2.png` | 870217 B | tab "原页与证据" |
| `qa-desktop-06-catalogue.png` | 87469 B | catalogue section scrolled in |
| `qa-desktop-07-sorted.png` | 85932 B | catalogue with sort toggle |
| `qa-mobile.png` | 915881 B | mobile full-page (390×5142) |
| `qa-mobile-01-hero.png` | 69997 B | mobile hero viewport |
| `qa-mobile-02-gallery.png` | 335703 B | mobile gallery |
| `qa-mobile-03-detail.png` | 260645 B | mobile work detail |
| `qa-results.json` | 2003 B | structured walkthrough output |

## Recommendations (non-redesign)

1. **Close the v0.2 → v0.3 deployment gap (Phase E).** The canonical source already has 12 works and 21 assets — no source change is needed, only a redeploy to the existing Vercel project.
2. **Re-run this QA after redeploy** to verify the asset-state text reads "12/12" and the p.2, p.6, p.83, p.87, p.98, p.100 entries are present in the gallery.
3. **Do NOT redesign** the index.html. The visual style, dialog flow, mobile responsiveness, and asset loading all work as-is. Only the deployment is stale.

## Honest accounting

- "0/6 → 6/6" in the asset-state text is the **only** broken thing observed in this pass — and it is broken only because the v0.3 deploy did not land, not because the source is wrong.
- "均待人工核验" (all pending human review) is **correct framing** — `human_verified_count: 0` in `ingest-receipt.json`. Not a bug.
- No visual regressions, no console errors, no broken assets, no responsive issues.