# v180 -> v181:寿之富士の絵。v178 の錦富士の 2 枚目(寿)を外す
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=180;\nconst SAVE='sumoManager180',SAVE179", "const APPV=181;\nconst SAVE='sumoManager181',SAVE180='sumoManager180',SAVE179")
rep('[SAVE179,SAVE178', '[SAVE180,SAVE179,SAVE178')
rep('<title>Grand Sumo Manager v180', '<title>Grand Sumo Manager v181')
import json as _j
i=s.index('const A={"錦富士": [');j=s.index(';for(const k in A)',i)
A=_j.loads(s[i+8:j]);A['錦富士']=A['錦富士'][1:]
s=s[:i+8]+_j.dumps(A,ensure_ascii=False)+s[j:]
ui = open(os.path.join(here, 'pi181_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
