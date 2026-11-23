# v146 -> v147:九州場所の日ごとの星・金星、実在の力士のこれまでの優勝回数・金星・三賞(ダルマさん「日ごとの星の並び、金星、これまでの優勝回数 … 実施」)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=146;\nconst SAVE='sumoManager146',SAVE145", "const APPV=147;\nconst SAVE='sumoManager147',SAVE146='sumoManager146',SAVE145")
rep('[SAVE145,SAVE144', '[SAVE146,SAVE145,SAVE144')
rep('<title>Grand Sumo Manager v146', '<title>Grand Sumo Manager v147')
data = os.path.join(here, '..', 'data')
B = []
for l in open(os.path.join(data, 'kyushu2026_bouts.txt'), encoding='utf-8'):
    if l.startswith('#'): continue
    d, e, r, w, k = l.rstrip('\n').split('|'); B.append([int(d), e, r, w, k])
C = {}
for l in open(os.path.join(data, 'career2026.txt'), encoding='utf-8'):
    if l.startswith('#'): continue
    a = l.strip().split('|'); C[a[0]] = [int(x) for x in a[1:]]
core = open(os.path.join(here, 'rk147_core.js'), encoding='utf-8').read().replace('__RK11B__', json.dumps(B, ensure_ascii=False, separators=(',', ':'))).replace('__RKCAR__', json.dumps(C, ensure_ascii=False, separators=(',', ':')))
rep("function rkReplay(){", core + "function rkReplay(){")
rep(" B.day=15;B.cur=[];B.next=[];\n G._rkYu=RK11YU;", " B.day=15;B.cur=[];B.next=[];\n rkCareer();rkBouts(B);\n G._rkYu=RK11YU;")
rep("(全員の勝ち負け・休場・優勝・三賞が実際のとおり)", "(全員の勝ち負け・休場・優勝・三賞、幕内・十両の日ごとの星と金星が実際のとおり。これまでの優勝回数・金星・三賞も実際の数)")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
