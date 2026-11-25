# v172 -> v173:北陣親方(元遠藤。ダルマさん「北陣 聖大」)・立田山親方(元薩洲洋。ダルマさん「立田山 裕教」)の絵。どちらも追手風部屋の部屋付き親方
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=172;\nconst SAVE='sumoManager172',SAVE171", "const APPV=173;\nconst SAVE='sumoManager173',SAVE172='sumoManager172',SAVE171")
rep('[SAVE171,SAVE170', '[SAVE172,SAVE171,SAVE170')
rep('<title>Grand Sumo Manager v172', '<title>Grand Sumo Manager v173')
ui = open(os.path.join(here, 'pi173_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
