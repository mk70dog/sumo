# 大関昇進の起点に平幕優勝・優勝があれば32勝  v34 -> v35
# 目安は「三役で3場所合計33勝以上」。栃ノ心(2018年)は平幕優勝の場所が大関取りの起点と位置づけられた(ABEMA TIMES)。
# 平成以降の大関昇進者は最低でも3場所合計32勝(SPAIA 2022/1/27)。32勝は3場所に優勝があるときだけ(推定)。
# 実際の番付(sumodb、2015〜2025年の7月場所を2年おきに6場所):横綱 平均2.2・大関3.0・関脇2.3人。v34 は大関 2.0 人。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v34</title>', '<title>Sumo Manager v35</title>')
rep("const APPV=34;\nconst SAVE='sumoManager34',SAVE33", "const APPV=35;\nconst SAVE='sumoManager35',SAVE34='sumoManager34',SAVE33")
rep('[SAVE33,SAVE32', '[SAVE34,SAVE33,SAVE32')
rep(" if(g.v===33){g.v=34;}\n return g.v===34?g:null;}", " if(g.v===33){g.v=34;}\n if(g.v===34){g.v=35;}\n return g.v===35?g:null;}")
rep('G={v:34,', 'G={v:35,')
rep("if(r.t==='S'&&!nt[id]){const h=r.hist.slice(-3);if(h.length===3&&h.every(x=>x.t==='S'||x.t==='K'||(x.t==null&&x.d===0&&/前頭1$/.test(x.rk)))&&h.reduce((s,x)=>s+x.w,0)>=33&&c.w>=10)nt[id]='O';}",
    "if(r.t==='S'&&!nt[id]){const h=r.hist.slice(-3);const sy=x=>x.t==='S'||x.t==='K'||(x.t==null&&x.d===0&&/前頭1$/.test(x.rk));const sm=h.reduce((s,x)=>s+x.w,0);if(h.length===3&&(sy(h[0])||(h[0].d===0&&h[0].yu))&&sy(h[1])&&sy(h[2])&&(sm>=33||(sm>=32&&h.some(x=>x.yu)))&&c.w>=10)nt[id]='O';}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
