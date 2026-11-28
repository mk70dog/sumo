# v194 -> v195:部屋の画面を iPad で 1 画面に(見本 fv1)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=194;\nconst SAVE='sumoManager194',SAVE193", "const APPV=195;\nconst SAVE='sumoManager195',SAVE194='sumoManager194',SAVE193")
rep('[SAVE193,SAVE192', '[SAVE194,SAVE193,SAVE192')
rep('<title>Grand Sumo Manager v194', '<title>Grand Sumo Manager v195')
ui = open(os.path.join(here, 'fv195_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
