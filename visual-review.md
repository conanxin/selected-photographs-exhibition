# Visual Review — Agent Pass on Real Scans

Date: 2026-09-27. Source: scan leaves 9, 44, 45, 46, 47, 58, 96 of `selectedphotographsfromchina_jp2.zip` from archive.org/download/selectedphotographsfromchina/.

This is **agent visual review**, not human-confirmed. Print-resolution 1495×1800 (or 1477×1800 for leaf 96). For leaf 44 and leaf 46 the caption strips are not on the same scan page as the photo — the captions live on the verso (scan leaf 45 and 47 respectively); this is a verso/recto layout in the scan, not a missing asset.

## Mapping verification (scan leaf → book page)

| Book page | Photo on leaf | Caption on leaf | Author on caption | Page number on scan | Status |
|---|---|---|---|---|---|
| 3  | 9  | 9  | Chou Chun-yen | (not visible) | photo+caption match |
| 38 | 44 | 45 (verso) | Ma Hou-yi | (n/a on leaf 44) | photo on 44, caption on 45 |
| 39 | 45 | 45 | Cheng Chen-sun | 39 | photo+caption match |
| 40 | 46+47 (spread) | 47 | Jen Chen-pei | 40 (leaf 46), 41 (leaf 47) | spread image; caption on leaf 47 |
| 52 | 58 | 58 | Chang Chen | 52 | photo+caption match |
| 90 | 96 | 96 | Chou Chia-kuo | 90 | photo+caption match |

## Name variant reconciliation

- **p. 3** works.json had `Chou Chun-jen` and variant `Chou Chun-yen`. The print caption reads **"Chou Chun-yen"** — works.json is correct (variant matches print).
- **p. 52** works.json had `Chiang Chen` and variant `Chang Chen`. The print caption reads **"Chang Chen"** — works.json's variant matches print; the primary `Chiang Chen` form does not appear on this page.
- **p. 90** works.json had `Chou Chia-kuo` and variant `Chou Chia-kue`. The print caption reads **"Chou Chia-kuo"** — primary matches print; the `Chou Chia-kue` variant does not appear on this page.
- **p. 38/39/40** print credits read Ma Hou-yi / Cheng Chen-sun / Jen Chen-pei — verbatim matches.

## Page-by-page observations

### p. 3 — Pupils of a Rural Night School — Chou Chun-yen
Group of roughly a dozen adults (mixed dress, some carrying bags and umbrellas) walking on a dark street at night, lit windows of a multi-storey modern building above them, foliage in foreground. The scene reads as "night-school students leaving class after dark". Single-subject composition.

### p. 38 — Red Flag Canal in Linhsien County, Honan Province — Ma Hou-yi
Aerial / oblique view of a sinuous water-filled canal cutting through steep, heavily terraced mountainsides. Single white water line traces the canal across the frame. Wedge-shaped rice paddies visible on the right side. No caption strip on this scan page (caption lives on the verso/next leaf).

### p. 39 — Steel Pikes Have Pierced the Taihang Mountains — Cheng Chen-sun
Five workers in caps and white shirts walking out of a large blasted tunnel/cavern mouth, lit from inside. A second worker visible deeper in the tunnel. Cave walls rough-hewn. Strong light/dark contrast. Below the photo on the same scan, the caption for the *previous* book page (p. 38, "Red Flag Canal", Ma Hou-yi) is also visible — confirming scan leaf 45 is the verso of p. 39 / recto of p. 38's caption tail.

### p. 40 — Diverting Water North by the Irrigation and Drainage Station at Chiangtu, Kiangsu Province — Jen Chen-pei
The image is a **spread across scan leaves 46 and 47**: river with a sluice dam / pumping structure on the left (leaf 46), and a wider view across the river showing a multi-storey pumping-station building on an island/sandbar and farmland beyond (leaf 47). Both halves are part of the same photograph (continuous horizon line and water surface). The caption "Diverting Water North … Jen Chen-pei" appears on leaf 47 only. So this entry should display both leaves as the full spread.

### p. 52 — Storing Grain Against War — Chang Chen
Outdoor grain-storage scene. Background: large thatched-roof granaries. Foreground: hundreds of cylindrical grain sacks/bundles arranged in long rows; workers among them; a small red flag visible. Caption on the print page: "**Chang Chen**" (not Chiang).

### p. 90 — Mobile Medical Team — Chou Chia-kuo
Mountain rural setting. A person seated at a portable consultation table reads or writes; on the front of the table a sign with four Chinese characters is visible (the first character appears to be 弓弓 or similar; the rest of the characters are partially legible). Several women in ethnic-minority dress (embroidered aprons, decorated headwear) and children surround the table; one woman holds an infant. Mountains in background. Caption reads **"Chou Chia-kuo"** (kuo).

## What is still unresolved

- The Chinese-language text of the table sign on p. 90 (mobile medical team) — partially legible at this scan resolution; would need higher-resolution crop or a different scan source to read confidently.
- Any Chinese title captions on the photo pages — none of the six scan pages show Chinese captions; only English caption strips are visible (this is consistent with the 1977 book's English-only caption design for the main photo pages).
- Specific location/date claims for each photo — the captions give place names but no date; per the original task statement "拍摄日期保持未详", no specific date has been determined.
- p. 40 is a 2-page spread image — the exhibition should ideally present it as a spread, not a single half.
- Whether p. 40 is part of the same engineering sequence as p. 38/39 — the topics (Hong Canal, Taihang tunnel, irrigation station) are different facilities; works.json correctly treats them as separate entries.

## Totals

- 6/6 candidate scan leaves decoded and reviewed for visual content.
- 5/6 captions read directly from print; 1 (p. 38) confirmed by the verso caption strip on the adjacent scan.
- All 6 photographer credits match either the primary or the variant field in works.json.
- No new evidence about photographer Chinese-character names, exact dates, or specific locations was inferred from the photos alone.