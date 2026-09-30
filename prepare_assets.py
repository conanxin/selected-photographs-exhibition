#!/usr/bin/env python3
"""Acquire this edition's JP2 scan archive and prepare complete-page previews.

No OCR, generative processing, crop, identity resolution, or automatic approval.
Requires Pillow with JPEG 2000 support. Run start.py for automatic local setup.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IDENTIFIER = 'selectedphotographsfromchina'
META_URL = f'https://archive.org/metadata/{IDENTIFIER}'
ZIP_NAME = f'{IDENTIFIER}_jp2.zip'
MAPPING_URL = f'https://archive.org/download/{IDENTIFIER}/{IDENTIFIER}_page_numbers.json'
# Scan leaves only, NOT asserted printed page numbers or confirmed front matter.
EVIDENCE_LEAVES = (0, 1, 2, 3, 4, 5, 6, 47, 59, 106)


def digest(path: Path, kind: str = 'sha256') -> str:
    h = hashlib.new(kind)
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def acquire(root: Path) -> tuple[Path, dict[str, Any]]:
    """Use the canonical public item, without guessed mirrors or credentials."""
    source = root / 'source'
    source.mkdir(exist_ok=True)
    request = urllib.request.Request(META_URL, headers={'User-Agent': 'SPFC-Exhibition-Research/0.2'})
    print('读取原条目文件清单…', flush=True)
    with urllib.request.urlopen(request, timeout=30) as response:
        metadata = json.load(response)
    if metadata.get('metadata', {}).get('identifier') != IDENTIFIER:
        raise ValueError('返回的条目不是目标摄影集；未继续下载。')
    file = next((f for f in metadata.get('files', []) if f.get('name') == ZIP_NAME), None)
    if file is None:
        raise ValueError('该条目当前未列出所需 JP2 ZIP；请重新检查原条目。')
    write_json(source / 'metadata.json', metadata)
    url = f'https://archive.org/download/{IDENTIFIER}/{ZIP_NAME}'
    target = source / ZIP_NAME
    if not target.exists():
        partial = target.with_suffix('.zip.part')
        print('下载原书逐页扫描包（不是重新生成照片）…', flush=True)
        req = urllib.request.Request(url, headers={'User-Agent': 'SPFC-Exhibition-Research/0.2'})
        with urllib.request.urlopen(req, timeout=120) as response, partial.open('wb') as output:
            total = 0
            last_print = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                total += len(chunk)
                if total - last_print >= 10 * 1024 * 1024:
                    print(f'  已接收 {total / 1024 / 1024:.1f} MiB', flush=True)
                    last_print = total
        expected_size = int(file.get('size', 0))
        if expected_size and partial.stat().st_size != expected_size:
            raise ValueError('下载长度与条目记录不匹配；保留 .part 供检查，未当作原书使用。')
        if not zipfile.is_zipfile(partial):
            raise ValueError('服务器没有返回有效 ZIP；可能是错误页面，未写入展览。')
        partial.replace(target)
    return target, {'source_url': url, 'expected_md5': file.get('md5'), 'metadata': metadata}


def prepare(root: Path, zip_path: Path, *, expected_md5: str | None = None,
            source_url: str | None = None) -> dict[str, Any]:
    """Convert known scan leaves to full-page JPEGs, keeping review pending."""
    from PIL import Image, features
    if not features.check('jpg_2000'):
        raise RuntimeError('当前 Pillow 没有 JPEG 2000 支持。请安装包含 OpenJPEG 的 Pillow wheel。')
    root = Path(root)
    zip_path = Path(zip_path)
    if expected_md5 and digest(zip_path, 'md5') != expected_md5:
        raise ValueError('原扫描包与条目记录的 MD5 不匹配，未更新展览。')
    if not zipfile.is_zipfile(zip_path):
        raise ValueError('输入不是有效的原书 ZIP 文件。')
    works = json.loads((root / 'works.json').read_text(encoding='utf-8'))
    assets_dir = root / 'assets'
    assets_dir.mkdir(exist_ok=True)
    pattern = re.compile(rf'^{re.escape(IDENTIFIER)}_(\d+)\.jp2$', re.IGNORECASE)
    decoded: dict[int, dict[str, Any]] = {}
    missing: list[int] = []
    with zipfile.ZipFile(zip_path) as archive:
        leaf_files: dict[int, str] = {}
        for name in archive.namelist():
            match = pattern.fullmatch(Path(name).name)
            if not match:
                continue
            leaf = int(match.group(1))
            if leaf in leaf_files:
                raise ValueError(f'扫描序号 {leaf} 存在重复文件（ambiguous leaf），未自动择一。')
            leaf_files[leaf] = name
        if not leaf_files:
            raise ValueError('ZIP 内未找到与目标条目标识相符的 JP2 页文件。')
        requested = sorted(set(EVIDENCE_LEAVES) | {int(w['leaf']) for w in works})
        for leaf in requested:
            if leaf not in leaf_files:
                missing.append(leaf)
                continue
            name = leaf_files[leaf]
            raw = archive.read(name)
            with Image.open(io.BytesIO(raw)) as image:
                image.load()
                size = list(image.size)
                if image.mode not in ('RGB', 'L'):
                    image = image.convert('RGB')
                # Only shrink if necessary; never crop, stretch or invent pixels.
                image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
                dest = assets_dir / f'leaf-{leaf:04}.jpg'
                kwargs = {'icc_profile': image.info['icc_profile']} if image.info.get('icc_profile') else {}
                image.save(dest, 'JPEG', quality=93, subsampling=0, **kwargs)
                decoded[leaf] = {
                    'leaf': leaf,
                    'archive_member': name,
                    'source_page_sha256': hashlib.sha256(raw).hexdigest(),
                    'source_size': size,
                    'display_size': list(image.size),
                    'display_file': dest.relative_to(root).as_posix(),
                    'display_sha256': digest(dest),
                    'cropped': False,
                    'representation': 'FULL_SCAN_PAGE',
                    'review_status': 'PENDING_VISUAL_REVIEW',
                }
    rows = []
    for w in works:
        row = {'page': w['page'], 'leaf': w['leaf'], 'mapping_source': MAPPING_URL,
               'mapping_status': 'PLATFORM_AUTOMATIC_UNVERIFIED',
               'review_status': 'PENDING_VISUAL_REVIEW'}
        if w['leaf'] in decoded:
            row.update(decoded[w['leaf']])
            row['status'] = 'DECODED'
        else:
            row['status'] = 'MISSING_LEAF'
        rows.append(row)
    loaded = sum(r['status'] == 'DECODED' for r in rows)
    receipt = {
        'version': '0.2',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'status': 'ACQUIRED_PENDING_REVIEW' if loaded == len(rows) else 'PARTIAL_PENDING_REVIEW',
        'source_identifier': IDENTIFIER,
        'source_url': source_url,
        'source_kind': 'CANONICAL_DOWNLOAD' if source_url else 'LOCAL_ZIP_UNVERIFIED_ORIGIN',
        'source_file': zip_path.name,
        'source_bytes': zip_path.stat().st_size,
        'source_sha256': digest(zip_path),
        'metadata_md5_matched': bool(expected_md5),
        'archive_leaf_count': len(leaf_files),
        'requested_work_count': len(works),
        'loaded_count': loaded,
        'human_verified_count': 0,
        'works': rows,
        'evidence_pages': [decoded[n] for n in EVIDENCE_LEAVES if n in decoded],
        'missing_scan_leaves': missing,
        'note': '下载及解码不是人工核验。完整书页不是已裁出的摄影作品。第106叶仅为书末候选，不标作已确认第100页。',
    }
    # works.json is the editable catalog; this is only its generated inline copy.
    html_path = root / 'index.html'
    if html_path.exists():
        html = html_path.read_text(encoding='utf-8')
        catalog_json = json.dumps(works, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        expression = r'(<script\b[^>]*\bid=[\"\']work-data[\"\'][^>]*>).*?(</script>)'
        updated, count = re.subn(expression, lambda match: match.group(1) + catalog_json + match.group(2), html, flags=re.S)
        if count != 1:
            raise ValueError('网页中作品数据区不唯一或不存在；未更新资料清单。')
        html_path.write_text(updated, encoding='utf-8')
    write_json(root / 'ingest-receipt.json', receipt)
    payload = json.dumps(receipt, ensure_ascii=True, separators=(',', ':')).replace('<', '\\u003c')
    (assets_dir / 'assets.js').write_text('window.SPFC_ASSETS = ' + payload + ';\n', encoding='utf-8')
    return receipt


def run(root: Path, local_zip: Path | None = None) -> dict[str, Any]:
    """Entry shared by the CLI and start.py."""
    try:
        if local_zip is not None:
            receipt = prepare(root, local_zip)
        else:
            source, details = acquire(root)
            receipt = prepare(root, source, expected_md5=details['expected_md5'], source_url=details['source_url'])
        print(f"接入 {receipt['loaded_count']}/{receipt['requested_work_count']} 张候选书页；人工核验 0 张。", flush=True)
        return receipt
    except Exception as exc:
        failure = {'status': 'ACQUISITION_FAILED', 'error': str(exc),
                   'created_at': datetime.now(timezone.utc).isoformat(),
                   'real_book_download_confirmed_this_run': False,
                   'note': '失败不改变既有书目结论，不自动选择替代作品，也不覆盖已有图像清单。'}
        write_json(root / 'last-error.json', failure)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', type=Path, help='已有的原条目 JP2 ZIP，跳过联网下载')
    args = parser.parse_args()
    try:
        result = run(Path(__file__).resolve().parent, args.zip)
        sys.exit(0 if result['loaded_count'] else 1)
    except Exception as exc:
        print(f'未完成图像接入：{exc}\n详细错误：last-error.json', file=sys.stderr)
        sys.exit(1)
