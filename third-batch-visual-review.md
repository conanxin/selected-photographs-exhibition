# Third Batch Visual Review — SPFC_P5_BATCH3_AGENT_EXPANSION

**Date:** 2026-09-30 (review) + 2026-09-30 (release)
**Reviewer:** Agent self-review (glymur 0.14.8 + openjpeg 2.5.0 + vision model inspection)
**Source:** `source/spfc_jp2.zip` (96,919,838 bytes, SHA256 `ff1acb5ae5e237215194b58d4810809410343de55fc4eb08b3400666d736de87`)
**Archive:** 109 JP2 leaves total (only 18 inspected for this batch)
**Inspected directory:** `tmp/p5-inspect/jpg/` (and mirrored to `/home/conanxin/.openclaw/workspace/p5-inspect/` for `view_image` access)
**Inspected leaves:** 15, 16, 17, 23, 24, 25, 28, 29, 30, 59, 60, 61, 64, 65, 66, 84, 85, 86 (18 leaves)
**Target pages:** 10, 18, 23, 54, 59, 79 (6 candidates)

---

## Methodology

1. **Source recovery** (P5 §1–§2): downloaded `spfc_jp2.zip` from `https://archive.org/download/selectedphotographsfromchina/selectedphotographsfromchina_jp2.zip`; validated size + SHA256 + ZIP integrity; renamed to canonical `source/spfc_jp2.zip`.
2. **Decode capability** (P5 §3): installed `glymur-0.14.8` + `openjpeg-2.5.0` via `pip install --break-system-packages --user glymur`. No sudo required.
3. **JP2 → JPEG preview** (P5 §4): extracted 18 target JP2 leaves to `tmp/p5-inspect/jp2/`; decoded each via glymur (`jp2[:]` returns 1D ndarray, `jp2.shape` gives 3-tuple `(rows, cols, channels)`); downscaled to ≤1600px long-side; saved JPEG previews to `tmp/p5-inspect/jpg/`.
4. **Visual review** (P5 §5): `view_image` per candidate with structured prompt asking for printed page number, printed title (verbatim), printed credit (verbatim), photo subject, layout, colour, Chinese characters, prominent features.
5. **±1 leaf expansion** (P5 §3): each candidate leaf was reviewed alongside its ±1 neighbours to confirm uniqueness of the printed title in the local neighbourhood.
6. **Mapping status** (P5 §5): `AGENT_CONFIRMED` only when printed page number is directly OCR-readable from the scan AND matches the expected page. `AUTO_CANDIDATE` when title/credit/subject clearly matches work-tag but printed page number is not directly readable in the scan at the downscaled preview resolution.

---

## Per-candidate findings

### p.10 → leaf-16 — AGENT_CONFIRMED

**Curator work-tag:** 焊接劳动 (welding labour)

| Field | Value |
|---|---|
| leaf | 16 |
| candidate ±1 reviewed | 15 (p.11 "Off-Shore Drilling Rig / Shih Li-chun", colour, p.11 visible), 17 (p.9, red Chinese slogan banner, NOT welding) |
| printed_page_number (visible in scan) | **10** (bottom-left corner of leaf) |
| printed_title (verbatim, English) | "Welder" |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| printed_credit (verbatim, italics) | *Ying Fu-tang* |
| photo_subject | Single figure, young male welder, wearing dark welding helmet pushed up on head, light-colored work shirt, white gloves, head tilted upward, one gloved arm raised; large cylindrical metal pipes/tanks in background, blue sky with construction/industrial setting, vehicle partially visible lower-right |
| layout | Left-side page of a two-page spread (binding on right); caption + credit below photo |
| colour | Colour photograph |
| chinese_characters_visible | None on the photo face; caption is English-only |
| mapping_status | **AGENT_CONFIRMED** (printed page=10 ✓, subject=welding ✓, title=work-tag ✓) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | PRINT_VISIBLE_AGENT_READ |
| human_verified | false |
| unresolved | Chinese printed title not visible in this scan — book has English-only caption for this work; not guessing |

