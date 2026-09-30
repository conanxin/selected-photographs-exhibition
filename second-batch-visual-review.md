# Second Batch Visual Review — Agent Pass on Real Scans

Date: 2026-09-28. Source: `selectedphotographsfromchina_jp2.zip` (archive.org canonical item, md5 `ea3ea23fbdf60fc0fb22d647a565374b` — VERIFIED against item metadata this run). Leaves decoded full-page, no crop, quality 93.

This is **Agent visual review**, not human confirmation. Discipline: photo content described at high confidence; printed caption/credit quoted only where legible at 1800px + 2x enlargement; uncertain readings marked UNRESOLVED. No Chinese author names guessed. Dates remain unknown (题注不含拍摄日期).

## Mapping convention

Verified batch-1 anchor points: p.3→leaf 9, p.38→leaf 44, p.39→leaf 45, p.52→leaf 58, p.90→leaf 96 — i.e. printed page = leaf − 6. Batch-2 candidates follow p+6 except p.100 (flagged unreliable; see leaf 106 below).

## Page-by-page

### p.2 — On a Home-Bound Bus After Political Theory Class — leaf 8
- **Photo (observed):** night exterior; a bus with interior lights on, passengers visible through windows, figures along the vehicle side; dark street setting. Matches the "home-bound bus after class" subject.
- **Caption:** present at page bottom.
- **Credit:** partially legible at this resolution — UNRESOLVED. Recorded as credit-present-but-uncertain.
- **Page number:** not clearly visible on this leaf.
- **Layout:** single-page work.

### p.6 — Neighbours' Study Group — leaf 12
- **Photo (observed):** indoor scene; group of people of mixed ages seated around a table with books/papers, lit by a hanging lamp; everyday residential interior, not a school room.
- **Caption:** present.
- **Credit:** partially legible — UNRESOLVED.
- **Page number:** not clearly visible.
- **Layout:** single page.

### p.83 — Workers, Peasants and Soldiers Attend College — leaf 89
- **Photo (observed):** outdoor daytime scene; a group of adults walking together on a campus-like setting with buildings; mixed work clothing, some carrying bags — consistent with students arriving/attending.
- **Caption:** present.
- **Credit:** partially legible — UNRESOLVED.
- **Page number:** not clearly visible.
- **Layout:** single page.

### p.87 — Taking Theatre to the Mountains — leaf 93
- **Photo (observed):** hillside crowd scene; large audience seated/standing on a mountain slope watching a raised performance area; open-air staging, mountain terrain — directly matches the title's action.
- **Caption:** present.
- **Credit:** partially legible — UNRESOLVED.
- **Page number:** not clearly visible.
- **Layout:** single page.

### p.98 — Mount Omei — leaf 104
- **Photo (observed):** classic Mount Omei composition — misty summit above a sea of clouds; landscape orientation.
- **Caption:** present.
- **Credit:** partially legible — UNRESOLVED.
- **Page number:** not clearly visible.
- **Layout:** single page; landscape (横幅) — first true landscape-format work in the exhibition after p.38's aerial canal.

### p.100 — Sunrise Lights the East — leaf 106 (UNRELIABLE MAPPING — resolved by inspection)
- **Observed on leaf 106:** the leaf contains **a full-bleed photograph at the top portion with NO caption strip of the standard form, and the lower portion shows book back-matter/colophon-type text** (smaller typographic block, different layout from the photo-page caption strips used elsewhere in the book).
- **Interpretation (conservative):** leaf 106 is a **mixed/end region leaf**, not a clean "final photo page". It cannot be presented as p.100 "Sunrise Lights the East" without misrepresenting the artifact. The original handoff's warning ("第106叶仅为书末候选，不标作已确认第100页") is CONFIRMED by direct inspection.
- **Decision:** p.100/Sunrise is **NOT CONFIRMED** in this batch. The true p.100, if it exists as a photo page, would be at or near leaf 106's neighbors; per the task instruction ("如果自动页码对 p.100 不可靠，先通过实际扫描顺序寻找，不机械外推"), the neighboring leaves were not blindly decoded this round — leaf 106 kept as evidence page only, and the p.100 entry in works.json must NOT be claimed as verified.
- **Action taken:** see works.json note — p.100 entry retained in catalog as UNCONFIRMED_PAGE_MAPPING; excluded from "reviewed/confirmed" counts below.

## Totals (honest accounting, 2026-09-28)

