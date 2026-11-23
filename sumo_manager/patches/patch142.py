# v138 -> v139:師匠の絵(ダルマさん「坊主は無双山 両国」=藤島親方〈元武双山〉・境川親方〈元両国〉)。スタッフの画面の「親方」と、実在の部屋を選ぶ画面の札に絵。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=138;\nconst SAVE='sumoManager138',SAVE137", "const APPV=139;\nconst SAVE='sumoManager139',SAVE138='sumoManager138',SAVE137")
rep('[SAVE137,SAVE136', '[SAVE138,SAVE137,SAVE136')
rep('<title>Grand Sumo Manager v138', '<title>Grand Sumo Manager v139')
ui = open(os.path.join(here, 'pi139_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
