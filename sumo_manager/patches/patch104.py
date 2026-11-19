# v100 -> v101:アプリ全体の細部の確認で見つけた不具合の直し(ダルマさん「実施」)。
# まだ番付に載っていない新弟子(前相撲・付出予定)には番付の文字(r.rk・r.rkS)がなく、その間にけがをすると
# 「けがの治療方針」の出来事に「海洋(undefined)が膝に重いけが…」と出ていた。
# 直し:力士を作ったときから「前相撲」、番付を作るたびに、まだ載っていない新弟子は「前相撲」か「付出予定」。前の保存データも読み込みで埋める。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v100</title>', '<title>Grand Sumo Manager v101</title>')
rep("const APPV=100;\nconst SAVE='sumoManager100',SAVE99", "const APPV=101;\nconst SAVE='sumoManager101',SAVE100='sumoManager100',SAVE99")
rep('[SAVE99,SAVE98', '[SAVE100,SAVE99,SAVE98')
rep(" if(g.v===99){g.v=100;}\n return g.v===100?g:null;}",
    " if(g.v===99){g.v=100;}\n if(g.v===100){g.v=101;for(const id in g.R){const r=g.R[id];if(r&&!r.rkS){r.rkS=r.tsuke?'付出予定':'前相撲';r.rk=r.rk||r.rkS;}}}\n return g.v===101?g:null;}")
rep('G={v:100,', 'G={v:101,')
rep("  menu:'申',it:1,wplan:1,tac:{ta:'任',kumi:'任'},injPol:'任',", "  rk:'前相撲',rkS:'前相撲',menu:'申',it:1,wplan:1,tac:{ta:'任',kumi:'任'},injPol:'任',")
rep("  if(i<r.best)r.best=i;});\n}",
    "  if(i<r.best)r.best=i;});\n {const inO=new Set(G.order);allPK('pend').concat(G.aiPend||[]).forEach(id=>{const r=G.R[id];if(r&&!inO.has(id)){r.rkS=r.tsuke?'付出予定':'前相撲';r.rk=r.rkS;}});}/* v101:番付に載る前の新弟子 */\n}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
