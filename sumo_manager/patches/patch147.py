# v143 -> v144:伊勢ノ海親方(元北勝鬨)の絵(ダルマさん「伊勢ノ海 準人」)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=143;\nconst SAVE='sumoManager143',SAVE142", "const APPV=144;\nconst SAVE='sumoManager144',SAVE143='sumoManager143',SAVE142")
rep('[SAVE142,SAVE141', '[SAVE143,SAVE142,SAVE141')
rep('<title>Grand Sumo Manager v143', '<title>Grand Sumo Manager v144')
ui = open(os.path.join(here, 'pi144_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
