// 稽古の決め方で、伸び・けが・関取の数がどれだけ変わるか(おまかせ/手で軽め/手で強め/手で猛稽古)
// usage: node kc217.js file.html years seed mode [heya]   mode: auto | light | hard | mou | best
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS,mode,heya]=process.argv;const yrs=+yS||5;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},window:{},setTimeout,JSON,Date};
ctx.Math.random=rnd;ctx.window=ctx;vm.createContext(ctx);
code+='\n;globalThis.__get=()=>G;globalThis.__X={own,ownAll,ovr,ME,WEEKS};';vm.runInContext(code,ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
C.newGameReal(heya||'高田川');const G=()=>C.__get();
const st={};C.own().forEach(r=>st[r.id]=C.ovr(r));let inj=0,wk=0,quit=0,dG=0,dN=0;const start=new Set(Object.keys(st));
for(let b=0;b<yrs*6;b++){
 const pre={};C.own().forEach(r=>pre[r.id]=C.ovr(r));
 while(G().phase==='train'){const g=G();g.kAuto=mode==='auto';
  if(mode!=='auto')C.own().forEach(r=>{if(r.inj){r.menu=r.inj.s>=2?'休':'基';r.it=0;return;}
   if(mode==='light'){r.menu='基';r.it=0;}else if(mode==='hard'){r.menu=r.fat>70?'休':'申';r.it=2;}else if(mode==='mou'){r.menu=r.d>=3?'ぶ':'申';r.it=3;}
   else if(mode==='best'){const late=g.wk>=C.WEEKS-1;r.menu=r.fat>70?'休':r.fat>55?'基':late?'申':(r.d<=1?'三':'申');r.it=r.fat>55||late?1:2;}});
  C.doWeek();C.own().forEach(r=>{wk++;if(r.inj)inj++;});}
 C.own().forEach(r=>{if(pre[r.id]!=null&&r.age<30){dG+=C.ovr(r)-pre[r.id];dN++;}});
 while(G().phase==='basho')C.advanceDay();
 let k=0;while(G().ev.length&&k++<50)C.resolveEv(G().ev[0].id,0);if(!C.nextCycle()){G().ev=[];C.nextCycle();}}
const o=C.own();let gain=0,n=0;o.forEach(r=>{if(st[r.id]!=null){gain+=C.ovr(r)-st[r.id];n++;}});
const lost=[...start].filter(id=>{const r=G().R[id];return !r||r.ret;}).length;
console.log(JSON.stringify({mode,seed:sS,場所ごとの伸び:+(dG/dN*100).toFixed(1),残った人:n,やめた引退:lost,けがの週の割合:+(inj/wk*100).toFixed(1),関取:o.filter(r=>r.d<=1).length,幕内:o.filter(r=>r.d===0).length}));
