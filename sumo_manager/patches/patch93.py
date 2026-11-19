# v89 -> v90:二人相撲 第 2 段階(一人用と二人用を同じ作りに・第 2 歩)。部品は patches/mp90.js
# 子の iPad も一人用と同じ画面。進めるボタンは「準備できた」に。子の操作は差分にして親へ送り、親が当ててから進める。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v89</title>', '<title>Grand Sumo Manager v90</title>')
rep("const APPV=89;\nconst SAVE='sumoManager89',SAVE88", "const APPV=90;\nconst SAVE='sumoManager90',SAVE89='sumoManager89',SAVE88")
rep('[SAVE88,SAVE87', '[SAVE89,SAVE88,SAVE87')
rep(" if(g.v===88){g.v=89;}\n return g.v===89?g:null;}", " if(g.v===88){g.v=89;}\n if(g.v===89){g.v=90;}\n return g.v===90?g:null;}")
rep('G={v:89,', 'G={v:90,')
mp = open(os.path.join(os.path.dirname(__file__), 'mp90.js'), encoding='utf-8').read()
rep('<script>\n/* v82:', mp + '\n<script>\n/* v82:')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
