// 40 年の手応えの確認:年ごとの資金・関取・弟子・評判・後援会・出来事の数を出す。
// usage: node tests/longrun.js 本体.html 年数 seed 種類(real:部屋名 / new / dok)
const fs=require('fs'),vm=require('vm');
const [,,file,yrsS,seedS,kind]=process.argv;const yrs=+yrsS||40;let seed=+seedS||1;
const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};
ctx.Math.random=rnd;ctx.window=ctx;vm.createContext(ctx);
vm.runInContext(code+'\n;globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,ME,TOSHI};',ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
const k=kind||'real:伊勢ヶ濱';
if(k.startsWith('real:'))C.newGameReal(k.slice(5));else if(k==='new')C.newGame('東雲','東雲','東','四',0,45);else if(k==='dok'){const T=C.TOSHI.find(t=>t[3]!==1&&t[2]==='伊勢ヶ濱')||C.TOSHI.find(t=>t[3]!==1);C.newGameDok(T[0],[]);}
const G=()=>C.__get();const rows=[];let evY=0,evK={},yu=0,sanY=0;
console.log(k,'start money',Math.round(G().money),'keys',Object.keys(G()).filter(x=>/rep|sup|hyo|kou|fame|jin/i.test(x)).join(','));
for(let b=0;b<yrs*6;b++){
 let g=G();
 if(g.phase==='train'){for(let w=0;w<6&&G().phase==='train';w++){g=G();if(g.wk===2&&g.pros&&g.pros.length){for(const p of g.pros.slice(0,4)){if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);}}C.doWeek();while(G().ev.length&&G().phase==='train'){const e=G().ev[0];evY++;evK[e.k]=(evK[e.k]||0)+1;C.resolveEv(e.id,0);}}}
 while(G().phase==='basho')C.advanceDay();
 g=G();if(g.last&&g.last.yu){g.last.yu.forEach(y=>{if(y.h===C.ME()&&y.d===0)yu++;});}
 let guard=0;while(g.ev.length&&guard++<50){const e=g.ev[0];evY++;evK[e.k]=(evK[e.k]||0)+1;const E=C.EVT[e.k];let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}C.resolveEv(e.id,e.k==='shokei'?0:Math.floor(rnd()*n));}
 if(b%6===5){const o=C.own();rows.push({y:b/6+1|0,sp:Math.round((g.yacc?g.yacc.o:0)),money:Math.round(g.money),seki:o.filter(r=>r.d<=1).length,mk:o.filter(r=>r.d===0).length,deshi:o.length,rep:Math.round(g.rep??-1),sup:g.sup??-1,ev:evY,yu});evY=0;}
 if(!C.nextCycle()){g.ev=[];C.nextCycle();}
 if(G().over){console.log('GAME OVER year',b/6|0,'money',Math.round(G().money),'over',JSON.stringify(G().over).slice(0,200),'oyAge',G().oy&&G().oy.age);break;}
}
console.log('年 資金(万) 関取 幕内 弟子 評判 後援会 出来事/年 幕内優勝累計');
rows.forEach(r=>{if(r.y<=5||r.y%5===0)console.log([r.y,r.money,r.seki,r.mk,r.deshi,r.rep,r.sup,r.ev,r.yu].join('\t'));});
const gg=G();const sk={};gg.order.forEach(id=>{const r=gg.R[id];if(r.d<=1)sk[r.h]=(sk[r.h]||0)+1;});const L=Object.values(sk).sort((a,b)=>b-a);console.log('40 年後の部屋ごとの関取の数(多い順)',L.join(','),'/ 部屋数',gg.heya.length,'/ 自分',sk[C.ME()]||0);
console.log('出来事の種類(多い順)',Object.entries(evK).sort((a,b)=>b[1]-a[1]).slice(0,12).map(x=>x.join(':')).join(' '));
