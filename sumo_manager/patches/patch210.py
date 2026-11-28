# v206 -> v207:タブの窓を部屋の画面と同じ色に(部屋の札 .hbp の色・文字色・ぼかし、見出しの色を読み取って使う)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=206;\nconst SAVE='sumoManager206',SAVE205", "const APPV=207;\nconst SAVE='sumoManager207',SAVE206='sumoManager206',SAVE205")
rep('[SAVE205,SAVE204', '[SAVE206,SAVE205,SAVE204')
rep('<title>Grand Sumo Manager v206', '<title>Grand Sumo Manager v207')
old = open(os.path.join(here,'pop209_ui.js'),encoding='utf-8').read()
new = open(os.path.join(here,'pop210_ui.js'),encoding='utf-8').read()
rep(old, new)
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
