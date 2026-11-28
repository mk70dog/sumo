# v201 -> v202:研修の期間・料金・研修中の留守
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=201;\nconst SAVE='sumoManager201',SAVE200", "const APPV=202;\nconst SAVE='sumoManager202',SAVE201='sumoManager201',SAVE200")
rep('[SAVE200,SAVE199', '[SAVE201,SAVE200,SAVE199')
rep('<title>Grand Sumo Manager v201', '<title>Grand Sumo Manager v202')

# v202:研修の期間・料金・留守のデメリット
rep(open(os.path.join(here,'grow201_ui.js'),encoding='utf-8').read(),open(os.path.join(here,'grow202_ui.js'),encoding='utf-8').read())
ui = ''

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
