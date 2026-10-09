"""그늘집심리학 EP.02 — 내기 판에서 먼저 무너지는 골퍼 6가지 유형 (무음 모션그래픽, 16:9).

실행: python3 motion/golf_ep02/ep02.py            -> motion/out/golf_ep02.mp4
     python3 motion/golf_ep02/ep02.py --preview 20 45 120   (해당 초의 프레임만 PNG로)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from engine import (W, H, back_out, clamp, draw, ease_in, ease_in_out, ease_out, prog,  # noqa: E402
                    render, rgba, text, text_block, window, wrap)

from content import CHANNEL, EP, TAGLINE, TITLE1, TITLE2, TYPES  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "golf_ep02.mp4")

# ---------- 브랜드 팔레트 (그늘집 = 페어웨이 그린 + 크림 + 앰버) ----------
BG_TOP = (20, 46, 35)
BG_BOT = (10, 26, 20)
CARD = (27, 58, 44)
CARD_LINE = (52, 92, 72)
CREAM = (245, 237, 218)
MUTED = (158, 180, 162)
AMBER = (236, 178, 72)
RED = (228, 96, 80)
DARK = (8, 20, 15)
WHITE = (255, 255, 255)

# ---------- 타임라인 ----------
T_INTRO, T_LOGO, T_TITLE = 0.0, 6.0, 10.5
T_TYPES = 17.0
TYPE_LEN = 32.0
T_SUMMARY = T_TYPES + TYPE_LEN * len(TYPES)  # 209
T_OUTRO = T_SUMMARY + 15.0                    # 224
DURATION = T_OUTRO + 13.0                     # 237

# ---------- 배경: 잔디 깎은 줄무늬 + 비네팅 ----------
STRIPE = 160


def _make_bg():
    bw = W + STRIPE * 2
    y = np.linspace(0, 1, H)[:, None]
    x = np.arange(bw)[None, :]
    base = np.array(BG_TOP) * (1 - y[..., None]) + np.array(BG_BOT) * y[..., None]
    base = np.broadcast_to(base, (H, bw, 3)).copy()
    # 대각선 잔디 줄무늬
    yy = np.arange(H)[:, None]
    band = (((x + yy * 0.45) // (STRIPE / 2)) % 2).astype(float)
    base += band[..., None] * 5.0
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-350, -280, W + 350, H + 280], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(180))
    return img, vig


BG_IMG, VIGNETTE = _make_bg()
DARK_IMG = Image.new("RGB", (W, H), (4, 12, 9))


def background(t):
    off = int(t * 12) % STRIPE
    img = BG_IMG.crop((off, 0, off + W, H))
    return Image.composite(img, DARK_IMG, VIGNETTE)


# ---------- 공용 그래픽 ----------
def flag(img, x, y, size, alpha, t=0.0, grow=1.0):
    """홀 깃발: (x, y)=홀 위치."""
    d = draw(img)
    h = size * grow
    d.ellipse([x - size * 0.35, y - size * 0.08, x + size * 0.35, y + size * 0.08], fill=rgba(DARK, alpha))
    d.line([(x, y), (x, y - h)], fill=rgba(CREAM, alpha), width=max(2, int(size * 0.05)))
    if grow > 0.6:
        fa = alpha * clamp((grow - 0.6) / 0.4)
        wave = math.sin(t * 4) * size * 0.04
        top = y - h
        d.polygon([(x, top), (x + size * 0.55, top + size * 0.14 + wave), (x, top + size * 0.3)], fill=rgba(AMBER, fa))


def chip(img, x, y, label, color, alpha, anchor="l", size=30):
    if alpha <= 0:
        return
    from engine import text_width
    w = text_width(label, "Bold", size) + size * 1.2
    h = size * 1.7
    left = x if anchor == "l" else x - w / 2
    draw(img).rounded_rectangle([left, y - h / 2, left + w, y + h / 2], h / 2, fill=rgba(color, alpha))
    text(img, left + w / 2, y, label, "Bold", size, DARK, alpha)


def brand_header(img, t):
    a = window(t, T_TITLE + 0.3, DURATION - 1.0, 0.8, 0.6) * 0.9
    if a <= 0:
        return
    flag(img, 96, 92, 56, a, t)
    text(img, 132, 70, CHANNEL, "Bold", 34, CREAM, a, anchor="lm")
    text(img, W - 80, 70, EP, "Bold", 30, MUTED, a, anchor="rm")


# ---------- 인트로 ----------
def scene_intro(img, t):
    out = 1 - ease_in(prog(t, 5.4, 0.6))
    a1, a2 = ease_out(prog(t, 0.3, 0.6)), ease_out(prog(t, 1.2, 0.6))
    text(img, W / 2, 380 + (1 - a1) * 30, "같은 실력인데,", "Bold", 80, CREAM, a1 * out)
    text(img, W / 2, 490 + (1 - a2) * 30, "내기만 걸리면", "Bold", 80, CREAM, a2 * out)
    s = back_out(prog(t, 2.2, 0.7))
    text(img, W / 2, 650, "왜 먼저 무너질까?", "Black", 136, AMBER, ease_out(prog(t, 2.2, 0.3)) * out, scale=max(s, 0.01))

    # 홀 앞에서 립아웃되는 공
    d = draw(img)
    hx, hy = 1250, 900
    ga = ease_out(prog(t, 0.2, 0.5)) * out
    d.ellipse([hx - 60, hy - 16, hx + 60, hy + 16], fill=rgba(DARK, ga))
    d.line([(hx, hy), (hx, hy - 150)], fill=rgba(CREAM, ga * 0.8), width=4)
    d.polygon([(hx, hy - 150), (hx + 70, hy - 132), (hx, hy - 114)], fill=rgba(AMBER, ga * 0.8))
    p = ease_out(prog(t, 0.5, 3.4))
    if t < 3.9:
        bx, by = -40 + (hx - 50 + 40) * p, hy
    else:
        q = ease_out(prog(t, 3.9, 0.9))
        bx = hx - 10 + 120 * q
        by = hy - math.sin(q * math.pi) * 22 - 4 * q
    r = 18
    d.ellipse([bx - r, by - r * 2 + 4, bx + r, by + 4], fill=rgba(WHITE, ga))


# ---------- 로고 ----------
def scene_logo(img, t):
    lt = t - T_LOGO
    a = window(lt, 0, 4.5, 0.4, 0.5)
    grow = ease_out(prog(lt, 0.1, 0.9))
    flag(img, W / 2, 470, 240, a, t, grow)
    s = back_out(prog(lt, 0.7, 0.6))
    text(img, W / 2, 590, CHANNEL, "Black", 128, CREAM, a * ease_out(prog(lt, 0.7, 0.3)), scale=max(s, 0.01))
    text(img, W / 2, 700, TAGLINE, "Medium", 42, MUTED, a * ease_out(prog(lt, 1.4, 0.6)))


# ---------- 에피소드 타이틀 ----------
def scene_title(img, t):
    lt = t - T_TITLE
    a = window(lt, 0, 6.5, 0.4, 0.6)
    chip(img, W / 2, 330, EP, AMBER, a * ease_out(prog(lt, 0.1, 0.4)), anchor="m", size=34)
    a1 = ease_out(prog(lt, 0.4, 0.6))
    text(img, W / 2, 470 + (1 - a1) * 30, TITLE1, "Black", 96, CREAM, a * a1)
    s = back_out(prog(lt, 1.0, 0.7))
    text(img, W / 2, 615, TITLE2, "Black", 150, AMBER, a * ease_out(prog(lt, 1.0, 0.3)), scale=max(s, 0.01))
    d = draw(img)
    for i in range(6):
        p = back_out(prog(lt, 2.2 + i * 0.18, 0.4))
        if p <= 0:
            continue
        cx = W / 2 + (i - 2.5) * 110
        r = 34 * p
        d.ellipse([cx - r, 800 - r, cx + r, 800 + r], outline=rgba(AMBER, a), width=4)
        text(img, cx, 800, str(i + 1), "Bold", 34, CREAM, a * clamp(p), scale=max(p, 0.01))


# ---------- 유형별 아이콘 ----------
def icon(img, kind, cx, cy, t, a):
    d = draw(img)
    if kind == "coins":
        n = 1 + int(5 * ease_out(prog(t, 0.8, 1.6)))
        for k in range(n):
            y = cy + 80 - k * 26
            d.ellipse([cx - 80, y - 22, cx + 80, y + 22], fill=rgba((178, 128, 44), a), outline=rgba(DARK, a * 0.5), width=2)
            d.ellipse([cx - 80, y - 30, cx + 80, y + 14], fill=rgba(AMBER, a))
        text(img, cx, cy + 72 - (n - 1) * 26, "₩", "Black", 34, DARK, a)
        drop = (t % 3.0) / 3.0
        text(img, cx + 130, cy - 60 + drop * 60, "−₩", "Black", 44, RED, a * (1 - drop))
    elif kind == "chase":
        pts = [(-130, -70), (-60, 50), (-10, 10), (40, 60), (130, -100)]
        pts = [(cx + x, cy + y) for x, y in pts]
        p = ease_in_out((t % 4.0) / 2.6)
        seg = p * (len(pts) - 1)
        k = int(seg)
        drawn = pts[:k + 1]
        if k < len(pts) - 1:
            f = seg - k
            drawn.append((pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f))
        if len(drawn) > 1:
            d.line(drawn, fill=rgba(RED, a), width=12, joint="curve")
            ex, ey = drawn[-1]
            d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=rgba(RED, a))
    elif kind == "eyes":
        for side in (-1, 1):
            ex = cx + side * 85
            top = [(ex + x, cy - 50 * (1 - (x / 70) ** 2)) for x in range(-70, 71, 5)]
            bot = [(ex + x, cy + 50 * (1 - (x / 70) ** 2)) for x in range(70, -71, -5)]
            d.polygon(top + bot, fill=rgba(CREAM, a))
            px = ex + 30 * math.sin(t * 1.6)
            d.ellipse([px - 26, cy - 26, px + 26, cy + 26], fill=rgba(DARK, a))
            d.ellipse([px - 8, cy - 14, px + 4, cy - 2], fill=rgba(WHITE, a))
    elif kind == "bubble":
        bob = math.sin(t * 2.2) * 6
        x0, y0, x1, y1 = cx - 125, cy - 75 + bob, cx + 125, cy + 45 + bob
        d.rounded_rectangle([x0, y0, x1, y1], 36, fill=rgba(CREAM, a))
        d.polygon([(cx - 60, y1 - 2), (cx - 100, y1 + 50), (cx - 10, y1 - 2)], fill=rgba(CREAM, a))
        text(img, cx, (y0 + y1) / 2, "OB 조심~", "Black", 46, DARK, a)
    elif kind == "shield":
        pts = [(0, -120), (100, -82), (92, 30), (0, 120), (-92, 30), (-100, -82)]
        pts = [(cx + x, cy + y) for x, y in pts]
        d.polygon(pts, fill=rgba((88, 150, 110), a * 0.45), outline=rgba(CREAM, a), width=6)
        c = ease_out(prog(t, 2.0, 1.2))
        if c > 0:
            crack = [(cx - 10, cy - 120), (cx + 20, cy - 50), (cx - 18, cy), (cx + 14, cy + 60), (cx - 4, cy + 120)]
            n = 1 + c * (len(crack) - 1)
            d.line(crack[:int(n) + 1], fill=rgba(RED, a), width=8, joint="curve")
    elif kind == "putt":
        hx, hy = cx + 70, cy + 40
        d.ellipse([hx - 70, hy - 22, hx + 70, hy + 22], fill=rgba(DARK, a))
        d.ellipse([hx - 70, hy - 22, hx + 70, hy + 22], outline=rgba((88, 150, 110), a), width=4)
        cyc = (t % 3.2) / 3.2
        if cyc < 0.6:
            q = ease_out(cyc / 0.6)
            bx, by = cx - 180 + (hx - 60 - (cx - 180)) * q, hy - 8
        else:
            q = ease_out((cyc - 0.6) / 0.4)
            bx, by = hx - 60 + 30 * q, hy - 8 - math.sin(q * math.pi) * 18
        d.ellipse([bx - 20, by - 36, bx + 20, by + 4], fill=rgba(WHITE, a))
        text(img, cx - 40, cy - 70, "1m", "Black", 56, CREAM, a)


# ---------- 유형 씬 ----------
CARD_X0, CARD_X1, CARD_Y0, CARD_Y1 = 880, 1790, 210, 860
PAD = 64


def section_alpha(lt, s, e):
    return window(lt, s, e, 0.5, 0.4)


def scene_type(img, t, idx):
    ty = TYPES[idx]
    lt = t - (T_TYPES + idx * TYPE_LEN)
    enter = ease_out(prog(lt, 0, 0.7))
    leave = ease_in(prog(lt, TYPE_LEN - 0.7, 0.7))
    A = enter * (1 - leave)
    dx = (1 - enter) * 160 - leave * 120

    # 왼쪽: 번호 / 이름 / 한 줄 설명 / 아이콘
    s = back_out(prog(lt, 0.15, 0.6))
    text(img, 150 + dx, 210, "TYPE", "Bold", 30, MUTED, A, anchor="lt")
    text(img, 140 + dx, 250, ty["no"], "Black", 230, AMBER, A * clamp(s), anchor="lt", scale=max(s, 0.01))
    icon(img, ty["icon"], 680 + dx, 380, lt, A * ease_out(prog(lt, 0.5, 0.6)))
    a_name = ease_out(prog(lt, 0.5, 0.6))
    text(img, 150 + dx, 560 + (1 - a_name) * 20, ty["name"], "Black", 96, CREAM, A * a_name, anchor="lt")
    a_tag = ease_out(prog(lt, 1.0, 0.6))
    text_block(img, 152 + dx, 700, wrap(ty["tag"], "Medium", 42, 620), "Medium", 42, MUTED, A * a_tag)
    d = draw(img)
    ln = ease_in_out(prog(lt, 0.9, 0.8)) * 560
    d.line([(152 + dx, 668), (152 + dx + ln, 668)], fill=rgba(AMBER, A), width=4)

    # 오른쪽 카드
    ca = A * ease_out(prog(lt, 0.6, 0.6))
    cdx = dx * 1.3
    d.rounded_rectangle([CARD_X0 + cdx, CARD_Y0, CARD_X1 + cdx, CARD_Y1], 36,
                        fill=rgba(CARD, ca * 0.92), outline=rgba(CARD_LINE, ca), width=2)
    x = CARD_X0 + PAD + cdx
    inner_w = CARD_X1 - CARD_X0 - PAD * 2

    # A. 증상
    sa = ca * section_alpha(lt, 1.4, 15.6)
    if sa > 0:
        chip(img, x, CARD_Y0 + 80, "이런 모습, 익숙하다면", AMBER, sa)
        y = CARD_Y0 + 170
        for k, sym in enumerate(ty["symptoms"]):
            p = ease_out(prog(lt, 2.6 + k * 3.0, 0.6))
            ba = sa * p
            off = (1 - p) * 30
            lines = wrap(sym, "Bold", 46, inner_w - 90)
            d.ellipse([x + off, y - 4, x + 52 + off, y + 48], fill=rgba(AMBER, ba))
            text(img, x + 26 + off, y + 22, str(k + 1), "Black", 30, DARK, ba)
            h = text_block(img, x + 84 + off, y, lines, "Bold", 46, CREAM, ba, line_h=1.4)
            y += max(h, 64) + 44

    # B. 심리학 키워드
    ka = ca * section_alpha(lt, 15.6, 23.2)
    if ka > 0:
        dy = (1 - ease_out(prog(lt, 15.6, 0.6))) * 30
        chip(img, x, CARD_Y0 + 80, "심리학 키워드", (130, 200, 150), ka)
        text(img, x, CARD_Y0 + 170 + dy, ty["term"], "Black", 92, CREAM, ka, anchor="lt")
        text(img, x + 4, CARD_Y0 + 290 + dy, ty["term_en"], "Medium", 36, MUTED, ka, anchor="lt")
        d.line([(x, CARD_Y0 + 360 + dy), (x + 120, CARD_Y0 + 360 + dy)], fill=rgba(AMBER, ka), width=5)
        da = ka * ease_out(prog(lt, 16.6, 0.8))
        text_block(img, x, CARD_Y0 + 410 + dy, wrap(ty["term_desc"], "Medium", 46, inner_w), "Medium", 46, CREAM, da, line_h=1.5)

    # C. 처방
    ra = ca * section_alpha(lt, 23.2, TYPE_LEN - 0.6)
    if ra > 0:
        dy = (1 - ease_out(prog(lt, 23.2, 0.6))) * 30
        chip(img, x, CARD_Y0 + 80, "그늘집 처방", AMBER, ra)
        hy = text_block(img, x, CARD_Y0 + 175 + dy, wrap(ty["rx"], "Black", 70, inner_w), "Black", 70, AMBER, ra, line_h=1.3)
        sa2 = ra * ease_out(prog(lt, 24.4, 0.7))
        text_block(img, x, CARD_Y0 + 215 + hy + dy, wrap(ty["rx_sub"], "Medium", 44, inner_w), "Medium", 44, CREAM, sa2, line_h=1.5)
        flag(img, CARD_X1 - 110 + cdx, CARD_Y1 - 70, 130, ra * 0.9, t)

    progress_dots(img, idx, A)


def progress_dots(img, cur, a):
    d = draw(img)
    gap = 70
    x0 = W / 2 - gap * 2.5
    y = 990
    for i in range(6):
        cx = x0 + i * gap
        if i == cur:
            d.rounded_rectangle([cx - 30, y - 18, cx + 30, y + 18], 18, fill=rgba(AMBER, a))
            text(img, cx, y, f"{i + 1}/6", "Bold", 22, DARK, a)
        else:
            col = CREAM if i < cur else CARD_LINE
            d.ellipse([cx - 8, y - 8, cx + 8, y + 8], fill=rgba(col, a * 0.9))


# ---------- 요약 ----------
def scene_summary(img, t):
    lt = t - T_SUMMARY
    a = window(lt, 0, T_OUTRO - T_SUMMARY, 0.5, 0.6)
    text(img, W / 2, 170, "한눈에 보기", "Black", 76, CREAM, a * ease_out(prog(lt, 0.1, 0.5)))
    text(img, W / 2, 250, "나는 몇 번 유형일까?", "Medium", 40, AMBER, a * ease_out(prog(lt, 0.5, 0.5)))
    cw, ch, gx, gy = 520, 270, 40, 36
    x0 = (W - (cw * 3 + gx * 2)) / 2
    y0 = 330
    d = draw(img)
    for i, ty in enumerate(TYPES):
        p = ease_out(prog(lt, 1.0 + i * 0.45, 0.6))
        ca = a * p
        if ca <= 0:
            continue
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy) + (1 - p) * 30
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], 28, fill=rgba(CARD, ca * 0.92), outline=rgba(CARD_LINE, ca), width=2)
        text(img, cx + 40, cy + 40, ty["no"], "Black", 64, AMBER, ca, anchor="lt")
        text(img, cx + 40, cy + 130, ty["name"], "Black", 52, CREAM, ca, anchor="lt")
        text(img, cx + 40, cy + 205, ty["term"], "Medium", 34, MUTED, ca, anchor="lt")


# ---------- 아웃트로 ----------
def scene_outro(img, t):
    lt = t - T_OUTRO
    out = 1 - ease_in(prog(lt, DURATION - T_OUTRO - 1.2, 1.0))
    a1 = ease_out(prog(lt, 0.2, 0.6))
    a2 = ease_out(prog(lt, 1.2, 0.6))
    text(img, W / 2, 360 + (1 - a1) * 30, "무너지는 순간을 알아차리는 것,", "Bold", 72, CREAM, a1 * out)
    s = back_out(prog(lt, 1.2, 0.7))
    text(img, W / 2, 490, "그게 첫 번째 회복입니다", "Black", 104, AMBER, a2 * out, scale=max(s, 0.01))
    a3 = ease_out(prog(lt, 3.5, 0.6))
    text(img, W / 2, 640, "당신은 몇 번 유형인가요? 댓글로 알려주세요", "Medium", 44, CREAM, a3 * out)
    # 구독 밴드
    b = ease_out(prog(lt, 5.0, 0.6))
    if b > 0:
        d = draw(img)
        bw, bh = 760, 120
        bx = W / 2 - bw / 2
        by = 760 + (1 - b) * 40
        d.rounded_rectangle([bx, by, bx + bw, by + bh], 60, fill=rgba(AMBER, b * out))
        flag(img, bx + 80, by + 92, 70, b * out, t)
        text(img, bx + 140, by + bh / 2, f"{CHANNEL}  구독하기", "Black", 50, DARK, b * out, anchor="lm")


# ---------- 프레임 ----------
def frame(t):
    img = background(t)
    if t < T_LOGO:
        scene_intro(img, t)
    elif t < T_TITLE:
        scene_logo(img, t)
    elif t < T_TYPES:
        scene_title(img, t)
    elif t < T_SUMMARY:
        scene_type(img, t, min(int((t - T_TYPES) // TYPE_LEN), len(TYPES) - 1))
    elif t < T_OUTRO:
        scene_summary(img, t)
    else:
        scene_outro(img, t)
    brand_header(img, t)
    fade = min(prog(t, 0, 0.4), 1 - prog(t, DURATION - 0.3, 0.3))
    if fade < 1:
        img = Image.blend(Image.new("RGB", (W, H)), img, fade)
    return img


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        outdir = sys.argv[-1] if not sys.argv[-1].replace(".", "").isdigit() else os.path.join(os.path.dirname(OUT), "preview")
        os.makedirs(outdir, exist_ok=True)
        for s in sys.argv[2:]:
            if s.replace(".", "").isdigit():
                frame(float(s)).save(os.path.join(outdir, f"t{float(s):06.1f}.png"))
        print("preview ->", outdir)
    else:
        print(f"duration {DURATION:.1f}s")
        render(frame, DURATION, OUT)
