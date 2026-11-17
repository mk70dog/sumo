const fs=require('fs'),vm=require('vm');
function mk(file,store){const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
 const ctx={console,localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
 vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__set=g=>{G=g;};globalThis.__X={own,ownAll,EVT};',ctx);return ctx;}
function play(C,n){for(let b=0;b<n;b++){const G=C.__get();
 while(C.__get().phase==='train'){const g=C.__get();if(g.wk===2&&g.pros)g.pros.slice(0,3).forEach(p=>{if(C.__X.ownAll().length<C.cap()-1)C.offerPros(p.cid,1);});C.doWeek();}
 while(C.__get().phase==='basho')C.advanceDay();const g=C.__get();while(g.ev.length)C.resolveEv(g.ev[0].id,Math.floor(Math.random()*2));C.nextCycle();}}
const s12={};const A=mk(process.argv[2],s12);A.newGameReal('伊勢ヶ濱');play(A,18);
// 稽古期間の途中で保存
A.doWeek();A.doWeek();A.save();
const OK=process.argv[4]||'sumoManager12';const s13={};s13[OK]=s12[OK];const B=mk(process.argv[3],s13);
const g=B.load();if(!g)throw new Error('load failed');B.__set(g);
console.log('loaded v',g.v,'supC',g.supC,'chi',JSON.stringify(g.chi),'bld',JSON.stringify(g.bld),'own',B.__X.own().length,'jin',g.jin,'meSel',JSON.stringify(g.meSel),'sh',B.__X.own().slice(0,3).map(r=>r.sh));
play(B,30);B.save();console.log('after 5y v',B.__get().v,'st16',JSON.stringify(B.__get().st16),'newkey',Object.keys(s13));
