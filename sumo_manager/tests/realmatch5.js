// 現実とのマッチング(5):番付どうしの対戦成績(横綱・大関・三役 対 平幕上位・中位・下位)
// usage: node realmatch5.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||20;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;',ctx);
const C=ctx;C.newGameReal('高田川');const T={};
const grp=(r,fm)=>{if(r.d!==0)return null;if(r.t==='Y')return '横綱';if(r.t==='O')return '大関';if(r.t==='S'||r.t==='K')return '三役';const n=Math.floor((r.pos-fm)/2)+1;return n<=5?'平幕上位(1-5)':n<=11?'平幕中位(6-11)':'平幕下位(12-)';};
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')C.doWeek();
 let G=C.__get();const fm=G.order.map(i=>G.R[i]).filter(r=>r.d===0&&!r.t).reduce((m,r)=>Math.min(m,r.pos),1e9);const g0={};G.order.forEach(id=>{g0[id]=grp(G.R[id],fm);});
 while(C.__get().phase==='basho'){const bs=C.advanceDay();bs.forEach(x=>{if(x.fus)return;const a=g0[x.w],c=g0[x.l];if(!a||!c||a===c)return;const k=a<c?a+'|'+c:c+'|'+a;T[k]=T[k]||{};T[k][a]=(T[k][a]||0)+1;});}
 G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
const out={};Object.keys(T).forEach(k=>{const [a,c]=k.split('|');const wa=T[k][a]||0,wc=T[k][c]||0;out[a+' 対 '+c]=(100*wa/(wa+wc)).toFixed(0)+'% ('+(wa+wc)+'番)';});
console.log(JSON.stringify(out,null,0));
