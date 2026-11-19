<script>
/* v80:二人相撲(第 1 段階)。親の iPad が計算し、GitHub の Gist で受け渡す。子は稽古・作戦・勧誘を決める */
const MP={iv:/mpmock/.test(location.hash)?600:5000,timer:null,err:'',lastRx:0,peer:null,busy:0};
function mpTok(){try{return localStorage.getItem('gsmTok')||'';}catch(e){return '';}}
/* --- 受け渡し(Gist。テスト用に #mpmock では localStorage) --- */
const MPT={
 mock:/mpmock/.test(location.hash),
 async create(files){if(this.mock){const id='m'+Math.random().toString(36).slice(2,10);localStorage.setItem('mpmock_'+id,JSON.stringify(files));return id;}
  const r=await fetch('https://api.github.com/gists',{method:'POST',headers:this.h(),body:JSON.stringify({description:'Grand Sumo Manager 二人相撲',public:false,files:this.wrap(files)})});
  if(!r.ok)throw new Error('作成できませんでした('+r.status+')');return (await r.json()).id;},
 async read(id){if(this.mock){const s=localStorage.getItem('mpmock_'+id);if(!s)throw new Error('合言葉が見つかりません');return JSON.parse(s);}
  const r=await fetch('https://api.github.com/gists/'+id+'?t='+Date.now(),{headers:this.h(),cache:'no-store'});
  if(r.status===404)throw new Error('合言葉が見つかりません');if(!r.ok)throw new Error('読めませんでした('+r.status+')');
  const j=await r.json(),out={};for(const k in j.files){const f=j.files[k];out[k]=f.truncated?await (await fetch(f.raw_url,{cache:'no-store'})).text():f.content;}return out;},
 async write(id,files){if(this.mock){const o=JSON.parse(localStorage.getItem('mpmock_'+id)||'{}');Object.assign(o,files);localStorage.setItem('mpmock_'+id,JSON.stringify(o));return;}
  const r=await fetch('https://api.github.com/gists/'+id,{method:'PATCH',headers:this.h(),body:JSON.stringify({files:this.wrap(files)})});if(!r.ok)throw new Error('書けませんでした('+r.status+')');},
 h(){return {Authorization:'Bearer '+mpTok(),Accept:'application/vnd.github+json','Content-Type':'application/json'};},
 wrap(f){const o={};for(const k in f)o[k]={content:f[k]};return o;}};
/* 世界のデータは圧縮して送る(1 ファイル 1MB までのため) */
async function mpEnc(str){if(typeof CompressionStream==='undefined')return 'js:'+str;
 const cs=new Blob([str]).stream().pipeThrough(new CompressionStream('gzip'));const b=new Uint8Array(await new Response(cs).arrayBuffer());
 let s='';for(let i=0;i<b.length;i+=8192)s+=String.fromCharCode.apply(null,b.subarray(i,i+8192));return 'gz:'+btoa(s);}
async function mpDec(t){if(!t)return null;if(t.startsWith('js:'))return t.slice(3);
 const bin=atob(t.slice(3)),b=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)b[i]=bin.charCodeAt(i);
 return await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text();}
