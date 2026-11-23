// v146:実名で始めると九州場所の実際の成績で終わっているか。次の場所の番付も見る。node tests/rk146.js sumo_manager_v146.html [部屋]
const {chromium}=require('playwright');const f=process.argv[2]||'sumo_manager_v146.html',hn=process.argv[3]||'伊勢ヶ濱';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1180,height:820}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(700);
const r=await p.evaluate((hn)=>{localStorage.clear();newGameReal(hn);UI.title=0;UI.start=0;UI.view='home';render();
 const L=G.last;const by=n=>G.order.map(i=>G.R[i]).find(x=>x.n===n);
 const out={phase:G.phase,b:bname(G.bnum),yu:L.yu.map(y=>y.n+' '+y.w+'-'+y.l+(y.po?'(決定戦)':'')),sh:L.sansho.map(x=>x.n+' '+x.t),po:L.po.length,
  hist:['大の里','若元春','獅司','白熊'].map(n=>{const x=by(n);const h=x.hist[x.hist.length-1];return n+' '+h.w+'-'+h.l+'-'+h.ab+(h.jn?' jn'+h.jn:'')+(x.inj?' inj'+x.inj.s:'');}),
  log:G.log.slice(0,4)};
 let bad=0;G.order.forEach(id=>{const x=G.R[id],h=x.hist[x.hist.length-1],k=RK11[x.n];if(k&&(h.w!==k[0]||h.l!==k[1]||h.ab!==k[2])){bad++;out.badN=(out.badN||[]).concat(x.n+' '+h.w+'-'+h.l+'-'+h.ab+' vs '+k);}});out.bad=bad;return out;},hn);
console.log(JSON.stringify(r,null,1));
await p.screenshot({path:'samples/rk146_post.png'});
const r2=await p.evaluate(()=>{let ok=false,k=0;while(!ok&&k++<20){G.ev.slice().forEach(e=>resolveEv(e.id,0));ok=nextCycle();}render();return {ok:ok,ev:G.ev.map(e=>e.k),phase:G.phase,b:bname(G.bnum),top:G.order.slice(0,20).map(i=>{const x=G.R[i];return x.rk+' '+x.n;}),
 juryoNew:G.order.slice(42,70).map(i=>G.R[i]).filter(x=>x.hist.length&&x.hist[x.hist.length-1].d>=2).map(x=>x.n),
 makNew:G.order.slice(0,42).map(i=>G.R[i]).filter(x=>x.hist.length&&x.hist[x.hist.length-1].d>=1).map(x=>x.n),
 where:['白熊','和真','獅司','朝紅龍','竜電','初山','若隆景','朝翠龍','大青山','栃武蔵','小林'].map(n=>{const i=G.order.findIndex(i=>G.R[i].n===n);return n+':'+(i>=0?G.R[G.order[i]].rk:'なし');}),down:G.order.slice(70,100).map(i=>G.R[i]).filter(x=>x.hist.length&&x.hist[x.hist.length-1].d<=1).map(x=>x.n)};});
console.log(JSON.stringify(r2,null,1),errs);
await p.screenshot({path:'samples/rk146_hatsu.png'});await b.close();})();
