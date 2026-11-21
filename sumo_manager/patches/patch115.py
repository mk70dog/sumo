# v112:育つ環境(指導力・稽古相手・施設と体づくり・稽古の中身)で、素質の上限そのものと伸びる速さが変わる。v111 → v112
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=111;\nconst SAVE='sumoManager111',SAVE110", "const APPV=112;\nconst SAVE='sumoManager112',SAVE111='sumoManager111',SAVE110")
rep('[SAVE110,SAVE109', '[SAVE111,SAVE110,SAVE109')
rep('<title>Grand Sumo Manager v111','<title>Grand Sumo Manager v112')
# 1. 伸びる速さの差を広げる(指導力 6→0.82、10→1.0、12→1.09、18→1.36。前は 0.88〜1.24)
rep("cf[k]=(.7+.03*best(k))*lf","cf[k]=(ENV.s0+ENV.s1*best(k))*lf")
# 2. 育つ環境の点数(0〜1)と、育つ時期の上限の動き
rep("function heyaH(h){","""/* v112 育つ環境:指導力 .35・稽古相手 .30・施設と体づくり .20・稽古の中身 .15(割合は推定)。
   育つ時期(入門 6 年=36 場所まで、または 24 歳まで)は、環境の点数に応じて素質の上限(体・技)が毎週少しずつ動く */
const ENV={s0:.55,s1:.045,K:.018,E0:.56,yrs:36,age:24,w:{sh:.35,pa:.30,fa:.20,ke:.15}};
function envPrep(){const M={};G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret||r.inj&&r.inj.s>=2)return;(M[r.h]=M[r.h]||[]).push(r.pos);});G._envM=M;G._envSh={};}
function envPa(r){const L=(G._envM||{})[r.h]||[];let c=0;for(const p of L){if(p<r.pos-4&&p>=r.pos-150)c++;else if(r.pos<40&&p>r.pos&&p<=r.pos+40)c+=.7;}return cl(c/3,0,1);}
function envSh(){const k=ME();if(G._envSh&&G._envSh[k]!=null)return G._envSh[k];const co=G.staff.filter(s=>s.role==='co'&&coA(s).t!=='one');const OY=me().oy;
 const C=['tai','osh','yot','waz','sei'];let t=0;C.forEach(c=>{t+=Math.max(OY[c],...co.filter(s=>coA(s).t!=='sk'||coA(s).s===c).map(s=>s.sk[c]));});
 const n=Math.max(1,ownAll().length),load=n/(co.length+1),lf=load>8?Math.pow(8/load,.35):1;const v=cl((t/5-6)/12,0,1)*lf;if(G._envSh)G._envSh[k]=v;return v;}
function envFa(){const f=G.fac,c=G.con||{};const L=v=>cl(((v||1)-1)/4,0,1);return .4*L(f.keiko)+.15*L(f.iryo)+.2*L(f.shoku)+(c.gym?.1:0)+(c.diet?.1:0)+((c.clinic||c.doc)?.05:0);}
function envKe(r,mk,it){if(mk==='休')return .2;let v=[.2,.6,.9,1][it]||.6;if(r.fat>75)v*=.5;return .5*v+.25*(r.mor||50)/100+.25*(r.tr==null?50:r.tr)/100;}
function envE(r,mk,it){const W=ENV.w;let pa=envPa(r);
 if(r.h===ME()){if(mk==='出')pa=Math.max(pa,.8);return W.sh*envSh()+W.pa*pa+W.fa*envFa()+W.ke*envKe(r,mk,it);}
 const h=G.heya[r.h];const q=h?cl(((h.q||1.04)-.9)/.26,0,1):.5;return .65*q+.35*pa;}
function envGrow(r,mk,it){if(r.ret)return;const young=(G.bnum-(r.join==null?-99:r.join))<ENV.yrs||r.age<=ENV.age;if(!young)return;
 const e=envE(r,mk,it);r.env=Math.round(e*100);const d=ENV.K*(e-ENV.E0);
 for(const k of PHYS.concat(TECH)){if(r.cap[k]==null)continue;r.cap[k]=Math.max(r.a[k],Math.min(22,r.cap[k]+d*R(.6,1.4)));}}
function heyaH(h){""")
rep(" decline(r,1);\n // 疲労"," envGrow(r,mk,it);\n decline(r,1);\n // 疲労")
rep("HP[ME()]=heyaH(ME());});\n const HA={};","HP[ME()]=heyaH(ME());});\n envPrep();\n const HA={};")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
