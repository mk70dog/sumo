<script>
/* v98:二人相撲 子が「部屋付き親方として独立」して参加できる。
   子は受け取った世界(親の世界)の中で、独立できる親方と内弟子を選んで申し込む(guest.json の dk)。
   親が次に見たときに、世界へ新しい部屋を足して子のプレイヤーにする(host.json の gh)。
   条件が変わっていて足せないときは host.json の dkno で知らせる。新しい部屋の始め方は一人用の独立(newGameDok)と同じ(推定値)。 */
const MPDK_MON={'横綱':1500,'大関':1000,'関脇':500,'小結':500};
/* --- 子:選べる親方を、受け取った世界の今の状態で絞る --- */
function mpDkOn(){return !!(UI.mpGuest&&UI.mpDk);}
function mpDkRoom(x){if(!G||!G.toshi)return -1;const tt=G.toshi.find(t=>t.n===x.n&&!t.left&&!t.shi&&t.heya===x.par);if(!tt||ageOf(tt.b)>=64)return -1;
 const i=G.heya.findIndex(h=>h.n===x.par&&!h.closed);if(i<0||isPH(i))return -1;if(G.heya.some(h=>!h.closed&&h.n===x.n))return -1;return i;}
const mpDL0=dokList;dokList=function(){const L=mpDL0();return mpDkOn()?L.filter(x=>mpDkRoom(x)>=0):L;};
const mpDW0=dokWs;dokWs=function(x){if(!mpDkOn())return mpDW0(x);if(x._wg)return x._wg;const i=mpDkRoom(x);
 const here=new Set(G.order.map(id=>G.R[id]).filter(r=>r&&r.h===i&&!r.ret).map(r=>r.n));x._wg=mpDW0(x).filter(w=>here.has(w.n));return x._wg;};
const mpDS0=doStartDok;doStartDok=function(n){if(!mpDkOn())return mpDS0(n);
 const ws=[...document.querySelectorAll('.dkw input:checked')].map(e=>e.value);if(!ws.length)return;const x=dokList().find(y=>y.n===n);if(!x)return;
 const r=dokGo(x,ws);MPG.dk={en:n,ws:r.go,stay:r.stay,oyT:($('#r_t')||{}).value||'四',par:x.par};MPG.gh=-1;UI.mpDk=0;heyaClose();mpSaveGuest();
 mpGuestSend().catch(e=>{MP.err=String(e.message||e);});render();};
function mpDkCancel(){MPG.dk=null;mpSaveGuest();mpGuestSend().catch(()=>{});render();}
/* 子の保存・送信・続きから */
mpSaveGuest=function(){try{localStorage.setItem('gsmGuest',JSON.stringify({id:MPG.id,gh:MPG.gh,o:MPG.o,dk:MPG.dk||null}));}catch(e){}};
const mpGC0=mpGuestCont;mpGuestCont=async function(){const s=mpJ(localStorage.getItem('gsmGuest'));MPG.dk=s.dk||null;await mpGC0();};
const mpGS0=mpGuestSend;mpGuestSend=async function(){if(MPG.dk&&MPG.gh<0){await MPT.write(MPG.id,{'guest.json':JSON.stringify({gh:-1,n:MPG.n,ready:0,dk:MPG.dk,ts:Date.now()})});return;}return mpGS0();};
/* 子:親が部屋を足したら(host.json の gh)、世界を受け取って自分の部屋にする。断られたら(dkno)知らせる */
const mpGT0=mpGuestTick;mpGuestTick=async function(){
 if(UI.mpDk&&MPG.gh<0){const f=await MPT.read(MPG.id);MP.lastRx=Date.now();MPG.host=mpJ(f['host.json']);return;}/* 親方と内弟子を選んでいる間は、5 秒ごとの描きかえで窓が閉じないように */
 if(MPG.dk&&MPG.gh<0){const f=await MPT.read(MPG.id);MP.lastRx=Date.now();const hj=mpJ(f['host.json']);MPG.host=hj;
  if(hj.dkno){const t=hj.dkno;MPG.dk=null;mpSaveGuest();try{await MPT.write(MPG.id,{'guest.json':JSON.stringify({gh:-1,n:MPG.n,ready:0,ts:Date.now()})});}catch(e){}alertM('独立できませんでした',t);render();return;}
  if(hj.gh>0){const w=mpJ(await mpDec(f['world.txt']));if(w.s){MPG.gh=hj.gh;MPG.dk=null;mpGLoad(w);mpSaveGuest();try{await mpGuestSend();}catch(e){}}}
  render();return;}
 return mpGT0();};
/* 子の画面:部屋選びに「独立して興す」を足す/親方選び/申し込み中 */
const mpGH2=mpGuestHTML;mpGuestHTML=function(){
 if(MPG.dk&&MPG.gh<0)return mpBar()+'<div class="pn"><h2>独立の申し込み中<span class="sub">'+esc(MPG.dk.en)+'部屋</span></h2><p class="kaku">'+esc(MPG.dk.en)+'親方(元'+esc(MPG.dk.par)+'部屋の部屋付き親方)が、内弟子 '+MPG.dk.ws.length+' 人を連れて独立します。親の iPad が受け付けるのを待っています…</p><button class="btn" onclick="mpDkCancel()">申し込みを取り消す</button></div>';
 if(UI.mpDk&&MPG.gh<0){let h=dokHTML();h=h.replace('onclick="goStart(null)"','onclick="UI.mpDk=0;render()"').replace(/<div class="hswarn">[^<]*<\/div>/,'');return mpBar()+h;}
 let o=mpGH2();
 if(MPG.gh<0&&G&&o.slice(-12)==='</div></div>')o=o.slice(0,-6)+'<p class="kaku mute" style="font-size:13px;margin:10px 0 4px">または、今いる部屋付き親方が独立して、新しい部屋を興すこともできます。</p><button class="btn main" onclick="UI.mpDk=1;UI.dk=null;render()">独立して新しい部屋を興す</button></div>';
 return o;};
