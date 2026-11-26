# v186 -> v187:部屋の声(師匠・おかみさん・部屋付き親方)の言葉を週ごとに変える
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=186;\nconst SAVE='sumoManager186',SAVE185", "const APPV=187;\nconst SAVE='sumoManager187',SAVE186='sumoManager186',SAVE185")
rep('[SAVE185,SAVE184', '[SAVE186,SAVE185,SAVE184')
rep('<title>Grand Sumo Manager v186', '<title>Grand Sumo Manager v187')
ui = open(os.path.join(here, 'koe187.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
