# v193 -> v194:新弟子・記録タブの新しい情報に「新」の印、上にまとめる
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=193;\nconst SAVE='sumoManager193',SAVE192", "const APPV=194;\nconst SAVE='sumoManager194',SAVE193='sumoManager193',SAVE192")
rep('[SAVE192,SAVE191', '[SAVE193,SAVE192,SAVE191')
rep('<title>Grand Sumo Manager v193', '<title>Grand Sumo Manager v194')
ui = open(os.path.join(here, 'nw194_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
