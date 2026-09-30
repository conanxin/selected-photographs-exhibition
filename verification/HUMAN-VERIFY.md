# Human Verification Pack — 2026-09-30

## P1 result

**User decision received in ChatGPT on 2026-09-30: CONFIRM for all four priority works.** The canonical catalog may therefore upgrade p.3, p.40–41, p.52 and p.90 to `HUMAN_VERIFIED`. This records the user's explicit confirmation of the provided evidence pack; it does not add any claim about unknown capture dates or photographer Chinese-character names.

This pack is the next-step evidence package for **your** human-eye verification of four priority works. The Agent (this OpenClaw session) has done its honest best: tesseract OCR has confirmed every printed credit in these scans, and the credit metadata has been migrated into `works.json` with full transparency. This pack is the bridge from Agent-reached review to Human verification.

**Discipline:** the four crops below are **only** crop+resize+stitch operations on the original `assets/leaf-*.jpg` files. No AI upscaling, no generation, no redraw, no OCR replacement. They are non-generative evidence images. Each shows the caption strip of the leaf so a human can confirm printed page number, printed title, printed credit, and visual extent.

**Decision template:** for each work, fill in one of:

```
USER_DECISION=CONFIRM
USER_DECISION=REJECT
USER_DECISION=NEEDS_MORE_EVIDENCE
```

The Agent will **never** fill this in. Only you (the human with a physical 1977 printing of *Selected Photographs from China*) can authoritatively decide.

---

## Work 1 — p.3 — Pupils of a Rural Night School

| Field | Value |
|---|---|
| `book_page` | 3 |
| `scan_leaf` | 9 |
| `printed_title` | Pupils of a Rural Night School |
| `printed_credit` | Chou Chun-yen |
| `catalog_credit_variant` | Chou Chun-jen (old form preserved for transparency) |
| `evidence_image` | `verification/p003-credit.jpg` (bottom 22% of leaf-0009.jpg, 1800px max) |
| `agent_observation` | Caption strip at bottom of leaf reads "Pupils of a Rural Night School Chou Chun-yen" via tesseract OCR. The "Chou Chun-jen" form is the catalog/Internet-Archive-side spelling and does not appear on this leaf. Visual review (2026-09-27) confirmed adult students walking at night below lit classroom windows. |
| `current_mapping_status` | `AGENT_CONFIRMED` |
| `current_review_status` | `AGENT_VISUALLY_REVIEWED` |
| `current_credit_status` | `PRINT_VISIBLE_AGENT_READ` |
| `current_human_verified` | `false` |
| `USER_DECISION` | **CONFIRM — user, 2026-09-30** |
| _If REJECT or NEEDS_MORE_EVIDENCE, please note what specifically is wrong or missing (printed credit spelling? page number? caption text? photo subject?)_ | |

---

## Work 2 — p.40-41 — Diverting Water North (spread)

| Field | Value |
|---|---|
| `book_page` | 40 (left page of spread) and 41 (right page of spread; caption lives on p.41) |
| `scan_leaf` | 46 (left page, photo continuation) + 47 (right page, photo continuation + caption) |
| `printed_title` | Diverting Water North by the Irrigation and Drainage Station at Chiangtu, Kiangsu Province |
| `printed_credit` | Jen Chen-pei |
| `catalog_credit_variant` | none (no alternate spelling known) |
| `evidence_image` | `verification/p040-spread.jpg` (leaf-0046 + leaf-0047 side-by-side stitched, bottom 22% cropped, 1800px max) |
| `agent_observation` | The image is a 2-page spread across scan leaves 46 (left, p.40) and 47 (right, p.41). Continuous horizon line and water surface confirm this is one photograph spanning two printed pages. The caption "Diverting Water North by the Irrigation and Drainage Station at Chiangtu, Kiangsu Province / Jen Chen-pei" appears on leaf 47 only. Tesseract OCR confirmed both printed page numbers (40 on leaf 46, 41 on leaf 47) and the credit. |
| `current_mapping_status` | `AGENT_CONFIRMED` |
| `current_review_status` | `AGENT_VISUALLY_REVIEWED` |
| `current_credit_status` | `PRINT_VISIBLE_AGENT_READ` |
| `current_human_verified` | `false` |
| `USER_DECISION` | **CONFIRM — user, 2026-09-30** |
| _Please note: confirm that p.40-41 is correctly treated as a spread (not two separate works), and that the credit Jen Chen-pei matches printed credit. If a physical copy shows different, please give the printed text verbatim._ | |

