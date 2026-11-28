# v211 -> v212:実在の力士の性格を 3 人足す(data/per2026.txt の v212 の欄)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=211;\nconst SAVE='sumoManager211',SAVE210", "const APPV=212;\nconst SAVE='sumoManager212',SAVE211='sumoManager211',SAVE210")
rep('[SAVE210,SAVE209', '[SAVE211,SAVE210,SAVE209')
rep('<title>Grand Sumo Manager v211', '<title>Grand Sumo Manager v212')
# 性格
P = {}
for l in open(os.path.join(here, '..', 'data', 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
i = s.index('const REALPER='); j = s.index(';', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '性格', len(P), '人')
