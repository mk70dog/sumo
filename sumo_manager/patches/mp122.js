<script>
/* v122:二人相撲 第 3 段階=通信が切れたときの扱い(見本 cn1)。
   ①つながり具合を帯の左の札に(つながっています/つながりにくい/切れています/鍵が使えません/回数の上限/合言葉が見つかりません/相手の iPad が開いていない)。
     うまくいかないときは帯のすぐ下に細い帯でわけと「今すぐやり直す」「⚙ 設定を開く」。
   ②失敗が続くと読みにいく間隔をのばす(5→15→30→60 秒)。電波が戻ったとき・アプリの画面に戻ったときはすぐ読む。
   ③1 分ごとに「いる印」(hb_h.json・hb_g.json)を書き、相手から 5 分以上届かなければ知らせる。
   ④親:相手を待つ時間(5・10・30 分・待たない、G.mp.wait)と「待たずに進める」(G.mp.go)。
   ⑤子:切れている間に決めた稽古・作戦などは、新しい週の世界が届いたらもう一度当てる。当てられないもの(お金を使うことなど)は知らせる。 */
Object.assign(MP,{fail:0,failSince:0,ek:'',to:null,on:0,hbAt:0,peerHb:0,kind:''});
const MPX_RK={menu:1,it:1,pm:1,wplan:1,injPol:1,sh:1,tac:1};
const MPX_PK={dekH:1,kDays:1,meal:1,coAs:1,kpol:1,meSel:1,rengoOff:1};
function mpErrKind(e){const m=String(e&&e.message||e||'');const c=(m.match(/\((\d{3})\)/)||[])[1];
 if(typeof navigator!=='undefined'&&navigator.onLine===false)return 'off';
 if(/Failed to fetch|NetworkError|Load failed|network/i.test(m))return 'off';
 if(c==='401')return 'key';if(c==='403'||c==='429')return 'limit';if(c==='404'||/合言葉が見つかりません/.test(m))return 'nf';return 'slow';}
function mpIvNow(){const f=MP.fail;const k=f<=0?1:f===1?3:f===2?6:12;return MP.iv*k;}
function mpSched(){if(MP.to)clearTimeout(MP.to);MP.to=null;if(MP.on)MP.to=setTimeout(mpTick,mpIvNow());}
mpStop=function(){MP.on=0;if(MP.to)clearTimeout(MP.to);MP.to=null;if(MP.timer)clearInterval(MP.timer);MP.timer=null;};
mpStart=function(){mpStop();MP.on=1;MP.fail=0;MP.failSince=0;mpTick();};
function mpRetry(){if(!MP.on)return;MP.fail=Math.min(MP.fail,1);mpTick();}
/* いる印(1 分ごと)。親は hb_h.json、子は hb_g.json */
async function mpHb(){const now=Date.now();if(now-MP.hbAt<60000)return;let id=null,f=null;
 if(UI.mpGuest&&MPG.id&&MPG.gh>0){id=MPG.id;f='hb_g.json';}else if(G&&G.mp&&G.mp.role==='host'&&G.mp.id){id=G.mp.id;f='hb_h.json';}
 if(!id)return;MP.hbAt=now;const o={};o[f]=JSON.stringify({ts:now});await MPT.write(id,o);}
/* 相手のいる印を読む(本物の Gist は read で全部のファイルが来る。テスト用の受け渡しは読むファイルを足す) */
if(MPT.mock){const r0=MPT.read.bind(MPT);MPT.read=async function(id){const o=await r0(id);['hb_h.json','hb_g.json'].forEach(k=>{const v=localStorage.getItem('mpmock_'+id+'_'+k);if(v!=null)o[k]=v;});return o;};}
{const r1=MPT.read.bind(MPT);MPT.read=async function(id){const o=await r1(id);const k=UI.mpGuest?'hb_h.json':'hb_g.json';const v=mpJ(o[k]);MP.peerHb=v&&v.ts||0;return o;};}
const mpTk0=mpTick;
mpTick=async function(){if(MP.busy)return;if(!(UI.mpGuest&&MPG.id)&&!(G&&G.mp&&G.mp.role==='host')){mpSched();return;}
 MP.busy=1;let ok=false;const k0=mpConn().k;
 try{if(UI.mpGuest&&MPG.id)await mpGuestTick();else await mpHostTick();ok=true;MP.err='';try{await mpHb();}catch(e){}}
 catch(e){MP.err=String(e&&e.message||e);MP.ek=mpErrKind(e);}
 finally{MP.busy=0;}
 if(ok){MP.fail=0;MP.failSince=0;MP.ek='';}else{MP.fail++;if(!MP.failSince)MP.failSince=Date.now();}
 mpSched();if(mpConn().k!==k0&&!UI.mpDk&&!UI.title){try{render();}catch(e){}}};
