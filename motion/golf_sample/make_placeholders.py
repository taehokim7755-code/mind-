"""실제 스톡/AI 이미지가 들어오기 전까지 쓸 임시 배경 일러스트 생성.

결과: motion/golf_sample/assets/placeholder/bg_01.png ~ bg_06.png (2400x1350, 켄번스 여유분 포함)
실제 이미지를 motion/golf_sample/assets/bg_01.jpg 처럼 넣으면 sample.py가 그걸 우선 사용합니다.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BW, BH = 2400, 1350
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "placeholder")


def vgrad(top, bot, h=BH, w=BW, curve=1.0):
    y = (np.linspace(0, 1, h) ** curve)[:, None, None]
    arr = np.array(top)[None, None, :] * (1 - y) + np.array(bot)[None, None, :] * y
    return Image.fromarray(np.broadcast_to(arr, (h, w, 3)).astype(np.uint8), "RGB")


def glow(img, cx, cy, r, color, strength=1.0):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.6))
    a = np.asarray(img).astype(float) + np.asarray(layer).astype(float) * strength
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def hill(img, base_y, amp, freq, phase, color, blur=0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pts = [(x, base_y + amp * math.sin(x * freq + phase) + amp * 0.4 * math.sin(x * freq * 2.7 + phase * 1.3))
           for x in range(0, BW + 20, 20)]
    ImageDraw.Draw(layer).polygon(pts + [(BW, BH), (0, BH)], fill=color + (255,))
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(layer, (0, 0), layer)
    return pts


def mist(img, y, h, alpha, blur=60):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle([0, y, BW, y + h], fill=(235, 230, 220, int(255 * alpha)))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(layer, (0, 0), layer)


def bokeh(img, n, color, rmin, rmax, y0, y1, alpha=0.25, seed=1):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        r = rnd.uniform(rmin, rmax)
        x, y = rnd.uniform(0, BW), rnd.uniform(y0, y1)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (int(255 * alpha * rnd.uniform(0.4, 1)),))
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    img.paste(layer, (0, 0), layer)


def grain(img, amount=10, seed=0):
    rng = np.random.default_rng(seed)
    a = np.asarray(img).astype(np.int16) + rng.normal(0, amount, (BH, BW, 1)).astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def stripes(img, y_top, color_a, color_b, n=9):
    """원근감 있는 페어웨이 잔디 줄무늬."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    vx = BW * 0.55
    for i in range(-n, n + 1):
        x0 = vx + i * 40
        x1 = vx + i * 520
        x0b = vx + (i + 1) * 40
        x1b = vx + (i + 1) * 520
        d.polygon([(x0, y_top), (x0b, y_top), (x1b, BH), (x1, BH)], fill=(color_a if i % 2 else color_b) + (255,))
    return layer


def golf_ball(img, cx, cy, r, light=(1, -1)):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r * 1.1, cy + r * 0.7, cx + r * 1.3, cy + r * 1.15], fill=(0, 0, 0, 120))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.15))
    d = ImageDraw.Draw(layer)
    for k in range(int(r), 0, -2):  # 구 셰이딩
        t = k / r
        c = int(160 + 95 * (1 - t) ** 0.6)
        ox, oy = (1 - t) * r * 0.35 * -light[0], (1 - t) * r * 0.35 * light[1]
        d.ellipse([cx + ox - k, cy + oy - k, cx + ox + k, cy + oy + k], fill=(c, c, min(255, c + 4), 255))
    rnd = random.Random(3)
    for _ in range(int(r * 1.2)):  # 딤플
        a, rr = rnd.uniform(0, 2 * math.pi), r * math.sqrt(rnd.uniform(0, 0.85))
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        s = r * 0.035
        d.ellipse([x - s, y - s, x + s, y + s], fill=(205, 205, 210, 255))
    img.paste(layer, (0, 0), layer)


def flagstick(img, x, y, h, w=6, flag=(210, 60, 50), pole=(235, 235, 230)):
    d = ImageDraw.Draw(img)
    d.line([(x, y), (x, y - h)], fill=pole, width=w)
    d.polygon([(x, y - h), (x + h * 0.32, y - h + h * 0.09), (x, y - h + h * 0.18)], fill=flag)


