// v27:血縁は本割で当たらない・実名の出身校・母校の化粧廻し・新弟子の大会記録
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2],'utf8');
let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
let seed=3;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT};',ctx);
const C=ctx;C.newGameReal('高砂');let G=C.__get();
const by=n=>Object.values(G.R).find(r=>r.n===n);
const out={};
out.onosato=[by('大の里').hs,by('大の里').uni];out.asa=[by('朝玉勢').hs,by('朝玉勢').uni];
out.kin=[C.kin2(by('王鵬'),by('夢道鵬')),C.kin2(by('夢道鵬'),by('納谷')),C.kin2(by('若元春'),by('大の里'))];
out.rel=Object.entries(G.rel||{}).slice(0,6);
// 母校の化粧廻し
const r=by('朝玉勢');const e={k:'kesho',rid:r.id};out.choices=C.__X.EVT.kesho.c(e);
const rel0=(G.rel||{})['近畿大学']||0;out.msg=C.__X.EVT.kesho.ap(e,3);out.relUp=((G.rel||{})['近畿大学']||0)-rel0;
// 40 場所すすめて、血縁どうしの本割がないか
for(let b=0;b<40;b++){while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();const g=C.__get();while(g.ev.length)C.resolveEv(g.ev[0].id,0);C.nextCycle();}
G=C.__get();let bad=0,pairs=0;const KINP=vm.runInContext('KINP',ctx);
Object.values(G.R).forEach(a=>{const L=KINP[a.kk||a.n];if(!L)return;Object.values(G.R).forEach(b=>{if(b===a||!L.includes(b.kk||b.n))return;pairs++;if(a.h2h&&a.h2h[b.id])bad++;});});
out.kinPairs=pairs/2;out.kinBouts=bad;
const nw=Object.values(G.R).filter(x=>x.arec&&x.arec.some(y=>y.p<=8));out.recruitsWithRec=nw.length;out.sample=nw.slice(0,2).map(x=>[x.n,x.tsuke||'',x.arec.filter(y=>y.p<=8).map(y=>y.t+y.p).join(',')]);
console.log(JSON.stringify(out));
