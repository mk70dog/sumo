const fs=require('fs'),vm=require('vm');const [,,file,yS,sS]=process.argv;const yrs=+yS||3;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__bn=bname;',ctx);
const C=ctx;C.newGameReal('高田川');const out=[];
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')C.doWeek();
 let G=C.__get();const top=t=>G.order.map(i=>G.R[i]).filter(r=>r.d===0&&r.t===t).map(r=>r.n);
 const Y=top('Y'),O=top('O');
 while(C.__get().phase==='basho')C.advanceDay();G=C.__get();
 const y=G.last.yu.find(x=>x.d===0);
 out.push([C.__bn(G.bnum),y.n,y.rk,y.w+'勝'+y.l+'敗'+(y.po?'(決定戦)':''),Y.join('・')||'-',O.join('・')||'-']);
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
console.log(out.map(r=>r.join('|')).join('\n'));
