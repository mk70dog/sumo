# v171 -> v172:追手風親方(元大翔山。追手風部屋の師匠)の絵(ダルマさん「追手風 直樹」)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=171;\nconst SAVE='sumoManager171',SAVE170", "const APPV=172;\nconst SAVE='sumoManager172',SAVE171='sumoManager171',SAVE170")
rep('[SAVE170,SAVE169', '[SAVE171,SAVE170,SAVE169')
rep('<title>Grand Sumo Manager v171', '<title>Grand Sumo Manager v172')
ui = open(os.path.join(here, 'pi172_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
