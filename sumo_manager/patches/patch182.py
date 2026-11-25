# v178 -> v179:力士の絵(錦木。若元春は 2 枚目で場所ごとに替わる)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=178;\nconst SAVE='sumoManager178',SAVE177", "const APPV=179;\nconst SAVE='sumoManager179',SAVE178='sumoManager178',SAVE177")
rep('[SAVE177,SAVE176', '[SAVE178,SAVE177,SAVE176')
rep('<title>Grand Sumo Manager v178', '<title>Grand Sumo Manager v179')
ui = open(os.path.join(here, 'pi179_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
