# mind- 프로젝트 가이드

## 디자인 시스템

ChatGPT × NVIDIA 모션그래픽 영상(`motion/nvidia_gpt/`)의 모든 화면은 아래 디자인 시스템을 따른다.
색·서체·간격·모션 토큰은 frontmatter 값을 그대로 쓰고(임의 변경·반올림 금지), 본문의 Do/Don't와 Pre-Render Self-Audit를 렌더 전에 점검한다.

@motion/nvidia_gpt/design.md

- 미리보기: `motion/nvidia_gpt/frame-showcase.html` (렌더 이미지 `frame-showcase.png`)
- 서체 파일: `motion/fonts/` (Pretendard Medium·Bold·Black)
- HyperFrames 프로젝트는 `motion/nvidia_gpt/`에서 작업한다. 스펙 탐색 순서상 같은 폴더에 `frame.md`를 새로 만들면 `design.md`보다 우선하므로 만들지 않는다.
