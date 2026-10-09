"""경제 채널 모션그래픽 샘플: '매달 100만 원, 10년 뒤 차이' (15초, 1920x1080, 30fps).

실행: python3 motion/sample_compound.py  ->  motion/out/sample_compound.mp4
"""
import functools
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1920, 1080, 30, 15.0
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "sample_compound.mp4")

BG = (14, 20, 36)
GRID = (32, 42, 66)
WHITE = (240, 243, 250)
MUTED = (130, 142, 170)
GOLD = (255, 196, 56)
BLUE = (88, 160, 255)


@functools.lru_cache(maxsize=None)
def font(weight, size):
    size = max(1, int(size))
    return ImageFont.truetype(os.path.join(HERE, "fonts", f"Pretendard-{weight}.otf"), size)


# ---- 데이터: 매달 100만 원 적립, 10년, 연 7% 월복리 ----
MONTHLY, MONTHS, RATE = 100, 120, 0.07 / 12
saving = [MONTHLY * m for m in range(MONTHS + 1)]
invest = [MONTHLY * ((1 + RATE) ** m - 1) / RATE for m in range(MONTHS + 1)]
GAP = invest[-1] - saving[-1]


def won(v_manwon):
    """만 원 단위 숫자를 '1억 7,308만 원' 형태로."""
    v = int(round(v_manwon))
    eok, man = divmod(v, 10000)
    if eok and man:
        return f"{eok}억 {man:,}만 원"
    if eok:
        return f"{eok}억 원"
    return f"{man:,}만 원"


# ---- 이징 ----
def clamp(x):
    return max(0.0, min(1.0, x))


def ease_out(x):
    return 1 - (1 - clamp(x)) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back_out(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def prog(t, start, dur):
    return clamp((t - start) / dur)


# ---- 그리기 헬퍼 ----
def text(img, xy, s, fnt, fill, alpha=1.0, anchor="mm", dy=0.0):
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0], xy[1] + dy), s, font=fnt, fill=fill + (int(255 * alpha),), anchor=anchor)
    img.alpha_composite(layer)


VIGNETTE = Image.new("L", (W, H), 0)
ImageDraw.Draw(VIGNETTE).ellipse([-300, -250, W + 300, H + 250], fill=255)
VIGNETTE = VIGNETTE.filter(ImageFilter.GaussianBlur(160))
DARK = Image.new("RGBA", (W, H), (6, 9, 18, 255))


def background(t):
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    off = (t * 20) % 80  # 천천히 흐르는 그리드
    for x in range(-80, W + 80, 80):
        d.line([(x + off, 0), (x + off, H)], fill=GRID, width=1)
    for y in range(-80, H + 80, 80):
        d.line([(0, y + off * 0.5), (W, y + off * 0.5)], fill=GRID, width=1)
    # 비네팅
    return Image.composite(img, DARK, VIGNETTE)


def scene_title(img, t):
    # 0~3.4s: "매달 100만 원씩" / "10년 모으면 얼마?"
    a1 = ease_out(prog(t, 0.2, 0.6))
    a2 = ease_out(prog(t, 0.9, 0.6))
    out = 1 - ease_in_out(prog(t, 2.9, 0.5))
    text(img, (W / 2, H / 2 - 70), "매달 100만 원씩", font("Bold", 96), WHITE, a1 * out, dy=(1 - a1) * 40)
    s = back_out(prog(t, 0.9, 0.7))
    if s > 0:
        f = font("Black", int(150 * max(s, 0.01)))
        text(img, (W / 2, H / 2 + 90), "10년 모으면 얼마?", f, GOLD, a2 * out)
    # 밑줄 와이프
    u = ease_in_out(prog(t, 1.5, 0.6)) * out
    d = ImageDraw.Draw(img)
    if u > 0:
        half = 520 * u
        d.rounded_rectangle([W / 2 - half, H / 2 + 185, W / 2 + half, H / 2 + 195], 5, fill=GOLD)


CH = dict(x0=260, x1=1240, y0=880, y1=300)  # 차트 영역


def to_px(i, v):
    x = CH["x0"] + (CH["x1"] - CH["x0"]) * i / MONTHS
    y = CH["y0"] - (CH["y0"] - CH["y1"]) * v / 18000
    return x, y