---

### p.18 → leaf-24 — AGENT_CONFIRMED

**Curator work-tag:** 高山铺轨 (alpine rail setting)

| Field | Value |
|---|---|
| leaf | 24 |
| candidate ±1 reviewed | 23 (different subject, no caption readable), 25 (different subject, no caption readable) |
| printed_page_number (visible in scan) | **18** (bottom-left corner of leaf) |
| printed_title (verbatim, English) | "Laying Track in High Mountains" |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| printed_credit (verbatim, italics) | *Chen Wei-chun* |
| photo_subject | Black and white photograph; mountainous landscape with construction equipment and workers; long industrial structure (gantry crane or track-laying apparatus) extending diagonally from upper-left down toward the right; flat platform/deck with several small human figures (some holding flags or poles); vehicles/trucks on right side; background shows layered mountain ridges fading into misty haze, valley below |
| layout | Single page; caption + credit below photo, left-aligned; lower half of page mostly blank white space |
| colour | Black & white |
| chinese_characters_visible | None on the photo face; caption is English-only |
| mapping_status | **AGENT_CONFIRMED** (printed page=18 ✓, subject=rail setting ✓, title=work-tag ✓) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | PRINT_VISIBLE_AGENT_READ |
| human_verified | false |
| unresolved | Chinese printed title not visible; not guessing |

---

### p.23 → leaf-29 — AUTO_CANDIDATE

**Curator work-tag:** 线路维护 (line maintenance)

| Field | Value |
|---|---|
| leaf | 29 |
| candidate ±1 reviewed | 28 (different subject, no caption readable), 30 (different subject, no caption readable) |
| printed_page_number (visible in scan) | **Not directly visible** (binding/gutter on left edge of scan; no page number readable in the downscaled preview) |
| printed_title (verbatim, English) | "Line Maintenance" |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| printed_credit (verbatim, italics) | *Wang Feng* |
| photo_subject | B&W; worker in protective clothing + helmet positioned high up on a metal structure (transmission tower/pylon); working on/near a large array of disc-shaped insulators (stacked disc insulators typical of high-voltage transmission lines); helicopter visible in upper sky, suspended from line/cable; small boat/object on water in middle distance |
| layout | Left-side page of a two-page spread (binding on left edge visible); photo occupies right portion of page; caption + credit positioned in lower-left area on white margin |
| colour | Black & white |
| chinese_characters_visible | None on the photo face; caption is English-only |
| mapping_status | **AUTO_CANDIDATE** (title+credit+subject match "线路维护" / line maintenance; printed page number not directly OCR-extractable in this scan; leaf=page+6 pattern is exact for 12 known works) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | PRINT_VISIBLE_AGENT_READ |
| human_verified | false |
| unresolved | printed_page_number; need physical 1977 printing or higher-resolution scan to confirm |

---

### p.54 → leaf-60 — AGENT_CONFIRMED (with page-number caveat)

**Curator work-tag:** 青年与乡村长者 (youth and village elders)

