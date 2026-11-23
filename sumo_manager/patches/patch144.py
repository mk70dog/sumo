# v140 -> v141:熱海富士の絵(ダルマさん「熱海富士」)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=140;\nconst SAVE='sumoManager140',SAVE139", "const APPV=141;\nconst SAVE='sumoManager141',SAVE140='sumoManager140',SAVE139")
rep('[SAVE139,SAVE138', '[SAVE140,SAVE139,SAVE138')
rep('<title>Grand Sumo Manager v140', '<title>Grand Sumo Manager v141')
ui = open(os.path.join(here, 'pi141_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
