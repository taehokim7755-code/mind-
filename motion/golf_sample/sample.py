"""그늘집심리학 롱폼 1분 샘플 — 배경 이미지(스톡/AI) + 모션그래픽 오버레이.

배경 교체: motion/golf_sample/assets/bg_01.jpg ~ bg_06.jpg (png/webp도 가능)를 넣으면
         임시 일러스트(assets/placeholder/) 대신 자동으로 사용됩니다.
실행:     python3 motion/golf_sample/sample.py            -> motion/out/golf_sample_1min.mp4
         python3 motion/golf_sample/sample.py --preview 5 20 40
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "golf_ep02"))
from engine import (W, H, back_out, clamp, draw, ease_in, ease_in_out, ease_out, prog,  # noqa: E402
                    render, rgba, text, text_block, text_width, wrap)
from ep02 import AMBER, CREAM, DARK, MUTED, RED, chip, flag  # noqa: E402

OUT = os.path.join(HERE, "..", "out", "golf_sample_1min.mp4")
DURATION = 60.0
XFADE = 0.8
BW, BH = 2400, 1350  # 켄번스용 여유 해상도


# ---------- 배경 로딩 ----------
def load_bg(n):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = os.path.join(HERE, "assets", f"bg_{n:02d}.{ext}")
        if os.path.exists(p):
            break
    else:
        p = os.path.join(HERE, "assets", "placeholder", f"bg_{n:02d}.png")
    im = Image.open(p).convert("RGB")
    s = max(BW / im.width, BH / im.height)  # cover
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    l, t = (im.width - BW) // 2, (im.height - BH) // 2
    return im.crop((l, t, l + BW, t + BH))


BGS = {n: load_bg(n) for n in range(1, 7)}

# 샷 목록: (시작, 끝, 배경번호, 줌 시작, 줌 끝, 초점 x0,y0 -> x1,y1 (0~1), 어둡게)
SHOTS = [
    (0.0, 4.8, 1, 1.00, 1.10, (0.55, 0.55), (0.62, 0.58), 0.35),
    (4.8, 9.4, 2, 1.05, 1.30, (0.50, 0.60), (0.42, 0.55), 0.40),
    (9.4, 15.4, 1, 1.15, 1.25, (0.60, 0.50), (0.55, 0.50), 0.65),
    (15.4, 24.4, 3, 1.00, 1.12, (0.40, 0.50), (0.55, 0.50), 0.45),
    (24.4, 38.4, 4, 1.05, 1.20, (0.50, 0.55), (0.60, 0.62), 0.45),
    (38.4, 48.4, 5, 1.00, 1.10, (0.45, 0.60), (0.50, 0.65), 0.40),
    (48.4, 60.0, 6, 1.10, 1.00, (0.50, 0.55), (0.50, 0.50), 0.40),
]


def shot_frame(shot, t):
    s, e, n, z0, z1, f0, f1, dark = shot
    p = ease_in_out(prog(t, s, e - s))
    z = z0 + (z1 - z0) * p
    fx = f0[0] + (f1[0] - f0[0]) * p
    fy = f0[1] + (f1[1] - f0[1]) * p
    cw, ch = BW / z, BH / z
    l = clamp(fx * BW - cw / 2, 0, BW - cw)
    tp = clamp(fy * BH - ch / 2, 0, BH - ch)
    img = BGS[n].resize((W, H), Image.BILINEAR, box=(l, tp, l + cw, tp + ch))
    return Image.blend(img, Image.new("RGB", (W, H)), dark)


# 화면 왼쪽/아래를 더 어둡게 해 글자 가독성 확보
def _grade():
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    for x in range(W):
        d.line([(x, 0), (x, H)], fill=int(150 * (1 - x / W) ** 1.6))
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-300, -250, W + 300, H + 250], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(200))
    return g, v


GRADE_L, VIGNETTE = _grade()
BLACK = Image.new("RGB", (W, H), (0, 0, 0))


def background(t):
    cur = [sh for sh in SHOTS if sh[0] - XFADE / 2 <= t < sh[1] + XFADE / 2]
    img = shot_frame(cur[0], t)
    if len(cur) > 1:  # 크로스페이드
        a = ease_in_out((t - (cur[1][0] - XFADE / 2)) / XFADE)
        img = Image.blend(img, shot_frame(cur[1], t), clamp(a))
    img = Image.composite(BLACK, img, GRADE_L)
    img = Image.composite(img, BLACK, VIGNETTE)
    return img


# ---------- 공용 그래픽 ----------
def glass(img, box, alpha, radius=32):
    """반투명 프로스티드 글래스 패널."""
    if alpha <= 0:
        return
    x0, y0, x1, y1 = [int(v) for v in box]
    region = img.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(22))
    region = Image.blend(region, Image.new("RGB", region.size, (10, 24, 18)), 0.55)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius, fill=int(255 * alpha))
    img.paste(region, (x0, y0), mask)
    draw(img).rounded_rectangle(box, radius, outline=rgba((255, 255, 255), 0.18 * alpha), width=2)


def brand_header(img, t):
    a = clamp(ease_out(prog(t, 9.8, 0.8)) * (1 - ease_in(prog(t, 59.0, 0.8)))) * 0.95
    if a <= 0:
        return
    flag(img, 96, 92, 56, a, t)
    text(img, 132, 70, "그늘집심리학", "Bold", 34, CREAM, a, anchor="lm")
    text(img, W - 80, 70, "EP.02", "Bold", 30, MUTED, a, anchor="rm")


def type_badge(img, t, a):
    """우상단 진행 표시 (01/06 판돈 계산형)."""
    if a <= 0:
        return
    chip(img, W - 80 - 300, 140, "01 / 06  판돈 계산형", AMBER, a, size=26)


# ---------- 장면 ----------
def s_hook(img, t):
    a1 = ease_out(prog(t, 0.5, 0.7)) * (1 - ease_in(prog(t, 4.3, 0.5)))
    a2 = ease_out(prog(t, 1.6, 0.7)) * (1 - ease_in(prog(t, 4.3, 0.5)))
    text(img, 160, 430 + (1 - a1) * 30, "같은 실력인데,", "Bold", 92, CREAM, a1, anchor="lm")
    text(img, 160, 560 + (1 - a2) * 30, "내기만 걸리면", "Bold", 92, CREAM, a2, anchor="lm")
    # 2번째 샷: 홀 앞의 공
    s = back_out(prog(t, 5.2, 0.7))
    a3 = ease_out(prog(t, 5.2, 0.3)) * (1 - ease_in(prog(t, 8.8, 0.5)))
    text(img, 160, 500, "왜 먼저", "Black", 150, CREAM, a3, anchor="lm", scale=max(s, 0.01))
    text(img, 160, 680, "무너질까?", "Black", 170, AMBER, a3 * ease_out(prog(t, 5.7, 0.4)), anchor="lm")


def s_title(img, t):
    lt = t - 9.4
    a = ease_out(prog(lt, 0.4, 0.5)) * (1 - ease_in(prog(lt, 5.4, 0.6)))
    grow = ease_out(prog(lt, 0.3, 0.8))
    flag(img, W / 2, 330, 150, a, t, grow)
    text(img, W / 2, 420, "그늘집심리학", "Black", 72, CREAM, a * ease_out(prog(lt, 0.8, 0.4)))
    chip(img, W / 2, 530, "EP.02", AMBER, a * ease_out(prog(lt, 1.2, 0.4)), anchor="m", size=32)
    a1 = ease_out(prog(lt, 1.5, 0.6))
    text(img, W / 2, 650 + (1 - a1) * 30, "내기 판에서 먼저 무너지는", "Black", 90, CREAM, a * a1)
    s = back_out(prog(lt, 2.0, 0.7))
    text(img, W / 2, 790, "골퍼 6가지 유형", "Black", 140, AMBER, a * ease_out(prog(lt, 2.0, 0.3)), scale=max(s, 0.01))


def s_type_intro(img, t):
    lt = t - 15.4
    a = ease_out(prog(lt, 0.4, 0.6)) * (1 - ease_in(prog(lt, 8.5, 0.5)))
    if a <= 0:
        return
    s = back_out(prog(lt, 0.5, 0.6))
    text(img, 160, 300, "TYPE", "Bold", 34, MUTED, a, anchor="lt")
    text(img, 150, 350, "01", "Black", 300, AMBER, a * clamp(s), anchor="lt", scale=max(s, 0.01))
    an = ease_out(prog(lt, 1.0, 0.6))
    text(img, 160, 700 + (1 - an) * 20, "판돈 계산형", "Black", 130, CREAM, a * an, anchor="lt")
    ln = ease_in_out(prog(lt, 1.4, 0.8)) * 760
    draw(img).line([(162, 862), (162 + ln, 862)], fill=rgba(AMBER, a), width=5)
    text(img, 162, 900, "공보다 돈을 먼저 본다", "Medium", 52, CREAM, a * ease_out(prog(lt, 1.8, 0.6)), anchor="lt")


SYMPTOMS = [
    "남은 홀 × 판돈을 머릿속으로 계산한다",
    "퍼팅 전 '빠지면 얼마'부터 떠오른다",
    "잃은 돈이 신경 쓰여 스윙이 짧아진다",
]


def s_symptoms(img, t):
    lt = t - 24.4
    a = ease_out(prog(lt, 0.4, 0.6)) * (1 - ease_in(prog(lt, 13.6, 0.5)))
    if a <= 0:
        return
    type_badge(img, t, a)
    box = (120, 250, 1080, 900)
    glass(img, box, a)
    chip(img, 180, 330, "이런 모습, 익숙하다면", AMBER, a)
    y = 420
    for k, sym in enumerate(SYMPTOMS):
        p = ease_out(prog(lt, 1.2 + k * 3.4, 0.6))
        ba = a * p
        off = (1 - p) * 30
        d = draw(img)
        d.ellipse([180 + off, y - 2, 236 + off, y + 54], fill=rgba(AMBER, ba))
        text(img, 208 + off, y + 26, str(k + 1), "Black", 32, DARK, ba)
        h = text_block(img, 270 + off, y, wrap(sym, "Bold", 50, 760), "Bold", 50, CREAM, ba, line_h=1.4)
        y += max(h, 70) + 50

    # 우측: 판돈 계산 팝업 (첫 증상 강조)
    pa = a * ease_out(prog(lt, 2.4, 0.6)) * (1 - ease_in(prog(lt, 7.0, 0.5)))
    if pa > 0:
        bx, by = 1300, 380
        glass(img, (bx, by, bx + 480, by + 300), pa, 28)
        holes = 7 - min(4, int(max(0, lt - 3.0) / 0.9))
        text(img, bx + 40, by + 70, "남은 홀", "Medium", 34, MUTED, pa, anchor="lm")
        text(img, bx + 440, by + 70, f"{holes}홀", "Black", 44, CREAM, pa, anchor="rm")
        text(img, bx + 40, by + 140, "× 판돈", "Medium", 34, MUTED, pa, anchor="lm")
        text(img, bx + 440, by + 140, "1만 원", "Black", 44, CREAM, pa, anchor="rm")
        draw(img).line([(bx + 40, by + 190), (bx + 440, by + 190)], fill=rgba(CREAM, pa * 0.5), width=2)
        text(img, bx + 440, by + 245, f"−{holes}만 원?", "Black", 60, RED, pa, anchor="rm")


def s_term(img, t):
    lt = t - 38.4
    a = ease_out(prog(lt, 0.4, 0.6)) * (1 - ease_in(prog(lt, 9.6, 0.5)))
    if a <= 0:
        return
    type_badge(img, t, a)
    chip(img, 160, 300, "심리학 키워드", (130, 200, 150), a)
    an = ease_out(prog(lt, 0.7, 0.6))
    text(img, 160, 390 + (1 - an) * 20, "손실 회피", "Black", 140, CREAM, a * an, anchor="lt")
    text(img, 166, 560, "Loss Aversion", "Medium", 42, MUTED, a * an, anchor="lt")
    # 막대 비교: 얻는 기쁨 1 vs 잃는 고통 2
    base_x, y1, y2 = 160, 700, 860
    full = 900
    p1 = ease_out(prog(lt, 2.0, 1.0))
    p2 = ease_out(prog(lt, 3.2, 1.6))
    d = draw(img)
    text(img, base_x, y1 - 10, "1만 원 땄을 때 기쁨", "Bold", 34, CREAM, a, anchor="lb")
    d.rounded_rectangle([base_x, y1 + 10, base_x + full * 0.5 * p1, y1 + 70], 14, fill=rgba((130, 200, 150), a))
    text(img, base_x, y2 - 10, "1만 원 잃었을 때 고통", "Bold", 34, CREAM, a, anchor="lb")
    d.rounded_rectangle([base_x, y2 + 10, base_x + full * p2, y2 + 70], 14, fill=rgba(RED, a))
    ma = a * ease_out(prog(lt, 4.8, 0.5))
    s = back_out(prog(lt, 4.8, 0.6))
    text(img, base_x + full + 40, y2 + 40, "약 2배", "Black", 80, AMBER, ma, anchor="lm", scale=max(s, 0.01))


def s_rx(img, t):
    lt = t - 48.4
    a = ease_out(prog(lt, 0.4, 0.6)) * (1 - ease_in(prog(lt, 10.8, 0.7)))
    if a <= 0:
        return
    type_badge(img, t, a)
    box = (120, 300, 1240, 860)
    glass(img, box, a)
    chip(img, 180, 380, "그늘집 처방", AMBER, a)
    p = ease_out(prog(lt, 0.9, 0.6))
    hy = text_block(img, 180, 460 + (1 - p) * 20, ["판돈은 '입장료'로", "정하고 잊어라"], "Black", 88, AMBER, a * p, line_h=1.25)
    text_block(img, 180, 500 + hy, wrap("계산은 18홀이 끝난 뒤, 그늘집에서 해도 늦지 않다", "Medium", 46, 1000),
               "Medium", 46, CREAM, a * ease_out(prog(lt, 2.2, 0.7)), line_h=1.45)
    flag(img, 1140, 820, 120, a, t)


def frame(t):
    img = background(t)
    if t < 9.4:
        s_hook(img, t)
    elif t < 15.4:
        s_title(img, t)
    elif t < 24.4:
        s_type_intro(img, t)
    elif t < 38.4:
        s_symptoms(img, t)
    elif t < 48.4:
        s_term(img, t)
    else:
        s_rx(img, t)
    brand_header(img, t)
    fade = min(prog(t, 0, 0.5), 1 - prog(t, DURATION - 0.6, 0.6))
    if fade < 1:
        img = Image.blend(BLACK, img, fade)
    return img


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        outdir = os.path.join(HERE, "..", "out", "preview")
        nums = [a for a in sys.argv[2:] if a.replace(".", "").isdigit()]
        if not sys.argv[-1].replace(".", "").isdigit():
            outdir = sys.argv[-1]
        os.makedirs(outdir, exist_ok=True)
        for s in nums:
            frame(float(s)).save(os.path.join(outdir, f"s{float(s):05.1f}.png"))
        print("preview ->", outdir)
    else:
        render(frame, DURATION, OUT)