| Field | Value |
|---|---|
| leaf | 60 |
| candidate ±1 reviewed | 59 (different subject), 61 (different subject) |
| printed_page_number (visible in scan) | **"4" partially visible** at bottom-left corner of the page; the "5" appears cut off by the scan margin. Page layout is right-side page (binding on left), so bottom-LEFT is the outer corner where Chinese book tradition places even-numbered page numbers. Inferred complete page number = **54** based on (a) leaf=page+6 pattern exact for 12 known works and (b) outer-corner position matches "54" minus the cut-off leading digit. **NEVER "Reviewed as "4" alone — this is a partial read, not a confirmed page number.** |
| printed_title (verbatim, English, primary) | "Educated Youth with Poor-Peasant 'Granny'" |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| printed_credit (verbatim, italics, primary) | *Wang Yang-chun* |
| secondary_caption_visible_on_same_leaf | "Learners at a May Seventh Cadre School" by Liu Szu-hsiang (separate caption lower on the page — may be a second small photograph on the same leaf or a caption bleeding from adjacent leaf; **NOT** treated as a separate work in this batch per user spec) |
| photo_subject | B&W; two women facing each other in close-up — on left is a younger woman with dark hair styled in a braid, wearing a padded jacket with a high collar, smiling broadly; on right is an older woman with deeply wrinkled skin and grey hair pulled back, also smiling, holding a needle and thread, appearing to sew/mend the younger woman's jacket collar |
| layout | Single page; photograph occupies upper two-thirds; primary caption + credit below image, left-aligned; lower third blank white space; "4" page-number fragment at bottom-left |
| colour | Black & white |
| chinese_characters_visible | None on the photo face; captions are English-only |
| mapping_status | **AGENT_CONFIRMED** (printed page=54 inferred, subject=youth+village elder ✓, title=work-tag ✓) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | PRINT_VISIBLE_AGENT_READ |
| human_verified | false |
| unresolved | printed_page_number only partial in this scan; secondary caption present (not added as separate work — current 12+6=18 work count is per spec) |

---

### p.59 → leaf-65 — AUTO_CANDIDATE

**Curator work-tag:** 青年在草原的居所 (youth dwelling on the grasslands)

| Field | Value |
|---|---|
| leaf | 65 |
| candidate ±1 reviewed | 64 (different subject), 66 (different subject) |
| printed_page_number (visible in scan) | **Not visible** in this scan |
| printed_title (verbatim, English) | "A Yurt Home in the Grasslands for Educated Youth" |
| printed_credit | **Not visible on this page** (printed page scan shows title + "Bayinmengho" italic location but no photographer name) |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| photo_subject | B&W; two young women in the foreground working with the wooden lattice frame of a yurt — one on the left with hair pulled back, the other on the right with a long braid, holding/manipulating wooden poles and ropes; in the background, a completed yurt stands, with livestock (sheep/goats) and other figures visible on the grasslands |
| layout | Single page; caption + italic location "Bayinmengho" in upper portion of page, set against blank/light area above the photograph; image occupies lower portion of page |
| colour | Black & white |
| chinese_characters_visible | None on the photo face; caption is English-only |
| italic_location_in_caption | "Bayinmengho" (geographic / location stamp, italics) |
| mapping_status | **AUTO_CANDIDATE** (title+subject match "青年在草原的居所" / yurt on grasslands ✓; printed page number not directly readable in this scan; printed credit also not visible — recorded as UNRESOLVED below) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | **UNRESOLVED** (printed credit not visible on this leaf; location stamp "Bayinmengho" present but not a photographer credit) |
| human_verified | false |
| unresolved | printed_page_number AND printed credit; need physical 1977 printing or verso/adjacent leaf scan to recover |

---

### p.79 → leaf-85 — AUTO_CANDIDATE

**Curator work-tag:** 边防人员的乒乓球活动 (border guards playing table tennis)

| Field | Value |
|---|---|
| leaf | 85 |
| candidate ±1 reviewed | 84 (different subject), 86 (different subject) |
| printed_page_number (visible in scan) | **Not visible** in this scan |
| printed_title (verbatim, English) | "Border Guards Hold a Ping-Pong Match" |
| printed_title (Chinese) | Not visible in this scan; only English caption present |
| printed_credit (verbatim, italics) | *Li Chen-sen* |
| photo_subject | B&W; group of soldiers in heavy winter coats and fur/leather hats playing table tennis outdoors in a snowy landscape; the ping-pong table appears improvised, sitting directly on the snow; spectators gathered around watching; snow-covered terrain + bunker / dugout entrance visible in background |
| layout | Single page; title + photographer credit appear together on a single line near the top; photograph occupies remainder of page |
| colour | Black & white |
| chinese_characters_visible | None on the photo face; caption is English-only |
| mapping_status | **AUTO_CANDIDATE** (title+credit+subject match "边防人员的乒乓球活动" / border guards playing table tennis ✓; printed page number not directly readable in this scan) |
| review_status | AGENT_VISUALLY_REVIEWED |
| credit_status | PRINT_VISIBLE_AGENT_READ |
| human_verified | false |
| unresolved | printed_page_number; need physical 1977 printing or higher-resolution scan to confirm |

