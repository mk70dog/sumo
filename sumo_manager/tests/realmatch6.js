// 番付の力の調整用:優勝の割合・決定戦・金星・大関対横綱・三役対平幕上位
// usage: node realmatch6.js file.html years seed [BZ式 例 "Y:.04,O:.03,S:.02,K:.015"]
const fs=require('fs'),vm=require('vm');
const [,,file,yS,sS,bz]=process.argv;const yrs=+yS||20;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
if(bz)code=code.replace(/const BZ=\{[^}]*\};/,'const BZ={'+bz+'};');
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout:()=>0,clearTimeout:()=>0};
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;',ctx);
const C=ctx;C.newGameReal('高田川');const T={};const A={yu:{Y:0,O:0,SK:0,M:0},n:0,po:0,kin:0,ybs:0,yw:[],ow:[],sw:[]};
const grp=(r,fm)=>{if(r.d!==0)return null;if(r.t==='Y')return 'Y';if(r.t==='O')return 'O';if(r.t==='S'||r.t==='K')return 'SK';const n=Math.floor((r.pos-fm)/2)+1;return n<=5?'M1':n<=11?'M2':'M3';};
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')C.doWeek();
 let G=C.__get();const fm=G.order.map(i=>G.R[i]).filter(r=>r.d===0&&!r.t).reduce((m,r)=>Math.min(m,r.pos),1e9);const g0={};G.order.forEach(id=>{g0[id]=grp(G.R[id],fm);});
 while(C.__get().phase==='basho'){const bs=C.advanceDay();bs.forEach(x=>{if(x.fus)return;const a=g0[x.w],c=g0[x.l];if(!a||!c||a===c)return;const k=a<c?a+'|'+c:c+'|'+a;T[k]=T[k]||{};T[k][a]=(T[k][a]||0)+1;});}
 G=C.__get();const L=G.last;A.n++;A.kin+=(L.kin||[]).length;const y0=(L.yu||[]).find(y=>y.d===0);if(y0&&y0.po)A.po++;
 Object.values(G.R).forEach(r=>{const x=r.hist&&r.hist[r.hist.length-1];if(!x||x.b!==G.bnum||x.d!==0)return;const g=bzGrp(x.t);if(x.t==='Y'){A.ybs++;if(!x.ab)A.yw.push(x.w);}if(x.t==='O'&&!x.ab)A.ow.push(x.w);if((x.t==='S'||x.t==='K')&&!x.ab)A.sw.push(x.w);if(x.yu){A.yu[x.t==='Y'?'Y':x.t==='O'?'O':(x.t==='S'||x.t==='K')?'SK':'M']++;}});
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
function bzGrp(t){return t;}
const pct=(a,c)=>{const k=a<c?a+'|'+c:c+'|'+a;const t=T[k]||{};const wa=t[a]||0,wc=t[c]||0;return (100*wa/Math.max(1,wa+wc)).toFixed(0);};
const av=a=>(a.reduce((s,x)=>s+x,0)/Math.max(1,a.length)).toFixed(1);const yt=A.yu.Y+A.yu.O+A.yu.SK+A.yu.M;
console.log(JSON.stringify({優勝:{横綱:(100*A.yu.Y/yt).toFixed(0),大関:(100*A.yu.O/yt).toFixed(0),三役:(100*A.yu.SK/yt).toFixed(0),平幕:(100*A.yu.M/yt).toFixed(0)},決定戦:(100*A.po/A.n).toFixed(0),金星per横綱場所:(A.kin/Math.max(1,A.ybs)).toFixed(2),横綱数:(A.ybs/A.n).toFixed(1),
 大関対横綱:pct('O','Y'),三役対横綱:pct('SK','Y'),大関対三役:pct('O','SK'),大関対平幕上位:pct('O','M1'),三役対平幕上位:pct('SK','M1'),三役対平幕中位:pct('SK','M2'),横綱対平幕上位:pct('Y','M1'),皆勤勝:{横綱:av(A.yw),大関:av(A.ow),三役:av(A.sw)}}));
