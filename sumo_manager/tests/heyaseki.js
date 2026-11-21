// 部屋ごとの関取の人数の散らばり(実際:45 部屋・関取 70 人、多い部屋 7 人、0 人の部屋が多い)。usage: node heyaseki.js file.html years seed
// 素質(入門したときの見込み)ごとに、どこまで出世したかを数える
// usage: node soshitsu.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,potOf,gradeOf};',ctx);
const C=ctx;C.newGameReal('高田川');const E=x=>vm.runInContext(x,ctx);
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')E('doWeek()');while(C.__get().phase==='basho')E('advanceDay()');const G=C.__get();while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
console.log(E(`(function(){const c={};G.heya.forEach((h,i)=>{if(!h.closed)c[i]=0;});Object.values(G.R).forEach(r=>{if(!r.ret&&r.d<=1&&c[r.h]!=null)c[r.h]++;});const v=Object.values(c).sort((a,b)=>b-a);const z=v.filter(x=>x===0).length;return JSON.stringify({heya:v.length,seki:v.reduce((s,x)=>s+x,0),top5:v.slice(0,5),zero:z});})()`));
