# v144 -> v145:甲山親方(元大碇。伊勢ノ海部屋の部屋付き親方)の絵(ダルマさん「甲山 剛」)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=144;\nconst SAVE='sumoManager144',SAVE143", "const APPV=145;\nconst SAVE='sumoManager145',SAVE144='sumoManager144',SAVE143")
rep('[SAVE143,SAVE142', '[SAVE144,SAVE143,SAVE142')
rep('<title>Grand Sumo Manager v144', '<title>Grand Sumo Manager v145')
ui = open(os.path.join(here, 'pi145_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
