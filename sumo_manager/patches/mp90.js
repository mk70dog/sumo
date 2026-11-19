<script>
/* v90:二人相撲 第 2 段階。子の iPad も一人用と同じ画面で遊ぶ(部屋・稽古・経営・スタッフ・出来事・記録)。
   子が参加したら親が addPlayer(子の部屋)。子は受け取った世界で自分のプレイヤーに切りかえ(pUse)、ふだんの画面を使う。
   進めるボタンは「準備できた」になる。子の操作は「差分」(受け取った世界とくらべて変わったところ)にして親へ送り、親が当ててから進める。 */
const MPX={base:null,sent:'',idMin:5e6};
/* テスト用(#mpmock)の受け渡しは、ファイルごとに分けて置く(2 つのページが同時に書いても消し合わないように。本物の Gist も、書いたファイルだけが変わる) */
if(MPT.mock){MPT.create=async function(files){const id='m'+Math.random().toString(36).slice(2,10);localStorage.setItem('mpmock_'+id,'{}');await this.write(id,files);return id;};
 MPT.read=async function(id){if(localStorage.getItem('mpmock_'+id)==null)throw new Error('合言葉が見つかりません');const o={};['world.txt','host.json','guest.json'].forEach(k=>{const v=localStorage.getItem('mpmock_'+id+'_'+k);if(v!=null)o[k]=v;});return o;};
 MPT.write=async function(id,files){for(const k in files)localStorage.setItem('mpmock_'+id+'_'+k,files[k]);};}
const MP_BLK={mp:1,nid:1,sid:1,PA:1,phase:1,bnum:1,wk:1,wn:1,v:1,order:1,last:1,lastB:1,lastRec:1,hs:1,yusho:1};
/* 比べやすい形:プレイヤーのデータを全部 G.P に入れ、比べないもの(親の設定・番号の数え・'_' で始まる一時の値)を外す */
function mpCanon(){const o=JSON.parse(saveStr());if(o.P){const a=o.PA||0;PKEYS.forEach(k=>{if(k in o){o.P[a][k]=o[k];delete o[k];}});}
 for(const k in MP_BLK)if(k!=='B')delete o[k];if(o.B)o.B={tac:o.B.tac||{}};return o;}
const mpEq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function mpDiff(a,b,p,ops){if(a===b)return ops;
 const oa=a!==null&&typeof a==='object',ob=b!==null&&typeof b==='object';
 if(!oa||!ob||Array.isArray(a)!==Array.isArray(b)){if(b===undefined)ops.push(['d',p]);else ops.push(['s',p,b]);return ops;}
 if(Array.isArray(a)){
  if(a.length===b.length){for(let i=0;i<a.length;i++)mpDiff(a[i],b[i],p.concat(i),ops);return ops;}
  if(b.length>a.length){const n=b.length-a.length;
   if(mpEq(a,b.slice(0,a.length))){ops.push(['a',p,b.slice(a.length)]);return ops;}
   if(mpEq(a,b.slice(n))){ops.push(['u',p,b.slice(0,n)]);return ops;}}
  ops.push(['s',p,b]);return ops;}
 for(const k in a)if(!(k in b))ops.push(['d',p.concat(k)]);
 for(const k in b){if(!(k in a))ops.push(['s',p.concat(k),b[k]]);else mpDiff(a[k],b[k],p.concat(k),ops);}
 return ops;}
/* 親:差分を当てる(G.P の受け持ち中のプレイヤーは G の上にいる) */
function mpPut(ops){let n=0;(ops||[]).forEach(op=>{try{const p=op[1];if(!p.length||MP_BLK[p[0]]&&!(p[0]==='B'&&p[1]==='tac'))return;
  let o=G,i=0;if(p[0]==='P'){const k=+p[1];if(!G.P||!G.P[k]||p.length<3)return;o=k===(G.PA||0)?G:G.P[k];i=2;}
  if(p[0]==='B'&&!G.B)return;
  for(;i<p.length-1;i++){if(o[p[i]]==null||typeof o[p[i]]!=='object')o[p[i]]=(typeof p[i+1]==='number')?[]:{};o=o[p[i]];}
  const k=p[p.length-1];
  if(op[0]==='s')o[k]=op[2];else if(op[0]==='d'){if(Array.isArray(o))o.splice(k,1);else delete o[k];}
  else if(op[0]==='a')o[k]=(Array.isArray(o[k])?o[k]:[]).concat(op[2]);
  else if(op[0]==='u')o[k]=op[2].concat(Array.isArray(o[k])?o[k]:[]);
  n++;}catch(e){sysLog&&sysLog('二人相撲の差分',e);}});return n;}
/* 子:自分で作る力士・スタッフの番号は 5,000,000 から(親の番号とぶつからないように) */
function mpIdRange(){let r=MPX.idMin,s=MPX.idMin;for(const id in G.R)if(+id>=r)r=+id+1;
 const st=[].concat(G.staff||[],G.market||[]);(G.P||[]).forEach(p=>{st.push(...(p.staff||[]),...(p.market||[]));});st.forEach(x=>{if(x&&x.sid>=s)s=x.sid+1;});G.nid=r;G.sid=s;}
