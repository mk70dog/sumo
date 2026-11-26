# v183 -> v184:阿武剋の絵
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=183;\nconst SAVE='sumoManager183',SAVE182", "const APPV=184;\nconst SAVE='sumoManager184',SAVE183='sumoManager183',SAVE182")
rep('[SAVE182,SAVE181', '[SAVE183,SAVE182,SAVE181')
rep('<title>Grand Sumo Manager v183', '<title>Grand Sumo Manager v184')
ui = open(os.path.join(here, 'pi184_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
