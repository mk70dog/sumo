# 設計 18 の推定値を実データに置き換え  v15 -> v16
import os
import sys,re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(old,new,n=1):
    global s
    c=s.count(old)
    if c!=n: raise SystemExit('一致数 %d (期待 %d): %r'%(c,n,old[:80]))
    s=s.replace(old,new)
IC={'出羽海':0,'二所ノ関':1,'時津風':2,'高砂':3,'伊勢ヶ濱':4}
rows=[l.split(',') for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','myo2026.txt'),encoding='utf-8').read().split()]
assert len(rows)==105
names="["+",".join("'%s'"%r[0] for r in rows)+"]"
mydo="{"+",".join("'%s':['%s',%d]"%(r[0],r[1],IC[r[2]]) for r in rows)+"}"
rep('<title>Sumo Manager v15</title>','<title>Sumo Manager v16</title>')
rep("const SAVE='sumoManager15',SAVE14","const SAVE='sumoManager16',SAVE15='sumoManager15',SAVE14")
rep('[SAVE14,SAVE13','[SAVE15,SAVE14,SAVE13')
rep("if(g.v===14){mig15(g);g.v=15;}\n return g.v===15?g:null;}","if(g.v===14){mig15(g);g.v=15;}\n if(g.v===15){mig16(g);g.v=16;}\n return g.v===16?g:null;}")
rep('G={v:15,','G={v:16,')
s=re.sub(r"const MYO105=\[[^\]]*\];","const MYO105="+names+";\n/* 2026 年 10 月 31 日時点の名跡・部屋・一門(土俵の目撃者「相撲の親方一覧」)。峰崎・出来山は未襲名で、一門は過去の襲名者からの推定 */\nconst MYOD="+mydo+";",s,count=1)
# 初期化:一門は実データ、空きは峰崎・出来山、現役保有・遺族保有は 0(実名モード)
rep("MYO105.forEach((n,k)=>{const hi=hn[n];M[n]={st:hi!=null?(hi===0?'own':'ai'):'ai',ic:hi!=null?(hi===0?(X.heya[0].ic>=0?X.heya[0].ic:k%5):X.heya[hi].ic):k%5};});",
    "MYO105.forEach((n,k)=>{const hi=hn[n];M[n]={st:hi===0?'own':'ai',ic:MYOD[n]?MYOD[n][1]:k%5};});")
rep("const c=MYO105.filter(n=>M[n].st==='ai'&&hn[n]==null);if(!c.length)return;const nn=c[Math.floor(Math.random()*c.length)];",
    "let c=MYO105.filter(n=>M[n].st==='ai'&&hn[n]==null&&MYOD[n]&&MYOD[n][0]===X.heya[0].n);if(!c.length)c=MYO105.filter(n=>M[n].st==='ai'&&hn[n]==null);if(!c.length)return;const nn=c[Math.floor(Math.random()*c.length)];")
rep(" take('free',3);take('gen',6);take('izoku',3);",
    " if(X.real){['峰崎','出来山'].forEach(n=>{if(M[n].st==='ai')M[n].st='free';});}else{take('free',2);take('izoku',1);}")
# 定年後も名跡を持ったまま貸す親方が多い:空きより遺族・元親方の保有に回りやすく
rep("if(m.st==='ai'&&!hn.has(n)){if(r<.0065)m.st='free';else if(r<.0075)m.st='izoku';}",
    "if(m.st==='ai'&&!hn.has(n)){if(r<.0035)m.st='free';else if(r<.0065)m.st='izoku';}")
rep("else if(myoCnt('izoku')>0&&Math.random()<.3){","else if(myoCnt('izoku')>0&&Math.random()<.6){")
MIG=r"""function mig16(g){if(!g.myo){myoInit(g);return;}const RN={'君ヶ浜':'君ヶ濱','根岸':'大鳴戸','秩父山':'陣幕'};
 for(const o in RN){const nn=RN[o];if(g.myo[o]){g.myo[nn]=g.myo[o];delete g.myo[o];}
  (g.myoL||[]).forEach(m=>{if(m.n===o)m.n=nn;});(g.staff||[]).forEach(x=>{if(x.myo===o)x.myo=nn;});g.heya.forEach(h=>{if(h.n===o)h.n=nn;});(g.myoM||[]).forEach(m=>{if(m.n===o)m.n=nn;});}
 MYO105.forEach(n=>{if(!g.myo[n])g.myo[n]={st:'ai',ic:0};if(MYOD[n])g.myo[n].ic=MYOD[n][1];});}
"""
rep("function mig15(g){myoInit(g);}","function mig15(g){myoInit(g);}\n"+MIG)
# 実名モードの開始時に名跡を実データで作り直す
rep(" G.tkPol='old';G.rel={};G.ama=null;amaInit();mig11(G);mig12(G);\n addNews(bname(G.bnum)+'の番付から始めます。'",
    " G.tkPol='old';G.rel={};G.ama=null;amaInit();mig11(G);mig12(G);myoInit(G);refreshMyo();\n addNews(bname(G.bnum)+'の番付から始めます。'")

open(dst,'w',encoding='utf-8').write(s);print('ok',len(s))
