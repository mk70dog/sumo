// 素質(入門したときの見込み)ごとに、どこまで出世したかを数える
// usage: node soshitsu.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,potOf,gradeOf};',ctx);
const C=ctx;C.newGameReal('高田川');
const g0={},best={};const RK={Y:5,O:4,S:3,K:3};
for(let b=0;b<yrs*6;b++){
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();
 const G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);
 Object.values(G.R).forEach(r=>{if(b>0&&g0[r.id]==null&&!r.ret){g0[r.id]=C.__X.gradeOf(C.__X.potOf(r));}
  if(g0[r.id]!=null){const v=r.t?RK[r.t]:r.d===0?2:r.d===1?1:0;best[r.id]=Math.max(best[r.id]||0,v);}});
 C.nextCycle();
}
const out={};
for(const id in g0){const g=g0[id];out[g]=out[g]||{n:0,sekitori:0,makuuchi:0,sanyaku:0,ozeki:0,yokozuna:0};const o=out[g],v=best[id]||0;o.n++;if(v>=1)o.sekitori++;if(v>=2)o.makuuchi++;if(v>=3)o.sanyaku++;if(v>=4)o.ozeki++;if(v>=5)o.yokozuna++;}
console.log(JSON.stringify(out));