const mpJ=s=>{try{return JSON.parse(s||'{}');}catch(e){return {};}};
function mpHeyaN(i){return G&&G.heya[i]?G.heya[i].n+'部屋':'?';}
function mpTime(t){if(!t)return '—';const d=new Date(t);return ('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2)+':'+('0'+d.getSeconds()).slice(-2);}
/* --- 親 --- */
async function mpWriteWorld(){const m=G.mp;const w=JSON.stringify({n:m.n,ts:Date.now(),s:saveStr()});
 await MPT.write(m.id,{'world.txt':await mpEnc(w),'host.json':JSON.stringify({n:m.n,ready:m.hReady?1:0,act:m.act||'',gh:m.gh,ts:Date.now()})});}
async function mpHostInit(){const m=G.mp;MP.err='';
 try{const w=JSON.stringify({n:0,ts:Date.now(),s:saveStr()});m.id=await MPT.create({'world.txt':await mpEnc(w),'host.json':JSON.stringify({n:0,ready:0,gh:-1,ts:Date.now()}),'guest.json':JSON.stringify({gh:-1,n:-1})});save();}
 catch(e){MP.err=String(e.message||e);}render();mpStart();}
const MP_ACT={doWeekUI:'1 週間を過ごす',doToBasho:'初日まで進める',stepDay:'次の日を取る',stepAll:'千秋楽まで進める',doNext:'次の場所へ進む'};
const MP_ORIG={};
Object.keys(MP_ACT).forEach(k=>{MP_ORIG[k]=window[k];window[k]=function(){if(G&&G.mp&&G.mp.role==='host'&&G.mp.id&&G.mp.gh>=0)return mpHostReady(k);return MP_ORIG[k].apply(this,arguments);};});
function mpHostReady(k){if(k==='doNext'&&G.ev&&G.ev.length){return MP_ORIG.doNext();}
 const m=G.mp;m.act=k;m.hReady=1;m.since=Date.now();save();render();mpWriteWorld().catch(e=>{MP.err=String(e.message||e);render();});mpTick();}
function mpCancel(){const m=G.mp;m.act=null;m.hReady=0;save();render();mpWriteWorld().catch(()=>{});}
function mpApply(o){const gh=G.mp.gh;if(!o)return;
 for(const id in (o.m||{})){const r=G.R[id];if(r&&r.h===gh&&MENU[o.m[id][0]]){r.gm=o.m[id][0];r.gi=cl(+o.m[id][1]||1,0,3);}}
 for(const id in (o.t||{})){const r=G.R[id];if(r&&r.h===gh)r.tac={ta:TAN[o.t[id].ta]?o.t[id].ta:'任',kumi:KUN[o.t[id].kumi]?o.t[id].kumi:'任'};}
 (o.off||[]).forEach(cid=>{const p=G.pros.find(x=>x.cid===cid);if(!p||G.phase==='basho')return;
  if(p.r.fr&&Object.values(G.R).some(x=>x.h===gh&&!x.ret&&x.fr)){addNews(mpHeyaN(gh)+'は'+p.n+'を勧誘しましたが、外国出身の力士は 1 部屋 1 人までです。');return;}
  if(Math.random()<.55){const r=p.r;r.h=gh;r.n=shikona();r.tsuke=p.ama;r.join=G.bnum;if(p.sch&&!r.hs&&!r.uni){if(p.kind==='大学')r.uni=p.sch;else r.hs=p.sch;}G.R[r.id]=r;G.aiPend.push(r.id);G.pros=G.pros.filter(x=>x!==p);
   addNews('〔二人相撲〕'+p.n+'('+(p.sch||p.kind)+')は'+mpHeyaN(gh)+'への入門を決めました。四股名は「'+r.n+'」。');}
  else{p.int+=20;addNews('〔二人相撲〕'+mpHeyaN(gh)+'の勧誘は、'+p.n+'に断られました。');}});}
async function mpHostTick(){const m=G.mp;if(!m.id)return;const f=await MPT.read(m.id);const g=mpJ(f['guest.json']);MP.peer=g;MP.lastRx=Date.now();
 if(m.gh<0&&g.gh>0&&G.heya[g.gh]){m.gh=g.gh;m.gname=G.heya[g.gh].n;addNews('〔二人相撲〕'+mpHeyaN(g.gh)+'が参加しました。');save();await mpWriteWorld();render();return;}
 if(!m.hReady||!m.act)return;
 const late=Date.now()-(m.since||Date.now())>10*60*1000;
 if((g.n===m.n&&g.ready)||late){mpApply(g.n===m.n?g.o:null);if(late&&!(g.n===m.n&&g.ready))addNews('〔二人相撲〕'+mpHeyaN(m.gh)+'の準備が 10 分間なかったので、前の週と同じ設定で進めました。');
  const k=m.act;m.act=null;m.hReady=0;m.n++;MP_ORIG[k]();save();await mpWriteWorld();render();}}
/* --- 子 --- */
const MPG={id:null,gh:-1,n:-1,ready:0,o:{m:{},t:{},off:[]},host:null,view:'heya'};
async function mpJoin(id0){const id=(id0||($('#mp_code')?$('#mp_code').value:'')||'').trim();if(!mpTok()&&!MPT.mock){alertM('鍵がありません','先に GitHub の鍵を入れてください。');return;}
 try{const f=await MPT.read(id);const w=mpJ(await mpDec(f['world.txt']));if(!w.s)throw new Error('世界のデータがありません');
  G=migrate(JSON.parse(w.s));MPG.id=id;MPG.n=w.n;MPG.host=mpJ(f['host.json']);const old=mpJ(f['guest.json']);MPG.gh=old.gh>0?old.gh:-1;
  UI.mpGuest=1;UI.title=false;UI.start=null;mpSaveGuest();render();mpStart();}
 catch(e){alertM('参加できませんでした',String(e.message||e));}}
function mpSaveGuest(){try{localStorage.setItem('gsmGuest',JSON.stringify({id:MPG.id,gh:MPG.gh,o:MPG.o}));}catch(e){}}
async function mpGuestCont(){const s=mpJ(localStorage.getItem('gsmGuest'));if(!s.id)return;MPG.o=s.o||MPG.o;await mpJoin(s.id);}
async function mpPick(i){MPG.gh=i;mpSaveGuest();await mpGuestSend();render();}
async function mpGuestSend(){await MPT.write(MPG.id,{'guest.json':JSON.stringify({gh:MPG.gh,n:MPG.n,ready:MPG.ready,o:MPG.o,ts:Date.now()})});}
async function mpGuestReady(v){MPG.ready=v?1:0;mpSaveGuest();render();try{await mpGuestSend();}catch(e){MP.err=String(e.message||e);render();}}
async function mpGuestTick(){const f=await MPT.read(MPG.id);MP.lastRx=Date.now();MPG.host=mpJ(f['host.json']);const hn=MPG.host.n;
 if(hn>MPG.n){const w=mpJ(await mpDec(f['world.txt']));if(w.s&&w.n>MPG.n){G=migrate(JSON.parse(w.s));MPG.n=w.n;MPG.ready=0;MPG.o.off=[];MPG.o.t={};mpSaveGuest();}}
 render();}
function mpSet(kind,id,key,v){if(kind==='m'){const x=MPG.o.m[id]||[G.R[id].gm||'申',G.R[id].gi!=null?G.R[id].gi:1];x[key]=key===1?+v:v;MPG.o.m[id]=x;}
 else{const x=MPG.o.t[id]||Object.assign({ta:'任',kumi:'任'},G.R[id].tac||{});x[key]=v;MPG.o.t[id]=x;}MPG.ready=0;mpSaveGuest();render();}
function mpOff(cid,on){const L=MPG.o.off||[];MPG.o.off=on?L.concat([cid]):L.filter(x=>x!==cid);MPG.ready=0;mpSaveGuest();render();}
/* --- 進めかた --- */
async function mpTick(){if(MP.busy)return;MP.busy=1;try{if(UI.mpGuest&&MPG.id)await mpGuestTick();else if(G&&G.mp&&G.mp.role==='host')await mpHostTick();MP.err='';}catch(e){MP.err=String(e.message||e);}finally{MP.busy=0;}}
function mpStart(){mpStop();MP.timer=setInterval(mpTick,MP.iv);mpTick();}
function mpStop(){if(MP.timer)clearInterval(MP.timer);MP.timer=null;}
/* --- 画面 --- */
function mpBar(){let a,b,code;
 if(UI.mpGuest){const hr=MPG.host&&MPG.host.ready&&MPG.host.n===MPG.n;a=[mpHeyaN(0)+'(親)',hr?'ok':'wait',hr?'準備できた':'準備中…'];b=[mpHeyaN(MPG.gh)+'(子)',MPG.ready?'ok':'wait',MPG.ready?'準備できた':'準備中…'];code=MPG.id;}
 else{const m=G.mp;const g=MP.peer||{};const gr=g.n===m.n&&g.ready;a=[mpHeyaN(0)+'(親)',m.hReady?'ok':'wait',m.hReady?'準備できた':'準備中…'];b=m.gh>0?[mpHeyaN(m.gh)+'(子)',gr?'ok':'wait',gr?'準備できた':'準備中…']:['相手','wait','参加を待っています'];code=m.id||'作成中';}
 const pl=x=>'<span class="pl"><span class="dot '+x[1]+'"></span>'+esc(x[0])+' '+x[2]+'</span>';
 return '<div class="mpb"><b>二人相撲</b>'+pl(a)+pl(b)+(MP.err?'<span class="mperr">'+esc(MP.err)+'</span>':'')+'<span class="mpt">受け取り '+mpTime(MP.lastRx)+'</span></div>';}
function mpCardHost(){const m=G.mp;
 if(!m.id)return '<div class="mpc"><h3>二人相撲の準備</h3><p class="kaku">'+(MP.err?'<span class="shu">'+esc(MP.err)+'</span><br>':'')+'Gist を作っています…</p>'+(MP.err?'<button class="btn" onclick="mpHostInit()">もう一度</button>':'')+'</div>';
 if(m.gh<0)return '<div class="mpc"><h3>相手の参加を待っています</h3><p class="kaku">相手の iPad で「二人相撲」→「合言葉で参加する」を押し、この合言葉を入れてもらいます(LINE などで送ってください)。</p><div class="code" style="word-break:break-all">'+esc(m.id)+'</div><button class="btn sm" onclick="mpCopy()">合言葉をコピー</button><p class="mute kaku" style="font-size:12px">相手が参加するまでは、ひとりのときと同じように進められます。</p></div>';
 const g=MP.peer||{};const gr=g.n===m.n&&g.ready;const gh=m.gh;const L=Object.values(G.R).filter(r=>r.h===gh&&!r.ret);const sek=L.filter(r=>r.d<=1).length;
 const top=L.slice().sort((x,y)=>x.pos-y.pos)[0];const lh=top&&top.hist[top.hist.length-1];
 return '<div class="mpc"><h3>今週のようす</h3><div class="mpg"><div class="mpp"><b>'+esc(mpHeyaN(0))+'(親)</b><br>'+(m.hReady?'<span class="ok2">● 準備できた('+esc(MP_ACT[m.act]||'')+')</span>':'<span class="wt2">● 稽古を決めています…</span>')+'</div>'+
 '<div class="mpp"><b>'+esc(mpHeyaN(gh))+'(子)</b><br>関取 '+sek+' 人・弟子 '+L.length+' 人'+(lh?'<br>前の場所:'+esc(top.n)+' '+lh.w+'勝'+(lh.l+(lh.ab||0))+'敗':'')+'<br>'+(gr?'<span class="ok2">● 準備できた</span>':'<span class="wt2">● 稽古を決めています…</span>')+'</div></div>'+
 '<p class="kaku" style="font-size:13px">進めるボタン(1 週間を過ごす・次の日を取る など)を押すと「準備できた」になり、ふたりとも準備できたら進みます。10 分たつと、相手は前の週と同じ設定で進みます。</p>'+(m.hReady?'<button class="btn" onclick="mpCancel()">準備を取り消す</button>':'')+'</div>';}
function mpCopy(){try{navigator.clipboard.writeText(G.mp.id);toast('合言葉をコピーしました');}catch(e){}}
function mpGuestHTML(){if(!G)return '';
 if(MPG.gh<0){const L=G.heya.map((h,i)=>[h,i]).filter(([h,i])=>i>0&&G.order.some(id=>G.R[id].h===i));
  return mpBar()+'<div class="pn"><h2>受け持つ部屋を選ぶ<span class="sub">'+esc(mpHeyaN(0))+'(親)の世界に参加します</span></h2><div class="mpsel">'+L.map(([h,i])=>{const n=G.order.filter(id=>G.R[id].h===i).length,s=G.order.filter(id=>G.R[id].h===i&&G.R[id].d<=1).length;return '<button class="btn" onclick="mpPick('+i+')">'+esc(h.n)+'部屋<small>関取 '+s+'・弟子 '+n+'</small></button>';}).join('')+'</div></div>';}
 const tabs=[['heya','部屋'],['banzuke','番付'],['news','ニュース']];
 let h=mpBar()+'<div id="hdr"><div class="row"><div class="title">'+esc(mpHeyaN(MPG.gh))+'<small>二人相撲(子)</small></div><span class="cal">'+bname(G.bnum)+'・'+phaseText()+'</span><span class="hbtns"><button class="hbtn" onclick="quitTop()">終了(トップへ)</button></span></div></div>'+
  '<div id="nav">'+tabs.map(([k,n])=>'<button class="'+(MPG.view===k?'on':'')+'" onclick="MPG.view=\''+k+'\';render()">'+n+'</button>').join('')+'</div>';
 if(MPG.view==='banzuke'){UI.div=UI.div||0;return h+banzukeHTML();}
 if(MPG.view==='news')return h+'<div class="pn"><h2>ニュース</h2><div class="hl">'+(G.news||[]).slice(0,40).map(esc).join('<br>')+'</div></div>';
 const L=G.order.map(id=>G.R[id]).filter(r=>r&&r.h===MPG.gh&&!r.ret).sort((a,b)=>a.pos-b.pos);
 const MK=Object.keys(MENU);const B=G.phase==='basho'&&G.B;
 const opp=r=>{if(!B||!B.cur)return null;const p=B.cur.find(x=>x[0]===r.id||x[1]===r.id);return p?G.R[p[0]===r.id?p[1]:p[0]]:null;};
 h+='<div class="pn"><h2>'+(B?'作戦':'稽古')+'<span class="sub">決めたら「準備できた」</span></h2><div class="mpready">'+(MPG.ready?'<button class="btn" onclick="mpGuestReady(0)">準備を取り消す</button><span class="ok2">● 準備できた(親を待っています)</span>':'<button class="btn main" onclick="mpGuestReady(1)">準備できた</button>')+'</div>'+
  '<div style="overflow-x:auto"><table class="tb"><tr><th>番付</th><th>四股名</th><th>前の場所</th><th>'+(B?'今日の相手':'稽古')+'</th><th>'+(B?'立ち合い・組み手':'強さ')+'</th></tr>'+
  L.map(r=>{const lh=r.hist[r.hist.length-1];const om=MPG.o.m[r.id]||[r.gm||'申',r.gi!=null?r.gi:1];const ot=MPG.o.t[r.id]||Object.assign({ta:'任',kumi:'任'},r.tac||{});
   let c1,c2;if(B){const o=opp(r);c1=o?esc(o.n)+'<div class="mute" style="font-size:11px">'+esc(o.rkS||'')+'・'+styleName(o)+'</div>':'<span class="mute">—</span>';
    c2=o?'<select onchange="mpSet(\'t\','+r.id+',\'ta\',this.value)">'+Object.keys(TAN).map(k=>'<option value="'+k+'"'+(ot.ta===k?' selected':'')+'>'+TAN[k]+'</option>').join('')+'</select> <select onchange="mpSet(\'t\','+r.id+',\'kumi\',this.value)">'+Object.keys(KUN).map(k=>'<option value="'+k+'"'+(ot.kumi===k?' selected':'')+'>'+KUN[k]+'</option>').join('')+'</select>':'';}
   else{c1='<select onchange="mpSet(\'m\','+r.id+',0,this.value)">'+MK.map(k=>'<option value="'+k+'"'+(om[0]===k?' selected':'')+'>'+MENU[k].n+'</option>').join('')+'</select>';
    c2='<select onchange="mpSet(\'m\','+r.id+',1,this.value)">'+INT.map((x,i)=>'<option value="'+i+'"'+(+om[1]===i?' selected':'')+'>'+x.n+'</option>').join('')+'</select>';}
   return '<tr><td>'+esc(r.rkS||(r.t?'':'前相撲'))+'</td><td style="white-space:nowrap"><span class="nm">'+esc(r.n)+'</span><div class="mute" style="font-size:11px">'+Math.floor(r.age)+'歳・'+styleName(r)+(r.inj?'・<span class="shu">けが</span>':'')+'</div></td><td>'+(lh?lh.w+'勝'+(lh.l+(lh.ab||0))+'敗':'—')+'</td><td>'+c1+'</td><td>'+c2+'</td></tr>';}).join('')+'</table></div></div>';
 if(!B){const P=(G.pros||[]).slice(0,10);
  h+='<div class="pn"><h2>新弟子の候補<span class="sub">勧誘したい候補に印。親が週を進めるときに結果が出ます(断られることもあります)</span></h2>'+(P.length?'<div class="mpsel">'+P.map(p=>{const on=(MPG.o.off||[]).includes(p.cid);return '<label class="mpo2"><input type="checkbox"'+(on?' checked':'')+' onchange="mpOff(\''+p.cid+'\',this.checked)"> <b>'+esc(p.n)+'</b> '+esc(p.sch?schLabel(p.sch):p.kind)+'・'+p.age+'歳・'+Math.round(p.r.ht)+'cm・'+Math.round(p.r.w)+'kg'+(p.osp?'・'+esc(p.osp.s):'')+'</label>';}).join('')+'</div>':'<p class="mute kaku">今は候補がいません。</p>')+'</div>';}
 return h;}
/* 画面に差しこむ */
const mpR0=render0;
render0=function(){if(UI.mpGuest&&!UI.title){document.body.classList.remove('st-top');$('#app').innerHTML=mpGuestHTML();return;}
 mpR0();if(G&&G.mp&&G.mp.role==='host'&&!UI.title){const app=$('#app');app.insertAdjacentHTML('afterbegin',mpBar());if(UI.view==='home'){const p=app.querySelector(':scope > .oc')||app.querySelector(':scope > .pn');if(p)p.insertAdjacentHTML('afterend',mpCardHost());}}};
const mpQuit=quitTop;quitTop=function(){mpStop();if(UI.mpGuest){UI.mpGuest=0;G=load();UI.title=true;UI.mode=null;render();return;}mpQuit();};
const mpSave=save;save=function(){if(UI.mpGuest)return;if(G&&G.mp){try{localStorage.setItem('gsmMP',saveStr());}catch(e){}return;}mpSave();};
/* 親の始めかた:実在の部屋の選び方を使う */
const mpNGR=newGameReal;newGameReal=function(){mpNGR.apply(this,arguments);if(UI.mpNew){G.mp={role:'host',id:null,gh:-1,n:0,act:null,hReady:0};UI.mpNew=0;setTimeout(mpHostInit,0);}};
function mpNewHost(){if(!mpTok()&&!MPT.mock){alertM('鍵がありません','先に GitHub の鍵を入れてください。');return;}UI.mpNew=1;goStart('real');}
function mpHostCont(){const s=localStorage.getItem('gsmMP');if(!s)return;const g=migrate(JSON.parse(s));if(!g)return;G=g;applyMode(!!G.real);UI.title=false;UI.start=null;UI.view='home';render();mpStart();}
function mpSaveTok(){const v=($('#mp_tok').value||'').trim();try{localStorage.setItem('gsmTok',v);}catch(e){}toast(v?'鍵を保存しました':'鍵を消しました');render();}
/* スタート画面の二人相撲 */
const mpTop=topHTML;topHTML=function(){let h=mpTop();if(UI.mode!=='two')return h;
 const hasH=!!localStorage.getItem('gsmMP'),gs=mpJ(localStorage.getItem('gsmGuest'));
 const body='<button class="st-cont st-back2" onclick="topMode(null)"><b>← 一人相撲・二人相撲を選び直す</b></button>'+
  (hasH?'<button class="st-cont" onclick="mpHostCont()"><b>続きから(親)</b><small>前に親として始めた二人相撲</small></button>':'')+(gs.id?'<button class="st-cont" onclick="mpGuestCont()"><b>続きから(子)</b><small>前に参加した二人相撲</small></button>':'')+
  '<button class="st-real" onclick="mpNewHost()"><b>親になって新しく始める</b><small>実在の部屋を選んで世界を作ります。合言葉が出るので、相手に伝えます。</small></button>'+
  '<button class="st-dok" onclick="UI.mpJoin=1;render()"><b>合言葉で参加する</b><small>相手から聞いた合言葉を入れて、残りの部屋から選びます。</small></button>'+
  '<div class="mpkey">'+(UI.mpJoin?'<label>合言葉</label><input id="mp_code" placeholder="親の画面に出ている合言葉"><button class="btn main" onclick="mpJoin()">参加する</button><br>':'')+
  '<label>GitHub の鍵(gist だけ書ける鍵。この端末の中だけに保存。ふたりとも同じ鍵を使います)</label><input id="mp_tok" type="password" value="'+esc(mpTok())+'"><button class="btn" onclick="mpSaveTok()">鍵を保存</button></div>';
 return h.replace(/<div class="st-go">[\s\S]*?<\/div><div class="st-credit">/,'<div class="st-go st-go2">'+body+'</div><div class="st-credit">');};
</script>
<style id="mpCss">
.mpb{position:relative;z-index:60;display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:#1d2a3a;color:#fff;padding:6px 12px;font:13px sans-serif}
.mpb .pl{display:flex;align-items:center;gap:6px;background:#ffffff1a;border-radius:14px;padding:2px 10px}
.mpb .dot{width:10px;height:10px;border-radius:50%;background:#888}.mpb .dot.ok{background:#5c5}.mpb .dot.wait{background:#fc4;animation:mpbl 1s infinite}
@keyframes mpbl{50%{opacity:.3}}.mpb .mpt{margin-left:auto;opacity:.8}.mpb .mperr{color:#ffb4a8}
@media(max-width:600px){.mpb .mpt{display:none}.mpb{font-size:12px;padding:4px 8px}}
.mpc{border:2px solid var(--ai);border-radius:10px;padding:12px;margin:10px 0}.mpc h3{margin:0 0 8px}
.mpg{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:600px){.mpg{grid-template-columns:1fr}}
.mpp{border:1px solid var(--line);border-radius:8px;padding:8px}.mpp b{color:var(--ai)}
.ok2{color:#2e7d4f;font-weight:bold}.wt2{color:#b5651d;font-weight:bold}
.code{font:bold 16px monospace;background:#f1e8d4;color:#222;padding:6px 10px;border-radius:6px;margin:6px 0}
.mpsel{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}.mpsel .btn small{display:block;font-size:12px;opacity:.8}
.mpo2{display:block;border:1px solid var(--line);border-radius:6px;padding:6px 8px;font-size:13px}
.mpready{display:flex;align-items:center;gap:10px;margin:6px 0}
.st-go2{flex-wrap:wrap}.mpkey{flex:1 1 100%;background:rgba(20,16,10,.88);border:1px solid #c9a24a;border-radius:6px;padding:10px 14px;color:#f3e7c9;font:13px sans-serif}
.mpkey input{width:100%;max-width:420px;font-size:15px;padding:6px;margin:4px 0;border-radius:6px;border:1px solid #c9a24a}.mpkey label{display:block;margin-top:6px}
</style>
