# v210 -> v211:実在の部屋付き親方の出身校を 30 人足す(data/co_sch_notes.txt)・実在の力士の性格を 4 人足す(data/per2026.txt の v211 の欄)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=210;\nconst SAVE='sumoManager210',SAVE209", "const APPV=211;\nconst SAVE='sumoManager211',SAVE210='sumoManager210',SAVE209")
rep('[SAVE209,SAVE208', '[SAVE210,SAVE209,SAVE208')
rep('<title>Grand Sumo Manager v210', '<title>Grand Sumo Manager v211')
# 出身校
add = []
on = False
for l in open(os.path.join(here, '..', 'data', 'co_sch_notes.txt'), encoding='utf-8'):
    if l.startswith('# 2026-11-28'): on = True; continue
    if not on or l.startswith('#') or not l.strip(): continue
    a = l.rstrip('\n').split('|')
    add.append('%s:[%s,%s]' % (a[0], json.dumps(a[1], ensure_ascii=False).replace('"', "'"), json.dumps(a[2], ensure_ascii=False).replace('"', "'")))
rep("宝富士:['','近畿大学']};", "宝富士:['','近畿大学'],\n " + ','.join(add) + '};')
# 前の版の保存:実在の部屋付き親方の出身校を新しい表で上書きする
rep("function coEnsure(s){if(!isCo(s)||s.prof)return s;", "function coEnsure(s){if(isCo(s)&&s.prof&&s.prof.src==='実在'){const c=COSCH[cnm(s)];if(c&&(s.prof.hs!==c[0]||s.prof.uni!==c[1])){s.prof.hs=c[0];s.prof.uni=c[1];}}if(!isCo(s)||s.prof)return s;")
# 性格
P = {}
for l in open(os.path.join(here, '..', 'data', 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
i = s.index('const REALPER='); j = s.index(';', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '出身校', len(add), '人 / 性格', len(P), '人')
