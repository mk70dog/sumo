// 現実とのマッチング(4):番付ごとの勝ち星・大関の角番率・三役の勝率
// usage: node realmatch4.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||25;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;',ctx);
const C=ctx;C.newGameReal('高田川');
const S={};const add=(k,w,l,ab)=>{S[k]=S[k]||{n:0,w:0,full:0,fw:0,mk:0,ky:0};const s=S[k];s.n++;s.w+=w;if(ab===0){s.full++;s.fw+=w;}if(w<8)s.mk++;if(ab>0)s.ky++;};
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')C.doWeek();while(C.__get().phase==='basho')C.advanceDay();const G=C.__get();
 Object.values(G.R).forEach(r=>{if(!r.hist||!r.hist.length)return;const x=r.hist[r.hist.length-1];if(x.b!==G.bnum||!/横綱|大関|関脇|小結|前頭/.test(x.rk||''))return;const m=(x.rk||'').match(/前頭(\d+)/);const k=/横綱/.test(x.rk)?'横綱':/大関/.test(x.rk)?'大関':/関脇/.test(x.rk)?'関脇':/小結/.test(x.rk)?'小結':(m&&+m[1]<=4)?'前頭1-4':'前頭5-';add(k,x.w,x.l,x.ab||0);});
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
const out={};Object.keys(S).forEach(k=>{const s=S[k];out[k]={'場所数':s.n,'平均勝ち星':(s.w/s.n).toFixed(2),'皆勤の平均':(s.fw/Math.max(1,s.full)).toFixed(2),'負け越し%':(100*s.mk/s.n).toFixed(0),'休場あり%':(100*s.ky/s.n).toFixed(0)};});
console.log(JSON.stringify(out));
