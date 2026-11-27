# v190 -> v191:おかみさんの絵 2 枚(スタッフの画面と部屋の声の窓)。部屋の声の窓に師匠・弟子の絵も
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=190;\nconst SAVE='sumoManager190',SAVE189", "const APPV=191;\nconst SAVE='sumoManager191',SAVE190='sumoManager190',SAVE189")
rep('[SAVE189,SAVE188', '[SAVE190,SAVE189,SAVE188')
rep('<title>Grand Sumo Manager v190', '<title>Grand Sumo Manager v191')
ui = open(os.path.join(here, 'okami191_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
