// v147:九州場所の日ごとの星・金星・これまでの優勝回数。node tests/rk147.js sumo_manager_v147.html
const {chromium}=require('playwright');const f=process.argv[2]||'sumo_manager_v147.html';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1180,height:820}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(700);
const r=await p.evaluate(()=>{localStorage.clear();newGameReal('二所ノ関');UI.title=0;UI.start=0;UI.view='home';render();
 const by=n=>G.order.map(i=>G.R[i]).find(x=>x.n===n);const o={};
 ['大の里','豊昇龍','若隆景','玉鷲','藤凌駕','宇良','熱海富士','若元春','栃武蔵','御嶽海','朝乃山'].forEach(n=>{const x=by(n);o[n]='yu'+x.yu.join(',')+' kin'+x.kin+' sh'+x.sansho;});
 const st=n=>{const x=by(n);const c=G.lastB.rec[x.id];return c?c.res.map(e=>e?e.r+(e.o!=null&&G.R[e.o]?G.R[e.o].n:''):'_').join(' '):'(記録なし)';};
 o.star_大の里=st('大の里');o.star_豊昇龍=st('豊昇龍');o.star_琴栄峰=st('琴栄峰');o.star_白熊=st('白熊');o.kin=G.last.kin.map(k=>G.R[k[0]].n);
 let bad=0;G.order.slice(0,70).forEach(id=>{const x=G.R[id],c=G.lastB.rec[id];if(!c)return;const w=c.res.filter(e=>e&&(e.r==='○'||e.r==='□')).length,l=c.res.filter(e=>e&&(e.r==='●'||e.r==='■')).length,a=c.res.filter(e=>e&&e.r==='や').length;if(w!==c.w||l!==c.l||a!==c.ab){bad++;o['bad_'+x.n]=[w,l,a,c.w,c.l,c.ab].join(',');}});o.bad=bad;return o;});
console.log(JSON.stringify(r,null,1),errs);
await p.evaluate(()=>{const x=G.order.map(i=>G.R[i]).find(x=>x.n==='大の里');go('rikishi');showR(x.id);});await p.waitForTimeout(400);await p.screenshot({path:'samples/rk147_onosato.png',fullPage:false});
await b.close();})();
