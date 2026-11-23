# v134 -> v135:力士・親方の絵(ダルマさん「錦富士 翠富士 桐山親方 画像追加する サンプル」)。絵は data/portraits135.json、画面は patches/pi135_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=134;\nconst SAVE='sumoManager134',SAVE133", "const APPV=135;\nconst SAVE='sumoManager135',SAVE134='sumoManager134',SAVE133")
rep('[SAVE133,SAVE132', '[SAVE134,SAVE133,SAVE132')
rep('<title>Grand Sumo Manager v134', '<title>Grand Sumo Manager v135')
ui = open(os.path.join(here, 'pi135_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
