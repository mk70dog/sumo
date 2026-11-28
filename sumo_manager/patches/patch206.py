# v202 -> v203:目標(30 種)・若い衆のライバル・兄弟子と弟弟子の絆・跡継ぎを育てる
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=202;\nconst SAVE='sumoManager202',SAVE201", "const APPV=203;\nconst SAVE='sumoManager203',SAVE202='sumoManager202',SAVE201")
rep('[SAVE201,SAVE200', '[SAVE202,SAVE201,SAVE200')
rep('<title>Grand Sumo Manager v202', '<title>Grand Sumo Manager v203')

# v203:目標・若い衆のライバル・兄弟子の絆・跡継ぎ
ui = open(os.path.join(here,'mk203_ui.js'),encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
