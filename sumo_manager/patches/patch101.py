# v97 -> v98:二人相撲で、子も「部屋付き親方として独立」して参加できる(ダルマさん「子が独立して新しい部屋を興して参加する機能は必要」→「実施」)。部品は patches/mp98.js
# 子は親の世界の中で独立できる親方と内弟子を選んで申し込み(guest.json の dk)、親が世界に新しい部屋を足して子のプレイヤーにする。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v97</title>', '<title>Grand Sumo Manager v98</title>')
rep("const APPV=97;\nconst SAVE='sumoManager97',SAVE96", "const APPV=98;\nconst SAVE='sumoManager98',SAVE97='sumoManager97',SAVE96")
rep('[SAVE96,SAVE95', '[SAVE97,SAVE96,SAVE95')
rep(" if(g.v===96){g.v=97;}\n return g.v===97?g:null;}", " if(g.v===96){g.v=97;}\n if(g.v===97){g.v=98;}\n return g.v===98?g:null;}")
rep('G={v:97,', 'G={v:98,')
mp = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mp98.js'), encoding='utf-8').read()
rep('<script>\n/* v82:', mp + '\n<script>\n/* v82:')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
