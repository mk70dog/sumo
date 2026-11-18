# 土俵の動き:札・行司の声・印の文字が重ならないように  v55 -> v56
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v55</title>', '<title>Sumo Manager v56</title>')
rep("const APPV=55;\nconst SAVE='sumoManager55',SAVE54", "const APPV=56;\nconst SAVE='sumoManager56',SAVE55='sumoManager55',SAVE54")
rep('[SAVE54,SAVE53', '[SAVE55,SAVE54,SAVE53')
rep(" if(g.v===54){g.v=55;}\n return g.v===55?g:null;}", " if(g.v===54){g.v=55;}\n if(g.v===55){g.v=56;}\n return g.v===56?g:null;}")
rep('G={v:55,', 'G={v:56,')
# 2 人の札が近いときは、西(後ろに描く側)の札を頭の上へ。名前とも重ならないよう、名前のさらに上。
rep("dhPose(ge,p.E,p.W,p.stance,pt*dur/1000,p.push>0,p.lose==='E'?p.fall:0,fxE);dhPose(gw,p.W,p.E,p.stance,pt*dur/1000+.5,p.push<0,p.lose==='W'?p.fall:0,fxW);",
    "dhPose(ge,p.E,p.W,p.stance,pt*dur/1000,p.push>0,p.lose==='E'?p.fall:0,fxE);dhPose(gw,p.W,p.E,p.stance,pt*dur/1000+.5,p.push<0,p.lose==='W'?p.fall:0,fxW);\n  {const hE=+ge.dataset.h,hW=+gw.dataset.h;const tE=ge.querySelector('.tg'),tW=gw.querySelector('.tg'),nE=ge.querySelector('.nm'),nW=gw.querySelector('.nm');const ex=p.E[0]*S,ey=p.E[1]*S,wx=p.W[0]*S,wy=p.W[1]*S;\n   tE.setAttribute('y',hE+22);tW.setAttribute('y',hW+22);nE.setAttribute('y',-hE-14);nW.setAttribute('y',-hW-14);\n   if(fxE.tag&&fxW.tag&&Math.abs(ex-wx)<110&&Math.abs((ey+hE+22)-(wy+hW+22))<26)tW.setAttribute('y',-hW-32);\n   if(Math.abs(ex-wx)<90&&Math.abs((ey-hE)-(wy-hW))<20){if(ey<=wy)nW.setAttribute('y',hW+(fxW.tag&&+tW.getAttribute('y')>0?40:22));else nE.setAttribute('y',hE+(fxE.tag?40:22));}}")
# 行司の声:組の近くにいるときは小さく薄く
rep("const gt=gy.querySelector('.gyt');gt.textContent=",
    "const gt=gy.querySelector('.gyt');{const gd=Math.hypot(gp[0]-cx,gp[1]-cy);gt.setAttribute('opacity',gd<.42?.55:1);gt.setAttribute('font-size',gd<.42?10:12);gt.setAttribute('y',gp[1]<cy?-24:28);}gt.textContent=")
# 決着:札を消してから印と軍配
rep("else{const lo=p.lose==='E'?p.E:p.W;mk.setAttribute","else{fxE.tag=fxW.tag='';ge.querySelector('.tg').textContent='';gw.querySelector('.tg').textContent='';const lo=p.lose==='E'?p.E:p.W;mk.setAttribute")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
