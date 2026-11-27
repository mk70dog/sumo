# v192 -> v193:絵のない力士の共通の絵 4 枚
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=192;\nconst SAVE='sumoManager192',SAVE191", "const APPV=193;\nconst SAVE='sumoManager193',SAVE192='sumoManager192',SAVE191")
rep('[SAVE191,SAVE190', '[SAVE192,SAVE191,SAVE190')
rep('<title>Grand Sumo Manager v192', '<title>Grand Sumo Manager v193')
ui = open(os.path.join(here, 'genr193_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
