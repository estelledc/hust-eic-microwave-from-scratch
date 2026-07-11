#!/usr/bin/env python3
"""Generate the repository's deterministic 1200x630 social preview."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/images/og-microwave.png"


def font_path(*names: str) -> str:
    roots = (
        Path("/usr/share/fonts/truetype/dejavu"),
        Path("/System/Library/Fonts/Supplemental"),
        Path("/Library/Fonts"),
    )
    for root in roots:
        for name in names:
            candidate = root / name
            if candidate.exists():
                return str(candidate)
    raise SystemExit("No supported system font found for OG generation.")


def main() -> None:
    width, height = 1200, 630
    paper = "#F7F3EA"
    surface = "#FFFDF7"
    ink = "#1D211F"
    muted = "#655F55"
    teal = "#0F766E"
    teal_soft = "#D9EEE9"
    orange = "#B45309"
    rule = "#D8CEBD"

    sans = font_path("DejaVuSans.ttf", "Arial.ttf")
    bold = font_path("DejaVuSans-Bold.ttf", "Arial Bold.ttf")
    mono = font_path("DejaVuSansMono.ttf", "Andale Mono.ttf")
    fonts = {
        "eyebrow": ImageFont.truetype(mono, 18),
        "title": ImageFont.truetype(bold, 53),
        "body": ImageFont.truetype(sans, 23),
        "metric": ImageFont.truetype(bold, 30),
        "small": ImageFont.truetype(mono, 15),
        "signal": ImageFont.truetype(bold, 20),
    }

    image = Image.new("RGB", (width, height), paper)
    draw = ImageDraw.Draw(image)

    for x in range(0, width, 40):
        draw.line((x, 0, x, height), fill="#EEE7DA", width=1)
    for y in range(0, height, 40):
        draw.line((0, y, width, y), fill="#EEE7DA", width=1)

    draw.rounded_rectangle((42, 38, 1158, 592), radius=18, fill=surface, outline=rule, width=2)
    draw.line((790, 38, 790, 592), fill=rule, width=2)

    draw.text((82, 78), "OPEN COURSE SYSTEM / JASON XU", font=fonts["eyebrow"], fill=teal)
    draw.multiline_text(
        (78, 126),
        "MICROWAVE\nTECHNOLOGY\nFROM SCRATCH",
        font=fonts["title"],
        fill=ink,
        spacing=2,
    )
    draw.multiline_text(
        (82, 330),
        "Physical intuition -> equations -> problems -> measurement\nA searchable and auditable undergraduate learning path.",
        font=fonts["body"],
        fill=muted,
        spacing=8,
    )

    metrics = (("169", "PAGES"), ("08", "STAGES"), ("63", "AUDITED"))
    for index, (value, label) in enumerate(metrics):
        left = 82 + index * 220
        draw.text((left, 489), value, font=fonts["metric"], fill=ink)
        draw.text((left, 532), label, font=fonts["small"], fill=muted)

    draw.text((832, 78), "LEARNING SIGNAL PATH", font=fonts["eyebrow"], fill=muted)
    panel = (830, 124, 1118, 430)
    draw.rounded_rectangle(panel, radius=14, fill="#F1EBDD", outline=rule, width=2)
    center_y = 280
    points: list[tuple[int, int]] = []
    for x in range(856, 1093):
        y = center_y + int(math.sin((x - 856) / 18) * 42)
        points.append((x, y))
    draw.line(points, fill=teal, width=5)
    draw.line((856, 210, 1092, 210), fill=rule, width=1)
    draw.line((856, 350, 1092, 350), fill=rule, width=1)
    for x, label in ((856, "PROP"), (974, "MODE"), (1092, "VNA")):
        draw.ellipse((x - 8, center_y - 8, x + 8, center_y + 8), fill=orange, outline=surface, width=3)
        draw.text((x - 19, 380), label, font=fonts["small"], fill=muted)
    draw.text((858, 150), "lambda_g / S11 / TE10", font=fonts["small"], fill=teal)

    steps = ("PROPAGATION", "REFLECTION", "BOUNDARY", "PORT", "MEASURE")
    for index, label in enumerate(steps):
        y = 456 + index * 23
        draw.rectangle((832, y + 5, 840, y + 13), fill=teal if index < 4 else orange)
        draw.text((854, y), f"0{index + 1}  {label}", font=fonts["small"], fill=ink)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)
    print(f"Generated {OUTPUT.relative_to(ROOT)} ({width}x{height})")


if __name__ == "__main__":
    main()
