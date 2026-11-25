# v181 -> v182:絵の取り違えの直し(錦富士の 2 枚目=嵐富士の絵を外す・旭富士の絵を正しく)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=181;\nconst SAVE='sumoManager181',SAVE180", "const APPV=182;\nconst SAVE='sumoManager182',SAVE181='sumoManager181',SAVE180")
rep('[SAVE180,SAVE179', '[SAVE181,SAVE180,SAVE179')
rep('<title>Grand Sumo Manager v181', '<title>Grand Sumo Manager v182')
import json as _j
i=s.index('const A={"錦富士": [');j=s.index(';for(const k in A)',i)
A=_j.loads(s[i+8:j]);del A['錦富士']
s=s[:i+8]+_j.dumps(A,ensure_ascii=False)+s[j:]
ui = open(os.path.join(here, 'pi182_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