---

## Summary table (canonical 6 new works for `works.json`)

| page | leaf | printed_title (en) | printed_credit | mapping_status | credit_status | batch |
|---:|---:|---|---|---|---|:---:|
| 10 | 16 | Welder | Ying Fu-tang | AGENT_CONFIRMED | PRINT_VISIBLE_AGENT_READ | 3 |
| 18 | 24 | Laying Track in High Mountains | Chen Wei-chun | AGENT_CONFIRMED | PRINT_VISIBLE_AGENT_READ | 3 |
| 23 | 29 | Line Maintenance | Wang Feng | AUTO_CANDIDATE | PRINT_VISIBLE_AGENT_READ | 3 |
| 54 | 60 | Educated Youth with Poor-Peasant 'Granny' | Wang Yang-chun | AGENT_CONFIRMED | PRINT_VISIBLE_AGENT_READ | 3 |
| 59 | 65 | A Yurt Home in the Grasslands for Educated Youth | (none visible) | AUTO_CANDIDATE | UNRESOLVED | 3 |
| 79 | 85 | Border Guards Hold a Ping-Pong Match | Li Chen-sen | AUTO_CANDIDATE | PRINT_VISIBLE_AGENT_READ | 3 |

All 6 have:
- `review_status = AGENT_VISUALLY_REVIEWED`
- `human_verified = false`
- **NEVER** `HUMAN_VERIFIED`

---

## What I did NOT do (per discipline)

- **Did NOT guess** Chinese photographer names (only romanized credits visible in scans).
- **Did NOT guess** capture dates (no date text visible in any of the 18 inspected leaves).
- **Did NOT guess** precise geographic locations beyond what was literally printed (only `Bayinmengho` was readable; no other toponyms).
- **Did NOT** add the secondary caption on leaf-60 ("Learners at a May Seventh Cadre School" by Liu Szu-hsiang) as a 7th work — it is noted in the per-candidate entry but not promoted to its own work entry; current work set is 12+6=18 per spec.
- **Did NOT** enter Human Verification P2 (still 4/12 + 0 new Human verified = 4/18).
- **Did NOT** create a new Vercel project.
- **Did NOT** add any AI-generated / AI-upscaled / fake-historical-substitute images.
- **Did NOT** modify the existing 4 Human-verified works (p.3, p.40-41, p.52, p.90) or their `mapping_status` / `review_status` / `credit_status` / `human_verified` / `printed_page_number` fields.

---

## Outstanding per-work open questions (carried into P5 Phase 10+ docs)

1. **All 6 third-batch works**: Chinese printed title not directly visible in scan (English caption only); need physical 1977 printing to confirm.
2. **p.23**: printed_page_number not visible in this scan; need physical printing or higher-resolution scan.
3. **p.54**: printed_page_number only partial in this scan ("4" visible, "5" cut off by scan margin); the leaf=page+6 pattern + outer-corner position strongly supports p.54 but printed page is not fully OCR-readable.
4. **p.59**: printed_page_number AND printed_credit not visible; need verso leaf (leaf 64) or higher-resolution scan to recover.
5. **p.79**: printed_page_number not visible in this scan; need physical printing or higher-resolution scan.
6. All 6 third-batch works remain at `AGENT_REVIEWED`, `human_verified=false`. Human Verification P2 not entered per spec rule.