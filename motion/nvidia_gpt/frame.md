---
version: alpha
name: GREEN COMPUTE — Frame (ChatGPT × NVIDIA 모션그래픽)
description: >
  ChatGPT의 등장과 엔비디아 주가 폭발을 다루는 모션그래픽 영상의 프레임 단위 디자인 시스템.
  엔비디아 CI/BI(NVIDIA Green #76B900 · 블랙 · 화이트 · 강한 산세리프)를 원자로 삼고,
  GTC 키노트 무대의 분위기(완전한 검은 공간, 그린 림라이트, 회로 트레이스, 원근 그리드,
  데이터센터 반복 구조, 거대한 스펙 숫자)를 프레임 문법으로 옮긴다.
unit: the frame — 1920×1080 (16:9) primary · 30fps · 9:16 / 1:1 documented
principle: 검은 공간 위 단 하나의 초록 · 그린은 '연산(Compute)'의 색 · 숫자는 대본에서만 온다

colors:
  # — 공식 CI 값 —
  nvidia-green: "#76B900"     # NVIDIA Green (Pantone 376 C). 유일한 브랜드 액센트
  black: "#000000"            # GTC 무대 배경. 순흑
  white: "#FFFFFF"            # 헤드라인
  # — 이 영상용 파생 토큰 (공식 아님, 그린/블랙에서 파생) —
  green-glow: "#A4E33B"       # 블룸·하이라이트 코어. 그린을 발광시킬 때만
  green-deep: "#2F4A00"       # 그리드 라인·차트 면적 하단·트레이스 잔상
  green-tint-20: "rgba(118,185,0,0.20)"   # 대기 글로우·면적 채움
  green-tint-12: "rgba(118,185,0,0.12)"   # 그리드·고스트 숫자
  carbon: "#0A0C0A"           # 패널 바닥 (그린 쪽으로 기운 블랙)
  graphite: "#151815"         # 카드 면
  hairline: "#2A2F28"         # 1–2px 구조선
  text-muted: "#A6ADA3"       # 본문·보조
  text-hint: "#5F665C"        # 메타·출처
  prompt-white: "#ECEFF1"     # ChatGPT/프롬프트 캐릭터 색 (그린과 구분되는 차가운 백색)
  loss-red: "#E5484D"         # 하락 표시 전용. 프레임당 1회 이하

typography:
  # 한글·라틴 모두 Pretendard (motion/fonts: Medium 500 · Bold 700 · Black 900)
  # 데이터·티커·메타는 JetBrains Mono (HyperFrames 내장)
  # NVIDIA Sans는 사내 전용 서체 → Pretendard로 대체 (기하학적 그로테스크 계열로 톤이 가까움)
  display:    { fontFamily: "Pretendard", px: 168, cqw: 8.75, weight: 900, lineHeight: 0.95, tracking: "-0.04em" }
  stat-hero:  { fontFamily: "Pretendard", px: 240, cqw: 12.5, weight: 900, lineHeight: 0.9, tracking: "-0.05em", tabular: true }
  h1:         { fontFamily: "Pretendard", px: 112, cqw: 5.83, weight: 900, lineHeight: 1.05, tracking: "-0.03em" }
  h2:         { fontFamily: "Pretendard", px: 76,  cqw: 3.96, weight: 700, lineHeight: 1.12, tracking: "-0.02em" }
  h3:         { fontFamily: "Pretendard", px: 52,  cqw: 2.71, weight: 700, lineHeight: 1.2,  tracking: "-0.01em" }
  lead:       { fontFamily: "Pretendard", px: 40,  cqw: 2.08, weight: 500, lineHeight: 1.45 }
  body:       { fontFamily: "Pretendard", px: 32,  cqw: 1.67, weight: 500, lineHeight: 1.5 }
  label:      { fontFamily: "JetBrains Mono", px: 22, cqw: 1.15, weight: 700, tracking: "0.16em", upper: true }
  data:       { fontFamily: "JetBrains Mono", px: 28, cqw: 1.46, weight: 400, tracking: "0.02em", tabular: true }
  source:     { fontFamily: "JetBrains Mono", px: 18, cqw: 0.94, weight: 400, tracking: "0.06em" }

spacing:
  pad-x: "140px"     # 7.3cqw — GTC 슬라이드처럼 여백 넉넉히
  pad-y: "110px"
  gap-xl: "96px"
  gap-lg: "64px"
  gap-md: "32px"
  gap-sm: "16px"
  grid-cell: "80px"  # 원근 그리드·배경 그리드 기본 셀

motion:
  fps: 30
  ease-enter: "expo.out"          # 무겁게 들어와서 부드럽게 멈춤
  ease-move: "power3.inOut"       # 카메라 이동·패널 전환
  ease-hit: "back.out(1.4)"       # 숫자·칩 '착지'에만
  ease-trace: "none"              # 회로 트레이스는 선형 드로우
  dur-enter: "0.6–0.9s"
  dur-hold-min: "2.0s"            # 텍스트 최소 노출
  dur-transition: "0.5–0.8s"
  camera-drift: "scale 1.00→1.04 / 장면 전체, 멈추지 않는 느린 푸시인"
  glow-pulse: "opacity 0.75↔1.0, 2.4s 주기"
  stagger: "0.06–0.10s"

components:
  stage:
    background: "{colors.black} 단색 + 화면 하단/중앙 국소 radial glow ({colors.green-tint-20} → transparent, 반경 45–60%)"
    description: "모든 장면의 바닥. 전면 linear-gradient 금지(압축 밴딩). 빛은 국소적으로만."
  perspective-grid:
    stroke: "1px {colors.green-deep}, 원근 소실점 화면 중앙 하단, 바닥면만"
    description: "GTC 무대 바닥 느낌. 앞쪽 셀이 크고 멀수록 페이드. 느리게 앞으로 스크롤."
  circuit-trace:
    stroke: "2px {colors.nvidia-green}, 끝점에 6px {colors.green-glow} 발광 헤드"
    path: "직각 + 45° 꺾임만 허용 (PCB 배선 문법)"
    description: "장면 연결선·데이터 흐름. 선형으로 '그려지며' 들어오고 잔상은 {colors.green-deep}."
  kicker:
    typography: "{typography.label}"
    marker: "14×14px {colors.nvidia-green} 정사각 블록 + 16px 간격"
    description: "헤드라인 위 섹션 표식. 예: ■ CHAPTER 02 · THE DEMAND"
  headline:
    typography: "{typography.h1} / {typography.display}"
    color: "{colors.white}, 핵심 단어 1개만 {colors.nvidia-green}"
    description: "GTC 키노트 슬라이드 문법. 흰 대형 타이틀 + 한 단어 그린."
  stat-hero:
    typography: "{typography.stat-hero} {colors.nvidia-green} + 하단 {typography.h3} {colors.white} + {typography.source}"
    effect: "숫자에 text-shadow 0 0 40px {colors.green-tint-20} (블룸), 카운트업 후 back.out 착지"
    description: "스펙 숫자 한 개가 화면을 지배. 뒤에 같은 숫자를 {colors.green-tint-12} 고스트로 2배 크기."
  stock-chart:
    line: "4px {colors.nvidia-green}, 선 끝 발광 점 16px {colors.green-glow}"
    area: "선 아래 {colors.green-tint-20} → transparent (세로 국소 그라디언트)"
    axis: "1px {colors.hairline}, 라벨 {typography.data} {colors.text-muted}, 왼쪽·아래 축만"
    marker: "이벤트 지점(예: ChatGPT 출시일)에 세로 점선 {colors.prompt-white} + 라벨 칩"
    description: "영상의 클라이맥스 컴포넌트. 선이 왼→오 드로우, 카메라가 선 끝을 따라감."
  prompt-box:
    surface: "{colors.graphite}, 2px {colors.hairline}, radius 20px"
    text: "{typography.lead} {colors.prompt-white}, 깜빡이는 블록 커서"
    description: "ChatGPT를 상징하는 '대화 입력창'. 실제 OpenAI UI·로고 복제 금지 — 일반화된 입력창 형태로."
  chip-die:
    form: "정사각 다이 + 내부 블록 그리드 와이어프레임, 1.5px {colors.nvidia-green}, 블록 일부 {colors.green-tint-20} 채움"
    description: "GPU 상징. 와이어프레임이 그려진 뒤 블록이 순차 점등."
  rack-array:
    form: "세로 랙 유닛 반복, 각 유닛 전면 LED 점 {colors.nvidia-green}, 원근 배열"
    description: "데이터센터 스케일. LED가 파도처럼 점등되며 확장감."
  data-card:
    surface: "{colors.graphite}, 상단만 2px {colors.nvidia-green} 보더, radius 0"
    typography: "{typography.label} + {typography.h2} + {typography.body}"
    description: "비교·스펙 카드. 최대 3장."
  lower-third:
    form: "좌하단, 6px 그린 세로 바 + {typography.h3} 이름 + {typography.label} 직함"
    description: "인물·기관 소개."
  ticker:
    typography: "{typography.data}"
    form: "화면 하단 48px 띠 {colors.carbon}, 상승 ▲ {colors.nvidia-green} / 하락 ▼ {colors.loss-red}"
    description: "금융 맥락 장면에서만. 좌로 흐름."
  source-tag:
    typography: "{typography.source} {colors.text-hint}"
    placement: "우하단, pad 안쪽"
    description: "모든 수치·차트 장면에 출처 필수. 예: SOURCE · {출처}, {기준일}"
  logo-slot:
    description: "NVIDIA·OpenAI 로고는 공식 배포 파일만 사용. 재작도·재채색·변형·글로우 금지. 최소 여백 = 로고 높이의 50%."
---

# GREEN COMPUTE — Frame

## Overview

이 영상의 한 줄 컨셉: **"검은 공간에 프롬프트 하나가 입력되자, 세상의 연산이 초록으로 켜진다."**

엔비디아 CI의 본질은 단순하다 — **블랙 + 화이트 + NVIDIA Green 단 하나.** GTC 키노트 무대는 이 원칙을 극장 규모로 키운 것이다: 끝이 보이지 않는 검은 공간, 그 위에 떠 있는 흰 대형 타이포, 핵심 단어와 스펙 숫자만 초록으로 빛나고, 배경에는 회로·칩·데이터센터가 빛의 선으로 그려진다.

이 시스템은 색에 **의미**를 고정한다.

| 색 | 의미 | 쓰는 곳 |
| --- | --- | --- |
| `nvidia-green` | 엔비디아 · 연산 · 상승 | 핵심 단어, 스펙 숫자, 주가 선, 회로, 칩 |
| `prompt-white` | ChatGPT · 인간의 질문 | 프롬프트 박스, 커서, 이벤트 마커 |
| `white` | 내레이션의 목소리 | 헤드라인 |
| `loss-red` | 하락 · 경고 | 티커 하락값, 위기 장면 (드물게) |

**스토리 속 색의 흐름:** 오프닝은 거의 무채색(검정 + `prompt-white`) → ChatGPT가 등장하며 첫 초록 트레이스가 켜짐 → 칩·데이터센터로 초록이 번짐 → 주가 차트에서 화면이 초록으로 '폭발'. **초록의 화면 점유율 자체가 스토리의 그래프다.**

## The Frame

### Frame Craft Bar

- **Squint** — 화면을 흐리게 봤을 때 **초록 덩어리 하나만** 보여야 한다.
- **Void** — 프레임의 **50–65%는 순흑**. GTC의 고급스러움은 비어 있는 검정에서 나온다.
- **One green** — 그린 계열 외 유채색은 `loss-red` 단 하나, 그것도 프레임당 1회 이하.
- **Reference** — GTC 키노트 슬라이드 · 제품 리빌 영상 · 칩 다이샷 B-roll. 실패 모습은 "초록 형광 게이밍 광고" 또는 "증권사 HTS 화면".

- **기본:** 1920×1080, 30fps. 세이프 영역 `pad-x 140px / pad-y 110px`.
- **세로(9:16) 1080×1920 / 정사각(1:1) 1080×1080**은 아래 Aspect-Ratio 표 참고.
- HyperFrames 구현 시 프레임 루트에 `container-type: size`, 크기는 `cqw` 사용 (토큰에 px·cqw 병기). 기존 PIL 엔진(`motion/engine.py`)에서는 px 값을 그대로 사용.

## Colors

- **배경은 언제나 `black` (#000000).** 패널이 필요하면 `carbon`/`graphite`. 회색 배경 금지.
- **NVIDIA Green #76B900은 절대 바꾸지 않는다.** 밝게 빛나야 할 때는 색을 바꾸지 말고 `green-glow` 코어 + 블룸(text-shadow/blur)을 겹친다.
- 대기 글로우는 `green-tint-20`(15–25% 체감), 그리드·고스트는 `green-tint-12`. 이보다 옅으면 압축 후 사라진다.
- 전면 linear-gradient 금지 — 화면 국소 radial glow만.
- 흰 글자 위에 그린 글자를 겹치지 말 것. 한 줄 안에서 **그린 단어는 1개**.

## Typography

- **Pretendard Black 900**이 모든 타이틀·숫자를 맡는다 (엔비디아 브랜드 서체 NVIDIA Sans의 굵고 단단한 인상을 대체). 본문은 Medium 500, 서브는 Bold 700. **400 이하 웨이트는 사용하지 않는다** (repo에 없고, 영상에서 약해 보임).
- **JetBrains Mono**는 '기계의 목소리' — 라벨·티커·축·출처·코드에만. 대문자 + 넓은 자간.
- 디스플레이 자간 −0.03~−0.05em, 줄간 0.9–1.05.
- **가독 하한:** 의미 있는 텍스트 28px 이상, 라벨 18px 이상.
- **분량 맞춤:** 1–3단어 → `display`, 4–8단어 → `h1`, 그 이상 → `h2`. 한 프레임에 대형 텍스트 모먼트는 1개.
- 숫자는 `font-variant-numeric: tabular-nums` (카운트업 시 흔들림 방지).

## Depth & Light

GTC 분위기의 핵심은 **빛**이다. 그림자 대신 발광으로 깊이를 만든다.

1. **배경층** — 순흑 + 국소 그린 radial glow + 원근 그리드 또는 고스트 숫자/칩 실루엣 (12–20%).
2. **중경층** — 메시지: 헤드라인, 차트, 칩, 프롬프트 박스.
3. **전경층** — 킥커, 회로 트레이스, 출처 태그, 파티클(작은 그린 점 2–4px, 느린 상승), 미세 필름 그레인(3–5%).

- 발광 = `text-shadow`/`filter: drop-shadow`/blur 레이어의 그린 블룸. 드롭섀도(검은 그림자) 금지.
- 라운드: `prompt-box`만 20px. 나머지 카드·칩·바는 **직각(0)** — 엔비디아의 공업적 인상.
- 보더는 영상 기준 1–2px, 구조선은 `hairline`.

## Motion

- **무게감:** 진입은 `expo.out` 0.6–0.9s. 튀는 바운스 금지, `back.out`은 숫자·칩 착지 순간에만.
- **카메라는 멈추지 않는다:** 모든 장면에 느린 푸시인(scale 1.00→1.04) 또는 그리드 전진.
- **그리는 선:** 회로 트레이스·차트 선은 선형으로 그려지고, 진행 헤드가 `green-glow`로 빛난다.
- **점등:** 칩 블록·랙 LED는 0.06–0.10s 스태거로 파도처럼 켜진다.
- **전환:** 기본은 블랙 딥(검정으로 꺼졌다 켜짐) 또는 트레이스가 다음 장면으로 이어지는 매치컷. 화려한 3D 플립·와이프 금지.
- 텍스트 최소 노출 2.0s.

## Scene Treatments (스토리 비트 제안)

> 레시피: 바닥 · 구성 · 초점 · 액센트 · 여백 · 고정/자유. 수치는 모두 대본·출처에서.

### 1 · Cold Open — "프롬프트" (무채색)
**바닥** 순흑. **구성** prompt-box 하나, 블록 커서. **초점** 화면 중앙에 질문이 타이핑됨 (`prompt-white`). **액센트** 엔터 순간 박스 아래에서 첫 초록 트레이스가 출발. **여백** ~75%. **고정** 그린은 마지막 1초에만. **자유** 프롬프트 문구.

### 2 · The Moment — ChatGPT 출시
**바닥** 순흑 + 중앙 약한 백색 glow. **구성** kicker(■ 2022.11.30), h1, 사용자 수 stat-hero(`prompt-white`), source-tag. **초점** 숫자. **액센트** 숫자만 백색 발광 — 아직 그린이 주인공이 아님. **자유** 지표·문구.

### 3 · The Demand — 연산이 필요하다
**바닥** 순흑 + 원근 그리드 진입. **구성** 프롬프트 박스에서 뻗은 circuit-trace가 화면을 가로질러 chip-die에 연결. **초점** 칩 와이어프레임이 그려지고 블록 점등. **액센트** 그린 트레이스. **여백** ~55%.

### 4 · The Factory — 데이터센터 스케일
**바닥** 순흑. **구성** rack-array 원근 배열, kicker, h2. **초점** LED 파도가 화면 끝까지 번짐. **액센트** 그린 LED 수천 개. **여백** ~45% (스케일감을 위해 예외적으로 밀도↑).

### 5 · The Explosion — 주가 (클라이맥스)
**바닥** 순흑 + 하단 그린 glow가 점점 커짐. **구성** stock-chart, 이벤트 마커(ChatGPT 출시 = `prompt-white` 점선), stat-hero(상승률), source-tag. **초점** 선이 드로우되며 카메라가 선 끝을 추적, 꺾여 치솟는 구간에서 화면 글로우 최대. **액센트** 그린 선 + 발광 헤드. **고정** 왼·아래 축만, 출처 필수.

### 6 · The Ranking — 시가총액 비교
**바닥** 순흑. **구성** 가로 막대 3–5개(타사 = `text-hint`, 엔비디아 = `nvidia-green`), data 라벨, source-tag. **초점** 엔비디아 막대가 마지막에 자라나 1위로 착지. **액센트** 그린 막대 하나.

### 7 · Keynote Statement
**바닥** 순흑 + 중앙 그린 glow. **구성** kicker, display 한 문장(핵심 단어 그린). **초점** 문장. **여백** ~60%. GTC 슬라이드를 가장 직접적으로 오마주하는 프레임.

### 8 · End Card
**바닥** 순흑. **구성** 채널명/시리즈명 h2, 그린 정사각 블록 마크, 원근 그리드 페이드아웃. **고정** 공식 로고 사용 시 logo-slot 규칙.

## Composition Rules

### Do
- 순흑 배경, 프레임의 절반 이상은 비워 둔다.
- 한 프레임 = 한 메시지 = 그린 하나.
- 그린은 '연산/엔비디아/상승'에만, `prompt-white`는 'ChatGPT/질문'에만 — 의미를 섞지 않는다.
- 모든 수치 장면에 `source-tag` (출처 + 기준일).
- 회로 트레이스로 장면과 장면을 연결해 "프롬프트 → 연산 → 돈"의 인과를 시각화.

### Don't
- #76B900을 다른 초록(형광 #00FF00, 민트 등)으로 바꾸거나 그라디언트로 변형하지 않는다.
- 엔비디아·OpenAI 로고를 재작도·재채색·발광 처리하지 않는다. 공식 파일만.
- 전면 그라디언트 배경, 회색 배경, 검은 드롭섀도, 둥근 카드(프롬프트 박스 제외) 금지.
- 증권사 HTS처럼 빨강/초록 숫자를 화면 가득 채우지 않는다.
- Pretendard Black + 다른 산세리프 혼용 금지 (보조는 JetBrains Mono만).

## Aspect-Ratio Behavior

| Treatment | 16:9 | 9:16 | 1:1 |
| --- | --- | --- | --- |
| Cold Open | 박스 중앙 | 박스 중앙, 폭 88% | 박스 중앙 |
| Stat | 숫자 좌, 설명 우 | 숫자 위, 설명 아래 | 숫자 중앙 |
| Stock Chart | 전체 폭 | 차트 하단 60%, 숫자 상단 | 차트 70% |
| Rack / Chip | 원근 좌→우 | 원근 아래→위 | 정면 대칭 |
| Statement | display 좌정렬 | display 3줄 이내 | 중앙 |

세로형에서는 `display`를 1단계 낮추고(`h1`), `pad-x`를 80px로 줄인다.

## Approved Entities & Brand Use

- **NVIDIA, ChatGPT/OpenAI**는 해설·보도 목적의 언급 대상이다. 로고가 필요하면 각 사 공식 프레스킷 파일을 그대로 사용하고, 이 디자인 시스템의 그린·발광 효과를 로고에 적용하지 않는다.
- 영상 자체는 **엔비디아 공식 콘텐츠처럼 보이면 안 된다.** 채널 고유 마크(그린 정사각 블록 + 채널명)를 오프닝·엔딩에 두어 제작 주체를 분명히 한다.
- 젠슨 황 등 실존 인물 이미지는 보도용 사진(출처 표기)만, 합성·변조 금지.

## Numerals & Claims (hard rule)

주가, 상승률, 시가총액, 사용자 수 등 **모든 수치는 대본과 출처에서만** 가져온다. 디자인 단계의 숫자는 `{NN%}`, `— figure —` 같은 플레이스홀더로 둔다. 차트는 실제 데이터 CSV(종가, 기준일 명시)로 그리고 `source-tag`에 출처·기준일을 표기한다.

## Pre-Render Self-Audit

- **Squint** — 초록 덩어리 하나만 보이는가?
- **Void** — 50% 이상 순흑인가?
- **Color** — #76B900 그대로인가? 그린/프롬프트화이트 의미가 섞이지 않았나? 레드는 1회 이하인가?
- **Type** — Pretendard 500/700/900 + JetBrains Mono만? 28px 하한?
- **Light** — 깊이는 발광으로, 검은 그림자 없음, 전면 그라디언트 없음?
- **Facts** — 모든 숫자에 출처·기준일?
- **Brand** — 로고 원본 그대로, 채널 마크로 제작 주체 표시?

## Known Gaps

- NVIDIA Sans는 공개 서체가 아니므로 Pretendard로 대체했다. 실제 GTC 슬라이드와 글자 디테일은 다르다.
- `green-glow`, `green-deep`, `carbon` 등은 이 영상을 위한 파생 토큰이며 엔비디아 공식 보조색이 아니다.
- 3D(칩·랙)는 CSS/SVG 와이어프레임 기준으로 정의했다. 사실적인 3D가 필요하면 Three.js 어댑터 또는 이미지 생성 B-roll로 확장.
