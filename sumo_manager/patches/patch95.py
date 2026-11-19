# v91 -> v92:二人相撲の子の iPad で、本場所のその日の結果と取組の動き(土俵で見る)が出ていなかったのを直す
# 親の iPad は取組を進めた結果を UI.bouts に持つが、子は世界を受け取るだけで UI.bouts が空のままだった。世界の G.B.last(その日の取組)から入れる。
# 千秋楽が終わって受け取ったときは、子の iPad でも場所の終わりのまど(bashoEndModal)を出す。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v91</title>', '<title>Grand Sumo Manager v92</title>')
rep("const APPV=91;\nconst SAVE='sumoManager91',SAVE90", "const APPV=92;\nconst SAVE='sumoManager92',SAVE91='sumoManager91',SAVE90")
rep('[SAVE90,SAVE89', '[SAVE91,SAVE90,SAVE89')
rep(" if(g.v===90){g.v=91;}\n return g.v===91?g:null;}", " if(g.v===90){g.v=91;}\n if(g.v===91){g.v=92;}\n return g.v===92?g:null;}")
rep('G={v:91,', 'G={v:92,')
rep("function mpGLoad(w){G=migrate(JSON.parse(w.s));applyMode(!!G.real);",
    "function mpGLoad(w){const pb=G&&G.phase==='basho'&&UI.mpGuest;G=migrate(JSON.parse(w.s));applyMode(!!G.real);\n UI.bouts=(G.phase==='basho'&&G.B&&G.B.day>0&&G.B.last)?G.B.last:[];if(pb&&G.phase==='post'&&mpIsP0())setTimeout(()=>{try{UI.view='home';render();bashoEndModal();}catch(e){}},0);")
rep("function mpIsP(){", "function mpIsP0(){return !!(G&&G.P&&MPG.gh>0&&pI(MPG.gh)>=0);}\nfunction mpIsP(){")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
