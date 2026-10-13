# -*- coding: utf-8 -*-
# 그늘집 심리학 EP.04 — 본인만 모르고 동반자들은 다 아는 골프장 행동 5가지
import os, re
TITLE = '동반자만 아는 내 골프장 행동 5'
CHANNEL = '그늘집 심리학'
SLOGAN = '마음을 쉬어 가는 곳'
LOGO_SMALL = '골프 멘탈 이야기'

CHAPTERS = [(0, '인트로'), (14, '행동 1 · 훈수'), (36, '행동 2 · 내 이야기'), (56, '행동 3 · 기다림'),
            (80, '행동 4 · 한숨'), (102, '행동 5 · 침묵'), (121, '정리')]
CHAP_TITLES = {
  14: ('HABIT 1', ['묻지 않은', '훈수']),
  36: ('HABIT 2', ['내 이야기로', '돌아가는 대화']),
  56: ('HABIT 3', ['나만 모르는', '기다림']),
  80: ('HABIT 4', ['미스 샷 뒤의', '한숨']),
  102: ('HABIT 5', ['남의 좋은 샷', '앞의 침묵']),
}
B = []
def blk(a, b, typ, **d):
  B.append(dict(a=a, b=b, type=typ, **d))

# ── 인트로
blk(0, 2, 'quote', ttl='지난달 라운드', lines=['동반자 셋이', '당신만 빼고'], src='이유는 스코어가 아니다', src_at=1)
blk(3, 4, 'versus', kick='실제 실험 · 조명 효과', ttl='남들은 생각보다 안 본다',
    L=dict(label='알아챌 거라 예상', val='약 절반', tone='up', at=3), R=dict(label='실제로 알아챈 사람', val='약 4분의 1', tone='dn', at=3),
    foot=('두 배나 높게 짐작했다', 4))
blk(6, 8, 'quote', ttl='특히 첫 번째는', lines=['친구를 돕는다고', '믿으면서 하는 행동'], src='하나라도 해당되면, 연락이 늦게 온다', src_at=7)

# ── 행동 1 · 훈수
blk(23, 25, 'panel', date='2018 · 샤에러 연구팀', hl=['조언하는', '사람의 마음'], hl_at=[23, 23],
    body=[('조언하면 스스로 더 힘 있다고 느낀다', 24), ('부탁받든 안 받든 똑같다', 25)])
blk(26, 29, 'versus', kick='훈수의 진실', ttl='누가 기분 좋은가',
    L=dict(label='하는 사람', val='힘이 생긴 느낌', tone='up', at=27), R=dict(label='듣는 사람', val='너는 틀렸다', tone='dn', at=29))
blk(31, 33, 'list3', kick='1번 처방', ttl='묻기 전엔 말하지 않는다',
    items=[('스윙 이야기', '상대가 물을 때만', 32), ('대신', '오늘 뭐가 잘 됐어?', 33), ('결과', '친구가 편하게 친다', 33)])
blk(34, 35, 'quote', ttl='윤이 떠올린 주인공', lines=['내 스윙을', '고치러 온 사람'], src='', src_at=35)

# ── 행동 2 · 내 이야기
blk(43, 45, 'panel', date='2012 · 하버드 타미르와 미첼', hl=['자기 이야기를', '할 때의 뇌'], hl_at=[43, 43],
    body=[('보상·쾌감 회로가 켜진다', 44), ('음식·돈에 반응하는 바로 그 회로', 45)])
blk(47, 48, 'quote', ttl='연구팀의 설명', lines=['말의 30~40%가', '자기 이야기'], src='돈을 덜 받아도 자기 이야기를 골랐다', src_at=47)
blk(51, 53, 'list3', kick='2번 처방', ttl='질문을 하나 더',
    items=[('순서', '내 이야기보다 질문 먼저', 52), ('한 마디', '이름은 뭐로 지었어?', 53), ('결과', '이야기가 상대에게 남는다', 53)])
blk(54, 55, 'quote', ttl='강이 떠올린 주인공', lines=['모든 이야기가', '자기 이야기로 끝나는 사람'], src='', src_at=55)

# ── 행동 3 · 기다림
blk(59, 61, 'num', kick='7번 홀 숲속', ttl='공 찾는 시간', fig=4, dec=0, unit='분', tone='dn', hit=60,
    desc='동기 셋은 말없이 시계를 본다', facts=[])
