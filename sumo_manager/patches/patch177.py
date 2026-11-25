# v173 -> v174:高島親方(元高望山。追手風部屋の部屋付き親方)の絵(ダルマさん「高島 大造」)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=173;\nconst SAVE='sumoManager173',SAVE172", "const APPV=174;\nconst SAVE='sumoManager174',SAVE173='sumoManager173',SAVE172")
rep('[SAVE172,SAVE171', '[SAVE173,SAVE172,SAVE171')
rep('<title>Grand Sumo Manager v173', '<title>Grand Sumo Manager v174')
ui = open(os.path.join(here, 'pi174_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