# ---------- 장면들 ----------
def bg_dawn():
    img = vgrad((40, 58, 92), (236, 168, 104), curve=1.3)
    img = glow(img, BW * 0.68, BH * 0.52, 260, (255, 200, 120), 0.9)
    hill(img, 700, 40, 0.0016, 0.5, (58, 82, 70), blur=4)
    hill(img, 780, 30, 0.002, 2.0, (44, 70, 52), blur=2)
    mist(img, 720, 120, 0.55)
    fw = stripes(img, 820, (62, 112, 58), (70, 124, 64))
    img.paste(fw, (0, 0), fw)
    hill(img, 1080, 60, 0.0014, 4.0, (30, 56, 36))
    flagstick(img, int(BW * 0.58), 830, 90, 3)
    mist(img, 800, 80, 0.35, 40)
    return grain(img, 7)


def bg_ball_hole():
    img = vgrad((52, 88, 50), (88, 140, 70), curve=0.7)
    bokeh(img, 40, (255, 230, 170), 20, 70, 0, 380, 0.35)
    blur_top = img.crop((0, 0, BW, 420)).filter(ImageFilter.GaussianBlur(12))
    img.paste(blur_top, (0, 0))
    d = ImageDraw.Draw(img)
    hx, hy = BW * 0.56, BH * 0.66
    d.ellipse([hx - 330, hy - 95, hx + 330, hy + 95], fill=(16, 22, 14))
    d.ellipse([hx - 330, hy - 95, hx + 330, hy + 40], fill=(28, 36, 24))
    d.arc([hx - 330, hy - 95, hx + 330, hy + 95], 180, 360, fill=(230, 232, 225), width=10)
    golf_ball(img, int(hx - 300), int(hy - 160), 120)
    # 깃대 그림자
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(hx + 60, hy), (BW, hy - 260), (BW, hy - 200), (hx + 60, hy + 20)], fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.paste(sh, (0, 0), sh)
    return grain(img, 8)


def bg_scorecard():
    img = vgrad((30, 34, 30), (14, 16, 14))
    img = glow(img, BW * 0.3, BH * 0.2, 400, (90, 80, 60), 0.6)
    d = ImageDraw.Draw(img, "RGBA")
    # 지폐들 (기울어진 사각형)
    def note(cx, cy, w, h, ang, col):
        pts = []
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            x, y = sx * w / 2, sy * h / 2
            pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
        d.polygon(pts, fill=col, outline=(0, 0, 0, 80))
        d.ellipse([cx - h * 0.25, cy - h * 0.25, cx + h * 0.25, cy + h * 0.25], outline=(255, 255, 255, 60), width=4)
    note(820, 760, 820, 400, -0.18, (196, 160, 92, 255))
    note(1000, 820, 820, 400, 0.08, (118, 150, 112, 255))
    note(1180, 700, 820, 400, -0.05, (196, 160, 92, 255))
    # 스코어카드
    cx0, cy0 = 1350, 300
    card = Image.new("RGBA", (900, 620), (244, 238, 222, 255))
    cd = ImageDraw.Draw(card)
    for r in range(7):
        cd.line([(30, 90 + r * 80), (870, 90 + r * 80)], fill=(150, 150, 140, 255), width=3)
    for c in range(10):
        cd.line([(30 + c * 93, 90), (30 + c * 93, 570)], fill=(150, 150, 140, 255), width=3)
    cd.rectangle([30, 30, 870, 80], fill=(46, 86, 60, 255))
    card = card.rotate(9, expand=True, resample=Image.BICUBIC)
    img.paste(card, (cx0, cy0), card)
    golf_ball(img, 700, 400, 110)
    golf_ball(img, 2000, 1080, 95)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    return grain(img, 9)


