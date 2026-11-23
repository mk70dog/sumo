# v145 -> v146:2026 年九州場所の実際の成績を入れる(ダルマさん「2026 九州場所は終了したので実際のデータを収集して反映させる」→ 設計案 →「実施」)。
#   ① data/kyushu2026.txt(全 592 人の成績)を RK11 として入れ、実名で始めると九州場所を実際の成績で終えたところから始まる(rk146_core.js)。
#   ② 優勝決定戦の勝者と三賞を実際のとおりにする(endBasho に G._rkYu・G._rkSh の口を足す)。
#   ③ 実在の力士の補正値 REALX を、九州場所を足した直近 6 場所(2026 年 1 月〜11 月)で作り直す(tools/mkrealx146.py → patches/realx146.json)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=145;\nconst SAVE='sumoManager145',SAVE144", "const APPV=146;\nconst SAVE='sumoManager146',SAVE145='sumoManager145',SAVE144")
rep('[SAVE144,SAVE143', '[SAVE145,SAVE144,SAVE143')
rep('<title>Grand Sumo Manager v145', '<title>Grand Sumo Manager v146')
# ③ REALX
i = s.index('const REALX='); j = s.index(';', i)
X = open(os.path.join(here, 'realx146.json'), encoding='utf-8').read().strip()
s = s[:i] + 'const REALX=' + X + s[j:]
# ② 優勝決定戦・三賞
rep("if(top.length>1){let pool=top.slice();",
    "if(top.length>1&&G._rkYu&&G._rkYu[d]&&top.some(x=>G.R[x].n===G._rkYu[d])){win=top.find(x=>G.R[x].n===G._rkYu[d]);sum.po.push({d:d,ids:top,w:win});}\n  else if(top.length>1){let pool=top.slice();")
rep("sh.forEach(([id,t])=>{const r=G.R[id];r.sansho++;",
    "if(G._rkSh){sh.length=0;G._rkSh.forEach(([n,t])=>{const id=G.order.find(x=>G.R[x].n===n);if(id!=null)sh.push([id,t]);});}\n sh.forEach(([id,t])=>{const r=G.R[id];r.sansho++;")
rep("function retireCheck(){\n const B=G.B;", "function retireCheck(){\n if(G._rkYu)return;/* v146:九州場所を実際の成績で終えるときは、ゲームの引退は起こさない(実際の発表がまだないため) */\n const B=G.B;")
# ① 実際の成績
d = {}
for l in open(os.path.join(here, '..', 'data', 'kyushu2026.txt'), encoding='utf-8'):
    if l.startswith('#'): continue
    rk, nm, ro, w, lo, a = l.strip().split('|'); d[nm] = [int(w), int(lo), int(a)]
core = open(os.path.join(here, 'rk146_core.js'), encoding='utf-8').read().replace('__RK11__', json.dumps(d, ensure_ascii=False, separators=(',', ':')))
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("addNews('力士・部屋・師匠・一門は 2026 年の実在のものです。能力は番付と年齢からの推定で、これから起きる出来事はすべてゲーム内の架空のものです。');\n}",
    "addNews('力士・部屋・師匠・一門は 2026 年の実在のものです。能力は番付・年齢と直近 6 場所の成績からの推定で、これから起きる出来事はすべてゲーム内の架空のものです。');\n rkReplay();\n}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
