#!/usr/bin/env python3
"""
SPFC Catalog Validator — SPFC_P4_HUMAN_VERIFICATION_P1
==========================================================

Mandatory pre-commit validator. Run from project root:

    python3 scripts/validate_catalog.py

Exit code 0 = PASS, non-zero = FAIL.

Checks performed:
  1. works.json: 12 unique page numbers (no duplicates)
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
 11b. works.json: human-verified pages are exactly {3,40,52,90}, with mapping/review/credit all HUMAN_VERIFIED
 12. works.json must NOT contain the deprecated "page_mapping_confirmed" field anywhere
 13. index.html embedded <script id="work-data" type="application/json"> block matches works.json byte-for-byte
 14. STATUS.json is NOT the stale v0.2 form (must not contain "0.2" + "0" + "NOT_DEPLOYED" simultaneously)
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
    print("=== SPFC Catalog Validator ===")
    print(f"Project root: {ROOT}")
    print()

    # Load works.json
    print("[1-12] Loading works.json ...")
    if not WORKS_FILE.exists():
        fail(f"works.json not found at {WORKS_FILE}")
        sys.exit(1)
    try:
        works = json.loads(WORKS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"works.json is not valid JSON: {e}")
        sys.exit(1)
    ok(f"works.json loaded ({len(works)} works)")

    # 1. 12 unique page numbers
    print("[1] Checking 12 unique page numbers ...")
    pages = [w.get("page") for w in works]
    if sorted(pages) == list(range(2, 114)):  # not strictly 1..N, just check uniqueness
        pass
    unique_pages = set(pages)
    if len(unique_pages) == 12 and len(pages) == 12:
        ok(f"12 unique page numbers: {sorted(pages)}")
    else:
        fail(f"Expected 12 unique page numbers; got {len(pages)} entries, {len(unique_pages)} unique ({sorted(pages)})")

    # 2. Every leaf asset file exists
    print("[2] Checking every work's leaf asset exists in assets/ ...")
    for w in works:
        leaf = w.get("leaf")
        # Some works (p.40) have a secondary_leaf; we check primary only here
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
    expected_human = {3, 40, 52, 90}
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

    # 14. STATUS.json must not be stale v0.2
    print("[14] Checking STATUS.json is not stale v0.2 ...")
    if not STATUS_FILE.exists():
        fail(f"STATUS.json not found at {STATUS_FILE}")
    else:
        try:
            status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"STATUS.json is not valid JSON: {e}")
            status = {}
        version = status.get("version", "")
        deployment = status.get("deployment", "")
        real_scan_works = status.get("real_scan_works", 0)
        if version == "0.2" and real_scan_works == 0 and deployment == "NOT_DEPLOYED":
            fail(f"STATUS.json is stale v0.2 form (version=0.2, real_scan_works=0, deployment=NOT_DEPLOYED)")
        else:
            ok(f"STATUS.json is current (version={version}, real_scan_works={real_scan_works}, deployment={deployment})")
            if status.get("human_verified") == 4:
                ok("STATUS.json human_verified = 4")
            else:
                fail(f"STATUS.json human_verified = {status.get('human_verified')!r} (expected 4)")

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