if(typeof window!=='undefined'){window.addEventListener('online',()=>{if(MP.on){MP.fail=Math.min(MP.fail,1);mpTick();}});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&MP.on)mpTick();});}
/* 今のつながり具合 */
function mpAgo(t){const s=Math.max(0,Math.round((Date.now()-t)/1000));return s<60?s+' 秒':Math.floor(s/60)+' 分';}
function mpConn(){const C=(k,c,t,d,b)=>({k:k,c:c,t:t,d:d,b:b||''});
 const retry='<button class="btn sm" onclick="mpRetry()">今すぐやり直す</button>';
 if(MP.fail>0){const since=MP.failSince?'('+mpAgo(MP.failSince)+'前から)':'';
  if(MP.ek==='off')return C('off','#f66','切れています'+since,'ネットにつながっていません。電波が戻ると、すぐに受け取り直します。'+(MP.fail>2?' いまは '+Math.round(mpIvNow()/1000)+' 秒ごとにやり直しています。':''),retry);
  if(MP.ek==='key')return C('key','#f66','GitHub の鍵が使えません','鍵の期限が切れたか、消されたようです。⚙ 設定で鍵を入れ直してください。','<button class="btn sm" onclick="UI.view=\'sys\';render()">⚙ 設定を開く</button>');
  if(MP.ek==='nf')return C('nf','#f66','合言葉が見つかりません','受け渡しの場所(Gist)が消されたか、合言葉がちがうようです。親の iPad の合言葉を確かめてください。','');
  if(MP.ek==='limit')return C('limit','#fc4','回数の上限です'+since,'GitHub に短い間にたくさん読みにいったため、少し待っています。'+Math.round(mpIvNow()/1000)+' 秒ごとにやり直します。',retry);
  if(MP.fail>=2)return C('slow','#fc4','つながりにくい'+since,'受け取りに '+MP.fail+' 回続けて失敗しました。'+Math.round(mpIvNow()/1000)+' 秒ごとにやり直しています。',retry);}
 const who=UI.mpGuest?'親':'子';const gh=UI.mpGuest?MPG.gh:(G&&G.mp&&G.mp.gh);
 if(gh>0&&MP.peerHb&&Date.now()-MP.peerHb>5*60*1000)return C('away','#fc4',who+'の iPad が開いていないようです',who+'の iPad から '+mpAgo(MP.peerHb)+'なにも届いていません。'+who+'の iPad で二人相撲の画面を開いてもらってください。'+(UI.mpGuest?'':' 待つ時間がたつと、子の部屋は前の週と同じ設定のまま進みます。'),'');
 if(!MP.lastRx)return C('wait','#aaa','つないでいます…','','');
 return C('ok','#5c5','つながっています','','');}
const mpBar122=mpBar;mpBar=function(){let h=mpBar122();const x=mpConn();
 h=h.replace(/<span class="mperr">[\s\S]*?<\/span>/,'');
 h=h.replace('<div class="mpb"><b>二人相撲</b>','<div class="mpb"><span class="cnst" style="border-color:'+x.c+'"><span class="cd" style="background:'+x.c+'"></span>'+esc(x.t)+'</span><b>二人相撲</b>');
 if(x.d){const i=h.indexOf('</div>');if(i>=0)h=h.slice(0,i+6)+'<div class="cnx" style="border-left-color:'+x.c+'">'+esc(x.d)+(x.b?' '+x.b:'')+'</div>'+h.slice(i+6);}
 return h;};
