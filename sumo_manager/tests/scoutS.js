// 素質 S をどれだけスカウトできるか:見立てで S に見える候補を親方が見に行き、いちばん高い支度金で勧誘し続ける「欲ばり」な遊び方で数える
// usage: node scoutS.js file.html years seed [heya]
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS,heya]=process.argv;const yrs=+yS||10;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},window:{},setTimeout,JSON,Date};
ctx.Math.random=rnd;ctx.window=ctx;vm.createContext(ctx);
code+='\n;globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,me,potOf,gradeOf,visitors,ME};';vm.runInContext(code,ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
C.newGameReal(heya||'高田川');const G=()=>C.__get();
const seen=new Set(),pool={S:0,A:0,B:0,C:0,D:0},poolSeen=new Set(),join={S:0,A:0,B:0,C:0,D:0},lookS={n:0,trueS:0},offers={S:[0,0]};
const lg={S:0,A:0,B:0,C:0,D:0};const lgSeen=new Set(Object.keys(G().R));
for(let b=0;b<yrs*6;b++){
 while(G().phase==='train'){const g=G();
  g.pros.forEach(p=>{if(!poolSeen.has(p.cid)){poolSeen.add(p.cid);pool[C.gradeOf(C.potOf(p.r))]++;}});
  // 見に行く:見立ての高い順に、行ける人の数だけ
  const V=C.visitors();const L=g.pros.slice().sort((a,b)=>(b.ep||0)-(a.ep||0));
  V.forEach((v,i)=>{const p=L[i];if(p&&g.money>50)C.trackPros(p.cid,v.k==='oy'?null:v.k);});
  // S に見える候補は、いちばん高い支度金で勧誘
  g.pros.slice().forEach(p=>{if((p.ep||0)>=16&&C.ownAll().length<C.cap()-1&&g.money>500){
   const before=G().pros.length;const ok=C.offerPros(p.cid,2)==='OK';const S=C.gradeOf(C.potOf(p.r))==='S';
   if(ok){lookS.n++;if(S)lookS.trueS++;}if(S){offers.S[0]++;if(ok)offers.S[1]++;}}});
  C.doWeek();}
 while(G().phase==='basho')C.advanceDay();
 let k=0;while(G().ev.length&&k++<50)C.resolveEv(G().ev[0].id,0);
 const g=G();Object.values(g.R).forEach(r=>{if(r.h===C.ME()&&!seen.has(r.id)&&!r.ret){seen.add(r.id);if(!r.real)join[C.gradeOf(C.potOf(r))]++;}
  if(!lgSeen.has(String(r.id))){lgSeen.add(String(r.id));lg[C.gradeOf(C.potOf(r))]++;}});
 if(!C.nextCycle()){g.ev=[];C.nextCycle();}
}
console.log(JSON.stringify({yrs,seed:sS,heya:heya||'高田川',候補の本当の素質:pool,入門した弟子の素質:join,S見立てで入門:lookS,本当にSへの勧誘:offers.S,全部屋の新弟子:lg,money:Math.round(G().money)}));
