#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import argparse
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# ------------------------- DO NOT CHANGE ------------------------- #
def extract_map(map_path: Path, dest_root: Path):
    """
    Read a .js.map file and write each embedded source
    into dest_root/<original/source/path>, shared globally.
    """
    with map_path.open(encoding="utf-8") as f:
        sm = json.load(f)

    sources = sm.get("sources", [])
    contents = sm.get("sourcesContent", [])

    if not sources or not contents:
        print(f"⚠️  Skipping {map_path.name}: no sourcesContent")
        return

    for src, content in zip(sources, contents):
        if not content:
            continue
        # preserve directory structure, strip webpack prefix
        rel = src[len("webpack:///"):] if src.startswith("webpack:///") else src
        rel = rel.lstrip('/')
        out_file = dest_root / rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        print(f"✅ Extracted from {map_path.name} → {out_file}")
# ----------------------------------------------------------------- #

DOWNLOAD_ROOT = Path("sourcemap-download")         # fixed location

def download_map(js_url: str) -> Path | None:
    """
    Append '.map' to js_url, attempt download, save under DOWNLOAD_ROOT.
    Returns the saved Path or None on failure.
    """
    map_url = js_url.rstrip('/') + '.map'
    name = Path(urlparse(map_url).path).name or 'unnamed.map'
    dest = DOWNLOAD_ROOT / name

    try:
        r = requests.get(map_url, timeout=15)
        if r.ok and r.text.lstrip().startswith('{'):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(r.text, encoding='utf-8')
            print(f"⬇️  {map_url} → {dest}")
            return dest
        else:
            print(f"⚠️  Failed ({r.status_code}) {map_url}")
    except requests.RequestException as e:
        print(f"⚠️  Error {map_url}: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Given a TXT file of JS URLs, append .map, download concurrently, then extract sources."
    )
    parser.add_argument(
        '-l', '--list',
        dest='url_file',
        required=True,
        help='TXT file containing one JS URL per line'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        required=True,
        help='Directory to write extracted source files'
    )
    parser.add_argument(
        '-c', '--concurrency',
        type=int,
        default=min(32, (os.cpu_count() or 4) * 2),
        help='Number of parallel download workers (default: %(default)s)'
    )
    args = parser.parse_args()

    url_file = Path(args.url_file)
    if not url_file.is_file():
        print(f"Error: {url_file!r} is not a file.")
        sys.exit(1)

    output_root = Path(args.output_dir)
    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    with url_file.open() as f:
        urls = [ln.strip() for ln in f if ln.strip()]

    # -------- concurrent download -------- #
    downloaded: list[Path] = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        future_to_url = {pool.submit(download_map, u): u for u in urls}
        for fut in as_completed(future_to_url):
            path = fut.result()
            if path:
                downloaded.append(path)

    # -------- extract each .map -------- #
    for map_path in downloaded:
        extract_map(map_path, output_root)

if __name__ == "__main__":
    main()
