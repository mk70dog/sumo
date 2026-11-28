# v196 -> v197:上の段とタブをどのタブでも細く
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=196;\nconst SAVE='sumoManager196',SAVE195", "const APPV=197;\nconst SAVE='sumoManager197',SAVE196='sumoManager196',SAVE195")
rep('[SAVE195,SAVE194', '[SAVE196,SAVE195,SAVE194')
rep('<title>Grand Sumo Manager v196', '<title>Grand Sumo Manager v197')

ui = open(os.path.join(here, 'hd197_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