/* 親:相手を待つ時間・待たずに進める */
function mpWaitMs(){const w=G&&G.mp&&G.mp.wait;if(w===0)return Infinity;return (w||10)*60*1000;}
function mpSetWait(w){G.mp.wait=w;save();render();}
function mpGoNow(){const m=G.mp;if(!m.hReady||!m.act)return;m.go=1;save();mpTick();}
const mpCard122=mpCard;mpCard=function(){let h=mpCard122();const m=G&&G.mp;if(UI.mpGuest||!m||!m.id||!(m.gh>0))return h;
 const g=MP.peer||{};const gr=g.n===m.n&&g.ready;const w=m.wait==null?10:m.wait;
 let rest='';if(m.hReady&&!gr){if(w===0)rest='子の準備ができるまで待ちます';else{const r=Math.max(0,(m.since||Date.now())+w*60000-Date.now());rest='あと '+Math.floor(r/60000)+' 分 '+Math.floor(r%60000/1000)+' 秒で、子の部屋は前の週と同じ設定のまま進みます';}}
 const row='<div class="cnrow"><b>相手を待つ時間</b>'+[[5,'5 分'],[10,'10 分'],[30,'30 分'],[0,'待たない']].map(([v,t])=>'<button class="pc'+(w===v?' on':'')+'" onclick="mpSetWait('+v+')">'+(w===v?'✓ ':'')+t+'</button>').join('')+(rest?'<span class="mute">'+rest+'</span>':'')+'</div>'+
  (m.hReady&&!gr?'<div class="btns"><button class="btn main" onclick="mpGoNow()">待たずに進める</button></div>':'');
 const i=h.lastIndexOf('</div>');return i<0?h+row:h.slice(0,i)+row+h.slice(i);};
/* 子:切れている間の変更を守る */
const mpGS122=mpGuestSend;mpGuestSend=async function(){let s=null;try{if(mpIsP()&&MPX.base)s=JSON.stringify(mpDiff(MPX.base,mpCanon(),[],[]));}catch(e){}
 await mpGS122.apply(this,arguments);if(s!=null)MPX.okOps=s;};
const mpGL122=mpGLoad;mpGLoad=function(w){let keep=null;
 try{if(UI.mpGuest&&mpIsP()&&MPX.base&&w&&w.n>MPG.n){const ops=mpDiff(MPX.base,mpCanon(),[],[]);if(ops.length&&JSON.stringify(ops)!==MPX.okOps)keep=ops;}}catch(e){}
 mpGL122(w);if(!keep||!mpIsP())return;
 const gh=MPG.gh,gi=pI(gh);let ok=0,ng=0;
 keep.forEach(op=>{const p=op[1];try{
  if(op[0]==='s'&&p[0]==='R'&&p.length>=3&&MPX_RK[p[2]]){const r=G.R[p[1]];if(r&&r.h===gh&&!r.ret){let o=r;for(let i=2;i<p.length-1;i++){if(o[p[i]]==null||typeof o[p[i]]!=='object')o[p[i]]={};o=o[p[i]];}o[p[p.length-1]]=op[2];ok++;return;}}
  if(op[0]==='s'&&p[0]==='P'&&+p[1]===gi&&p.length>=3&&MPX_PK[p[2]]){let o=G;for(let i=2;i<p.length-1;i++){if(o[p[i]]==null||typeof o[p[i]]!=='object')o[p[i]]={};o=o[p[i]];}o[p[p.length-1]]=op[2];ok++;return;}
  if(p[0]==='B'&&p[1]==='tac'){ng++;return;}
  if(p[0]==='R'||String(p[2]||'').charAt(0)==='_')return;/* 力士の画面の控えなど、決めたことではないもの */
  ng++;}catch(e){ng++;}});
 MPX.lost={ok:ok,ng:ng};
 setTimeout(()=>{try{alertM('つながっていない間に決めたこと','つながっていない間に、親の iPad が週を進めました。'+(ok?'稽古・接し方・出稽古先など '+ok+' 件は、新しい週にもう一度当てました(親へ送り直します)。':'')+(ng?'お金を使うこと・新弟子の勧誘・作戦など '+ng+' 件は間に合いませんでした。もう一度決めてください。':''));}catch(e){}},50);};
</script>
<style id="mp122">.mpb .cnst{display:inline-flex;align-items:center;gap:6px;border:2px solid;border-radius:14px;padding:1px 10px;font-weight:bold;background:#0006}.mpb .cnst .cd{width:10px;height:10px;border-radius:50%}
.cnx{background:#2b2116;color:#f3e7c9;border-left:6px solid;padding:6px 12px;font:13px sans-serif;position:relative;z-index:59}.cnx .btn{margin-left:8px}
.cnrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 8px;font:14px sans-serif}.cnrow .pc{font-size:15px;padding:6px 14px;border-radius:18px;border:2px solid #8a7040;background:#fff;color:#1a140c;width:auto}.cnrow .pc.on{background:#7a1d10;border-color:#7a1d10;color:#fff;font-weight:bold}.cnrow .mute{font-size:12px}</style>
