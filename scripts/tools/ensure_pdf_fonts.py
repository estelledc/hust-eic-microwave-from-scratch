#!/usr/bin/env python3
"""Download bundled Noto Sans SC woff2 for offline PDF export (CJK fallback)."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FONTS_DIR = ROOT / "assets" / "fonts"

# Fontsource CDN — Chinese Simplified subset, regular + bold
FONT_FILES: dict[str, str] = {
    "noto-sans-sc-regular.woff2": (
        "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc@5.2.5/files/"
        "noto-sans-sc-chinese-simplified-400-normal.woff2"
    ),
    "noto-sans-sc-bold.woff2": (
        "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc@5.2.5/files/"
        "noto-sans-sc-chinese-simplified-700-normal.woff2"
    ),
}


def ensure_fonts(*, force: bool = False) -> list[Path]:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for name, url in FONT_FILES.items():
        dest = FONTS_DIR / name
        if dest.exists() and not force:
            downloaded.append(dest)
            continue
        print(f"Downloading {name} …")
        urllib.request.urlretrieve(url, dest)
        downloaded.append(dest)
    return downloaded


def main() -> None:
    force = "--force" in sys.argv
    paths = ensure_fonts(force=force)
    print(f"PDF fonts ready ({len(paths)} files) in {FONTS_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
