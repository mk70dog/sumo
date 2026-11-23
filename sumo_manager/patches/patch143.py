# v139 -> v140:親方の絵 4 枚(ダルマさん「もと旭富士 もと照ノ富士 もと魁皇 もとカイセイ」)。部屋付き親方も元の四股名で絵を引く。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=139;\nconst SAVE='sumoManager139',SAVE138", "const APPV=140;\nconst SAVE='sumoManager140',SAVE139='sumoManager139',SAVE138")
rep('[SAVE138,SAVE137', '[SAVE139,SAVE138,SAVE137')
rep('<title>Grand Sumo Manager v139', '<title>Grand Sumo Manager v140')
ui = open(os.path.join(here, 'pi140_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
