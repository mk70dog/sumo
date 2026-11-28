# v205 -> v206:タブを部屋の上の窓(ポップアップ)で開く。× か窓の外で部屋に戻る。設定で前の形にも戻せる
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=205;\nconst SAVE='sumoManager205',SAVE204", "const APPV=206;\nconst SAVE='sumoManager206',SAVE205='sumoManager205',SAVE204")
rep('[SAVE204,SAVE203', '[SAVE205,SAVE204,SAVE203')
rep('<title>Grand Sumo Manager v205', '<title>Grand Sumo Manager v206')
ui = open(os.path.join(here,'pop209_ui.js'),encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
