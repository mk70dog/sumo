# v175 -> v176:若元春の絵(ダルマさん「ワカモトハル」。青地に星・前垂れの下に「東京石灰工業」)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=175;\nconst SAVE='sumoManager175',SAVE174", "const APPV=176;\nconst SAVE='sumoManager176',SAVE175='sumoManager175',SAVE174")
rep('[SAVE174,SAVE173', '[SAVE175,SAVE174,SAVE173')
rep('<title>Grand Sumo Manager v175', '<title>Grand Sumo Manager v176')
ui = open(os.path.join(here, 'pi176_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
