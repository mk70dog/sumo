# v191 -> v192:トレーナーの絵 4 枚(外部との契約のボタンと部屋の声)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=191;\nconst SAVE='sumoManager191',SAVE190", "const APPV=192;\nconst SAVE='sumoManager192',SAVE191='sumoManager191',SAVE190")
rep('[SAVE190,SAVE189', '[SAVE191,SAVE190,SAVE189')
rep('<title>Grand Sumo Manager v191', '<title>Grand Sumo Manager v192')
ui = open(os.path.join(here, 'tr192_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