blk(64, 67, 'panel', date='1979 · 로스와 시콜리', hl=['내 몫은', '크게 기억한다'], hl_at=[64, 64],
    body=[('부부, 대학 농구 선수, 실험실 학생', 65), ('자기 몫을 남들보다 크게 기억', 66)])
blk(68, 70, 'versus', kick='자기중심적 편향', ttl='골프장의 기다림',
    L=dict(label='내가 기다린 시간', val='생생하다', tone='up', at=70), R=dict(label='기다리게 한 시간', val='흐릿하다', tone='dn', at=70))
blk(71, 73, 'list3', kick='3번 처방', ttl='숫자를 정해 둔다',
    items=[('3분', '못 찾으면 잠정구', 72), ('사과', '다음 티박스에서 먼저', 73), ('재촉', '하기 전에 내 시간부터', 73)])
blk(74, 75, 'quote', ttl='서가 떠올린 주인공', lines=['남은 재촉하고,', '자기는 기다리게 하는 사람'], src='', src_at=75)
blk(76, 79, 'quote', ttl='여기서 하나만', lines=['세 가지 중', '동반자가 본 건 몇 번?'], src='댓글에 번호 하나만', src_at=78)

# ── 행동 4 · 한숨
blk(87, 89, 'panel', date='2002 · 와튼 바사데', hl=['몰래 들어간', '배우 한 명'], hl_at=[87, 87],
    body=[('어떤 모임에선 밝게', 89), ('어떤 모임에선 가라앉게', 89)])
blk(90, 93, 'versus', kick='한 사람의 기분이 번졌다', ttl='모임의 결과',
    L=dict(label='가라앉은 사람', val='다툼 늘고 덜 풀림', tone='dn', at=91), R=dict(label='밝은 사람', val='더 협력하고 잘 풀림', tone='up', at=92),
    foot=('이걸 감정 전염이라고 부른다', 93))
blk(96, 99, 'list3', kick='4번 처방', ttl='열 걸음 규칙',
    items=[('화', '나도 괜찮다', 97), ('열 걸음', '그 안에 두고 온다', 98), ('카트', '표정을 바꾸고 탄다', 99)])
blk(100, 101, 'quote', ttl='윤이 떠올린 주인공', lines=['같이 있으면', '나까지 공이 안 맞는 사람'], src='', src_at=101)

# ── 행동 5 · 침묵
blk(104, 105, 'num', kick='15번 홀 · 서의 벙커샷', ttl='핀까지', fig=50, dec=0, unit='cm', tone='up', hit=104,
    desc='오늘 서의 가장 좋은 샷', facts=[])
blk(109, 113, 'panel', date='2021 · 시카고대 자오와 에플리', hl=['칭찬하는', '사람의 예상'], hl_at=[109, 109],
    body=[('받는 기쁨은 실제보다 낮게', 112), ('어색함 걱정은 실제보다 크게', 113)])
blk(116, 118, 'quote', ttl='처방은 두 단어', lines=['나이스', '샷'], src='내 퍼트를 보기 전에', src_at=117)
blk(119, 120, 'quote', ttl='서가 떠올린 주인공', lines=['내 좋은 샷은', '한 번도 봐 준 적 없는 사람'], src='', src_at=120)

# ── 정리
blk(121, 126, 'timeline', kick='본인만 모르는', ttl='다섯 가지 행동',
    pts=[('1', '묻지 않은 훈수', '', 122), ('2', '내 이야기', '', 123), ('3', '남 재촉', '', 124), ('4', '한숨', '', 125), ('5', '침묵', '', 126)])
blk(129, 131, 'versus', kick='동반자들이 기억한 것', ttl='걱정 vs 실제',
    L=dict(label='내가 걱정한 것', val='7번 홀 OB', tone='gold', at=129), R=dict(label='그들이 기억한 것', val='나의 태도', tone='up', at=130),
    foot=('실수가 아니라 태도를 본다', 131))
blk(133, 134, 'quote', ttl='18번 홀', lines=['나이스', '샷'], src='누구보다 먼저', src_at=134)
blk(139, 140, 'quote', ttl='그늘집 심리학', lines=['다섯 가지 중', '가장 찔리는 번호는?'], src='댓글에 번호 하나', src_at=140)
blk(141, 142, 'end', ttl='그늘집 심리학', lines=['18홀 사이,', '마음을 쉬어 가는 곳'], src='오늘도 끝까지 봐 주셔서 고맙습니다')
BLOCKS = B

