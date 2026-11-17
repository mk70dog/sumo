// 現実とのマッチング用:1 場所あたりの休場者(関取・全体)、けがの件数、不祥事の件数を測る
// usage: node realmatch.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||20;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
code=code.replace('function injure(r,src){','function injure(r,src){globalThis.__inj=(globalThis.__inj||0)+1;if(r.h===0)globalThis.__injO=(globalThis.__injO||0)+1;');
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT};',ctx);
const C=ctx;C.newGameReal('高田川');
const S={n:0,sekK:0,sekN:0,allK:0,allN:0,makK:0,zen:0,sus:0,scOwn:0,newsSc:0,ownN:0,ownK:0};
for(let b=0;b<yrs*6;b++){
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();
 const G=C.__get();S.n++;
 Object.values(G.R).forEach(r=>{const x=r.hist&&r.hist[r.hist.length-1];if(!x||x.b!==G.bnum)return;const k=(x.ab||0)>0;S.allN++;if(k)S.allK++;if(/横綱|大関|関脇|小結|前頭|十両/.test(x.rk)){S.sekN++;if(k)S.sekK++;}if(/横綱|大関|関脇|小結|前頭/.test(x.rk)&&k)S.makK++;if((x.ab||0)>=15||(x.w+x.l===0&&k))S.zen++;if(r.h===0){S.ownN++;if(k)S.ownK++;}});
 G.ev.forEach(e=>{if(e.k==='scand')S.scOwn++;});
 const nn=(G.news||[]).filter(x=>/の問題があり、/.test(typeof x==='string'?x:(x.t||'')));
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
const G=C.__get();
const nsc=(G.news||[]).length;
console.log(JSON.stringify({basho:S.n,'関取の休場/場所':(S.sekK/S.n).toFixed(2),'関取の休場率%':(S.sekK/S.sekN*100).toFixed(1),'幕内の休場/場所':(S.makK/S.n).toFixed(2),'全体の休場/場所':(S.allK/S.n).toFixed(1),'全体の休場率%':(S.allK/S.allN*100).toFixed(1),'全休/場所':(S.zen/S.n).toFixed(1),'自分の部屋の休場率%':(S.ownK/S.ownN*100).toFixed(1),'けが/年(全体)':((ctx.__inj||0)/yrs).toFixed(0),'けが/年(自部屋)':((ctx.__injO||0)/yrs).toFixed(1),'自部屋の不祥事/年':(S.scOwn/yrs).toFixed(2)}));
