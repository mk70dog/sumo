# v215 -> v216:親方の物語(ダルマさん「親方にも物語があるね」)。元データ data/oyastory2026.txt、部品 patches/oya219_ui.js。
#   実在の師匠 5 人の歩み(出典つき)、ゲームの中の師匠の物語(部屋を興す・初の関取・初の賜杯・大関・横綱・師匠を超えた・師匠ゆずりの型)、
#   部屋を譲るときの名場面 3 つと「歴代の師匠」。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=215;\nconst SAVE='sumoManager215',SAVE214", "const APPV=216;\nconst SAVE='sumoManager216',SAVE215='sumoManager215',SAVE214")
rep('[SAVE214,SAVE213', '[SAVE215,SAVE214,SAVE213')
rep('<title>Grand Sumo Manager v215', '<title>Grand Sumo Manager v216')
D = {}
for l in open(os.path.join(here, '..', 'data', 'oyastory2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.rstrip('\n').split('|'); n = a[0]
    d = D.setdefault(n, {'sum': '', 'ev': []})
    if a[1] == 'まとめ': d['sum'] = a[2]
    elif a[1] == '型':
        d[a[2]] = int(a[3]) if a[3].isdigit() else a[3]
    else: d['ev'].append([a[1], a[2], a[3] if len(a) > 3 else ''])
ui = open(os.path.join(here, 'oya219_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', '<script>window.OYSD=' + json.dumps(D, ensure_ascii=False) + ';\n' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '親方の物語', len(D), '人')
