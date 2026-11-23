# v142 -> v143:間垣親方(元石浦)の絵(ダルマさん「間垣 喜翔」)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=142;\nconst SAVE='sumoManager142',SAVE141", "const APPV=143;\nconst SAVE='sumoManager143',SAVE142='sumoManager142',SAVE141")
rep('[SAVE141,SAVE140', '[SAVE142,SAVE141,SAVE140')
rep('<title>Grand Sumo Manager v142', '<title>Grand Sumo Manager v143')
ui = open(os.path.join(here, 'pi143_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
