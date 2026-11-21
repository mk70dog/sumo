# v103 -> v104:実在の力士のけがの記録に、十両の 2021 年 11 月〜2025 年 9 月を足す(ダルマさん「お任せで実施」)。
# v100 では十両は資料がなく幕内だけだった。sumodb の番付ページ(十両の星取)を WebFetch で読み、data/kyujo_juryo_2021_2025.txt にまとめた。
# 2026 年の番付にいない力士の分も入れるが、名前で引くので使われない。四股名は今の名前に(伯桜鵬→伯乃富士、琴ノ若→琴櫻)。同じ場所が重なれば先に読んだ方(rec6 → 幕内 → 十両)。
import sys, os, json, re
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v103</title>', '<title>Grand Sumo Manager v104</title>')
rep("const APPV=103;\nconst SAVE='sumoManager103',SAVE102", "const APPV=104;\nconst SAVE='sumoManager104',SAVE103='sumoManager103',SAVE102")
rep('[SAVE102,SAVE101', '[SAVE103,SAVE102,SAVE101')
rep(" if(g.v===102){g.v=103;}\n return g.v===103?g:null;}", " if(g.v===102){g.v=103;}\n if(g.v===103){g.v=104;}\n return g.v===104?g:null;}")
rep('G={v:103,', 'G={v:104,')
m = re.search(r'const REALB=(\[.*?\]);', s); names = {x.split('|')[1] for x in json.loads(m.group(1))}
REN = {'伯桜鵬': '伯乃富士', '琴ノ若': '琴櫻'}
rec = {}; skip = set()
def load(fn):
    for l in open(os.path.join(here, '..', 'data', fn), encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        f = l.strip().split('|')
        if len(f) < 7: continue
        try: ab = int(f[6])
        except: continue
        n = REN.get(f[3], f[3])
        if ab > 0:
            if n not in names: skip.add(n)
            full = 7 if f[1] == 'S' else 15
            L = rec.setdefault(n, [])
            if not any(x[0] == int(f[0]) for x in L): L.append([int(f[0]), ab, full])
load('rec6_2026.txt'); load('kyujo_makuuchi_2021_2025.txt'); load('kyujo_juryo_2021_2025.txt')
for k in rec: rec[k].sort()
m = re.search(r'const REC5=\{.*?\};[^\n]*\n', s)
if not m: raise SystemExit('REC5 なし')
s = s.replace(m.group(0), 'const REC5=' + json.dumps(rec, ensure_ascii=False, separators=(',', ':')) + ';/* 2021 年 11 月〜2025 年 9 月は幕内(英語版 Wikipedia)と十両(sumodb)、2025 年 11 月から幕内・十両・幕下(sumodb) */\n')
# 十両の分だけけがしやすい力士が増えたので、全体の数が変わらないよう割る数を 1.03 → 1.05 に(測定で合わせた推定)
rep("function injProne(r){return Math.min(1.5,1+.08*injSum(r))/1.03;}/* 1.03=", "function injProne(r){return Math.min(1.5,1+.08*injSum(r))/1.05;}/* 1.05(v104。v103 までは 1.03)=")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '人数', len(rec), '件数', sum(len(v) for v in rec.values()), '2026 年の番付の名前と合わない(使われない)', sorted(skip))
