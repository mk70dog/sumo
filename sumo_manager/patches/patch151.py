# v147 -> v148:九州場所の幕下以下の日ごとの星、十両以下のこれまでの優勝(2021 年以前を含む幕内 31 人)、十両の力士の金星・三賞(一部)。
#   data/kyushu2026_bouts.txt(全段 2243 番)と data/career2026.txt から、本体の RK11B・RKCAR を作り直す。
import sys, os, json, re
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=147;\nconst SAVE='sumoManager147',SAVE146", "const APPV=148;\nconst SAVE='sumoManager148',SAVE147='sumoManager147',SAVE146")
rep('[SAVE146,SAVE145', '[SAVE147,SAVE146,SAVE145')
rep('<title>Grand Sumo Manager v147', '<title>Grand Sumo Manager v148')
data = os.path.join(here, '..', 'data')
B = []
for l in open(os.path.join(data, 'kyushu2026_bouts.txt'), encoding='utf-8'):
    if l.startswith('#'): continue
    d, e, r, w, k = l.rstrip('\n').split('|'); B.append([int(d), e, r, w, k])
C = {}
for l in open(os.path.join(data, 'career2026.txt'), encoding='utf-8'):
    if l.startswith('#'): continue
    a = l.strip().split('|'); C[a[0]] = [int(x) for x in a[1:]]
def setconst(name, val):
    global s
    i = s.index('const ' + name + '='); j = s.index(';\n', i)
    s = s[:i] + 'const ' + name + '=' + json.dumps(val, ensure_ascii=False, separators=(',', ':')) + s[j:]
setconst('RK11B', B); setconst('RKCAR', C)
rep("   幕下以下は日ごとの並びが入っていない(勝ち負けの数だけ)。", "   v148:幕下以下も全段の取組を入れた(2243 番。番付外の本田との一番は相手がいないので空ける)。")
rep("   十両以下の各段優勝は 2022 年以降の一覧から取ったので、それより前だけに優勝した人は 0 のまま。十両の力士の金星・三賞は入っていない。 */",
    "   v148:幕内 31 人の幕下以下の優勝は全期間(観戦ガイド)。そのほかの人の十両以下の優勝は 2022 年以降の一覧から。十両の力士の金星・三賞は明生・翔猿・御嶽海・千代翔馬・正代・若隆景・翠富士の分だけ。 */")
rep("(全員の勝ち負け・休場・優勝・三賞、幕内・十両の日ごとの星と金星が実際のとおり。", "(全員の勝ち負け・休場・優勝・三賞、全段の日ごとの星と金星が実際のとおり。")
rep(" G.order.forEach(i=>{const r=G.R[i],c=B.rec[i];if(r.d>1||!(c.ab>0))return;for(let x=0;x<15;x++)if(!c.res[x])c.res[x]={r:'や'};});}",
    " G.order.forEach(i=>{const r=G.R[i],c=B.rec[i];if(!(c.ab>0))return;if(r.d<=1){for(let x=0;x<15;x++)if(!c.res[x])c.res[x]={r:'や'};}else if(c.w+c.l===0)(c.days||[]).forEach(x=>{if(!c.res[x-1])c.res[x-1]={r:'や'};});});}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, len(B), len(C))
