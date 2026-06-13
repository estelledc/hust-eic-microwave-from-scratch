#!/usr/bin/env python3
"""Verify all relative href/src targets in built site/ exist."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
LINK_RE = re.compile(r'(href|src)="([^"#?][^"#?]*)"')

def main() -> int:
    missing: list[str] = []
    for html in SITE.rglob("*.html"):
        for attr, link in LINK_RE.findall(html.read_text(encoding="utf-8")):
            if link.startswith(("http://", "https://", "mailto:", "//", "data:")):
                continue
            target = (html.parent / unquote(link)).resolve()
            if not target.exists():
                missing.append(f"{html.relative_to(SITE)}: {attr}={link}")
    if missing:
        print("Missing links:")
        for m in missing[:30]:
            print(" ", m)
        if len(missing) > 30:
            print(f"  ... and {len(missing) - 30} more")
        return 1
    print("All internal links resolved.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
