# v99 -> v100:実在の力士のけがの記録を 5 年分に(ダルマさん「許可するのでもう一度」)。
# v99 は直近 6 場所(data/rec6_2026.txt)だけ。2021 年 11 月〜2025 年 9 月の幕内の休場(data/kyujo_makuuchi_2021_2025.txt、英語版 Wikipedia「20XX in sumo」)を足す。
import sys, os, json, re
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v99</title>', '<title>Grand Sumo Manager v100</title>')
rep("const APPV=99;\nconst SAVE='sumoManager99',SAVE98", "const APPV=100;\nconst SAVE='sumoManager100',SAVE99='sumoManager99',SAVE98")
rep('[SAVE98,SAVE97', '[SAVE99,SAVE98,SAVE97')
rep(" if(g.v===98){g.v=99;}\n return g.v===99?g:null;}", " if(g.v===98){g.v=99;}\n if(g.v===99){g.v=100;}\n return g.v===100?g:null;}")
rep('G={v:99,', 'G={v:100,')
rec = {}
def load(fn):
    for l in open(os.path.join(here, '..', 'data', fn), encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        f = l.strip().split('|')
        if len(f) < 7: continue
        try: ab = int(f[6])
        except: continue
        if ab > 0:
            full = 7 if f[1] == 'S' else 15
            L = rec.setdefault(f[3], [])
            if not any(x[0] == int(f[0]) for x in L): L.append([int(f[0]), ab, full])
load('rec6_2026.txt'); load('kyujo_makuuchi_2021_2025.txt')
for k in rec: rec[k].sort()
m = re.search(r'const REC5=\{.*?\};\n', s)
if not m: raise SystemExit('REC5 なし')
s = s.replace(m.group(0), 'const REC5=' + json.dumps(rec, ensure_ascii=False, separators=(',', ':')) + ';/* 2021 年 11 月〜2025 年 9 月は幕内だけ(英語版 Wikipedia)、2025 年 11 月から幕内・十両・幕下(sumodb) */\n')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '人数', len(rec), '件数', sum(len(v) for v in rec.values()))
