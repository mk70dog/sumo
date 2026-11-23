# v155 -> v156:実在の力士の性格を 2 人足す(玉鷲=記事、尊富士=Claude の見立て。data/per2026.txt の v156 の欄)。
#   前の版の保存データも、実在の力士で「ふつう」のままの人は読み込みのときに新しい表の性格にする。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=155;\nconst SAVE='sumoManager155',SAVE154", "const APPV=156;\nconst SAVE='sumoManager156',SAVE155='sumoManager155',SAVE154")
rep('[SAVE154,SAVE153', '[SAVE155,SAVE154,SAVE153')
rep('<title>Grand Sumo Manager v155', '<title>Grand Sumo Manager v156')
P = {}
for l in open(os.path.join(here, '..', 'data', 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
i = s.index('const REALPER='); j = s.index(';\n', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, len(P), '人')
