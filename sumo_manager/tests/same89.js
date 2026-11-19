// v89 の確認:同じ乱数で動かし、ゲームの中身(G)が前の版と同じになるか。usage: node same89.js file.html years seed [heya]
// 版の番号や v89 で足した記録(oh・_psup・subX と、場所の成績の h)は比べる前に外す。
const fs=require('fs'),vm=require('vm'),crypto=require('crypto');
const [,,file,yrsS,seedS,heya]=process.argv;const yrs=+yrsS||10;
let seed=+seedS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');
const a=html.indexOf("'use strict';"),b=html.indexOf('/* ========== 画面');
let code=html.slice(a,b);
const store={};
const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},window:{},setTimeout,JSON,Date};
ctx.Math.random=rnd;ctx.window=ctx;
vm.createContext(ctx);
code+='\n;globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,me};';
vm.runInContext(code,ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
C.newGameReal(heya||'高田川');
const G=()=>C.__get();
const snaps=[];
for(let bb=0;bb<yrs*6;bb++){
  for(let w=0;w<6&&G().phase==='train';w++){
    const g=G();
    if(g.wk===2&&g.pros&&g.pros.length){for(const p of g.pros.slice(0,4)){if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);}}
    C.doWeek();}
  while(G().phase==='basho')C.advanceDay();
  let guard=0;const g=G();
  while(g.ev.length&&guard++<50){const e=g.ev[0];const E=C.EVT?C.EVT[e.k]:null;let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}
    const i=e.k==='shokei'?0:Math.floor(rnd()*n);C.resolveEv(e.id,i);}
  if(!C.nextCycle()){g.ev=[];C.nextCycle();}
  if(bb%6===5)snaps.push(hash());
}
function norm(k,v){if(k==='v'||k==='oh'||k==='_psup'||k==='subX')return undefined;return v;}
function hash(){const g=JSON.parse(JSON.stringify(G(),norm));if(g.last&&g.last.own)g.last.own.forEach(x=>delete x.h);
  // キーの順番をそろえる
  const sortK=o=>Array.isArray(o)?o.map(sortK):(o&&typeof o==='object')?Object.keys(o).sort().reduce((a,k)=>(a[k]=sortK(o[k]),a),{}):o;
  return crypto.createHash('md5').update(JSON.stringify(sortK(g))).digest('hex').slice(0,10);}
console.log(JSON.stringify({file:file.split('/').pop(),seed:seedS,money:Math.round(G().money),n:G().order.length,snaps}));
