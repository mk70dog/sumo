# v62 -> v63:行司の軍配を上げる動き・終盤の観客の盛り上がり(見本 gun1)
import sys
sys.path.insert(0, 'patches')
import gun65
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v62</title>', '<title>Sumo Manager v63</title>')
rep("const APPV=62;\nconst SAVE='sumoManager62',SAVE61", "const APPV=63;\nconst SAVE='sumoManager63',SAVE62='sumoManager62',SAVE61")
rep('[SAVE61,SAVE60', '[SAVE62,SAVE61,SAVE60')
rep(" if(g.v===61){g.v=62;}\n return g.v===62?g:null;}", " if(g.v===61){g.v=62;}\n if(g.v===62){g.v=63;}\n return g.v===63?g:null;}")
rep('G={v:62,', 'G={v:63,')
s = gun65.apply(s, 1)
# 軍配は大きくしすぎず、勝った力士の札を隠さない
rep("const g0=[16,-14],g1=[30,-2];","const g0=[16,-14],g1=[24,-6];")
rep("') scale('+(1+.9*e).toFixed(2)+')'","') scale('+(1+.55*e).toFixed(2)+')'")
# 決着のとき、行司は力士と重ならない場所へさっと下がり、いちばん手前に描く(軍配が隠れないように)
rep("{const wv=p.lose==='E'?p.W:p.E;const gb=gy.querySelector('.gb');const ga=",
    "{const mx=(p.E[0]+p.W[0])/2,my=(p.E[1]+p.W[1])/2;let best=null;for(let i=0;i<16;i++){const a=i*Math.PI/8;let x=mx+Math.cos(a)*.8,y=my+Math.sin(a)*.8;const r=Math.hypot(x,y);if(r>.9){x*=.9/r;y*=.9/r;}const d=Math.min(Math.hypot(x-p.E[0],y-p.E[1]),Math.hypot(x-p.W[0],y-p.W[1]));const sc=Math.min(d,.72)*3-.5*Math.hypot(x-gp[0],y-gp[1]);if(!best||sc>best[2])best=[x,y,sc];}"
    "const g0=gp.slice(),t0=performance.now();gp=[best[0],best[1]];gy.parentNode.appendChild(gy);const mv=now=>{const t=Math.min(1,(now-t0)/260);gy.setAttribute('transform','translate('+((g0[0]+(gp[0]-g0[0])*t)*S).toFixed(1)+','+((g0[1]+(gp[1]-g0[1])*t)*S).toFixed(1)+')');if(t<1)requestAnimationFrame(mv);};requestAnimationFrame(mv);}"
    "{const wv=p.lose==='E'?p.W:p.E;const gb=gy.querySelector('.gb');const ga=")
# 決着のときは行司を薄くしない(軍配がはっきり見えるように)
rep("gy.querySelector('.gyt').classList.add('fin');{const gx=gp[0]*S,gyy=gp[1]*S;", "gy.setAttribute('opacity',1);gy.querySelector('.gyt').classList.add('fin');{const gx=gp[0]*S,gyy=gp[1]*S;")
# 「勝負あり」の縦書きは、行司・軍配・力士のどれとも重ならず、土俵からはみ出さない場所を選んで置く
rep("t.setAttribute('x',(gx+(gx>0?-34:34)).toFixed(0));t.setAttribute('y',(gyy-40).toFixed(0));",
    "{const ca=Math.cos(ga*Math.PI/180),sa=Math.sin(ga*Math.PI/180);const tip=[gx+ca*42,gyy+sa*42];const R=[[p.E[0]*S,p.E[1]*S],[p.W[0]*S,p.W[1]*S]];const lim=S*.95;let bst=null;"
    "for(let i=0;i<12;i++){const a=i*Math.PI/6;for(const k of [1,1.35,1.7,2.1]){const cx=gx+Math.cos(a)*52*k,cy=gyy+Math.sin(a)*96*k;const x0=cx-25,x1=cx+25,y0=cy-68,y1=cy+68;"
    "const dB=(px,py)=>Math.hypot(Math.max(x0-px,0,px-x1),Math.max(y0-py,0,py-y1));let sc=-.4*k-.3*(Math.cos(a)*ca+Math.sin(a)*sa);"
    "if(x0<-lim||x1>lim||y0<-lim||y1>lim)sc-=50;sc-=Math.max(0,30-dB(gx,gyy))*.2+Math.max(0,24-dB(tip[0],tip[1]))*.2;R.forEach(r=>{sc-=Math.max(0,40-dB(r[0],r[1]))*.15;});"
    "if(!bst||sc>bst[2])bst=[cx,cy,sc];}}t.setAttribute('x',bst[0].toFixed(0));t.setAttribute('y',(bst[1]-68).toFixed(0));}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
