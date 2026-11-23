# v150 -> v151:①成長型「晩成」の裏付け(新入幕が 27 歳以上で、今 30 歳未満の幕内力士。data/shinnyu2026.txt、観戦ガイド)
#   ②性格の裏付けを 6 人足した(data/per2026.txt。v149 の patch152 が作る REALPER を作り直す)。ダルマさん「続ける」。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=150;\nconst SAVE='sumoManager150',SAVE149", "const APPV=151;\nconst SAVE='sumoManager151',SAVE150='sumoManager150',SAVE149")
rep('[SAVE149,SAVE148', '[SAVE150,SAVE149,SAVE148')
rep('<title>Grand Sumo Manager v150', '<title>Grand Sumo Manager v151')
data = os.path.join(here, '..', 'data')
P = {}
for l in open(os.path.join(data, 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
LATE = {}
for l in open(os.path.join(data, 'shinnyu2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    n, b, d, j, m = l.strip().split('|')
    if not b or not m: continue
    by, bm = int(b[:4]), int(b[5:7]); my, mm = int(m[:4]), int(m[5:7])
    LATE[n] = round((my * 12 + mm - by * 12 - bm) / 12, 1)
i = s.index('const REALPER='); j = s.index(';\n', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("function realTraits(r,t,i){r.real=1;r.gt=(r.age>=30&&i<42)?3:1;",
    "const REALNYU=" + json.dumps(LATE, ensure_ascii=False, separators=(',', ':')) + ";/* v151:新入幕の年齢(data/shinnyu2026.txt) */\n"
    "function realTraits(r,t,i){r.real=1;r.gt=(r.age>=30&&i<42)?3:((REALNYU[r.n]||0)>=27&&r.age<30)?2:1;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'per', len(P), 'late', [k for k, v in LATE.items() if v >= 27])