# ── 배경: 문장 번호 구간 → 그룹. g_* = 실사 스톡 여러 개를 돌려 씀, 나머지 = 이야기 장면용 AI 그림 1장(한 장 9초 이하)
GROUPS = {
  'g_putt': ['px_퍼팅_클로즈업', 'px_홀컵_깃대', 'px_그린_동반자'],
  'g_tee': ['px_티샷_시니어', 'px_드라이버_스윙', 'px_티샷_터널스윙'],
  'g_fairway': ['px_페어웨이_원경', 'px_페어웨이_전경', 'px_페어웨이_걷기', 'px_그린_카트원경'],
  'g_aerial': ['px_항공_그린벙커', 'px_항공_골프장', 'px_항공_호수골프장', 'px_항공_리조트연못', 'px_항공_골프장도로2'],
  'g_sunset': ['px_노을_골프장', 'px_항공_가을강'],
  'g_brain': ['뇌과학_009', '뇌과학_010', '뇌과학_011', '뇌과학_016', '뇌과학_035', '뇌과학_049'],
  'g_lab': ['뇌과학_012', '뇌과학_023', '뇌과학_029', '뇌과학_032'],
  'g_calm': ['자연_098', 'px_항공_숲호수', '자연_083'],
  'g_morning': ['자연_097', '자연_086', '자연_031'],
}
SCENE = [
  (0, 0, '세친구_떠남'), (1, 2, '밤_OB곱씹기'), (3, 3, 'g_lab'), (4, 4, '숲으로_티샷'), (5, 6, 'g_fairway'), (7, 7, '휴대폰_조용'),
  (8, 8, 'g_aerial'), (9, 9, '그늘집_외경'), (10, 10, 'g_aerial'), (11, 11, '네명_1번홀_동기'), (12, 12, '세친구_떠남'), (13, 13, '휴대폰_조용'),
  (14, 15, 'g_morning'), (16, 16, '윤_티샷오른쪽'), (17, 18, '주인공_훈수'), (19, 19, 'g_tee'), (20, 21, '윤_억지웃음'), (22, 22, 'g_fairway'),
  (23, 23, '조언_실험'), (24, 25, 'g_lab'), (26, 27, 'g_brain'), (28, 30, 'g_tee'), (31, 32, '주인공_질문'), (33, 33, 'g_fairway'), (34, 35, '윤_억지웃음'),
  (36, 37, 'g_aerial'), (38, 38, '그늘집_손자사진'), (39, 41, '주인공_말가로채기'), (42, 42, '그늘집_손자사진'), (43, 43, '뇌스캔_실험'),
  (44, 45, 'g_brain'), (46, 47, '돈_대신_말'), (48, 50, 'g_lab'), (51, 51, 'g_calm'), (52, 53, '주인공_경청'), (54, 55, '그늘집_외경'),
  (56, 57, 'g_aerial'), (58, 58, '숲으로_티샷'), (59, 60, '숲속_공찾기'), (61, 61, '카트옆_시계'), (62, 63, '주인공_재촉'), (64, 64, 'g_lab'),
  (65, 65, '농구팀_설문'), (66, 67, 'g_brain'), (68, 70, 'g_lab'), (71, 72, '잠정구'), (73, 73, 'g_tee'), (74, 75, '카트옆_시계'), (76, 79, 'g_calm'),
  (80, 81, 'g_aerial'), (82, 83, '미스샷_한숨'), (84, 84, '카트_침묵'), (85, 86, '강_어프로치짧음'), (87, 88, '회의실_배우'), (89, 90, 'g_lab'),
  (91, 92, 'g_brain'), (93, 94, '카트_침묵'), (95, 95, '미스샷_한숨'), (96, 97, '열걸음'), (98, 99, 'g_fairway'), (100, 101, '열걸음'),
  (102, 103, 'g_aerial'), (104, 105, '서_벙커샷'), (106, 107, '주인공_라인보기'), (108, 108, '서_웨지넣기'), (109, 109, '칭찬_실험'), (110, 110, 'g_lab'),
  (111, 112, '칭찬_실험'), (113, 115, 'g_calm'), (116, 118, '나이스샷'), (119, 120, '서_웨지넣기'),
  (121, 126, 'g_fairway'), (127, 127, '밤_OB곱씹기'), (128, 128, '귀갓길_차안'), (129, 129, '숲으로_티샷'), (130, 130, 'g_morning'), (131, 131, 'g_sunset'),
  (132, 132, '18번홀_석양티박스'), (133, 134, '나이스샷'), (135, 135, '윤_돌아보며웃음'), (136, 136, '주차장_약속'), (137, 137, '주차장_약속'), (138, 138, 'g_sunset'),
  (139, 139, '네명_1번홀_동기'), (140, 140, 'g_calm'), (141, 141, 'g_sunset'), (142, 142, '그늘집_노을'),
]
_S = [p for p in re.split(r'(?<=[.!?。？！])\s+|\n+', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '나레이션.txt'), encoding='utf-8').read()) if p.strip()]
LEXICON = [(re.escape(_S[i]), g) for a, b, g in SCENE for i in range(a, b + 1)]
STOCK_GROUPS = {g: GROUPS.get(g, [g]) for g in sorted({g for _, _, g in SCENE})}
STOCK_GROUPS['default'] = ['px_항공_호수골프장', 'px_페어웨이_전경', 'px_페어웨이_원경']
DISCLAIMER_SFX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sfx', 'disclaimer.mp3')

