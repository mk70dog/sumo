// 同じ弟子で条件だけ変えてくらべる(親方・部屋付き親方・稽古場・稽古の強さ)。usage: node scoutx2.js file.html 0 seed [条件,条件...]
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS,SC]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,potOf,gradeOf};',ctx);
const C=ctx;const E=x=>vm.runInContext(x,ctx);C.newGameReal('高田川');
/* 1) 6 年間、ふつうに部屋を回しながら素質 B 以上を上から 2 人ずつ勧誘(支度金はいちばん高く)。2) そこで世界を写し取り、
   同じ弟子・同じ乱数の始まりで、条件だけ変えて 18 年進め、6 年の間に入った弟子の出世をくらべる */
const FIX=`globalThis.__fix=function(S){const OY=me().oy;const co=G.staff.filter(x=>x.role==='co');
 const setO=v=>['osh','yot','waz','tai','sei'].forEach(k=>OY[k]=v);const setC=v=>co.forEach(s=>['osh','yot','waz','tai','sei'].forEach(k=>s.sk[k]=v));
 if(S==='oyL'){setO(6);setC(1);}if(S==='oyM'){setO(12);setC(1);}if(S==='oyH'){setO(18);setC(1);}if(S==='stH'){setO(6);setC(18);}
 const fa=v=>{G.fac.keiko=v;G.fac.iryo=v;G.fac.shoku=v;G.con=v>=5?{gym:1,diet:1,clinic:1,doc:1}:{};};if(S==='min'){setO(6);setC(1);fa(1);}if(S==='max'){setO(18);setC(18);fa(5);}if(S==='k1')fa(1);if(S==='k5')fa(5);
 if(S==='it0'||S==='it2')own().forEach(r=>{if(r.menu!=='休')r.it=S==='it0'?0:2;});
 G.fac.shuku=Math.max(G.fac.shuku,8);if(G.money<3000)G.money=3000;};`;
E(FIX);
const REC=`(function(){const L=(G.pros||[]).slice().sort((a,b)=>potOf(b.r)-potOf(a.r));let n=0;for(const p of L){if(n>=2)break;if(potOf(p.r)<11)break;if(ownAll().length>=cap()-1)break;const bf=new Set(ownAll().map(r=>r.id));offerPros(p.cid,2);n++;ownAll().forEach(r=>{if(!bf.has(r.id))globalThis.__new=(globalThis.__new||[]).concat([r.id]);});}})()`;
function cycle(S,recruit){while(C.__get().phase==='train'){E(`__fix('${S}')`);if(recruit)E(REC);E('doWeek()');}
 while(C.__get().phase==='basho')E('advanceDay()');const G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
ctx.__new=[];for(let b=0;b<36;b++)cycle('base',true);
const coh=[...new Set(ctx.__new)].filter(id=>{const r=C.__get().R[id];return r&&!r.ret;});
const pot={};coh.forEach(id=>pot[id]=E(`potOf(G.R[${id}])`));
const snap=E('saveStr()');const seed0=seed;ctx.__snap=snap;
const RK={Y:5,O:4,S:3,K:3};const out=[];
for(const S of (SC||'base,min,oyL,oyH,stH,k1,k5,it0,it2,max').split(',')){
 E('G=migrate(JSON.parse(__snap));applyMode(!!G.real)');seed=seed0;const best={},peak={};
 for(let b=0;b<108;b++){cycle(S,false);const G=C.__get();coh.forEach(id=>{const r=G.R[id];if(!r)return;const v=r.t?RK[r.t]:r.d===0?2:r.d===1?1:0;best[id]=Math.max(best[id]||0,v);if(!r.ret)peak[id]=Math.max(peak[id]||0,E(`ovrOf(G.R[${id}].a,G.R[${id}].wT)`));});}
 const c=t=>coh.filter(id=>(best[id]||0)>=t).length;const pk=coh.reduce((s,id)=>s+(peak[id]||0),0)/Math.max(1,coh.length);
 out.push({S,n:coh.length,pot:+(coh.reduce((s,id)=>s+pot[id],0)/coh.length).toFixed(1),seki:c(1),maku:c(2),san:c(3),peak:+pk.toFixed(2)});
}
console.log(JSON.stringify({seed:sS,out}));