/* --- 親:世界へ新しい部屋を足して、子のプレイヤーにする --- */
function mpDokAdd(dk){
 const T=TOSHI.find(t=>t[0]===dk.en&&t[3]!==1);const tt=G.toshi&&G.toshi.find(t=>t.n===dk.en&&!t.left&&!t.shi);if(!T||!tt)return -1;
 const P=tt.heya;const i0=G.heya.findIndex(h=>h.n===P&&!h.closed);if(i0<0||isPH(i0)||ageOf(tt.b)>=64)return -1;
 if(G.heya.some(h=>!h.closed&&h.n===dk.en))return -1;
 const want=new Set(dk.ws||[]);let L=G.order.map(id=>G.R[id]).filter(r=>r&&r.h===i0&&!r.ret&&want.has(r.n));
 let fr=0;L=L.filter(r=>{if(!r.fr)return true;return ++fr<=1;});L=L.slice(0,8);if(!L.length)return -1;
 const src=G.heya[i0];
 const h={n:dk.en,o2:T[4],player:false,q:R(.98,1.1),hard:Math.random()<.3,ic:src.ic,oa:ageOf(tt.b),gen:1,ob:G.bnum,from:i0,loc:pick(LOCP),est:curYear(),hist:P+'部屋から独立して創設。'};
 G.heya.push(h);const k=G.heya.length-1;G.hs.tot[k]=0;G.hs.yr[k]=0;
 tt.heya=dk.en;tt.shi=1;if(G.myo&&G.myo[dk.en]){G.myo[dk.en].ic=h.ic;G.myo[dk.en].st='own';}
 L.forEach(r=>{r.h=k;});
 if(addPlayer(k)<0)return -1;
 const top=Object.keys(MPDK_MON).find(x=>T[5].indexOf(x)===0);const oyT=OYAB[dk.oyT]?dk.oyT:'四';
 h.oyT=oyT;h.oy=Object.assign({},OYAB[oyT]);{const b=top==='横綱'?1.5:top==='大関'?.8:0;for(const x in h.oy)h.oy[x]=Math.round(h.oy[x]+b);}
 h.o=dk.en+'(元・'+T[4]+')';
 inP(k,()=>{const o=own();const sek=o.filter(r=>r.d<=1).length;
  G.fac={keiko:1,iryo:1,shoku:1,shuku:2};G.capB=Math.max(0,o.length+3-(4+3*G.fac.shuku));G.bld={k:'rent'};
  G.money=1000+(top?MPDK_MON[top]:0);G.sup=(top==='横綱'?600:top==='大関'?400:top?200:100)+o.length*12+sek*60;G.supC=Math.round(2+o.length/3+sek*4);G.rep=cl(15+sek*5,0,90);
  G.supFee={i:2.1,c:20,t:''};G.dok={from:P,b:G.bnum};
  addNews(dk.en+'親方(元'+T[4]+')が'+P+'部屋から独立し、'+dk.en+'部屋を興しました。内弟子 '+o.length+' 人(関取 '+sek+' 人)、資金 '+man(G.money)+'(自己資金・推定)、建物は借りもの。');});
 if((dk.stay||[]).length)addNews(dk.stay.join('・')+'は、話し合いの末、元の'+P+'部屋に残ることになりました。');
 return k;}
const mpHT2=mpHostTick;mpHostTick=async function(){
 const m=G&&G.mp;
 if(m&&m.role==='host'&&m.id&&m.gh<0){const g=mpJ((await MPT.read(m.id))['guest.json']);
  if(g.dk&&g.dk.en){if(m.dkBad!==g.dk.en){MP.lastRx=Date.now();let k=-1;try{k=mpDokAdd(g.dk);}catch(e){try{sysLog('二人相撲の独立',e);}catch(x){}}
    if(k<0){m.dkBad=g.dk.en;m.dkno='その親方か内弟子の状況が変わって、独立を受け付けられませんでした(別の部屋になった、内弟子がいなくなった など)。もう一度選んでください。';save();await mpWriteWorld();return;}
    m.gh=k;m.gname=G.heya[k].n;m.dkBad=null;m.dkno='';m.n++;addNews('〔二人相撲〕'+mpHeyaN(k)+'が参加しました(独立して興した部屋)。');save();await mpWriteWorld();render();return;}}
  else if(m.dkBad){m.dkBad=null;m.dkno='';save();await mpWriteWorld();}}
 return mpHT2();};
/* host.json に、断った理由(dkno)も書く */
mpWriteWorld=async function(){const m=G.mp;const w=JSON.stringify({n:m.n,ts:Date.now(),s:saveStr()});
 await MPT.write(m.id,{'world.txt':await mpEnc(w),'host.json':JSON.stringify({n:m.n,ready:m.hReady?1:0,act:m.act||'',gh:m.gh,dkno:m.dkno||'',ts:Date.now()})});};
/* 二人相撲の画面(子):「合言葉で参加/子になる」の説明に独立も */
</script>
