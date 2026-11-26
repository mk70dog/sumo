// usage: node auto.js file.html years seed [heya]
const fs=require('fs'),vm=require('vm');
const [,,file,yrsS,seedS,heya]=process.argv;const yrs=+yrsS||40;
let seed=+seedS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');
const a=html.indexOf("'use strict';"),b=html.indexOf('/* ========== 画面');
let code=html.slice(a,b);
const store={};
const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},window:{},setTimeout,JSON,Date};
ctx.Math.random=rnd;ctx.window=ctx;
vm.createContext(ctx);
code+='\n;globalThis.__get=()=>G;globalThis.__set=g=>{G=g;};globalThis.__X={own,ownAll,EVT,me};';
vm.runInContext(code,ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
C.newGameReal(heya||'高田川');const BAD=process.env.BAD==='1';
const stats={err:0,errs:[],yoko:[],own:[],tr:[],quit:0,quitEarly:0,joined:0,scand:0,atmo:[],jin:[],ev:{}};
const t0=Date.now();
function G(){return C.__get();}
const seenOwn=new Set();
const seenO=new Set(G().order);const CO={};const seen=new Set(Object.keys(G().R));const CNT={};const RET={};const OWNN={};
for(let b=0;b<yrs*6;b++){
 {const g=G();const bi=(g.bnum-1)%6;const yr=Math.floor((g.bnum-1)/6);for(const id in g.R){if(!seen.has(id)){seen.add(id);const r=g.R[id];const k=yr+':'+bi;CNT[k]=(CNT[k]||0)+1;if(r.h===C.me().i||r.h===0)OWNN[yr]=(OWNN[yr]||0)+1;}}
  RET[yr]=Object.values(g.R).filter(r=>r.ret).length;}
 try{
  let g=G();
  // recruit
  if(g.phase==='train'){
   for(let w=0;w<6&&G().phase==='train';w++){
    g=G();
    if(g.wk===2&&g.pros&&g.pros.length){for(const p of g.pros.slice(0,4)){if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);}}
    if(BAD){const o=C.ownAll();o.forEach(r=>{r.sh='厳';});G().meSel={auto:0,ids:o.slice(0,2).map(r=>r.id)};}
    C.doWeek();}
  }
  {const g2=G();const bi=(g2.bnum-1)%6;const yr=Math.floor((g2.bnum-1)/6);for(const id of g2.order){if(!seenO.has(id)){seenO.add(id);const k=yr+':'+bi;CO[k]=(CO[k]||0)+1;}}}
  while(G().phase==='basho')C.advanceDay();
  g=G();
  g.order.forEach(id=>{const r=g.R[id];if(r.h===0&&!seenOwn.has(id)){seenOwn.add(id);}});
  let guard=0;
  while(g.ev.length&&guard++<50){const e=g.ev[0];stats.ev[e.k]=(stats.ev[e.k]||0)+1;if(e.k==='scand')stats.scand++;const E=C.EVT?C.EVT[e.k]:null;let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}
   const i=e.k==='shokei'?0:Math.floor(rnd()*n);C.resolveEv(e.id,i);}
  const own=C.own();
  stats.own.push(own.length);
  stats.atmo.push(C.atmo());
  if(g.jin!=null)stats.jin.push(g.jin);
  own.forEach(r=>stats.tr.push(r.tr));
  stats.yoko.push(g.order.filter(id=>g.R[id].t==='Y').length);
  if(!C.nextCycle()){g.ev=[];C.nextCycle();}
 }catch(e){stats.err++;if(stats.errs.length<5)stats.errs.push(String(e.stack).slice(0,400));const g=G();if(g.phase==='post'){g.ev=[];try{C.nextCycle();}catch(x){}}}
}
const g=G();
const own=g.retired.filter(x=>x.own);
const mean=a=>a.reduce((s,x)=>s+x,0)/Math.max(1,a.length);
const hist=a=>{const h=[0,0,0,0,0];a.forEach(x=>h[Math.min(4,Math.floor(x/20))]++);return h.map(x=>Math.round(x*100/Math.max(1,a.length)));};
const out={file,yrs,seed:seedS,err:stats.err,errs:stats.errs,sec:Math.round((Date.now()-t0)/1000),
 yokoAvg:+mean(stats.yoko).toFixed(2),yoko0:Math.round(stats.yoko.filter(x=>x===0).length*100/stats.yoko.length),
 ownAvg:+mean(stats.own).toFixed(1),trAvg:+mean(stats.tr).toFixed(1),trHist:hist(stats.tr),atmo:+mean(stats.atmo).toFixed(1),jin:stats.jin.length?+mean(stats.jin).toFixed(1):null,
 ownRetired:own.length,scand:stats.scand,ev:stats.ev,heyaN:g.heya.length,total:g.order.length,money:Math.round(g.money)};
if(g.st16)out.st16=g.st16;if(g.yfin)out.yfin=g.yfin.map(x=>[x.i-x.o,x.m]);out.over=!!g.over;out.supC=g.supC;out.sup=g.sup;out.chi=g.chi;
const Y={};for(const k in CNT){const [y,bi]=k.split(':');Y[y]=Y[y]||[0,0,0,0,0,0];Y[y][bi]+=CNT[k];}const Y2={};for(const k in CO){const [y,bi]=k.split(':');Y2[y]=Y2[y]||[0,0,0,0,0,0];Y2[y][bi]+=CO[k];}const ys=Object.keys(Y2).map(Number).sort((a,b)=>a-b).slice(1,-1);const avg=[0,1,2,3,4,5].map(i=>+(ys.reduce((s,y)=>s+Y2[y][i],0)/ys.length).toFixed(1));console.log('DEBUT',JSON.stringify(avg),'年',+(avg.reduce((a,b)=>a+b,0)).toFixed(1),JSON.stringify(ys.map(y=>Y2[y].reduce((a,b)=>a+b,0))));console.log('TOTAL',G().order.length);