/* --- 親 --- */
function mpGI(){return G&&G.mp&&G.mp.gh>0&&G.P?pI(G.mp.gh):-1;}
function mpUp(){const m=G&&G.mp;if(m&&m.role==='host'&&m.gh>0&&!(G.P&&pI(m.gh)>=0)){addPlayer(m.gh);save();}}
async function mpHostTick(){const m=G.mp;if(!m.id)return;mpUp();const f=await MPT.read(m.id);const g=mpJ(f['guest.json']);MP.peer=g;MP.lastRx=Date.now();
 if(m.gh<0&&g.gh>0&&G.heya[g.gh]&&!G.heya[g.gh].closed){m.gh=g.gh;m.gname=G.heya[g.gh].n;addPlayer(g.gh);m.n++;addNews('〔二人相撲〕'+mpHeyaN(g.gh)+'が参加しました。');save();await mpWriteWorld();render();return;}
 if(!m.hReady||!m.act)return;
 const late=Date.now()-(m.since||Date.now())>10*60*1000;const ok=g.n===m.n&&g.ready;
 if(ok||late){
  if(g.n===m.n&&g.d){const ops=mpJ(await mpDec(g.d));mpPut(ops.o);}
  if(late&&!ok)addNews('〔二人相撲〕'+mpHeyaN(m.gh)+'の準備が 10 分間なかったので、そのまま進めました。');
  if(G.phase==='post')inP(m.gh,()=>{let k=0;while(G.ev.length&&k++<40)resolveEv(G.ev[0].id,G.ev[0].k==='shokei'?0:0);});
  const k=m.act;m.act=null;m.hReady=0;m.n++;try{MP_ORIG[k]();}catch(e){MP.err=String(e.message||e);try{sysLog('二人相撲で進めるとき',e);}catch(x){}}finally{save();await mpWriteWorld();}render();}}
/* --- 子 --- */
function mpGLoad(w){G=migrate(JSON.parse(w.s));applyMode(!!G.real);MPG.n=w.n;MPG.ready=0;MPG.act=null;MPX.base=null;MPX.sent='';
 const i=G.P?pI(MPG.gh):-1;if(i>=0){pUse(i);mpIdRange();MPX.base=mpCanon();}}
function mpIsP(){return !!(UI.mpGuest&&G&&G.P&&MPG.gh>0&&pI(MPG.gh)===(G.PA||0));}
async function mpJoin(id0){const id=(id0||($('#mp_code')?$('#mp_code').value:'')||'').trim();if(!mpTok()&&!MPT.mock){alertM('鍵がありません','⚙ 設定で GitHub の鍵を読み込んでください。');return;}
 try{const f=await MPT.read(id);const w=mpJ(await mpDec(f['world.txt']));if(!w.s)throw new Error('世界のデータがありません');
  MPG.id=id;MPG.host=mpJ(f['host.json']);const old=mpJ(f['guest.json']);MPG.gh=old.gh>0?old.gh:-1;mpGLoad(w);
  UI.mpGuest=1;UI.title=false;UI.start=null;UI.view='home';mpSaveGuest();render();mpStart();}
 catch(e){alertM('参加できませんでした',String(e.message||e));}}
async function mpGuestSend(){let d='';if(mpIsP()&&MPX.base){const ops=mpDiff(MPX.base,mpCanon(),[],[]);d=ops.length?await mpEnc(JSON.stringify({o:ops})):'';}
 MPX.sent=d+'|'+MPG.ready;
 await MPT.write(MPG.id,{'guest.json':JSON.stringify({gh:MPG.gh,n:MPG.n,ready:MPG.ready,act:MPG.act||'',d:d,ts:Date.now()})});}
async function mpGuestReady(v,k){if(v&&G.phase==='post'&&G.ev.length){alertM('まだ決めていないことがあります','場所後の出来事に返事をしてから「準備できた」にしてください。');return;}
 MPG.ready=v?1:0;MPG.act=v?(k||'doWeekUI'):null;mpSaveGuest();render();try{await mpGuestSend();}catch(e){MP.err=String(e.message||e);render();}}
async function mpGuestTick(){const f=await MPT.read(MPG.id);MP.lastRx=Date.now();MPG.host=mpJ(f['host.json']);const hn=MPG.host.n;
 if(hn>MPG.n||(MPG.gh>0&&!mpIsP())){const w=mpJ(await mpDec(f['world.txt']));if(w.s&&(w.n>MPG.n||!mpIsP())){mpGLoad(w);mpSaveGuest();render();return;}}
 // 変えたところは、準備の前でも送っておく(親が 10 分待って進めるときに使う)
 if(mpIsP()&&MPX.base){const ops=mpDiff(MPX.base,mpCanon(),[],[]);const d=ops.length?JSON.stringify(ops).length:0;const key=d+':'+ops.length+'|'+MPG.ready;if(key!==MPX.sentK){MPX.sentK=key;await mpGuestSend();}}
 render();}
