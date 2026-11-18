// 若手の伸び:実在の若手の番付と力の推移、三役以上の年齢
// usage: node young.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||4;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');const code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;',ctx);
const C=ctx;C.newGameReal('高田川');
const W=['安青錦','藤ノ川','藤凌駕','伯乃富士','琴栄峰','嵐富士','丹治','旭富士','時不動','大の里','豊昇龍','霧島','琴櫻'];
const pos=r=>r.ret?'引退':(['幕内','十両','幕下','三段目','序二段','序ノ口'][r.d]+(r.t?'('+r.t+')':'')+' '+(r.pos-G().order.map(i=>G().R[i]).filter(x=>x.d===r.d).reduce((m,x)=>Math.min(m,x.pos),1e9)+1));
const G=()=>C.__get();const byN=n=>Object.values(G().R).find(r=>r.n===n);
const out={};W.forEach(n=>{const r=byN(n);if(!r){console.log('なし',n);return;}out[n]=[r.age.toFixed(0)+'歳 力'+C.ovr(r).toFixed(1)+'/上限'+C.potOf(r).toFixed(1)+' '+pos(r)];});
const sanAge=[];
for(let y=1;y<=yrs;y++){for(let b=0;b<6;b++){while(G().phase==='train')C.doWeek();while(G().phase==='basho')C.advanceDay();while(G().ev.length)C.resolveEv(G().ev[0].id,0);C.nextCycle();
  G().order.map(i=>G().R[i]).filter(r=>r.d===0&&r.t).forEach(r=>sanAge.push(r.age));}
 W.forEach(n=>{const r=byN(n);if(!out[n])return;if(!r){out[n].push('消');return;}out[n].push('力'+C.ovr(r).toFixed(1)+' '+pos(r));});}
const u25=sanAge.filter(a=>a<25).length/sanAge.length;
console.log(JSON.stringify({seed:+sS,三役以上の平均年齢:(sanAge.reduce((s,a)=>s+a,0)/sanAge.length).toFixed(1),三役以上で25歳未満:(100*u25).toFixed(0)+'%'}));
for(const n in out)console.log(n.padEnd(4,'　'),out[n].join(' → '));
