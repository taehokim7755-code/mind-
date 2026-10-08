"""인트로용 효과음 트랙(드론 + 알림음 + 글리치 노이즈 + 타이틀 붐)을 합성해 out/sfx.wav로 저장한다."""
import math
import os
import random
import struct
import wave

SR, DUR = 48000, 12.0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sfx.wav")
rng = random.Random(313)


def sample(t):
    s = 0.0
    # 저음 드론: 화면 내내 깔리는 불안감
    drone = math.sin(2 * math.pi * 55 * t) + 0.6 * math.sin(2 * math.pi * 82.4 * t + math.sin(2 * math.pi * 0.3 * t))
    s += 0.10 * drone * min(t / 1.5, 1) * (1 if t < 7 else 0.5)
    # 1.45s 시계가 03:13으로 바뀌는 순간의 지직
    s += 0.25 * (rng.random() * 2 - 1) * math.exp(-40 * abs(t - 1.45))
    # 2.0s 알림음 (두 음)
    for at, f1, f2, k in ((2.0, 1318.5, 1975.5, 6), (2.18, 1975.5, 2637.0, 7)):
        if t >= at:
            d = t - at
            s += 0.3 * (math.sin(2 * math.pi * f1 * d) + 0.55 * math.sin(2 * math.pi * f2 * d)) * math.exp(-k * d)
    # 6.0~6.95s 메시지가 무너지는 글리치 노이즈
    if 6.0 <= t <= 6.95:
        ramp = min(1, (t - 6.0) / 0.9) ** 2
        gate = 1 if math.sin(2 * math.pi * 23 * t) > 0 else 0.4
        s += 0.32 * (rng.random() * 2 - 1) * ramp * gate
        if t > 6.6 and math.sin(2 * math.pi * 31 * t) > 0.3:
            s += 0.18 * math.sin(2 * math.pi * 1000 * t)
    # 7.0s 타이틀 붐 (피치가 떨어지는 저음 + 짧은 노이즈)
    if t >= 7.0:
        d = t - 7.0
        phase = 2 * math.pi * (42 * d + 30 / 8 * (1 - math.exp(-8 * d)))
        s += 0.8 * math.sin(phase) * math.exp(-1.6 * d)
        s += 0.3 * (rng.random() * 2 - 1) * math.exp(-14 * d)
    # 타이틀 뒤 희미한 고음 패드
    if t >= 7.5:
        s += 0.05 * math.sin(2 * math.pi * 220 * t) * math.sin(math.pi * min(1, (t - 7.5) / 4.5))
    # 끝 1초 페이드아웃
    if t > 11.0:
        s *= max(0.0, 12.0 - t)
    return max(-1.0, min(1.0, s))


os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = bytearray()
    for i in range(int(SR * DUR)):
        v = int(sample(i / SR) * 32000)
        frames += struct.pack("<hh", v, v)
    w.writeframes(bytes(frames))
print(OUT)
