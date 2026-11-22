# v124 -> v125:本場所に向けたコンディション作り(ダルマさん「本場所に向けてのコンディション作り・場所中の調子・食事や休養は?」→ 答えと案 →「実施」→ 見本 bc1〜bc3・bcm →「おすすめの組み合わせは?」→ bc1+bc3 のおすすめボタン+bcm →「実施」)。
# 本体(計算):場所中の毎日の終わりに、プレイヤーの部屋の力士の朝稽古(r.bca)・午後(r.bcp)・勝負メシの効き目(bcDay)。ほかの部屋は今までどおり。
# 画面:patches/bc125.js。二人相撲の子が切れている間の当て直し(MPX_RK)にも bca・bcp を足す。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=124;\nconst SAVE='sumoManager124',SAVE123", "const APPV=125;\nconst SAVE='sumoManager125',SAVE124='sumoManager124',SAVE123")
rep('[SAVE123,SAVE122', '[SAVE124,SAVE123,SAVE122')
rep('<title>Grand Sumo Manager v124', '<title>Grand Sumo Manager v125')
CORE = r'''/* v125:場所中の過ごし方(プレイヤーの部屋の力士だけ。数字は推定)。朝稽古 し=しっかり 軽=軽め 休=休む、午後 昼=昼寝 治=治療 自=自由時間。
   朝稽古はその日の取組の力にも効く(しっかり +0.5%・休む −0.5%。bcX、prepF)。始めの設定:全員軽め(今までと同じ)、午後は昼寝(けが人は治療)。勝負メシ:場所中のちゃんこがソップ(鶏)なら気力 +0.2/日。 */
function bcDef(r){return {a:r.bca||'軽',p:r.bcp||(r.inj?'治':'昼')};}
function bcX(r){if(!G.B||!isPH(r.h))return 0;const a=bcDef(r).a;return a==='し'?.005:a==='休'?-.005:0;}
function bcDay(){const B=G.B;if(!B)return;G.order.forEach(id=>{const r=G.R[id];if(!r||!isPH(r.h))return;const c=B.rec[id];if(!c||c.ky)return;const o=bcDef(r);
 if(o.a==='し'){r.cond=cl(r.cond+.6,0,100);r.fat=cl(r.fat+1,0,100);}else if(o.a==='休'){r.fat=cl(r.fat-3,0,100);r.cond=cl(r.cond-.3,0,100);}
 if(o.p==='昼')r.fat=cl(r.fat-1,0,100);else if(o.p==='治'){r.fat=cl(r.fat-.5,0,100);if(r.inj){const con=pv(r.h,'con')||{};r.inj.wk-=.05*(con.clinic?1.5:1);if(r.inj.wk<=0)heal(r);}}else if(o.p==='自')r.mor=cl(r.mor+.4,0,100);
 const m=pv(r.h,'meal');if(m&&m.k==='ソップ')r.mor=cl(r.mor+.2,0,100);});}
'''
rep("function advanceDay(){", CORE + "function advanceDay(){")
rep("f*=1+(r.bfm||0)+(r.bzf||0);r._f=f;", "f*=1+(r.bfm||0)+(r.bzf||0)+bcX(r);r._f=f;")
rep(" G.order.concat(G.pend).forEach(id=>{const r=G.R[id];r.fat=cl(r.fat-(2+r.a.rec*.2),0,100);r.cond=cl(r.cond-.3,0,100);});\n B.last=bouts;",
    " G.order.concat(G.pend).forEach(id=>{const r=G.R[id];r.fat=cl(r.fat-(2+r.a.rec*.2),0,100);r.cond=cl(r.cond-.3,0,100);});\n bcDay();\n B.last=bouts;")
rep("const MPX_RK={menu:1,it:1,pm:1,wplan:1,injPol:1,sh:1,tac:1};", "const MPX_RK={menu:1,it:1,pm:1,wplan:1,injPol:1,sh:1,tac:1,bca:1,bcp:1};")
ui = open(os.path.join(here, 'bc125.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
