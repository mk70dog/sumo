# v177 -> v178:力士の絵(伯乃富士・義ノ富士・旭富士。錦富士 2 枚・炎鵬 1 枚は場所ごとに替わる)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=177;\nconst SAVE='sumoManager177',SAVE176", "const APPV=178;\nconst SAVE='sumoManager178',SAVE177='sumoManager177',SAVE176")
rep('[SAVE176,SAVE175', '[SAVE177,SAVE176,SAVE175')
rep('<title>Grand Sumo Manager v177', '<title>Grand Sumo Manager v178')
ui = open(os.path.join(here, 'pi178_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
