// v142 独立の段取り:画面を順に進めて、最後にゲームが始まるか確かめる。node tests/dp142.js sumo_manager_v142.html
const {chromium}=require('playwright');const f=process.argv[2]||'sumo_manager_v142.html';
(async()=>{const b=await chromium.launch();let bad=0;
for(const [W,H,tag] of [[1180,820,'a'],[820,1180,'b'],[390,844,'s']])for(let run=0;run<4;run++){
 const p=await b.newPage({viewport:{width:W,height:H}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(700);
 await p.evaluate(()=>{localStorage.clear();UI.title=false;UI.start='dok';render();});await p.waitForTimeout(200);await p.evaluate(()=>dokSheet('桐山'));await p.waitForTimeout(200);
 await p.evaluate(()=>{document.querySelectorAll('.dkw input').forEach((e,i)=>e.checked=i<4);doStartDok('桐山');});
 const shots=[];let guard=0;
 while(guard++<30){const st=await p.evaluate(()=>UI.dp?UI.dp.st:0);if(!st)break;
  if(run===0&&!shots.includes(st)){shots.push(st);await p.screenshot({path:'samples/dp142_'+tag+st+'.png'});}
  const ov=await p.evaluate(()=>{const e=document.querySelector('#dpx .in');return e.scrollWidth>e.clientWidth+1;});if(ov){console.log('overflow',tag,st);bad++;}
  await p.evaluate((run)=>{const bs=[...document.querySelectorAll('#dpx button')];const per=bs.find(x=>x.textContent==='もう一度説得');if(per&&run%2===0){per.click();return;}
   const may=bs.filter(x=>!x.classList.contains('ai'));if(may.length>=3&&!bs.some(x=>x.classList.contains('ai'))){may[run%3].click();return;}
   const ai=bs.find(x=>x.classList.contains('ai'));ai.click();},run);await p.waitForTimeout(80);}
 const r=await p.evaluate(()=>({me:G.heya[ME()].n,own:own().map(r=>r.n),dok:G.dok,news:G.log[0],title:UI.title}));
 console.log(tag,run,r.me,r.own.join(','),JSON.stringify(r.dok),r.news);if(errs.length){console.log('ERR',errs);bad++;}
 if(r.me!=='桐山'||!r.own.length)bad++;await p.close();}
await b.close();console.log(bad?'NG '+bad:'all ok');})();
