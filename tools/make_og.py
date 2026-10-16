"""Generate 1200x630 OGP cards for pages without a hand-made thumbnail.

Matches the style of blog/dev/assets/005_thumb.jpg (blue→green gradient, light card,
site icon, label, big title, colored chips). Re-run after editing PAGES:

    python tools/make_og.py
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "public_site"
OUT_DIR = SITE / "assets" / "og"
ICON = SITE / "assets" / "icon-512.png"
FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"

W, H = 1200, 630
TOP, BOTTOM = (2, 132, 199), (16, 185, 129)
CARD_BG = (240, 245, 247)
TITLE = (15, 23, 42)
MUTED = (71, 85, 105)
ACCENT = (2, 132, 199)
CHIP_COLORS = [(217, 119, 6), (2, 132, 199), (5, 150, 105)]


@dataclass(frozen=True)
class Card:
    slug: str
    label: str
    title: str
    chips: tuple[str, ...]
    footer: str = "dyussuca.com"


PAGES = [
    Card("home", "ポケスリ 料理計算機", "料理エナジー＆備蓄", ("全79レシピ", "3ジャンル備蓄", "料理記録")),
    Card("exp", "ポケスリ 育成シミュ", "EXP＆アメ計算機", ("必要アメ数", "ゆめのかけら", "おひるね島")),
    Card("blog", "dyussuca.com ブログ", "攻略コラム＆開発日誌", ("雑談・考察", "開発日誌")),
    Card("site", "ポケスリ計算機ツール", "dyussuca.com", ("料理計算機", "EXP計算機", "ブログ")),
    Card("dev-001", "開発日誌 #001", "平日＆日曜の分割調理", ("平日18食", "日曜3食", "大成功倍率")),
    Card("column-001", "雑談・考察 #001", "Ver.3.6.0 アメ仕様考察", ("段階的アメEXP", "おひるね島", "ゴンベ還元")),
    Card("column-002", "雑談・考察 #002", "キャンチケ備蓄戦略", ("鍋1.5倍", "3ジャンル備蓄", "除外フィルター")),
    Card("column-004", "雑談・考察 #004", "ニンジャサラダの寿命", ("鍋容量57〜94", "ABBウェーニバル")),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD, size)


def gradient() -> Image.Image:
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM))
        draw.line([(0, y), (W, y)], fill=color)
    return img


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 40 and draw.textlength(text, font=font(size)) > max_width:
        size -= 4
    return font(size)


def render(card: Card) -> Image.Image:
    img = gradient()
    box = (66, 84, W - 66, H - 84)

    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((box[0], box[1] + 10, box[2], box[3] + 10), 44, fill=90)
    img.paste((0, 0, 0), mask=shadow.filter(ImageFilter.GaussianBlur(18)))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, 44, fill=CARD_BG)

    # Site icon in a white circle.
    cx, cy, r = 202, 232, 80
    draw.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), fill=(226, 232, 240))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255))
    icon = Image.open(ICON).convert("RGBA").resize((2 * r - 16, 2 * r - 16), Image.LANCZOS)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, *icon.size), fill=255)
    img.paste(icon, (cx - r + 8, cy - r + 8), Image.composite(icon.getchannel("A"), mask, mask))

    text_x = 322
    draw.text((text_x, 156), card.label, font=font(36), fill=ACCENT)
    title_font = fit_font(draw, card.title, box[2] - 40 - text_x, 80)
    draw.text((text_x, 206), card.title, font=title_font, fill=TITLE)

    chip_font = font(34)
    x = 124
    for i, chip in enumerate(card.chips):
        w = draw.textlength(chip, font=chip_font) + 56
        draw.rounded_rectangle((x, 372, x + w, 446), 37, fill=CHIP_COLORS[i % len(CHIP_COLORS)])
        draw.text((x + 28, 409), chip, font=chip_font, fill=(255, 255, 255), anchor="lm")
        x += w + 22

    draw.text((124, 480), card.footer, font=font(28), fill=MUTED)
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for card in PAGES:
        path = OUT_DIR / f"{card.slug}.jpg"
        render(card).save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
