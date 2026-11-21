// スカウトを工夫した(素質 B 以上を上から 2 人ずつ・支度金いちばん高い)ときに、親方・部屋付き親方・稽古場・稽古の強さで出世がどれくらい変わるか
// usage: node scoutx.js file.html years seed 条件(base/oyL/oyM/oyH/stH/k1/k5/it0/it2)
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS,SC]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,potOf,gradeOf};',ctx);
const C=ctx;const E=x=>vm.runInContext(x,ctx);C.newGameReal('高田川');
/* 条件:base=そのまま / oyL・oyM・oyH=親方の指導力 6・12・18(部屋付き親方の力は 1 にして親方だけの差を見る) / stH=親方 6+部屋付き親方 18 / k1・k5=稽古場の段階 / it0・it2=稽古の強さ 軽め・強め */
const S=SC||'base';
ctx.__S=S;
E(`globalThis.__fix=function(){const S=globalThis.__S;const OY=me().oy;const co=G.staff.filter(x=>x.role==='co');
 const setO=v=>['osh','yot','waz','tai','sei'].forEach(k=>OY[k]=v);const setC=v=>co.forEach(s=>['osh','yot','waz','tai','sei'].forEach(k=>s.sk[k]=v));
 if(S==='oyL'){setO(6);setC(1);}if(S==='oyM'){setO(12);setC(1);}if(S==='oyH'){setO(18);setC(1);}if(S==='stH'){setO(6);setC(18);}
 if(S==='k1')G.fac.keiko=1;if(S==='k5')G.fac.keiko=5;
 if(S==='it0'||S==='it2')own().forEach(r=>{if(r.menu!=='休')r.it=S==='it0'?0:2;});
 G.fac.shuku=Math.max(G.fac.shuku,8);if(G.money<3000)G.money=3000;};`);
const pre=new Set(Object.keys(C.__get().R));const mine={},best={};const RK={Y:5,O:4,S:3,K:3};const YRS=yrs,CUT=process.env.CUTALL?1e9:(yrs-8)*6;
for(let b=0;b<YRS*6;b++){
 while(C.__get().phase==='train'){E('__fix()');
  E(`(function(){const L=(G.pros||[]).slice().sort((a,b)=>potOf(b.r)-potOf(a.r));let n=0;for(const p of L){if(n>=2)break;if(potOf(p.r)<11)break;if(ownAll().length>=cap()-1)break;const before=new Set(ownAll().map(r=>r.id));offerPros(p.cid,2);n++;ownAll().forEach(r=>{if(!before.has(r.id))globalThis.__new=(globalThis.__new||[]).concat([[r.id,G.bnum,+potOf(r).toFixed(1)]]);});}})()`);
  E('doWeek()');}
 while(C.__get().phase==='basho')E('advanceDay()');
 const G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);
 (ctx.__new||[]).forEach(([id,bn,pt])=>{if(mine[id]==null&&b<CUT)mine[id]=pt;});ctx.__new=[];
 Object.keys(mine).forEach(id=>{const r=G.R[id];if(!r)return;const v=r.t?RK[r.t]:r.d===0?2:r.d===1?1:0;best[id]=Math.max(best[id]||0,v);});
 C.nextCycle();
}
const ids=Object.keys(mine);const n=ids.length;const c=t=>ids.filter(id=>(best[id]||0)>=t).length;
const pa=ids.reduce((s,id)=>s+mine[id],0)/Math.max(1,n);
console.log(JSON.stringify({S,seed:sS,n,pot:+pa.toFixed(1),seki:c(1),maku:c(2),san:c(3)}));