# ── 소재 이름 정확히 맞추기: STOCK_GROUPS 값은 "파일 이름에 들어 있는 단어"(부분 일치)라 '한선생'이 한선생_조언·깃발·퍼트까지 끌어온다 → 단일 그림은 '이름.mp4'로
for _g in list(STOCK_GROUPS):
  if not _g.startswith(('g_', 'p_')) and _g != 'default':
    STOCK_GROUPS[_g] = [_g + '.mp4']
for _g in [k for k in GROUPS if k.startswith('p_')]:
  STOCK_GROUPS[_g] = [c + '.mp4' for c in GROUPS[_g]]

# ── 카드 구간 배경: build.py는 카드 하나의 배경을 카드 전체 문장으로 고르므로(첫 문장 그룹이 모든 8.5초 슬롯을 차지),
#    카드마다 문장 순서대로 SCENE 그룹을 나열해 둔다(BLK_SEQ). stock 뒤 fix_registry.py가 registry에 blk_ 그룹을 이 순서로 만든다.
def _grp(i):
  for a, b, g in SCENE:
    if a <= i <= b:
      return g
BLK_SEQ = {}
_lex = []
for _b in BLOCKS:
  if _b['type'] == 'chap':
    continue
  _seq = []
  for _i in range(_b['a'], _b['b'] + 1):
    _seq.append(_grp(_i))
  if len(_seq) > 1:
    _k = f"blk_{_b['a']}"
    BLK_SEQ[_k] = _seq
    _lex.append((re.escape(_S[_b['a']]), _k))
LEXICON = _lex + LEXICON

# ── 카드 밖 구간도 같은 처리: build.py는 카드 없는 문장을 5초 이상 덩어리로 묶고 덩어리 첫 문장으로 배경을 고른다.
#    같은 방식으로 덩어리를 미리 계산해, 여러 소재가 섞인 덩어리는 chk_ 그룹(문장 순서)으로 만든다.
import json as _json
_tp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'timing.json')
if os.path.isfile(_tp):
  _T = _json.load(open(_tp, encoding='utf-8'))
  _own = set()
  for _b in BLOCKS:
    _own.update(range(_b['a'], _b['b'] + 1))
  for _k in CHAP_TITLES:
    _own.update((_k, _k + 1))
  _bounds = [c[0] for c in CHAPTERS] + [len(_S)]
  _lex2 = []
  for _ci in range(len(CHAPTERS)):
    _i, _z = _bounds[_ci], _bounds[_ci + 1]
    while _i < _z:
      if _i in _own:
        _i += 1
        continue
      _j = _i
      while _j + 1 < _z and (_j + 1) not in _own and _T[_j][1] - _T[_i][0] < 5.0:
        _j += 1
      _seq = [_grp(_x) for _x in range(_i, _j + 1)]
      if len(set(_seq)) > 1:
        BLK_SEQ[f'chk_{_i}'] = _seq
        _lex2.append((re.escape(_S[_i]), f'chk_{_i}'))
      _i = _j + 1
  LEXICON = _lex2 + LEXICON
