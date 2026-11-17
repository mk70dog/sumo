// 現実とのマッチング(3):出世の速さ・決まり手・三賞金星決定戦・部屋の数
// usage: node realmatch3.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,openAI};globalThis.__K={};const __F=fight;fight=function(A,B,c){const r=__F(A,B,c);if(A.d===0&&B.d===0)__K[r.k]=(__K[r.k]||0)+1;return r;};',ctx);
const C=ctx;C.newGameReal('高田川');
const ever={},born={},A={nj:0,nm:0,jAge:[],jYrs:[],mAge:[],sansho:0,kin:0,po:0,n:0,heya:[],opened:0,closed:0,mv:{kk1:[],mk1:[]}};
let G=C.__get();Object.values(G.R).forEach(r=>{if(r.d<=1)ever[r.id]=r.d;});
let H0=G.heya.length,closed0=G.heya.filter(h=>h.closed).length;
for(let b=0;b<yrs*6;b++){
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();
 G=C.__get();const L=G.last;A.n++;A.sansho+=(L.sansho||[]).length;A.kin+=(L.kin||[]).length;const y0=(L.yu||[]).find(y=>y.d===0);if(y0&&y0.po)A.po++;
 // 前頭の 8-7・7-8 で何枚動くか
 const pre={};G.order.forEach(id=>{const r=G.R[id];if(r.d===0&&!r.t&&r.hist&&r.hist.length){const x=r.hist[r.hist.length-1];if(x.b===G.bnum&&!x.ab)pre[id]={pos:r.pos,w:x.w};}});
 Object.values(G.R).forEach(r=>{if(born[r.id]==null)born[r.id]=G.bnum;});
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();
 G=C.__get();
 G.order.forEach(id=>{const r=G.R[id];if(r.ret)return;
  if(r.d===1&&ever[id]==null){ever[id]=1;A.nj++;A.jAge.push(r.age);if(r.join>1)A.jYrs.push((G.bnum-r.join)/6);}
  if(r.d===0&&ever[id]!==0){if(ever[id]==null)A.nj++;ever[id]=0;A.nm++;A.mAge.push(r.age);}
  const p=pre[id];if(p&&r.d===0){const dm=(p.pos-r.pos)/2;if(p.w===8)A.mv.kk1.push(dm);if(p.w===7)A.mv.mk1.push(dm);}});
 A.heya.push(G.heya.filter(h=>!h.closed).length);}
const m=a=>a.length?a.reduce((t,x)=>t+x,0)/a.length:0;
const K=C.__K;const tot=Object.values(K).reduce((a,b)=>a+b,0);const top=Object.entries(K).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([k,v])=>k+' '+(v/tot*100).toFixed(1)+'%');
G=C.__get();
console.log(JSON.stringify({'新十両/場所':(A.nj/A.n).toFixed(2),'新入幕/場所':(A.nm/A.n).toFixed(2),'新十両の年齢':m(A.jAge).toFixed(1),'新十両まで(年,ゲーム中入門)':m(A.jYrs).toFixed(1),'新入幕の年齢':m(A.mAge).toFixed(1),
 '前頭8勝7敗の上昇(枚)':m(A.mv.kk1).toFixed(2),'前頭7勝8敗の下降(枚)':(-m(A.mv.mk1)).toFixed(2),
 '三賞/場所':(A.sansho/A.n).toFixed(2),'金星/年':(A.kin/yrs).toFixed(1),'幕内の決定戦%':(A.po/A.n*100).toFixed(1),
 '営業中の部屋(最初→最後)':A.heya[0]+'→'+A.heya[A.heya.length-1],'部屋の平均':m(A.heya).toFixed(1),'新設/年':((G.heya.length-H0)/yrs).toFixed(2),'閉鎖/年':((G.heya.filter(h=>h.closed).length-closed0)/yrs).toFixed(2),
 '決まり手(幕内)':top.join('・')}));
