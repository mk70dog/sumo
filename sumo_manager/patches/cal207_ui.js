/* v204 予定(カレンダー):年間(6 場所 × 6 週)と今場所まで(6 週)。本場所・巡業・連合稽古・稽古総見・番付発表・新弟子検査と、
   自分で入れる予定(稽古日数・休養の週・出稽古の週・研修・メモ)を一つの画面で管理する。
   日付:本場所の初日は奇数月の第 2 日曜日(2026 年は 1/11・3/8・5/10・7/12・9/13・11/8)。番付発表は初日の 13 日前の月曜日、
   新弟子検査は初日の 9〜10 日前(第 5 週)。稽古の第 1 週は初日の 6 週前の日曜日から(推定の割り当て)。 */
(function(){
const CALC={basho:['場','#8a2b1a'],tour:['巡','#3d7a4a'],rengo:['連','#2c5c8a'],soken:['総','#6a4a8a'],ban:['番','#6b6457'],ken:['検','#b06a1a'],
 kn:['研','#1f7a7a'],rest:['休','#7a7a7a'],dek:['出','#7a5230'],kd:['日','#4a5a3a'],memo:['メ','#9a7a2a']};
const CALN={basho:'本場所',tour:'巡業',rengo:'一門の連合稽古',soken:'横審の稽古総見',ban:'番付発表',ken:'新弟子検査',kn:'研修',rest:'休養の週',dek:'出稽古の週',kd:'稽古日数',memo:'メモ'};
function shoD(b){const y=(G.y0||2026)+Math.floor((b-1)/6),m=MONTH[(b-1)%6];const d=new Date(y,m-1,1);const f=(7-d.getDay())%7;return new Date(y,m-1,1+f+7);}
function wkD(b,w){const s=shoD(b);return new Date(s.getFullYear(),s.getMonth(),s.getDate()-(WEEKS+1-w)*7);}
const md=d=>(d.getMonth()+1)+'/'+d.getDate();
function planOf(b,w){return ((G.plan||{})[b]||{})[w]||null;}
function setPlan(b,w,p){G.plan=G.plan||{};G.plan[b]=G.plan[b]||{};const e=Object.keys(p).filter(k=>p[k]!=null&&p[k]!=='').length;if(e)G.plan[b][w]=p;else delete G.plan[b][w];
 for(const k in G.plan)if(+k<G.bnum)delete G.plan[k];}
function isPast(b,w){return b<G.bnum||(b===G.bnum&&(G.phase!=='train'||w<G.wk));}
/* その週の出来事(決まっているもの + 自分の予定) */
function calEv(b,w){const L=[];const m=MONTH[(b-1)%6];
 if(w==='B'){L.push(['basho',BASHO[(b-1)%6]+'場所('+CITY[(b-1)%6]+')']);return L;}
 const t=TOURW[m];if(t&&w>=t[0]&&w<=t[1])L.push(['tour',t[2]]);
 if(w===WEEKS-1){if(me().ic>=0&&!G.rengoOff)L.push(['rengo','一門の連合稽古']);L.push(['ban','番付発表']);L.push(['ken','新弟子検査']);}
 if(w===WEEKS&&[1,5,9].includes(m))L.push(['soken','横審の稽古総見']);
 /* 研修中(いま出ている人) */
 if(b===G.bnum&&G.phase==='train'&&G.ken){let ww=G.wk;for(const id in G.ken){const x=G.ken[id];if(!(x&&x.w>0))continue;if(w>=ww&&w<ww+x.w){const P=kenWho().find(p=>p.id===id);L.push(['kn',(P?P.n:'')+' 研修中']);}}}
 const p=planOf(b,w);if(p){if(p.kd)L.push(['kd','週 '+p.kd+' 日']);if(p.mn==='休')L.push(['rest','休養の週']);if(p.mn==='出')L.push(['dek','出稽古の週']);
  if(p.ken){const P=kenWho().find(x=>x.id===p.ken.id);const n=KENL[p.ken.L]||KENL.s;for(let i=0;i<n.w;i++){}L.push(['kn',(P?P.n.replace(/[((]師匠[))]/,''):'')+' '+n.n+'へ']);}
  if(p.memo)L.push(['memo',p.memo]);}
 /* 長い研修は 3 週続くので、後ろの週にも出す */
 for(let k=1;k<=2;k++){const q=typeof w==='number'?planOf(b,w-k):null;if(q&&q.ken&&(KENL[q.ken.L]||KENL.s).w>k){const P=kenWho().find(x=>x.id===q.ken.id);L.push(['kn',(P?P.n.replace(/[((]師匠[))]/,''):'')+' 研修中']);}}
 return L;}
const chip=(k,full)=>'<span class="cch" style="background:'+CALC[k][1]+'">'+CALC[k][0]+'</span>'+(full?'':'');
function legend(){return '<div class="cleg">'+Object.keys(CALC).map(k=>chip(k)+CALN[k]).join('')+'</div>';}
function yearHTML(){let h='<div class="cyr"><table><tr><th>場所</th>'+Array.from({length:WEEKS},(_,i)=>'<th>'+(i+1)+'週</th>').join('')+'<th>本場所</th></tr>';
 for(let b=G.bnum;b<G.bnum+6;b++){const s=shoD(b);
  h+='<tr><th class="cbn">'+BASHO[(b-1)%6]+'<small>'+s.getFullYear()+'年'+(s.getMonth()+1)+'月</small></th>';
  for(let w=1;w<=WEEKS+1;w++){const W=w>WEEKS?'B':w;const L=calEv(b,W);const past=W==='B'?(b<G.bnum||(b===G.bnum&&G.phase==='post')):isPast(b,w);
   const now=b===G.bnum&&((G.phase==='train'&&W===G.wk)||(G.phase==='basho'&&W==='B'));
   const can=W!=='B'&&!past;
   h+='<td class="'+(past?'past ':'')+(now?'now ':'')+(W==='B'?'bs ':'')+(can?'can':'')+'"'+(can?' onclick="calOpen('+b+','+w+')"':'')+'><div class="cd">'+md(W==='B'?s:wkD(b,w))+'</div>'+
    L.map(x=>chip(x[0])).join('')+'</td>';}
  h+='</tr>';}
 return h+'</table></div>'+legend()+'<div class="mute" style="font-size:12px;margin-top:4px">枠を押すと、その週の予定を入れられます(済んだ週は入れられません)。</div>';}
function monthHTML(){const b=G.bnum;let h='<div class="cmo">';
 for(let w=1;w<=WEEKS+1;w++){const W=w>WEEKS?'B':w;const L=calEv(b,W);const past=W==='B'?G.phase==='post':isPast(b,w);
  const now=(G.phase==='train'&&W===G.wk)||(G.phase==='basho'&&W==='B');const d0=W==='B'?shoD(b):wkD(b,w);const d1=new Date(d0.getFullYear(),d0.getMonth(),d0.getDate()+(W==='B'?14:6));
  h+='<div class="cwk '+(past?'past ':'')+(now?'now ':'')+(W==='B'?'bs':'')+'"><div class="cwh"><b>'+(W==='B'?'本場所':'第 '+w+' 週')+'</b><span>'+md(d0)+'〜'+md(d1)+'</span>'+(now?'<em>いま</em>':'')+'</div><div class="cwb">'+
   (L.length?L.map(x=>'<div class="cit">'+chip(x[0])+esc(x[1])+'</div>').join(''):'<div class="mute">ふだんの稽古</div>')+'</div>'+
   (W!=='B'&&!past?'<button class="btn sm" onclick="calOpen('+b+','+w+')">予定を入れる</button>':'')+'</div>';}
 return h+'</div>';}
function calHTML(){UI.calV=UI.calV||'m';const v=UI.calV;
 const nx=(G.plan&&Object.keys(G.plan).reduce((s,b)=>s+Object.keys(G.plan[b]).length,0))||0;
 return '<div class="pn"><h2>予定<span class="sub">'+bname(G.bnum)+'・'+phaseText()+'</span></h2>'+
  '<div class="divbtn" style="margin-bottom:8px"><button class="'+(v==='m'?'on':'')+'" onclick="UI.calV=\'m\';render()">今場所まで(6 週)</button><button class="'+(v==='y'?'on':'')+'" onclick="UI.calV=\'y\';render()">1 年(6 場所)</button></div>'+
  (v==='m'?monthHTML():yearHTML())+
  '<div class="hl" style="margin-top:8px">・入れた予定は、その週になると自動で行われます(入れた予定 '+nx+' 件)。<br>・研修は出発の週に費用を払います。資金が足りないと取りやめになります。</div></div>';}
window.calOpen=function(b,w){const p=Object.assign({},planOf(b,w)||{});UI.calE={b,w,p};calM();};
function calM(){const {b,w,p}=UI.calE;const d0=wkD(b,w);
 const L=calEv(b,w).filter(x=>!['kd','rest','dek','memo'].includes(x[0])||0);
 const opt=(name,cur,arr)=>'<div class="btns" style="flex-wrap:wrap">'+arr.map(([v,t])=>'<button class="btn sm'+((cur||'')===v?' main':'')+'" onclick="calSet(\''+name+'\',\''+v+'\')">'+t+'</button>').join('')+'</div>';
 const W=kenWho().filter(x=>!kenAway(x.id));const kp=p.ken||{};const P=W.find(x=>x.id===kp.id);
 let h='<h2>'+BASHO[(b-1)%6]+'場所前 第 '+w+' 週('+md(d0)+'〜)</h2>'+
  (L.length?'<div class="kaku" style="margin-bottom:6px">'+L.map(x=>chip(x[0])+esc(x[1])).join(' ')+'</div>':'')+
  '<h3>稽古の日数</h3>'+opt('kd',p.kd?String(p.kd):'',[['','いつも通り'],['6','週 6 日'],['5','週 5 日'],['4','週 4 日']])+
  '<h3>部屋全体</h3>'+opt('mn',p.mn,[['','いつも通り'],['休','休養の週(全員休む)'],['出','出稽古の週(関取・幕下)']])+
  '<h3>研修に出す</h3>'+opt('kid',kp.id,[['','出さない']].concat(W.map(x=>[x.id,x.n.replace(/[((]師匠[))]/,'')])))+
  (P?opt('kL',kp.L||'s',Object.keys(KENL).map(k=>[k,KENL[k].n+'('+KENL[k].w+' 週・'+man(Math.round(KENC[P.t]*KENL[k].c))+')'])) +
    opt('kk',kp.k,(KENK[P.t]||[]).map(k=>[k,KENN[k]||k])):'')+
  '<h3>メモ</h3><input id="calMemo" value="'+esc(p.memo||'')+'" maxlength="20" placeholder="例:けが明けの○○は軽め" style="width:100%;font-size:15px;padding:6px">'+
  '<div class="btns" style="margin-top:12px"><button class="btn main" onclick="calSave()">決める</button><button class="btn" onclick="UI.calE.p={};calSave()">予定を消す</button><button class="btn" onclick="closeM()">やめる</button></div>';
 openM(h);}
window.calSet=function(k,v){const p=UI.calE.p;const m=document.getElementById('calMemo');if(m)p.memo=m.value;
 if(k==='kd')p.kd=v?+v:null;else if(k==='mn')p.mn=v||null;
 else if(k==='kid'){if(!v)p.ken=null;else{const P=kenWho().find(x=>x.id===v);p.ken={id:v,L:(p.ken&&p.ken.L)||'s',k:(KENK[P.t]||[])[0]};}}
 else if(k==='kL'&&p.ken)p.ken.L=v;else if(k==='kk'&&p.ken)p.ken.k=v;calM();};
window.calSave=function(){const {b,w,p}=UI.calE;const m=document.getElementById('calMemo');if(m)p.memo=m.value.trim()||null;setPlan(b,w,p);closeM();save();render();};
window.calHTML=calHTML;window.calEv=calEv;window.planOf=planOf;
/* 週の始めに予定を当てはめ、週が終わったら元に戻す */
const dw0=doWeek;
doWeek=function(){const p=(G&&G.phase==='train')?planOf(G.bnum,G.wk):null;if(!p)return dw0.apply(this,arguments);
 const kd0=G.kDays,M0={};
 if(p.kd)G.kDays=p.kd;
 if(p.mn){ownAll().forEach(r=>{if(r.inj&&p.mn==='出')return;if(p.mn==='出'&&!(r.d<=2))return;M0[r.id]=[r.menu,r.it,r.pm,r.kMan];r.kMan=1;r.menu=p.mn;if(p.mn==='休'){r.it=0;r.pm='治';}});}
 if(p.ken&&!(G.ken&&G.ken[p.ken.id])){const P=kenWho().find(x=>x.id===p.ken.id);if(P){const L=KENL[p.ken.L]?p.ken.L:'s';const c=Math.round(KENC[P.t]*KENL[L].c);
   if(G.money>=c){G.money-=c;G.ken=G.ken||{};G.ken[p.ken.id]={k:p.ken.k||(KENK[P.t]||[])[0],b:G.bnum,L:L,w:KENL[L].w};addNews('予定どおり、'+P.n+'を'+KENW[P.t]+'('+KENL[L].n+')に出しました(費用 '+man(c)+')。');}
   else addNews('予定していた'+P.n+'の研修は、資金が足りず取りやめました。');}}
 if(p.mn==='休')addNews('予定どおり、今週は部屋全体で体を休めました。');
 if(p.mn==='出')addNews('予定どおり、今週は関取と幕下が出稽古に出ました。');
 try{return dw0.apply(this,arguments);}finally{if(p.kd)G.kDays=kd0;for(const id in M0){const r=G.R[id];if(!r)continue;const m=M0[id];r.menu=m[0];r.it=m[1];r.pm=m[2];if(m[3])r.kMan=m[3];else delete r.kMan;}}};
document.head.insertAdjacentHTML('beforeend','<style>.cch{display:inline-block;min-width:18px;height:18px;line-height:18px;border-radius:3px;color:#fff;font-size:11px;text-align:center;margin:1px;font-family:var(--kaku)}'+
 '.cleg{display:flex;flex-wrap:wrap;gap:2px 10px;font-size:12px;margin-top:6px}.cleg .cch{margin-right:2px}'+
 '.cyr{overflow-x:auto}.cyr table{border-collapse:collapse;width:100%;table-layout:fixed}.cyr th,.cyr td{border:1px solid #c8bb9e;padding:2px;vertical-align:top;font-size:12px}.cyr th{background:#e9dfca;font-weight:normal}'+
 '.cyr th.cbn{width:64px;text-align:left}.cyr th.cbn small{display:block;font-size:10px;opacity:.7}.cyr td{height:46px;background:#fbf7ee}.cyr td.can{cursor:pointer}.cyr td.can:hover{background:#f3e9d2}.cyr td.past{background:#e4e0d8;opacity:.55}.cyr td.bs{background:#f6e3dc}.cyr td.now{outline:3px solid #c9a227;outline-offset:-3px}.cyr .cd{font-size:10px;opacity:.65}'+
 '.cmo{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}.cwk{border:1px solid #c8bb9e;border-radius:4px;background:#fbf7ee;padding:6px;display:flex;flex-direction:column;min-height:150px}.cwk.past{opacity:.5;background:#e4e0d8}.cwk.bs{background:#f6e3dc}.cwk.now{outline:3px solid #c9a227;outline-offset:-3px}'+
 '.cwh{display:flex;flex-wrap:wrap;gap:2px 6px;align-items:baseline;border-bottom:1px solid #d9ccb0;padding-bottom:3px;margin-bottom:4px}.cwh span{font-size:12px;opacity:.7}.cwh em{font-style:normal;background:#c9a227;color:#fff;font-size:11px;padding:0 5px;border-radius:8px}'+
 '.cwb{flex:1;font-size:13px}.cit{margin:2px 0;line-height:1.35}.cwk .btn{margin-top:4px;width:100%}'+
 '@media (max-width:760px){.cmo{grid-template-columns:1fr}.cwk{min-height:0;flex-direction:row;flex-wrap:wrap;gap:4px}.cwh{width:100%}.cwk .btn{width:auto;margin-left:auto}.cyr th.cbn{width:44px}.cyr td{height:40px}.cyr .cch{min-width:14px;height:14px;line-height:14px;font-size:9px;margin:0}}'+
 'body.sk-yoru .cwk,body.sk-yoru .cyr td{background:#2c2620;border-color:#5a5040}body.sk-yoru .cyr th{background:#3a332a}</style>');
})();