def scene_chart(img, t):
    # 3.0~11.6s
    a = ease_out(prog(t, 3.0, 0.6)) * (1 - ease_in_out(prog(t, 11.2, 0.5)))
    if a <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    al = int(255 * a)
    # 축 & 눈금
    d.line([(CH["x0"], CH["y0"]), (CH["x1"], CH["y0"])], fill=MUTED + (al,), width=3)
    for yr in range(0, 11, 2):
        x, _ = to_px(yr * 12, 0)
        text(img, (x, CH["y0"] + 40), f"{yr}년", font("Medium", 30), MUTED, a)
    for v in (5000, 10000, 15000):
        _, y = to_px(0, v)
        d.line([(CH["x0"], y), (CH["x1"], y)], fill=GRID + (al,), width=2)
        text(img, (CH["x0"] - 20, y), won(v).replace(" 원", ""), font("Medium", 28), MUTED, a, anchor="rm")

    # 선 그리기 (3.6~8.6s)
    p = ease_in_out(prog(t, 3.6, 5.0))
    n = max(1, int(MONTHS * p))
    sv = [to_px(i, saving[i]) for i in range(n + 1)]
    iv = [to_px(i, invest[i]) for i in range(n + 1)]
    # 두 선 사이 면적
    if n > 1:
        area = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(area).polygon(iv + sv[::-1], fill=GOLD + (int(55 * a),))
        img.alpha_composite(area)
    d.line(sv, fill=BLUE + (al,), width=8, joint="curve")
    d.line(iv, fill=GOLD + (al,), width=10, joint="curve")
    for pts, col in ((sv, BLUE), (iv, GOLD)):
        x, y = pts[-1]
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=col + (al,))

    # 범례
    text(img, (CH["x0"], 190), "■ 그냥 저축", font("Bold", 40), BLUE, a, anchor="lm")
    text(img, (CH["x0"] + 300, 190), "■ 연 7% 투자", font("Bold", 40), GOLD, a, anchor="lm")

    # 끝값 카운터 (선 끝을 따라감)
    xs, ys = sv[-1]
    xi, yi = iv[-1]
    text(img, (xs + 30, ys + 30), won(saving[n]), font("Bold", 40), BLUE, a, anchor="lm")
    text(img, (xi + 30, yi - 30), won(invest[n]), font("Black", 52), GOLD, a, anchor="lm")

    # 차이 강조 (9.0s~)
    g = back_out(prog(t, 9.0, 0.6))
    if g > 0 and n == MONTHS:
        x, ytop = to_px(MONTHS, invest[-1])
        _, ybot = to_px(MONTHS, saving[-1])
        bx = x + 60
        d.line([(bx, ytop), (bx, ybot)], fill=WHITE + (al,), width=4)
        d.line([(bx - 14, ytop), (bx + 14, ytop)], fill=WHITE + (al,), width=4)
        d.line([(bx - 14, ybot), (bx + 14, ybot)], fill=WHITE + (al,), width=4)
        size = int(68 * max(g, 0.01))
        text(img, (bx + 30, (ytop + ybot) / 2), f"+{won(GAP)}", font("Black", size), WHITE, a, anchor="lm")


def scene_outro(img, t):
    # 11.6~15s
    a = ease_out(prog(t, 11.7, 0.6))
    text(img, (W / 2, H / 2 - 80), "차이를 만든 건", font("Bold", 80), WHITE, a, dy=(1 - a) * 30)
    b = back_out(prog(t, 12.3, 0.6))
    if b > 0:
        text(img, (W / 2, H / 2 + 70), "'시간'입니다", font("Black", int(170 * max(b, 0.01))), GOLD, ease_out(prog(t, 12.3, 0.4)))
    # 로워서드 (채널명 자리)
    l = ease_out(prog(t, 13.2, 0.5))
    if l > 0:
        d = ImageDraw.Draw(img, "RGBA")
        x = -560 + 680 * l
        d.rounded_rectangle([x, H - 190, x + 520, H - 90], 16, fill=(255, 196, 56, 235))
        text(img, (x + 40, H - 140), "경제 한 스푼 · 구독", font("Black", 46), BG, 1.0, anchor="lm")
    text(img, (W - 60, H - 40), "※ 연 7% 월복리 가정, 세금·수수료 제외", font("Medium", 24), MUTED, a, anchor="rm")


def frame(t):
    img = background(t)
    if t < 3.5:
        scene_title(img, t)
    if 3.0 <= t < 11.8:
        scene_chart(img, t)
    if t >= 11.6:
        scene_outro(img, t)
    # 전체 페이드 인/아웃
    fade = min(prog(t, 0, 0.3), 1 - prog(t, DUR - 0.4, 0.4))
    if fade < 1:
        black = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade))))
        img.alpha_composite(black)
    return img.convert("RGB")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        proc.stdin.write(frame(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print("saved", OUT)


if __name__ == "__main__":
    main()
