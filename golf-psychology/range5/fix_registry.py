# -*- coding: utf-8 -*-
# build.py stock 뒤에 실행: plan.py BLK_SEQ대로 registry.json에 blk_ 그룹을 만든다(문장 순서 = 슬롯 순서, 같은 그룹이면 다음 클립)
import json, os, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p', os.path.join(H, 'plan.py')); p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
rp = os.path.join(H, 'assets', 'stock', 'registry.json')
reg = {k: v for k, v in json.load(open(rp, encoding='utf-8')).items() if not k.startswith('blk_')}
for k, seq in p.BLK_SEQ.items():
  out, used = [], {}
  for g in seq:
    files = reg.get(g) or []
    if not files:
      continue
    f = files[used.get(g, 0) % len(files)]
    used[g] = used.get(g, 0) + 1
    if not out or out[-1] != f:
      out.append(f)
  reg[k] = out
json.dump(reg, open(rp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('blk 그룹', len(p.BLK_SEQ), '개 · 예시 blk_8 =', reg.get('blk_8'))
