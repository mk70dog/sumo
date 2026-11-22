// v131 部屋付き親方探し:声かけ → 候補 → 交渉、人柄・教え方、悩み相談の選択肢。usage: node co131.js file.html [real 1/0]
const fs=require('fs'),vm=require('vm');const html=fs.readFileSync(process.argv[2],'utf8');
const code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));const store={};
const ctx={console,localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,EVT,coReqSet,coAcc,hireStaff,coInit,heyaH,coGoodHito};',ctx);const X=ctx.__X;
if(process.argv[3]==='0')ctx.newGame&&ctx.newGame('テスト','高田川');else ctx.newGameReal('木瀬');const G=()=>ctx.__get();G().money=5000;const out={};
out.req=X.coReqSet('hito');
while(G().phase==='train')ctx.doWeek();while(G().phase==='basho')ctx.advanceDay();G().ev=[];ctx.nextCycle();
out.market=G().market.filter(s=>s.role==='co').map(s=>[s.n,s.req||'',s.hito,s.tch,s.from||'',Math.round(X.coAcc(s)*100)]);
const m=G().market.filter(s=>s.role==='co');out.hire=m.map(s=>X.hireStaff(s.sid));
out.staff=G().staff.filter(s=>s.role==='co').map(s=>[s.n,s.hito,s.tch]);out.good=!!X.coGoodHito();
const e={k:'soudan',tp:'nayami',rid:X.own()[0].id,id:'x'};out.c=X.EVT.soudan.c(e);if(out.c.length>2){G().ev.push(e);out.ap=ctx.resolveEv('x',2);}
console.log(JSON.stringify(out,null,1));
