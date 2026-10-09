"""모션그래픽 렌더링 공용 엔진 (PIL + ffmpeg).

- 베이스 프레임은 RGB, 도형은 ImageDraw(img, "RGBA")로 알파 블렌딩
- 텍스트는 (문자열, 굵기, 크기, 색) 단위로 캐시해 붙여넣기만 함
- 프레임은 멀티프로세스로 병렬 렌더 후 순서대로 ffmpeg에 전달
"""
import functools
import os
import subprocess
from multiprocessing import Pool

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30


# ---------- 이징 ----------
def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def ease_out(x):
    return 1 - (1 - clamp(x)) ** 3


def ease_in(x):
    return clamp(x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back_out(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def window(t, start, end, fade_in=0.5, fade_out=0.5):
    """start~end 구간에서 1, 앞뒤로 페이드되는 알파."""
    return min(ease_out(prog(t, start, fade_in)), 1 - ease_in(prog(t, end - fade_out, fade_out)))


# ---------- 폰트 / 텍스트 ----------
@functools.lru_cache(maxsize=None)
def font(weight, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", f"Pretendard-{weight}.otf"), max(1, int(size)))


@functools.lru_cache(maxsize=4096)
def _text_sprite(s, weight, size, color):
    f = font(weight, size)
    l, t, r, b = f.getbbox(s)
    pad = 4
    im = Image.new("RGBA", (r - l + pad * 2, b - t + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=color + (255,))
    # 기준선 정렬을 위해 ascent 기준 오프셋 보관
    asc, desc = f.getmetrics()
    return im, l - pad, t - pad, asc, desc


def text_width(s, weight, size):
    l, _, r, _ = font(weight, size).getbbox(s)
    return r - l


def wrap(s, weight, size, max_w):
    """공백 기준 자동 줄바꿈. 명시적 \\n은 유지."""
    lines = []
    for para in s.split("\n"):
        cur = ""
        for word in para.split(" "):
            cand = (cur + " " + word).strip()
            if cur and text_width(cand, weight, size) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = cand
        lines.append(cur)
    return lines


def _with_alpha(im, alpha):
    if alpha >= 0.999:
        return im
    im = im.copy()
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    im.putalpha(a)
    return im


def text(img, x, y, s, weight, size, color, alpha=1.0, anchor="mm", scale=1.0):
    """anchor: 가로 l/m/r + 세로 t/m/b (글자 높이 기준)."""
    if alpha <= 0.003 or not s:
        return
    sprite, ox, oy, asc, desc = _text_sprite(s, weight, int(size), color)
    if abs(scale - 1.0) > 0.01:
        if scale <= 0.02:
            return
        sprite = sprite.resize((max(1, int(sprite.width * scale)), max(1, int(sprite.height * scale))), Image.BILINEAR)
        ox, oy, asc = ox * scale, oy * scale, asc * scale
    w, h = sprite.size
    ax, ay = anchor[0], anchor[1]
    left = x - (0 if ax == "l" else w / 2 if ax == "m" else w)
    top = y - (0 if ay == "t" else h / 2 if ay == "m" else h)
    img.paste(sprite, (int(round(left)), int(round(top))), _with_alpha(sprite, alpha))


def text_block(img, x, y, lines, weight, size, color, alpha=1.0, anchor="lt", line_h=1.45):
    for i, ln in enumerate(lines):
        text(img, x, y + i * size * line_h, ln, weight, size, color, alpha, anchor=anchor)
    return len(lines) * size * line_h


# ---------- 도형 ----------
def rgba(c, a):
    return c + (int(255 * clamp(a)),)


def draw(img):
    return ImageDraw.Draw(img, "RGBA")


# ---------- 렌더 ----------
_RENDER = None


def _init(fn):
    global _RENDER
    _RENDER = fn


def _render_one(i):
    return _RENDER(i / FPS).tobytes()


def render(frame_fn, duration, out_path, workers=None, crf=18):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    n = int(round(duration * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(crf), "-preset", "medium",
           "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(workers or os.cpu_count(), initializer=_init, initargs=(frame_fn,)) as pool:
        for k, buf in enumerate(pool.imap(_render_one, range(n), chunksize=8)):
            proc.stdin.write(buf)
            if k % (FPS * 10) == 0:
                print(f"  {k / FPS:6.1f}s / {duration:.1f}s", flush=True)
    proc.stdin.close()
    proc.wait()
    print("saved", out_path)
