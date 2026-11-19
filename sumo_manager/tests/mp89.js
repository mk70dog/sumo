// v89 の確認:プレイヤー 2 人(親=部屋 0、子=もう 1 部屋)の中身だけを自動で動かす。usage: node mp89.js file.html years seed [親の部屋] [子の部屋]
// 2 人とも、一人用の自動プレイと同じやり方で新弟子を勧誘し、出来事に答える。
// 確かめること:エラー 0、子の部屋に勝手に新弟子が入らない(子が勧誘した弟子だけ)、2 人ともお金・出来事・日誌が動く。
const fs=require('fs'),vm=require('vm');
const [,,file,yrsS,seedS,hostH,guestH]=process.argv;const yrs=+yrsS||10;
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
C.newGameReal(hostH||'高田川');
const G=()=>C.__get();
const gh=G().heya.findIndex(h=>h.n===(guestH||'伊勢ヶ濱'));
C.addPlayer(gh);
const st={err:0,errs:[],ev:[0,0],money:[[],[]],own:[[],[]],sneak:0,joined:[0,0],retired:[0,0],news:[0,0],yu:[0,0],sek:[[],[]],staff:[[],[]],ach:[0,0]};
const known=[new Set(),new Set()];
function snapOwn(i){C.pUse(i);const s=new Set(C.ownAll().map(r=>r.id));C.pUse(0);return s;}
known[0]=snapOwn(0);known[1]=snapOwn(1);
const t0=Date.now();
for(let bb=0;bb<yrs*6;bb++){
 try{
  for(let w=0;w<6&&G().phase==='train';w++){
   for(let i=0;i<2;i++){C.pUse(i);const g=G();
    if(g.wk===2&&g.pros&&g.pros.length){for(const p of g.pros.slice(0,4)){if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);}}
    C.ownAll().forEach(r=>known[i].add(r.id));}
   C.pUse(0);C.doWeek();}
  while(G().phase==='basho')C.advanceDay();
  for(let i=0;i<2;i++){C.pUse(i);const g=G();let guard=0;
   while(g.ev.length&&guard++<50){const e=g.ev[0];st.ev[i]++;const E=C.EVT?C.EVT[e.k]:null;let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}
    const k=e.k==='shokei'?0:Math.floor(rnd()*n);C.resolveEv(e.id,k);}
   C.ownAll().forEach(r=>known[i].add(r.id));}
  C.pUse(0);
  if(!C.nextCycle()){for(let i=0;i<2;i++){C.pUse(i);G().ev=[];}C.pUse(0);C.nextCycle();}
  // 子の部屋に、子が勧誘していない弟子が入っていないか(部屋付き親方の独立で出ていくのはよい)
  for(let i=0;i<2;i++){C.pUse(i);C.own().forEach(r=>{if(!known[i].has(r.id)){st.sneak++;known[i].add(r.id);if(st.errs.length<8)st.errs.push('sneak p'+i+' '+r.n+' kind='+r.kind);}});
   const g=G();st.money[i].push(Math.round(g.money));st.own[i].push(C.own().length);st.sek[i].push(C.own().filter(r=>r.d<=1).length);st.staff[i].push(g.staff.length);}
  C.pUse(0);
 }catch(e){st.err++;if(st.errs.length<8)st.errs.push(String(e.stack).slice(0,500));try{C.pUse(0);}catch(x){}const g=G();if(g.phase==='post'){for(let i=0;i<2;i++){try{C.pUse(i);G().ev=[];}catch(x){}}C.pUse(0);try{C.nextCycle();}catch(x){}}}
}
const g=G();
for(let i=0;i<2;i++){C.pUse(i);const x=G();st.news[i]=x.log.length;st.ach[i]=x.ach.length;st.retired[i]=x.retired.filter(r=>r.oh===C.ME()).length;st.yu[i]=x.yusho.filter(y=>y.oh===C.ME()).length;}
C.pUse(0);
const mean=a=>Math.round(a.reduce((s,x)=>s+x,0)/Math.max(1,a.length)*10)/10;
const last=a=>a[a.length-1];
console.log(JSON.stringify({file:file.split('/').pop(),yrs,seed:seedS,guest:g.heya[gh].n,err:st.err,errs:st.errs,sec:Math.round((Date.now()-t0)/1000),sneak:st.sneak,
 ev:st.ev,ach:st.ach,news:st.news,retired:st.retired,yusho:st.yu,
 money:[last(st.money[0]),last(st.money[1])],ownAvg:[mean(st.own[0]),mean(st.own[1])],sekAvg:[mean(st.sek[0]),mean(st.sek[1])],staffLast:[last(st.staff[0]),last(st.staff[1])],
 total:g.order.length,heyaN:g.heya.filter(h=>!h.closed).length,P:g.P.map(p=>p.h),PA:g.PA}));