---

## Work 3 — p.52 — Storing Grain Against War

| Field | Value |
|---|---|
| `book_page` | 52 |
| `scan_leaf` | 58 |
| `printed_title` | Storing Grain Against War |
| `printed_credit` | Chang Chen |
| `catalog_credit_variant` | Chiang Chen (old form preserved for transparency) |
| `evidence_image` | `verification/p052-credit.jpg` (bottom 22% of leaf-0058.jpg, 1800px max) |
| `agent_observation` | Caption strip at bottom of leaf reads "Storing Grain Against War Chang Chen" via tesseract OCR. The "Chiang Chen" form was the older catalog/Internet-Archive spelling and does not appear on this leaf. Visual review (2026-09-27) confirmed outdoor grain-storage scene with thatched-roof granaries in background and hundreds of cylindrical grain sacks in long rows. |
| `current_mapping_status` | `AGENT_CONFIRMED` |
| `current_review_status` | `AGENT_VISUALLY_REVIEWED` |
| `current_credit_status` | `PRINT_VISIBLE_AGENT_READ` |
| `current_human_verified` | `false` |
| `USER_DECISION` | **CONFIRM — user, 2026-09-30** |
| _If REJECT or NEEDS_MORE_EVIDENCE, please note what specifically (e.g. is the printed credit actually "Chiang Chen" with the older spelling in your printing? Is the page number visible on the leaf in your copy?)_ | |

---

## Work 4 — p.90 — Mobile Medical Team

| Field | Value |
|---|---|
| `book_page` | 90 |
| `scan_leaf` | 96 |
| `printed_title` | Mobile Medical Team |
| `printed_credit` | Chou Chia-kuo |
| `catalog_credit_variant` | Chou Chia-kue (old form preserved for transparency) |
| `evidence_image` | `verification/p090-credit.jpg` (bottom 22% of leaf-0096.jpg, 1800px max) |
| `agent_observation` | Caption strip at bottom of leaf reads "Mobile Medical Team Chou Chia-kuo" via tesseract OCR. The "Chou Chia-kue" form was the older catalog/Internet-Archive spelling and does not appear on this leaf. Visual review (2026-09-27) confirmed rural mountain setting with medical consultation table, women in ethnic-minority dress (embroidered aprons, decorated headwear), one holding an infant, and a Chinese-character sign on the table front (the Chinese sign characters are partially legible at 1800px; a higher-resolution crop of the sign itself could help — please note this in NEEDS_MORE_EVIDENCE if relevant). |
| `current_mapping_status` | `AGENT_CONFIRMED` |
| `current_review_status` | `AGENT_VISUALLY_REVIEWED` |
| `current_credit_status` | `PRINT_VISIBLE_AGENT_READ` |
| `current_human_verified` | `false` |
| `USER_DECISION` | **CONFIRM — user, 2026-09-30** |
| _If REJECT or NEEDS_MORE_EVIDENCE, please note what specifically (printed credit spelling? Chinese-character sign on table? page number?)_ | |

---

## Applied result

The four CONFIRM decisions have been applied to `works.json`: `human_verified: true`, `mapping_status: HUMAN_VERIFIED`, `review_status: HUMAN_VERIFIED`, and `credit_status: HUMAN_VERIFIED` for p.3, p.40–41, p.52 and p.90. Other works remain at their prior evidence states.

If you have a physical 1977 printing of the book and can confirm any of the other 8 works (p.2, p.6, p.38, p.39, p.83, p.87, p.98, p.100), those are also welcome — but the four above are the priority set for this verification round.

The Agent did not originate these decisions; they were supplied explicitly by the user. Future works still require a new explicit human decision before any `HUMAN_VERIFIED` upgrade.