async function mpPick(i){MPG.gh=i;mpSaveGuest();try{await MPT.write(MPG.id,{'guest.json':JSON.stringify({gh:i,n:MPG.n,ready:0,ts:Date.now()})});}catch(e){MP.err=String(e.message||e);}render();}
/* 進めるボタン:子は「準備できた」に、親は今までどおり(相手がいれば準備できた) */
Object.keys(MP_ACT).forEach(k=>{const f0=window[k];window[k]=function(){if(UI.mpGuest)return mpIsP()?mpGuestReady(1,k):undefined;return f0.apply(this,arguments);};});
/* 画面:子もふだんの画面+上の帯+今週のようす。進めるボタンは準備できたら「準備できた(取り消す)」 */
function mpMine(){if(UI.mpGuest)return {r:MPG.ready,k:MPG.act,cancel:'mpGuestReady(0)'};const m=G.mp;return {r:m.hReady,k:m.act,cancel:'mpCancel()'};}
function mpCard(){const host=!UI.mpGuest;const m=G.mp;if(host&&(!m.id||m.gh<0))return mpCardHost();
 const g=MP.peer||{};const hr=host?m.hReady:(MPG.host&&MPG.host.ready&&MPG.host.n===MPG.n);const gr=host?(g.n===m.n&&g.ready):MPG.ready;
 const gh=host?m.gh:MPG.gh;const pane=(h,lab,rd,act)=>{const L=Object.values(G.R).filter(r=>r.h===h&&!r.ret);const sek=L.filter(r=>r.d<=1).length;const mon=pv(h,'money');
  return '<div class="mpp"><b>'+esc(mpHeyaN(h))+'('+lab+')</b><br>関取 '+sek+' 人・弟子 '+L.length+' 人'+(mon!=null?'・資金 '+man(mon):'')+'<br>'+(rd?'<span class="ok2">● 準備できた'+(act&&MP_ACT[act]?'('+esc(MP_ACT[act])+')':'')+'</span>':'<span class="wt2">● 決めています…</span>')+'</div>';};
 const mine=mpMine();
 return '<div class="mpc"><h3>今週のようす</h3><div class="mpg">'+pane(0,'親',hr,host?m.act:(MPG.host&&MPG.host.act))+pane(gh,'子',gr,host?g.act:MPG.act)+'</div>'+
  '<p class="kaku" style="font-size:13px">進めるボタン(1 週間を過ごす・次の日を取る など)を押すと「準備できた」になり、ふたりとも準備できたら親の iPad が進めます。どちらの部屋も、ひとりで遊ぶときと同じように稽古・経営・スタッフ・出来事を決められます。10 分たつと、そのときの設定のまま進みます。</p>'+
  (mine.r?'<button class="btn" onclick="'+mine.cancel+'">準備を取り消す</button>':'')+'</div>';}
function mpBtns(app){const mine=mpMine();if(!mine.r)return;
 app.querySelectorAll('button[onclick]').forEach(b=>{const k=(b.getAttribute('onclick')||'').replace(/\(.*$/,'');if(!MP_ACT[k])return;
  if(k===mine.k){b.textContent='✓ 準備できた(取り消す)';b.setAttribute('onclick',mine.cancel);b.classList.add('mprd');}else b.disabled=true;});}
const mpR1=render0;
render0=function(){
 if(UI.mpGuest&&!UI.title){if(!mpIsP()){document.body.classList.remove('st-top');$('#app').innerHTML=mpGuestHTML();return;}
  mpR0();const app=$('#app');app.insertAdjacentHTML('afterbegin',mpBar());
  if(UI.view==='home'){const p=app.querySelector(':scope > .oc')||app.querySelector(':scope > .pn');if(p)p.insertAdjacentHTML('afterend',mpCard());}
  mpBtns(app);return;}
 if(G&&G.mp&&G.mp.role==='host'&&!UI.title){mpR0();const app=$('#app');app.insertAdjacentHTML('afterbegin',mpBar());
  if(UI.view==='home'){const p=app.querySelector(':scope > .oc')||app.querySelector(':scope > .pn');if(p)p.insertAdjacentHTML('afterend',mpCard());}
  mpBtns(app);return;}
 mpR1();};
/* 子の部屋選び:まだプレイヤーでない部屋だけ */
const mpGH0=mpGuestHTML;mpGuestHTML=function(){if(MPG.gh>0&&!mpIsP())return mpBar()+'<div class="pn"><h2>'+esc(mpHeyaN(MPG.gh))+'<span class="sub">親の iPad が受け付けるのを待っています…</span></h2><p class="kaku">親の iPad で二人相撲の画面が開いていれば、数秒で始まります。</p></div>';return mpGH0();};
/* 親の続きから:前の版(第 1 段階)で参加していた子の部屋は、プレイヤーの部屋にする */
const mpHC0=mpHostCont;mpHostCont=function(){mpHC0();mpUp();};
</script>
<style>.btn.mprd{background:#2e7d4f!important;color:#fff!important;border-color:#2e7d4f!important}.mpc .mpp{line-height:1.6}</style>
