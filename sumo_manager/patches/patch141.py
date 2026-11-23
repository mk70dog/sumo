# v137 -> v138:絵を 3 枚足す(嵐富士・炎鵬・尊富士)と、独立のとき、残ると言った内弟子をもう一度説得できる(ダルマさん「独立して立ち上げモード時 力士を選択するが全員は来ない?」→ 案 →「2」)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=137;\nconst SAVE='sumoManager137',SAVE136", "const APPV=138;\nconst SAVE='sumoManager138',SAVE137='sumoManager137',SAVE136")
rep('[SAVE136,SAVE135', '[SAVE137,SAVE136,SAVE135')
rep('<title>Grand Sumo Manager v137', '<title>Grand Sumo Manager v138')
core = open(os.path.join(here, 'dp138_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("Object.assign(EVT,ST_EVT,RT_EVT,FM_EVT,YS_EVT);", "Object.assign(EVT,ST_EVT,RT_EVT,FM_EVT,YS_EVT,DP_EVT);")
rep(" if(R.stay.length)addNews(R.stay.join('・')+'は、話し合いの末、元の'+(x?x.par:'')+'部屋に残ることになりました(内弟子でも元の部屋に残る例があります)。');",
    " if(R.stay.length){addNews(R.stay.join('・')+'は「元の'+(x?x.par:'')+'部屋に残ります」と言っています(内弟子でも元の部屋に残る例があります)。もう一度説得することもできます。');R.stay.forEach(n=>{const w=x?dokWs(x).find(y=>y.n===n):null;G.ev.push({k:'dokPer',n:n,sc:w?w.sc:1,id:Math.random().toString(36).slice(2,8)});});}")
rep("let x=G.dekH!=null?L.find(y=>y.h===G.dekH):null;if(!x)x=L[0];return {h:x.h,s:x.s,q:.8+.1*Math.min(5,x.s)};",
    "let x=G.dekH!=null?L.find(y=>y.h===G.dekH):null;if(!x)x=L[0];const cool=G.dok&&G.dok.cool&&G.heya[x.h].n===G.dok.from?Math.max(.5,1-.1*G.dok.cool):1;return {h:x.h,s:x.s,q:(.8+.1*Math.min(5,x.s))*cool};")
import json
P = json.load(open(os.path.join(here, '..', 'data', 'portraits138.json'), encoding='utf-8'))
rep('</body>\n</html>', '<script>/* v138:絵を足す(嵐富士・炎鵬・尊富士。data/portraits138.json) */Object.assign(PIMG,' + json.dumps(P, ensure_ascii=False) + ');</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
