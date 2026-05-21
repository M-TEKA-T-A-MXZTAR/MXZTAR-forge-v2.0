#!/usr/bin/env python3
"""
Create a tiny test image for MXZTAR-forge vision service testing.
"""

from pathlib import Path
from PIL import Image, ImageDraw


def main() -> int:
    out_dir = Path("workspace/test_inputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / "mxztar_test_shapes.png"

    image = Image.new("RGB", (512, 512), (28, 28, 28))
    draw = ImageDraw.Draw(image)

    draw.rectangle((80, 80, 230, 230), outline=(220, 190, 80), width=6)
    draw.ellipse((280, 90, 430, 240), outline=(180, 180, 180), width=6)
    draw.polygon([(160, 330), (260, 270), (360, 330), (320, 430), (200, 430)], outline=(120, 200, 220), width=6)
    draw.line((80, 470, 430, 470), fill=(210, 210, 210), width=4)

    image.save(path)

    print("Created test image:")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
