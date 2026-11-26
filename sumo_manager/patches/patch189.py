# v185 -> v186:玉垣親方(元智乃花)の絵
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=185;\nconst SAVE='sumoManager185',SAVE184", "const APPV=186;\nconst SAVE='sumoManager186',SAVE185='sumoManager185',SAVE184")
rep('[SAVE184,SAVE183', '[SAVE185,SAVE184,SAVE183')
rep('<title>Grand Sumo Manager v185', '<title>Grand Sumo Manager v186')
ui = open(os.path.join(here, 'pi186_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
