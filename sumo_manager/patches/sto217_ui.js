/* v214 土俵の物語 ②③。
   ② ゲームの中で生まれる物語:金星の日、決定戦の雪辱、千秋楽の勝ち越し、横綱・大関から初めての白星、
      優勝次点が 3 回に届くと「あと一歩の男」(悲願の物語が始まる)、三段目以下まで落ちた元関取の関取復帰(復活の物語が始まる)、
      よその部屋の関取の昇進・優勝も書き足す(自分の部屋は「目標と歩み」に入る)。
   ③ 引退のときに名場面を 3 つ選んで振り返る(自分の部屋はまどで、殿堂の札にも残る。よその部屋の幕内優勝経験者などはニュース)。
   名場面の重みは推定。 */
(function(){
const sx=(r,t,s)=>storySx(r,t,s);
function stoScore(x){const t=x.t||'';
 if(x.k==='yu')return /幕内/.test(t)?100:/十両/.test(t)?45:25;
 if(x.k==='up')return /横綱/.test(t)?110:/大関/.test(t)?90:/三役|関脇|小結/.test(t)?70:/新入幕/.test(t)?60:/新十両/.test(t)?50:15;
 return {sh:40,fk:70,ok:25,rv:30,dk:35}[x.k]||8;}
function memOf(r){const A=[];(r.sto||[]).forEach(x=>{if(x.k==='in')return;A.push({b:x.b,t:x.t,s:stoScore(x)});});
 (r.stoX||[]).forEach(x=>A.push({b:x.b,t:x.t,s:x.s||50}));
 const seen={};return A.sort((a,b)=>b.s-a.s||a.b-b.b).filter(x=>{if(seen[x.b])return false;seen[x.b]=1;return true;}).slice(0,3).sort((a,b)=>a.b-b.b).map(x=>({b:x.b,t:bname(x.b)+'、'+x.t}));}
window.memOf=memOf;
function notable(r){return r&&!r.ret&&(isPH(r.h)||r.d<=1);}
/* ② 場所のあと */
const eb0=endBasho;endBasho=function(){const B=G.B;const rk=!!G._rkYu;const r0=eb0.apply(this,arguments);try{if(!rk)story2(B);}catch(e){console.error(e);}return r0;};
function story2(B){if(!B)return;const S=G.last||{po:[],kin:[]};
 (B.kin||[]).forEach(k=>{const W=G.R[k[0]],L=G.R[k[1]];if(W&&L)sx(W,k[2]+'日目、横綱 '+L.n+' を破って金星',60);});
 (S.po||[]).forEach(p=>{if(p.d!==0)return;p.ids.forEach(id=>{const r=G.R[id];if(!r)return;
   if(id===p.w){if(r.poL)sx(r,'優勝決定戦を制す。'+(r.poL+1)+' 度目の決定戦で、ついに雪辱',105);else sx(r,'優勝決定戦を制して賜杯',95);r.poL=0;}
   else r.poL=(r.poL||0)+1;});});
 Object.keys(B.rec).forEach(id=>{const r=G.R[id];if(!notable(r))return;const rc=B.rec[id];if(!rc||rc.ky)return;
  /* 千秋楽の勝ち越し */
  const last=rc.res&&rc.res[14];if(r.d<=1&&!r.sk8&&last&&(last.r==='○'||last.r==='□')&&rc.w===8&&rc.l+rc.ab===7){r.sk8=1;sx(r,'千秋楽、7 勝 7 敗から勝ち越しを決める',30);}
  /* 横綱・大関から初めての白星 */
  if(r.d===0&&rc.res)rc.res.forEach((x,i)=>{if(!x||x.r!=='○')return;const o=G.R[x.o];if(!o)return;
   if(o.t==='Y'&&!r.fY&&!r.t){r.fY=1;if(!(B.kin||[]).some(k=>k[0]==id&&k[2]===i+1))sx(r,(i+1)+'日目、横綱 '+o.n+' から初めての白星',45);}
   else if(o.t==='O'&&!r.fO&&!r.t){r.fO=1;sx(r,(i+1)+'日目、大関 '+o.n+' から初めての白星',35);}});
  /* よその部屋の関取の優勝(自分の部屋は「目標と歩み」に入る) */
  if(rc.yu&&!isPH(r.h)&&r.d<=1&&!(r.real&&window.STORYD&&STORYD[r.n])){const c=r.yu[r.d];if(c<=3||c%5===0)sx(r,DN[r.d]+'優勝('+(c>1?c+' 回目、':'')+rc.w+' 勝)',r.d===0?(c===1?100:85):45);}
  /* あと一歩の男 */
  if(r.d===0&&!rc.yu&&(rc.jn===1||rc.jn===2)){r.jnC=(r.jnC||0)+1;
   if(r.jnC>=3&&!r.yu[0]&&!(r.stK&&r.stK.higan)&&!(r.hg)){r.stK=Object.assign({},r.stK||{},{higan:[r.jnC,r.poL||0]});sx(r,'優勝次点 '+r.jnC+' 回。「あと一歩の男」と呼ばれ始める',55);
    addNews(r.n+'は優勝次点が '+r.jnC+' 回に。いつしか「あと一歩の男」と呼ばれ、悲願の賜杯に注目が集まっています。');}}});}
/* ② 番付発表:よその部屋の関取の昇進、元関取のどん底からの復帰 */
const nc0=nextCycle;nextCycle=function(){const old={};try{G.order.forEach(id=>{const r=G.R[id];if(r&&!r.ret)old[id]=[r.d,r.t];});}catch(e){}
 const res=nc0.apply(this,arguments);
 try{if(res!==false)Object.keys(old).forEach(id=>{const r=G.R[id];if(!r||r.ret)return;const o=old[id];
  if(r.sekD&&r.d>=3)r.fall=1;
  if(r.fall&&r.d<=1&&o[0]>1){r.fall=0;r.stK=Object.assign({},r.stK||{},{fukkatsu:[1]});sx(r,'三段目以下まで落ちてから、関取に復帰',70);
   if(isPH(r.h)||r.best!=null)addNews(r.n+'が関取に復帰。三段目以下まで落ちてからの、粘りの復活です。');}
  if(isPH(r.h))return;
  if(r.d===1&&o[0]>1&&!r.sekD0){r.sekD0=1;sx(r,'新十両',50);}
  else if(r.d===0&&o[0]>0&&!r.mkD0){r.mkD0=1;sx(r,'新入幕',60);}
  if((r.t==='S'||r.t==='K')&&!['S','K','O','Y'].includes(o[1])&&!r.sanD0){r.sanD0=1;sx(r,'新三役('+(r.t==='S'?'関脇':'小結')+')',70);}
  if(r.t==='O'&&o[1]!=='O'&&o[1]!=='Y'){sx(r,r.ozD?'大関に返り咲き':'大関に昇進',r.ozD?75:90);r.ozD=1;}
  if(r.t==='Y'&&o[1]!=='Y')sx(r,'横綱に昇進',110);});}catch(e){console.error(e);}
 return res;};
/* ③ 引退:名場面を 3 つ */
const dr0=doRetire0;doRetire0=function(r,why){const mem=memOf(r);const res=dr0.apply(this,arguments);
 try{const x=G.retired[0];if(x&&x.n===r.n)x.mem=mem;if(r.h===ME()&&mem.length){addNews(r.n+'の名場面:'+mem.map(m=>m.t).join(' / '));(UI.memQ=UI.memQ||[]).push({n:r.n,rk:bestRank(r),age:Math.floor(r.age),cw:r.cw,cl:r.cl,mem:mem});}}catch(e){console.error(e);}return res;};
const rc0=retireCheck;retireCheck=function(){const was={};G.order.forEach(id=>{const r=G.R[id];if(r&&!r.ret&&!isPH(r.h))was[id]=1;});const res=rc0.apply(this,arguments);
 try{Object.keys(was).forEach(id=>{const r=G.R[id];if(!r||!r.ret)return;if(!(r.yu[0]>0||r.t==='Y'||r.t==='O'||(r.real&&window.STORYD&&STORYD[r.n])||(r.stoX||[]).length>=4))return;
  const m=memOf(r);if(m.length)addNews(r.n+'('+bestRank(r)+')が引退。名場面:'+m.map(x=>x.t).join(' / '));});}catch(e){console.error(e);}return res;};
function memModal(){const q=UI.memQ;if(!q||!q.length||document.querySelector('#mdl.on'))return;const x=q.shift();
 openM('<div class="memx"><div class="memk">引退</div><h2>'+esc(x.n)+'</h2><p class="mute">最高位 '+esc(x.rk)+'・通算 '+x.cw+' 勝 '+x.cl+' 敗・'+x.age+' 歳</p><h3>名場面</h3><ol class="memo">'+x.mem.map((m,i)=>'<li><span class="memn">'+(i+1)+'</span>'+esc(m.t)+'</li>').join('')+'</ol><p class="mute" style="font-size:12px">記録は数字で残り、記憶は名場面で残ります。殿堂の札にも残します。</p><button class="btn main" onclick="closeM()">お疲れさまでした</button></div>');}
const rn0=render;render=function(){const x=rn0.apply(this,arguments);try{if(!UI.title&&G&&UI.memQ&&UI.memQ.length)setTimeout(memModal,50);}catch(e){}return x;};
document.head.insertAdjacentHTML('beforeend','<style>.memx{text-align:center}.memk{display:inline-block;padding:2px 10px;border:1px solid #c9a24a;color:#c9a24a;border-radius:3px;letter-spacing:.3em;font-size:12px}.memx h2{font-size:30px;margin:6px 0 2px;letter-spacing:.1em}.memo{list-style:none;padding:0;margin:8px auto 12px;max-width:520px;text-align:left}.memo li{display:flex;gap:10px;align-items:flex-start;padding:8px 4px;border-top:1px dashed rgba(201,162,74,.4);font-size:15px;line-height:1.6}.memn{flex:none;width:24px;height:24px;border-radius:50%;background:#c9a24a;color:#1a140c;font-weight:700;text-align:center;line-height:24px;font-size:13px}.hym{margin:6px 0 0;padding-left:1.2em;font-size:11px;text-align:left;opacity:.85}.hym li{margin:2px 0}</style>');
})();