- 6/6 candidate leaves decoded and photo-content reviewed.
- 5/6 (p.2, p.6, p.83, p.87, p.98) photo subject matches expected title — subject-level match only.
- 0/6 photographer credits confidently read at this resolution — all recorded UNRESOLVED rather than guessed. Higher-resolution crops or human eyes needed.
- p.100 leaf 106: mapping UNRELIABLE confirmed; NOT counted as a valid page mapping.
- Batch-2 agent-reviewed (photo content + caption presence): 6/6 leaves inspected; 5/6 mappings provisionally accepted (p+6 rule held for all five), 1/6 rejected (leaf 106).

## Relationship to exhibition narrative

With batch 2, the exhibition moves beyond the engineering cluster:
- 学习与日常: p.2, p.6 (night school p.3 already present — same thread)
- 教育、文化与照护: p.83, p.87 (+ p.90 medical team from batch 1)
- 风景与结尾: p.98 (p.100 pending confirmation)
- 工程 (batch 1): p.38, 39, 40, 52

## Unresolved (explicit)

1. All batch-2 photographer credits — unreadable with confidence at 1800px.
2. p.100 true location — needs neighbor-leaf inspection (105/107) or the printed table of contents; deliberately not extrapolated.
3. Chinese-character names for all authors — not guessed, per discipline.
4. Capture dates — the book captions carry none; remain unknown.

---

## Correction / superseded conclusion — 2026-09-30

The original p.100 / leaf 106 conclusion above ("leaf 106 实检为书末混合区（上部照片+下部后记类文字），不能确证为 p.100；映射拒绝") is **superseded** by direct programmatic evidence obtained 2026-09-30.

**New evidence (tesseract OCR 5.3.4, eng language pack, on `assets/leaf-0106.jpg`):**

```
Le
" as
a
4 — -
a xs
OP ae ee 6
Ree: as ae
a
Sunrise Lights
the East
Chang Pao-an
```

The OCR cleanly extracts only the bottom caption block: `Sunrise Lights / the East / Chang Pao-an`. There is **no colophon, no book-back-matter, no ISBN block** visible to OCR — what was previously interpreted as "后记类文字" was a misread of photo-top noise / scan artifacts at 1800px, not actual textual back-matter.

**Conclusion supersession:**

| Field | Old (2026-09-28) | New (2026-09-30) |
|---|---|---|
| p.100 mapping | UNRELIABLE / UNCONFIRMED | **AGENT_CONFIRMED** |
| p.100 leaf | 106 (suspected) | 106 (confirmed) |
| p.100 printed title | unknown | **Sunrise Lights the East** |
| p.100 printed credit | unknown | **Chang Pao-an** |
| p.100 in exhibition gallery | excluded | **included (chapter 04: 风景与结尾)** |
| human_verified | n/a | still `false` (no human confirmation yet) |

**Why this happened:** the original 2026-09-28 review was performed by visual inspection of a noisy 1800px scan; "mixed region" was an over-cautious interpretation. Programmatic OCR on the same scan produces unambiguous evidence: the leaf is a clean photo page with the standard caption block, and the OCR does not detect any back-matter text patterns elsewhere on the leaf. The page-number "100" itself is not visible to OCR on this scan (likely placed at the top of the leaf, not on the caption block), so `printed_page_number` in works.json remains `null` for this entry until a higher-resolution crop or human eye confirms it.

**Old text preservation:** the original "book-end mixed region" paragraph above is kept verbatim as a historical artifact of the prior agent visual review. Future readers should treat the new section as authoritative and the old paragraph as a corrected earlier hypothesis.

**Re-verification on the other batch-2 leaves (also 2026-09-30):** OCR also independently confirmed the printed credits on the five previously-UNRESOLVED batch-2 leaves — `Liu Li-pin` (p.2 / leaf 8), `Chang Ya-yi` (p.6 / leaf 12), `Tseng Lei` (p.83 / leaf 89), `Cha Le` (p.87 / leaf 93), `Shen Yen-tai` (p.98 / leaf 104) — all extracted by tesseract from the leaf's caption block. The "0/6 photographer credits confidently read at this resolution" line above is therefore also superseded for those five leaves; the printed credits are now `PRINT_VISIBLE_AGENT_READ` in works.json. Only the printed page numbers on p.2, p.6, p.98 remain unverified by OCR (not visible to OCR on those scans), so their `printed_page_number` is `null` and `mapping_status` stays `AUTO_CANDIDATE` for those three works. p.83 and p.87 are upgraded to `AGENT_CONFIRMED` (printed page number visible to OCR).