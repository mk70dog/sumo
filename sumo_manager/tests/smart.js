// 賢い自動プレイ(v170〜):関取が減っていくのは「でたらめな自動プレイ」のせいか「作り」のせいかを確かめる。
// usage: node tests/smart.js 本体.html 年数 seed 種類(real:部屋名 / new / dok) 方針(smart / rand)
// smart:候補を見に行き素質の高い順に誘う・宿舎/施設を広げる・コーチを雇う・出来事は 1 つめ(前向きな選択)・建物と夏合宿。
// rand :tests/longrun.js と同じ(候補を上から 4 人・出来事はでたらめ)。
const fs=require('fs'),vm=require('vm');
const [,,file,yrsS,seedS,kind,polS]=process.argv;const yrs=+yrsS||40;let seed=+seedS||1;const pol=polS||'smart';
const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};
ctx.Math.random=rnd;ctx.window=ctx;vm.createContext(ctx);
vm.runInContext(code+'\n;globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT,ME,TOSHI,cap,FCOST,ROLE,trackPros,offerPros,offerCost,prosOK,hireStaff,heyaH,potOf,ovr:typeof ovr!=="undefined"?ovr:null,bdBuy:typeof bdBuy!=="undefined"?bdBuy:null,campSet:typeof campSet!=="undefined"?campSet:null,campOpts:typeof campOpts!=="undefined"?campOpts:null};',ctx);
const C=new Proxy(ctx,{get:(t,k)=>(t.__X&&k in t.__X)?t.__X[k]:t[k]});
const k=kind||'real:伊勢ヶ濱';
if(k.startsWith('real:'))C.newGameReal(k.slice(5));else if(k==='new')C.newGame('東雲','東雲','東','四',0,45);else if(k==='dok'){const T=C.TOSHI.find(t=>t[3]!==1&&t[2]==='伊勢ヶ濱')||C.TOSHI.find(t=>t[3]!==1);C.newGameDok(T[0],[]);}
const G=()=>C.__get();const rows=[];let yu=0,sign=0,signP=[];
function reserve(){const g=G();return 1500+C.own().length*40;}
function smartWeek(){const g=G();
 // 候補を見に行く(1 週に何人か)→ 見込みの高い順に誘う
 const P=(g.pros||[]).filter(p=>!C.prosOK(p));
 P.filter(p=>p.v<3).sort((a,b)=>(b.ep??11)-(a.ep??11)).slice(0,3).forEach(p=>{try{C.trackPros(p.cid,'oy');}catch(e){}});
 const best=P.filter(p=>p.v>=1&&p.ep!=null).sort((a,b)=>b.ep-a.ep);
 for(const p of best){if(C.ownAll().length>=C.cap()){break;}
  const lv=p.ep>=13?2:p.ep>=11?1:-1;if(lv<0)break;if(g.money-C.offerCost(p,lv)<reserve())continue;
  const n0=C.ownAll().length;try{C.offerPros(p.cid,lv);}catch(e){}if(C.ownAll().length>n0){sign++;signP.push(+p.ep.toFixed(1));}}
 // 宿舎が足りなければ広げる/ほかの施設
 for(const f of ['shuku','keiko','iryo','shoku']){const lv=g.fac[f];if(lv>=5)continue;const c=C.FCOST[lv];if(f==='shuku'&&C.ownAll().length<C.cap()-1)continue;if(g.money-c>reserve()*1.5){g.money-=c;g.fac[f]++;}}
 // コーチ(部屋付き親方):弟子 6 人に 1 人くらい
 const co=g.staff.filter(s=>s.role==='co').length;if(co<C.ROLE.co.max&&C.own().length/(co+1)>6&&g.money>reserve()*2){const m=(g.market||[]).filter(s=>s.role==='co').sort((a,b)=>Math.max(...Object.values(b.sk))-Math.max(...Object.values(a.sk)))[0];if(m){try{C.hireStaff(m.sid);}catch(e){}}}
}
function smartBasho(){const g=G();const b=g.bld||{};
 if(C.bdBuy&&!b.pj&&!b.cx){for(const o of ['nr','nt','ng']){const c={nr:200000,nt:100000,ng:50000}[o];if(g.money>c+reserve()*3){try{C.bdBuy(o,1);}catch(e){}break;}}}
 if(C.campSet&&b.camp==null&&g.money>reserve()*2){try{const c=C.campOpts();if(c.length)C.campSet(c[0].g);}catch(e){}}
}
for(let b=0;b<yrs*6;b++){
 let g=G();
 if(pol==='smart')smartBasho();
 if(g.phase==='train'){for(let w=0;w<6&&G().phase==='train';w++){g=G();
   if(pol==='smart')smartWeek();else if(g.wk===2&&g.pros&&g.pros.length){for(const p of g.pros.slice(0,4)){if(C.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);}}
   C.doWeek();while(G().ev.length&&G().phase==='train'){const e=G().ev[0];C.resolveEv(e.id,pol==='smart'?0:0);}}}
 while(G().phase==='basho')C.advanceDay();
 g=G();if(g.last&&g.last.yu){g.last.yu.forEach(y=>{if(y.h===C.ME()&&y.d===0)yu++;});}
 let guard=0;while(g.ev.length&&guard++<50){const e=g.ev[0];const E=C.EVT[e.k];let n=2;try{const c=E&&(typeof E.c==='function'?E.c(e):E.c);n=c?c.length:2;}catch(x){}C.resolveEv(e.id,e.k==='shokei'?0:(pol==='smart'?0:Math.floor(rnd()*n)));}
 if(b%6===5){const o=C.own();const sk={};g.order.forEach(id=>{const r=g.R[id];if(r.d<=1&&!r.ret)sk[r.h]=(sk[r.h]||0)+1;});const L=Object.entries(sk).filter(x=>+x[0]!==C.ME()).map(x=>x[1]).sort((a,b)=>b-a);
  const H=C.heyaH(C.ME());const cf=Object.values(H.cf);
  rows.push({y:b/6+1|0,money:Math.round(g.money),seki:o.filter(r=>r.d<=1).length,mk:o.filter(r=>r.d===0).length,deshi:o.length,cap:C.cap(),co:g.staff.filter(s=>s.role==='co').length,cf:(cf.reduce((a,c)=>a+c,0)/cf.length).toFixed(2),kf:H.kf.toFixed(2),cpu:L.slice(0,3).join('/'),yu,sign});sign=0;}
 if(!C.nextCycle()){g.ev=[];C.nextCycle();}
 if(G().over){console.log('GAME OVER year',b/6|0,'money',Math.round(G().money));break;}
}
console.log(k,pol,'seed',+seedS||1);
console.log('年 資金 関取 幕内 弟子/上限 コーチ 育ち(cf) 稽古場(kf) ほかの部屋の関取 上位3 優勝累計 その年に入った弟子');
rows.forEach(r=>{if(r.y<=3||r.y%5===0)console.log([r.y,r.money,r.seki,r.mk,r.deshi+'/'+r.cap,r.co,r.cf,r.kf,r.cpu,r.yu,r.sign].join('\t'));});
const q=G().heya.map((h,i)=>i===C.ME()?null:h.q).filter(x=>x!=null).sort((a,b)=>b-a);console.log('ほかの部屋の育ち(q)上位',q.slice(0,5).map(x=>(+x).toFixed(2)).join(','),'中央',(+q[q.length>>1]).toFixed(2));
console.log('入れた弟子の見込み(ep)',signP.length,'人 平均',signP.length?(signP.reduce((a,c)=>a+c,0)/signP.length).toFixed(1):'-');
