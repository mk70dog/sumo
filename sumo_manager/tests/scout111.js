// スカウト(自分の部屋の新弟子)と全体の新弟子が関取・幕内になる割合。最後の 10 年に入門した人は数えない
// usage: node scout111.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,potOf,gradeOf};',ctx);
const C=ctx;C.newGameReal('高田川');
const first={},best={},mine={};const pre=new Set(Object.keys(C.__get().R));const cut=yrs*6-60;/* 最後の 10 年に入門した人は数えない(まだ途中) */
for(let b=0;b<yrs*6;b++){
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();
 const G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);
 Object.values(G.R).forEach(r=>{if(!pre.has(String(r.id))&&first[r.id]==null&&!r.ret){first[r.id]=b;mine[r.id]=r.h===C.ME();}
  if(first[r.id]!=null){const v=r.d===0?2:r.d===1?1:0;best[r.id]=Math.max(best[r.id]||0,v);}});
 C.nextCycle();
}
const o={all:[0,0,0],mine:[0,0,0]};
for(const id in first){if(first[id]>cut)continue;const v=best[id]||0;for(const k of ['all',...(mine[id]?['mine']:[])]){o[k][0]++;if(v>=1)o[k][1]++;if(v>=2)o[k][2]++;}}
const G=C.__get();const act=Object.values(G.R).filter(r=>!r.ret);
console.log(JSON.stringify({o,stock:[act.length,act.filter(r=>r.d===0).length]}));
