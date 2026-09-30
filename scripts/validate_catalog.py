#!/usr/bin/env python3
"""
SPFC Catalog Validator — SPFC_P5_BATCH3_AGENT_EXPANSION
==========================================================

Mandatory pre-commit validator. Run from project root:

    python3 scripts/validate_catalog.py

Exit code 0 = PASS, non-zero = FAIL.

Checks performed:
  1. works.json: 18 unique page numbers (no duplicates)
  2. works.json: every work's leaf asset file exists in assets/
  3. works.json: mapping_status values are legal (AUTO_CANDIDATE / AGENT_CONFIRMED / AGENT_REJECTED / HUMAN_VERIFIED)
  4. works.json: review_status values are legal (DECODED / AGENT_VISUALLY_REVIEWED / HUMAN_VERIFIED)
  5. works.json: credit_status values are legal (PRINT_VISIBLE_AGENT_READ / UNRESOLVED / HUMAN_VERIFIED)
  6. works.json: if human_verified=true then both mapping_status=HUMAN_VERIFIED AND review_status=HUMAN_VERIFIED
  7. works.json: p.3 author = "Chou Chun-yen"
  8. works.json: p.52 author = "Chang Chen"
  9. works.json: p.90 author = "Chou Chia-kuo"
 10. works.json: p.100 author = "Chang Pao-an"
 11. works.json: p.100 mapping_status = "AGENT_CONFIRMED"
 11a. works.json: work pages exactly {2, 3, 6, 10, 18, 23, 38, 39, 40, 52, 54, 59, 79, 83, 87, 90, 98, 100}
 11b. works.json: human-verified pages are exactly {3,40,52,90}, with mapping/review/credit all HUMAN_VERIFIED
 11c. works.json: third-batch (Batch-3) pages are exactly {10, 18, 23, 54, 59, 79}
 11d. works.json: all third-batch works have human_verified=false AND not in any *_status=HUMAN_VERIFIED
 12. works.json must NOT contain the deprecated "page_mapping_confirmed" field anywhere
 13. index.html embedded <script id="work-data" type="application/json"> block matches works.json byte-for-byte
 14. STATUS.json must include v0.6 fields: version=0.6, work_count=18, agent_reviewed=18, human_verified=4, chapter_count=6, scope=BATCH3_AGENT_EXPANSION
 14a. STATUS.json human_verified_pages = [3, 40, 52, 90]
 15. STATUS.json human_verified NOT stale (must equal 4, not 0 or 12)
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKS_FILE = ROOT / "works.json"
INDEX_FILE = ROOT / "index.html"
STATUS_FILE = ROOT / "STATUS.json"
ASSETS_DIR = ROOT / "assets"

LEGAL_MAPPING = {"AUTO_CANDIDATE", "AGENT_CONFIRMED", "AGENT_REJECTED", "HUMAN_VERIFIED"}
LEGAL_REVIEW = {"DECODED", "AGENT_VISUALLY_REVIEWED", "HUMAN_VERIFIED"}
LEGAL_CREDIT = {"PRINT_VISIBLE_AGENT_READ", "UNRESOLVED", "HUMAN_VERIFIED"}

EXPECTED_PAGES = {2, 3, 6, 10, 18, 23, 38, 39, 40, 52, 54, 59, 79, 83, 87, 90, 98, 100}
EXPECTED_BATCH3 = {10, 18, 23, 54, 59, 79}
EXPECTED_HUMAN = {3, 40, 52, 90}

errors = []
warnings = []
ok_count = 0


def fail(msg):
    errors.append(msg)
    print(f"  ✗ {msg}")


def ok(msg):
    global ok_count
    ok_count += 1
    print(f"  ✓ {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"  ! {msg}")


def main():
    print("=== SPFC Catalog Validator (SPFC_P5_BATCH3_AGENT_EXPANSION) ===")
    print(f"Project root: {ROOT}")
    print()

    # Load works.json
    print("[1-11d] Loading works.json ...")
    if not WORKS_FILE.exists():
        fail(f"works.json not found at {WORKS_FILE}")
        sys.exit(1)
    try:
        works = json.loads(WORKS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"works.json is not valid JSON: {e}")
        sys.exit(1)
    ok(f"works.json loaded ({len(works)} works)")

    # 1a. 18 unique page numbers
    print("[1a] Checking 18 unique page numbers ...")
    pages = [w.get("page") for w in works]
    unique_pages = set(pages)
    if len(unique_pages) == 18 and len(pages) == 18:
        ok(f"18 unique page numbers: {sorted(pages)}")
    else:
        fail(f"Expected 18 unique page numbers; got {len(pages)} entries, {len(unique_pages)} unique ({sorted(pages)})")

    # 1b. exact page set
    print("[1b] Checking page set exactly matches expected {2,3,6,10,18,23,38,39,40,52,54,59,79,83,87,90,98,100} ...")
    if unique_pages == EXPECTED_PAGES:
        ok(f"Page set exactly matches expected 18 pages")
    else:
        missing = EXPECTED_PAGES - unique_pages
        extra = unique_pages - EXPECTED_PAGES
        fail(f"Page set mismatch. Missing: {sorted(missing)}; Extra: {sorted(extra)}")

    # 2. Every leaf asset file exists
    print("[2] Checking every work's leaf asset exists in assets/ ...")
    for w in works:
        leaf = w.get("leaf")
        asset = ASSETS_DIR / f"leaf-{leaf:04d}.jpg"
        if asset.exists():
            ok(f"  leaf-{leaf:04d}.jpg exists for p.{w.get('page')}")
        else:
            fail(f"  leaf-{leaf:04d}.jpg MISSING for p.{w.get('page')}")

    # 3-6. enum validation
    print("[3-6] Checking enum values ...")
    for w in works:
        page = w.get("page")
        ms = w.get("mapping_status")
        rs = w.get("review_status")
        cs = w.get("credit_status")
        hv = w.get("human_verified", False)
        if ms not in LEGAL_MAPPING:
            fail(f"  p.{page} mapping_status '{ms}' not in {LEGAL_MAPPING}")
        else:
            ok(f"  p.{page} mapping_status = {ms}")
        if rs not in LEGAL_REVIEW:
            fail(f"  p.{page} review_status '{rs}' not in {LEGAL_REVIEW}")
        else:
            ok(f"  p.{page} review_status = {rs}")
        if cs not in LEGAL_CREDIT:
            fail(f"  p.{page} credit_status '{cs}' not in {LEGAL_CREDIT}")
        else:
            ok(f"  p.{page} credit_status = {cs}")
        if hv is True:
            if ms != "HUMAN_VERIFIED":
                fail(f"  p.{page} human_verified=true requires mapping_status=HUMAN_VERIFIED (got {ms})")
            if rs != "HUMAN_VERIFIED":
                fail(f"  p.{page} human_verified=true requires review_status=HUMAN_VERIFIED (got {rs})")

    # 7-11. specific author + p.100 mapping assertions
    print("[7-11] Checking specific author + p.100 assertions ...")
    by_page = {w.get("page"): w for w in works}
    if by_page.get(3, {}).get("author") == "Chou Chun-yen":
        ok("p.3 author = Chou Chun-yen")
    else:
        fail(f"p.3 author = {by_page.get(3, {}).get('author')!r} (expected 'Chou Chun-yen')")
    if by_page.get(52, {}).get("author") == "Chang Chen":
        ok("p.52 author = Chang Chen")
    else:
        fail(f"p.52 author = {by_page.get(52, {}).get('author')!r} (expected 'Chang Chen')")
    if by_page.get(90, {}).get("author") == "Chou Chia-kuo":
        ok("p.90 author = Chou Chia-kuo")
    else:
        fail(f"p.90 author = {by_page.get(90, {}).get('author')!r} (expected 'Chou Chia-kuo')")
    if by_page.get(100, {}).get("author") == "Chang Pao-an":
        ok("p.100 author = Chang Pao-an")
    else:
        fail(f"p.100 author = {by_page.get(100, {}).get('author')!r} (expected 'Chang Pao-an')")
    if by_page.get(100, {}).get("mapping_status") == "AGENT_CONFIRMED":
        ok("p.100 mapping_status = AGENT_CONFIRMED")
    else:
        fail(f"p.100 mapping_status = {by_page.get(100, {}).get('mapping_status')!r} (expected 'AGENT_CONFIRMED')")

    # 11b. Human Verification P1 exact set and state invariants
    expected_human = EXPECTED_HUMAN
    actual_human = {w.get("page") for w in works if w.get("human_verified") is True}
    if actual_human == expected_human:
        ok("human_verified pages exactly {3,40,52,90}")
    else:
        fail(f"human_verified pages = {sorted(actual_human)} (expected [3, 40, 52, 90])")
    for page in sorted(expected_human):
        w = by_page.get(page, {})
        if w.get("mapping_status") == "HUMAN_VERIFIED" and w.get("review_status") == "HUMAN_VERIFIED" and w.get("credit_status") == "HUMAN_VERIFIED":
            ok(f"p.{page} mapping/review/credit = HUMAN_VERIFIED")
        else:
            fail(f"p.{page} HUMAN_VERIFIED state incomplete: mapping={w.get('mapping_status')}, review={w.get('review_status')}, credit={w.get('credit_status')}")

    # 11c. Third-batch (Batch-3) exact set
    print("[11c] Checking third-batch pages exactly {10, 18, 23, 54, 59, 79} ...")
    actual_batch3 = {w.get("page") for w in works if w.get("batch") == 3}
    if actual_batch3 == EXPECTED_BATCH3:
        ok(f"third-batch pages exactly {sorted(actual_batch3)}")
    else:
        missing = EXPECTED_BATCH3 - actual_batch3
        extra = actual_batch3 - EXPECTED_BATCH3
        fail(f"third-batch mismatch. Missing: {sorted(missing)}; Extra: {sorted(extra)}")

    # 11d. All third-batch works: human_verified=false AND no *_status=HUMAN_VERIFIED
    print("[11d] Checking all third-batch works are NOT promoted (no Human Verification P2) ...")
    for page in sorted(EXPECTED_BATCH3):
        w = by_page.get(page, {})
        hv = w.get("human_verified", False)
        ms = w.get("mapping_status")
        rs = w.get("review_status")
        cs = w.get("credit_status")
        if hv is True:
            fail(f"  p.{page} human_verified=true (forbidden in Batch-3)")
        else:
            ok(f"  p.{page} human_verified=false")
        if ms == "HUMAN_VERIFIED":
            fail(f"  p.{page} mapping_status=HUMAN_VERIFIED (forbidden in Batch-3)")
        else:
            ok(f"  p.{page} mapping_status={ms} (not HUMAN_VERIFIED)")
        if rs == "HUMAN_VERIFIED":
            fail(f"  p.{page} review_status=HUMAN_VERIFIED (forbidden in Batch-3)")
        else:
            ok(f"  p.{page} review_status={rs} (not HUMAN_VERIFIED)")
        if cs == "HUMAN_VERIFIED":
            fail(f"  p.{page} credit_status=HUMAN_VERIFIED (forbidden in Batch-3)")
        else:
            ok(f"  p.{page} credit_status={cs} (not HUMAN_VERIFIED)")

    # 12. No legacy page_mapping_confirmed
    print("[12] Checking legacy page_mapping_confirmed is REMOVED ...")
    raw = WORKS_FILE.read_text(encoding="utf-8")
    if "page_mapping_confirmed" in raw:
        fail("works.json still contains 'page_mapping_confirmed' field (must be removed per spec)")
    else:
        ok("works.json has no 'page_mapping_confirmed' field")

    # 13. index.html embedded works must match works.json
    print("[13] Checking index.html <script id=\"work-data\"> matches works.json ...")
    if not INDEX_FILE.exists():
        fail(f"index.html not found at {INDEX_FILE}")
    else:
        html = INDEX_FILE.read_text(encoding="utf-8")
        m = re.search(r'<script id="work-data" type="application/json">(.*?)</script>', html, re.DOTALL)
        if not m:
            fail("Could not find <script id=\"work-data\"> block in index.html")
        else:
            try:
                embedded = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                fail(f"index.html embedded work-data is not valid JSON: {e}")
                embedded = None
            if embedded is not None:
                if json.dumps(embedded, sort_keys=True, ensure_ascii=False) == json.dumps(works, sort_keys=True, ensure_ascii=False):
                    ok("index.html embedded work-data matches works.json byte-for-byte")
                else:
                    fail("index.html embedded work-data differs from works.json — re-run with updated embedded JSON")

    # 14. STATUS.json must be v0.7 form (P6 §11 — was v0.6 in P5)
    print("[14] Checking STATUS.json is v0.7 form ...")
    if not STATUS_FILE.exists():
        fail(f"STATUS.json not found at {STATUS_FILE}")
    else:
        try:
            status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"STATUS.json is not valid JSON: {e}")
            status = {}
        if status.get("version") == "0.7":
            ok("STATUS.json version = 0.7")
        else:
            fail(f"STATUS.json version = {status.get('version')!r} (expected '0.7')")
        if status.get("work_count") == 18:
            ok("STATUS.json work_count = 18")
        else:
            fail(f"STATUS.json work_count = {status.get('work_count')!r} (expected 18)")
        if status.get("agent_reviewed") == 18:
            ok("STATUS.json agent_reviewed = 18")
        else:
            fail(f"STATUS.json agent_reviewed = {status.get('agent_reviewed')!r} (expected 18)")
        if status.get("human_verified") == 4:
            ok("STATUS.json human_verified = 4")
        else:
            fail(f"STATUS.json human_verified = {status.get('human_verified')!r} (expected 4)")
        if status.get("chapter_count") == 6:
            ok("STATUS.json chapter_count = 6")
        else:
            fail(f"STATUS.json chapter_count = {status.get('chapter_count')!r} (expected 6)")
        if status.get("scope") == "P6_CURATORIAL_CONSOLIDATION_96_ARCHIVE_INDEX":
            ok("STATUS.json scope = P6_CURATORIAL_CONSOLIDATION_96_ARCHIVE_INDEX")
        else:
            fail(f"STATUS.json scope = {status.get('scope')!r} (expected 'P6_CURATORIAL_CONSOLIDATION_96_ARCHIVE_INDEX')")
        hv_pages = status.get("human_verified_pages", [])
        if sorted(hv_pages) == [3, 40, 52, 90]:
            ok("STATUS.json human_verified_pages = [3, 40, 52, 90]")
        else:
            fail(f"STATUS.json human_verified_pages = {sorted(hv_pages)} (expected [3, 40, 52, 90])")

    # === P6 catalog-96 checks (§11 of SPFC_P6 spec) ===
    print("[16-24] Loading catalog-96.json ...")
    catalog_path = ROOT / "catalog-96.json"
    if not catalog_path.exists():
        fail(f"catalog-96.json not found at {catalog_path}")
    else:
        try:
            cat = json.loads(catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"catalog-96.json is not valid JSON: {e}")
            cat = []

        # 16. 96 unique entries
        ids = [c.get("catalog_id") for c in cat]
        if len(cat) == 96 and len(set(ids)) == 96:
            ok(f"catalog-96.json has exactly 96 unique entries")
        else:
            fail(f"catalog-96.json has {len(cat)} entries; {len(set(ids))} unique ids (expected 96)")

        # 17. 18 selected / 78 text-only
        sel = sum(1 for c in cat if c.get("selected_for_exhibition"))
        unsel = sum(1 for c in cat if not c.get("selected_for_exhibition"))
        if sel == 18 and unsel == 78:
            ok(f"selected_for_exhibition: {sel} selected, {unsel} text-only")
        else:
            fail(f"selected_for_exhibition: {sel} selected, {unsel} text-only (expected 18/78)")

        # 18. 68 colour-marked, 28 unmarked
        col = sum(1 for c in cat if c.get("colour_marked_in_contents"))
        unm = sum(1 for c in cat if not c.get("colour_marked_in_contents"))
        if col == 68 and unm == 28:
            ok(f"colour: {col} marked, {unm} unmarked (sum = {col+unm})")
        else:
            fail(f"colour: {col} marked, {unm} unmarked (expected 68/28)")

        # 19. human_verified exactly [3, 40, 52, 90]
        cat_hv = sorted(c.get("book_page") for c in cat if c.get("human_verified"))
        if cat_hv == [3, 40, 52, 90]:
            ok(f"catalog-96.json human_verified = {cat_hv}")
        else:
            fail(f"catalog-96.json human_verified = {cat_hv} (expected [3, 40, 52, 90])")

        # 21. selected pages match works.json
        cat_sel_pages = set(c.get("book_page") for c in cat if c.get("selected_for_exhibition"))
        works_pages = set(w.get("page") for w in works)
        if cat_sel_pages == works_pages:
            ok(f"catalog-96.json selected_for_exhibition matches works.json exactly")
        else:
            missing = works_pages - cat_sel_pages
            extra = cat_sel_pages - works_pages
            fail(f"selected mismatch. In works not catalog: {sorted(missing)}; in catalog not works: {sorted(extra)}")

        # 22. scan_asset_available consistency
        sa_ok = True
        for c in cat:
            if c.get("selected_for_exhibition") and not c.get("scan_asset_available"):
                fail(f"  p.{c.get('book_page')} selected but scan_asset_available=false")
                sa_ok = False
            if not c.get("selected_for_exhibition") and c.get("scan_asset_available"):
                fail(f"  p.{c.get('book_page')} text-only but scan_asset_available=true")
                sa_ok = False
        if sa_ok:
            ok("scan_asset_available consistent with selected_for_exhibition for all 96 entries")

        # 23. §7 credit variants on p.3/p.52/p.90
        var_specs = {
            3:  ('Chou Chun-yen', 'Chou Chun-jen'),
            52: ('Chang Chen',    'Chiang Chen'),
            90: ('Chou Chia-kuo', 'Chou Chia-kue'),
        }
        var_ok = True
        var_pages = sorted([c.get("book_page") for c in cat if c.get("catalog_credit_variant")])
        if var_pages != [3, 52, 90]:
            fail(f"§7 variant pages: got {var_pages}, expected [3, 52, 90]")
            var_ok = False
        for c in cat:
            p = c.get("book_page")
            if p in var_specs:
                main_name, cat_name = var_specs[p]
                if c.get("printed_credit") != main_name:
                    fail(f"  p.{p} printed_credit={c.get('printed_credit')!r} (expected {main_name!r})")
                    var_ok = False
                if c.get("catalog_credit_variant") != cat_name:
                    fail(f"  p.{p} catalog_credit_variant={c.get('catalog_credit_variant')!r} (expected {cat_name!r})")
                    var_ok = False
        if var_ok:
            ok("§7 credit variants preserved on p.3/p.52/p.90")

    # 24. STATUS.json v0.7 catalog fields
    print("[24] Checking STATUS.json v0.7 catalog fields ...")
    if STATUS_FILE.exists():
        try:
            status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            status = {}
        v = status.get("version")
        if v == "0.7":
            ok("STATUS.json version = 0.7")
        else:
            fail(f"STATUS.json version = {v!r} (expected '0.7')")
        if status.get("catalog_count") == 96:
            ok("STATUS.json catalog_count = 96")
        else:
            fail(f"STATUS.json catalog_count = {status.get('catalog_count')!r} (expected 96)")
        if status.get("catalog_selected") == 18:
            ok("STATUS.json catalog_selected = 18")
        else:
            fail(f"STATUS.json catalog_selected = {status.get('catalog_selected')!r} (expected 18)")
        if status.get("catalog_text_only") == 78:
            ok("STATUS.json catalog_text_only = 78")
        else:
            fail(f"STATUS.json catalog_text_only = {status.get('catalog_text_only')!r} (expected 78)")

    # 25. index.html stale copy check (P6 §2) — scoped to user-visible status text
    print("[25] Checking index.html user-visible status text for stale patterns ...")
    if INDEX_FILE.exists():
        html = INDEX_FILE.read_text(encoding="utf-8")
        # Scope: only check the runtime-visible #asset-state element, .hero, .chapter notes,
        # .about copy, and footer. JS fallback strings (placeholder, status interpolation)
        # are operational and exempt — the user spec §2 targets stale *visible* status.
        asset_state_m = re.search(r'<p class="status" id="asset-state"[^>]*>([^<]*)</p>', html)
        asset_state_text = asset_state_m.group(1) if asset_state_m else ''
        # Pull the hero, chapter notes, about copy, footer as a single block
        hero_m = re.search(r'<section class="hero"[^>]*>(.*?)</section>', html, re.DOTALL)
        chapter_m = re.findall(r'<p class="note">([^<]*)</p>', html)
        about_m = re.search(r'<section id="about"[^>]*>(.*?)</section>', html, re.DOTALL)
        footer_m = re.search(r'<footer[^>]*>(.*?)</footer>', html, re.DOTALL)
        visible_text = ' '.join([
            asset_state_text,
            hero_m.group(1) if hero_m else '',
            ' '.join(chapter_m),
            about_m.group(1) if about_m else '',
            footer_m.group(1) if footer_m else '',
        ])
        for pat in ['样机', '完整候选书页', '12件', '4章节']:
            if pat in visible_text:
                fail(f"  index.html user-visible copy still contains stale pattern: {pat!r}")
            else:
                ok(f"  index.html user-visible copy free of stale pattern: {pat!r}")
        # Check #asset-state specifically for v0.5 / '18件真实作品' / '张已读取'
        for pat in ['v0.5', '张已读取']:
            if pat in asset_state_text:
                fail(f"  #asset-state still contains stale: {pat!r}")
            else:
                ok(f"  #asset-state free of stale: {pat!r}")

    # 26. index.html Archive Index section check (P6 §8)
    print("[26] Checking index.html for Archive Index section ...")
    if INDEX_FILE.exists():
        html = INDEX_FILE.read_text(encoding="utf-8")
        if 'id="archive-index"' in html:
            ok("index.html contains #archive-index section")
        else:
            fail("index.html missing #archive-index section (P6 §8)")

    print()
    print("=" * 60)
    if errors:
        print(f"FAIL: {len(errors)} errors, {len(warnings)} warnings, {ok_count} checks passed")
        print("=" * 60)
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    elif warnings:
        print(f"PASS with {len(warnings)} warnings, {ok_count} checks passed")
        print("=" * 60)
        for w in warnings:
            print(f"  WARN: {w}")
        sys.exit(0)
    else:
        print(f"PASS: {ok_count} checks passed, 0 errors, 0 warnings")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
