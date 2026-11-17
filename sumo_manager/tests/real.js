const fs=require('fs'),vm=require('vm');
const [,,file,yrsS,seedS]=process.argv;const yrs=+yrsS||40;let seed=+seedS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.Math.random=rnd;ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,openAI:typeof openAI!=="undefined"?openAI:null,ageOf:typeof ageOf!=="undefined"?ageOf:null};',ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
C.newGameReal('高田川');
const G=()=>C.__get();
const hl={};const ohlog=ctx.hlog;
const Y=[];let seen=new Set(Object.keys(G().R));let newc=0,retAges=[],retN=0;
let lastRet=G().retired.length?G().retired[0]:null;
for(let b=0;b<yrs*6;b++){
 while(G().phase==='train'){const g=G();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(G().phase==='basho')C.advanceDay();
 const g=G();
 for(const id in g.R){if(!seen.has(id)){seen.add(id);newc++;}}
 // retired since last
 for(const x of g.retired){if(x===lastRet)break;retAges.push(x.age);retN++;}
 lastRet=g.retired[0];
 let guard=0;while(g.ev.length&&guard++<50){const e=g.ev[0];const E=C.EVT[e.k];let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}
  const i=(e.k==='shokei'||e.k==='dokuritsu')?0:Math.floor(rnd()*n);C.resolveEv(e.id,i);}
 if(g.bnum%6===0){const act=g.order.map(id=>g.R[id]).filter(r=>!r.ret);const mk=act.filter(r=>r.d===0);
  const hs=new Set(act.map(r=>r.h));
  Y.push({y:Y.length+1,heyaOpen:g.heya.filter(h=>!h.closed).length,heyaWithR:hs.size,total:act.length,newPerYr:newc,mkAge:+(mk.reduce((s,r)=>s+r.age,0)/mk.length).toFixed(1),mkKg:Math.round(mk.reduce((s,r)=>s+(r.w||0),0)/mk.length),mkFr:Math.round(mk.filter(r=>r.fr).length*100/mk.length),Y:act.filter(r=>r.t==='Y').length,O:act.filter(r=>r.t==='O').length,myoFree:g.myo?Object.values(g.myo).filter(m=>m.st==='free').length:null,myoIzo:g.myo?Object.values(g.myo).filter(m=>m.st==='izoku').length:null,myoOwn:g.myo?Object.values(g.myo).filter(m=>m.st==='own').length:null,retAge:retAges.length?+(retAges.reduce((a,b)=>a+b,0)/retAges.length).toFixed(1):null,retN});
  newc=0;retAges=[];retN=0;}
 C.nextCycle();
}
const pick=[1,5,10,20,30,40].map(i=>Y[i-1]).filter(Boolean);
console.log(JSON.stringify(pick));
const logs=(G().hlog||G().hl||[]);console.log('hlog sample',JSON.stringify((Array.isArray(logs)?logs:[]).slice(0,3)));
const H=G().hlog||[];const cat={};H.forEach(x=>{const t=x.t;const k=/独立/.test(t)?'独立':/閉/.test(t)?'閉鎖':/合併|吸収/.test(t)?'合併':/継/.test(t)?'継承':'他';cat[k]=(cat[k]||0)+1;});console.log('hlog',H.length,JSON.stringify(cat));
console.log(H.filter(x=>/独立/.test(x.t)).slice(0,4).map(x=>x.t).join('\n'));

const ML=G().myoLog||[];console.log('myoLog last30', JSON.stringify({ok:ML.filter(x=>/襲名しました/.test(x.t)).length,rent:ML.filter(x=>/預かって/.test(x.t)).length,leave:ML.filter(x=>/去りました/.test(x.t)).length}));
const hs=G().heya.filter(h=>!h.closed);const bad=hs.filter((h,i)=>G().myo&&G().myo[h.n]&&G().myo[h.n].ic!==h.ic&&h.ob);console.log('newHeya',hs.filter(h=>h.ob).length,'icMismatch',bad.length, hs.filter(h=>h.ob).slice(0,6).map(h=>h.n+'('+h.ic+')').join(' '));
const c=[0,0,0,0,0,0];Object.values(G().R).forEach(r=>{if(r.join>12)c[(r.join-1)%6]++;});console.log('join by basho (初春夏名秋九)',c);
if(G().toshi){const T=G().toshi;const al=T.filter(t=>!t.left);console.log('toshi alive',al.length,'shi',al.filter(t=>t.shi).length,'sanyo',al.filter(t=>t.post==='参与').length,'ageMax',Math.max(...al.map(t=>C.ageOf(t.b))),'heyaOpen',G().heya.filter(h=>!h.closed).length,'myo free',Object.values(G().myo).filter(m=>m.st==='free').length);}
if(G().toshi){console.log('old',JSON.stringify(G().toshi.map((t,k)=>[t,k]).filter(([t])=>!t.left&&C.ageOf(t.b)>72).map(([t,k])=>[t.n,t.heya,t.shi,t.post,C.ageOf(t.b),t.nost,C.__get().heya.findIndex(h=>!h.closed&&h.n===t.heya)])));}
