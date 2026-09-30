#!/usr/bin/env python3
"""Run in the extracted directory: python3 start.py
Downloads scan assets, then serves the existing exhibition on localhost only.
"""
from __future__ import annotations
import argparse
import http.server
import importlib
import subprocess
import sys
from functools import partial
from pathlib import Path


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip',type=Path,help='已有原书 JP2 ZIP；不联网获取原书')
    parser.add_argument('--port',type=int,default=8080)
    parser.add_argument('--prepare-only',action='store_true',help='接入后退出，不启动浏览器服务')
    parser.add_argument('--serve-only',action='store_true',help='仅查看已存在的页面，不下载或处理图像')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    if not args.serve_only:
        deps=root/'.deps'
        sys.path.insert(0,str(deps))
        try:
            importlib.import_module('PIL')
        except ImportError:
            print('在项目目录安装 Pillow（不改动系统 Python）…',flush=True)
            subprocess.run([sys.executable,'-m','pip','install','--quiet','--target',str(deps),'Pillow'],check=True)
            importlib.invalidate_caches()
        import prepare_assets
        receipt=prepare_assets.run(root,args.zip)
        if not receipt['loaded_count']:
            print('没有可解码的目标书页，未启动展览。',file=sys.stderr)
            return 1
    if args.prepare_only:
        return 0
    handler=partial(http.server.SimpleHTTPRequestHandler,directory=str(root))
    with http.server.ThreadingHTTPServer(('127.0.0.1',args.port),handler) as server:
        print(f'本地展厅：http://127.0.0.1:{args.port}\n按 Ctrl+C 停止。此操作不部署公网。',flush=True)
        try: server.serve_forever()
        except KeyboardInterrupt: pass
    return 0


if __name__=='__main__':
    try: sys.exit(main())
    except (Exception,) as exc:
        print(f'未完成：{exc}\n已有 ZIP 可改用：python3 start.py --zip 原书.zip',file=sys.stderr)
        sys.exit(1)
