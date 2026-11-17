// 現実とのマッチング(2):引退・番付と優勝・体格と入門者・お金を測る
// usage: node realmatch2.js file.html years seed
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS]=process.argv;const yrs=+yS||30;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);
vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT};',ctx);
const C=ctx;C.newGameReal('高田川');
const seen={},born={},A={yu:{Y:0,O:0,SK:0,M:0,J:0},yuW:[],oz:[],yo:[],wt:[],ht:[],ag:[],fr:[],uni:[],tot:[],newc:0,retAge:[],retAgeSek:[],car:[],early:[0,0],kadoDrop:0,ozPromo:0,yoPromo:0};
const MAK=/横綱|大関|関脇|小結|前頭/;
let prevO=new Set(),prevY=new Set();
const B0=C.__get().bnum;
for(let b=0;b<yrs*6;b++){
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();
 const G=C.__get();
 const act=Object.values(G.R).filter(r=>!r.ret&&r.hist&&r.hist.length&&r.hist[r.hist.length-1].b===G.bnum);
 act.forEach(r=>{const x=r.hist[r.hist.length-1];if(x.yu&&MAK.test(x.rk)){const k=/横綱/.test(x.rk)?'Y':/大関/.test(x.rk)?'O':/関脇|小結/.test(x.rk)?'SK':'M';A.yu[k]++;A.yuW.push(x.w);}});
 const mak=act.filter(r=>MAK.test(r.hist[r.hist.length-1].rk));
 A.wt.push(mak.reduce((t,r)=>t+r.w,0)/mak.length);A.ht.push(mak.reduce((t,r)=>t+r.ht,0)/mak.length);A.ag.push(mak.reduce((t,r)=>t+r.age,0)/mak.length);
 A.fr.push(mak.filter(r=>r.fr).length/mak.length);A.uni.push(mak.filter(r=>r.uni).length/mak.length);A.tot.push(G.order.filter(id=>!G.R[id].ret).length);
 const O=new Set(act.filter(r=>r.t==='O').map(r=>r.id)),Y=new Set(act.filter(r=>r.t==='Y').map(r=>r.id));A.oz.push(O.size);A.yo.push(Y.size);
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);
 Object.values(G.R).forEach(r=>{if(!seen[r.id]){seen[r.id]=1;if(b>0){born[r.id]=G.bnum;A.newc++;}}
  if(r.ret&&!r._m){r._m=1;A.retAge.push(r.age);if((r.nSk||0)>0)A.retAgeSek.push(r.age);if(born[r.id]!=null){A.car.push((G.bnum-born[r.id])/6);if(G.bnum-born[r.id]<=12)A.early[0]++;}}});
 C.nextCycle();
 const G2=C.__get();
 const O2=new Set(G2.order.filter(id=>G2.R[id].t==='O'&&!G2.R[id].ret)),Y2=new Set(G2.order.filter(id=>G2.R[id].t==='Y'&&!G2.R[id].ret));
 O2.forEach(id=>{if(!O.has(id)&&!Y.has(id))A.ozPromo++;});Y2.forEach(id=>{if(!Y.has(id))A.yoPromo++;});O.forEach(id=>{const r=G2.R[id];if(r&&!r.ret&&r.t!=='O'&&r.t!=='Y')A.kadoDrop++;});

}
const G=C.__get();
// 入門 2 年以内の廃業:最初の 18 年に入った人のうち、12 場所以内に辞めた割合
Object.keys(born).forEach(id=>{const r=G.R[id];if(!r)return;if(born[id]-B0>(yrs-3)*6)return;A.early[1]++;if(r.ret&&(r._rb||0)===0){}});
let eN=0;Object.keys(born).forEach(id=>{if(born[id]-B0<=(yrs-3)*6)eN++;});const early=A.early[0];
const m=a=>a.length?(a.reduce((t,x)=>t+x,0)/a.length):0;const md=a=>{const s=a.slice().sort((x,y)=>x-y);return s[Math.floor(s.length/2)];};
const yt=A.yu.Y+A.yu.O+A.yu.SK+A.yu.M;
console.log(JSON.stringify({
 '引退の平均年齢(全員)':m(A.retAge).toFixed(1),'引退の平均年齢(関取経験者)':m(A.retAgeSek).toFixed(1),'土俵生活の年数(中央値)':(md(A.car)||0).toFixed(1),'入門2年以内に辞めた割合%':(early/eN*100).toFixed(1),
 '幕内優勝 横綱%':(A.yu.Y/yt*100).toFixed(0),'大関%':(A.yu.O/yt*100).toFixed(0),'三役%':(A.yu.SK/yt*100).toFixed(0),'平幕%':(A.yu.M/yt*100).toFixed(0),'優勝の勝ち星(平均)':m(A.yuW).toFixed(2),
 '大関の数(平均)':m(A.oz).toFixed(2),'横綱の数(平均)':m(A.yo).toFixed(2),'新大関/年':(A.ozPromo/yrs).toFixed(2),'新横綱/年':(A.yoPromo/yrs).toFixed(2),'大関陥落/年':(A.kadoDrop/yrs).toFixed(2),
 '幕内の平均体重kg':m(A.wt).toFixed(1),'幕内の平均身長cm':m(A.ht).toFixed(1),'幕内の平均年齢':m(A.ag).toFixed(1),'幕内の外国出身%':(m(A.fr)*100).toFixed(1),'幕内の大学出身%':(m(A.uni)*100).toFixed(1),
 '新弟子/年':(A.newc/yrs).toFixed(1),'総数(平均)':m(A.tot).toFixed(0)}));