def bg_putter():
    img = vgrad((20, 30, 22), (64, 112, 60), curve=0.8)
    img = glow(img, BW * 0.2, BH * 0.25, 300, (255, 210, 150), 0.7)
    bokeh(img, 30, (255, 220, 160), 20, 60, 0, 500, 0.3, seed=5)
    d = ImageDraw.Draw(img)
    # 퍼터 샤프트와 헤드
    d.line([(1150, -50), (1330, 900)], fill=(190, 192, 196), width=26)
    d.line([(1150, -50), (1330, 900)], fill=(230, 232, 236), width=8)
    d.rounded_rectangle([1080, 880, 1560, 1000], 30, fill=(40, 42, 46))
    d.rounded_rectangle([1080, 880, 1560, 920], 20, fill=(90, 94, 100))
    d.line([(1300, 890), (1340, 890)], fill=(240, 240, 240), width=6)
    golf_ball(img, 1820, 920, 95)
    # 강한 측광 비네팅
    v = Image.new("L", img.size, 0)
    ImageDraw.Draw(v).ellipse([300, 100, 2300, 1500], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    img = Image.composite(img, Image.new("RGB", img.size, (6, 10, 8)), v)
    return grain(img, 9)


def bg_dusk_silhouette():
    img = vgrad((52, 40, 78), (246, 132, 72), curve=1.6)
    img = glow(img, BW * 0.5, BH * 0.7, 300, (255, 170, 90), 1.0)
    hill(img, 860, 25, 0.002, 1.0, (40, 30, 40), blur=3)
    hill(img, 960, 18, 0.0025, 3.0, (20, 16, 24))
    d = ImageDraw.Draw(img)
    # 골퍼 실루엣 (뒷모습)
    x, base = 1100, 960
    d.ellipse([x - 38, base - 380, x + 38, base - 300], fill=(12, 10, 16))
    d.polygon([(x - 70, base - 300), (x + 70, base - 300), (x + 55, base - 150), (x - 55, base - 150)], fill=(12, 10, 16))
    d.polygon([(x - 55, base - 150), (x + 55, base - 150), (x + 50, base), (x + 12, base), (x, base - 100),
               (x - 12, base), (x - 50, base)], fill=(12, 10, 16))
    d.line([(x + 40, base - 200), (x + 110, base - 10)], fill=(12, 10, 16), width=10)
    flagstick(img, 1500, 960, 150, 6, (12, 10, 16), (12, 10, 16))
    return grain(img, 7)


def bg_resthouse():
    img = vgrad((120, 160, 120), (70, 110, 70))
    bokeh(img, 50, (255, 240, 200), 30, 90, 0, 700, 0.35, seed=9)
    img = img.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(img)
    # 창틀 / 처마
    d.rectangle([0, 0, BW, 120], fill=(70, 46, 30))
    for x in (0, 780, 1580, 2340):
        d.rectangle([x, 0, x + 60, 760], fill=(80, 54, 36))
    # 나무 테이블
    tbl = vgrad((150, 104, 66), (96, 62, 36), h=600)
    img.paste(tbl, (0, 760))
    for y in range(780, BH, 90):
        d.line([(0, y), (BW, y + 10)], fill=(80, 52, 30), width=3)
    # 아이스 음료 잔
    for gx, liquid in ((900, (220, 150, 60)), (1300, (120, 70, 40))):
        d.rounded_rectangle([gx - 110, 420, gx + 110, 860], 30, fill=(230, 236, 236))
        d.rounded_rectangle([gx - 95, 520, gx + 95, 845], 24, fill=liquid)
        for k in range(4):
            d.rounded_rectangle([gx - 70 + k * 30, 540 + k * 40, gx - 20 + k * 30, 590 + k * 40], 8, fill=(240, 244, 244))
        d.line([(gx + 40, 380), (gx + 10, 700)], fill=(240, 80, 70), width=14)
    # 골프 장갑
    d.rounded_rectangle([1650, 820, 2050, 960], 50, fill=(244, 244, 240))
    d.rounded_rectangle([1660, 830, 1780, 900], 30, fill=(40, 70, 50))
    img = glow(img, BW * 0.85, BH * 0.15, 350, (255, 220, 160), 0.5)
    return grain(img, 7)


SCENES = [bg_dawn, bg_ball_hole, bg_scorecard, bg_putter, bg_dusk_silhouette, bg_resthouse]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate(SCENES, 1):
        fn().save(os.path.join(OUT, f"bg_{i:02d}.png"))
        print("saved", f"bg_{i:02d}.png")
