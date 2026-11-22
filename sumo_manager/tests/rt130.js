// v130 引退の相談:親方から切り出す・約束・引退後の道 の確認。usage: node rt130.js file.html
const fs=require('fs'),vm=require('vm');const html=fs.readFileSync(process.argv[2],'utf8');
const code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));const store={};
const ctx={console,localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,EVT,rtTalk,rtWhy,rtMood,rtAccept,rtPathC};',ctx);const X=ctx.__X;
ctx.newGameReal('木瀬');const G=()=>ctx.__get();const out={};
const L=X.own().sort((a,b)=>b.age-a.age);const a=L[0],b=L[1],c=L[2];
out.why=X.rtWhy(a);out.mood=X.rtMood(a)[0];out.acc=Math.round(X.rtAccept(a)*100);
a.age=36;a.mor=10;a.tr=90;let m='';for(let i=0;i<5&&!a.rtLast;i++){a.rtTk=null;m=X.rtTalk(a.id,'sus');}out.sus=[!!a.rtLast,m];
X.rtTalk(b.id,'kk');out.kk=b.rtC;out.twice=X.rtTalk(b.id,'hag')==='';
while(G().phase==='train')ctx.doWeek();while(G().phase==='basho')ctx.advanceDay();
const rb=G().lastRec?G().lastRec[b.id]:null;out.aRet=!!(G().R[a.id]&&G().R[a.id].ret);out.b=[G().R[b.id]&&G().R[b.id].ret,b.rtC,G().lastRec&&G().lastRec[b.id]];
out.ev=G().ev.map(e=>e.k);const p=G().ev.find(e=>e.k==='rtPath');if(p){out.pc=X.rtPathC(p);out.pm=ctx.resolveEv(p.id,0);out.sewa=G().sewa;}
console.log(JSON.stringify(out,null,1));
