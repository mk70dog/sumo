# v179 -> v180:藤ノ川の絵。v179 の若元春の 2 枚目を外す
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=179;\nconst SAVE='sumoManager179',SAVE178", "const APPV=180;\nconst SAVE='sumoManager180',SAVE179='sumoManager179',SAVE178")
rep('[SAVE178,SAVE177', '[SAVE179,SAVE178,SAVE177')
rep('<title>Grand Sumo Manager v179', '<title>Grand Sumo Manager v180')
import re
i=s.index('/* v179:');j=s.index('(function(){const A={"若元春"',i);k=s.index('</script>',j)
s=s[:j]+'/* v180 で若元春の 2 枚目は外した */\n'+s[k:]
ui = open(os.path.join(here, 'pi180_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
