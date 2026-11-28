/* v216 親方の物語(ダルマさん「親方にも物語があるね」)。
   ① 実在の師匠 5 人の現役時代の歩み(出典つき、data/oyastory2026.txt)を、親方の画面・部屋付き親方の札・部屋えらびの説明に出す。
   ② ゲームの中で師匠の物語を書き足す(金色の行):部屋を興す、弟子の新十両・新入幕・幕内優勝・大関・横綱、
      弟子が師匠の最高位や優勝回数を超えた日(「師匠を超えた」)、師匠ゆずりの型の完成、定年で部屋を譲る日。
   ③ 部屋を譲るとき、師匠の名場面を 3 つ選んで振り返り、「歴代の師匠」に残す。名場面の重みは推定。 */
(function(){
const OD=window.OYSD||{};
const RKN={Y:'横綱',O:'大関',S:'関脇',K:'小結'};
const lvB=b=>/横綱/.test(b)?5:/大関/.test(b)?4:/関脇/.test(b)?3:/小結/.test(b)?2:/前頭/.test(b)?1:/十両/.test(b)?0:-1;
const lvR=r=>r.t==='Y'?5:r.t==='O'?4:r.t==='S'?3:r.t==='K'?2:r.d===0?1:r.d===1?0:-1;
const nmR=r=>RKN[r.t]||(r.d===0?'幕内':'十両');
function oyMo(h){if(h.oyMo)return h.oyMo;const m=/元・([^))]+)[))]/.exec(h.o||'');return m?m[1]:'';}
function oyBest(h){if(h.oyBest!=null)return h.oyBest;const mo=oyMo(h);const T=(typeof TOSHI!=='undefined'&&mo)?TOSHI.find(t=>t[4]===mo):null;return T?T[5]:'';}
function oyYu(h){if(h.oyYuN!=null)return h.oyYuN;const D=OD[oyMo(h)];return D&&D.yu!=null?D.yu:null;}
function isReal(h){return !!(G.real&&typeof REALH!=='undefined'&&REALH.find(x=>x[0]===h.n));}
function ox(h,t,s){h.oyX=h.oyX||[];h.oyX.push({b:G.bnum,t:t,s:s||40});if(h.oyX.length>40)h.oyX.shift();}
window.oyStorySx=ox;
/* 師匠の物語を始める。いまの弟子がもう師匠を超えていたら、印だけ付けておく(初めの場所に一度に出ないように) */
function ens(hi){const h=G.heya[hi];if(!h||h.closed)return null;if(h.oyX)return h;h.oyX=[];h.oyF={sk:0,mk:0,yu:0,O:0,Y:0};
 if(!isReal(h)&&(h.gen||1)===1)ox(h,h.n+'部屋を興す',30);
 const b=lvB(oyBest(h)),yn=oyYu(h);
 Object.values(G.R).forEach(r=>{if(!r||r.ret||r.h!==hi)return;if(b>=0&&lvR(r)>b)r.oyOv=hi+1;if(yn!=null&&(r.yu[0]||0)>yn)r.oyOvY=hi+1;if(r.tk&&r.tk.v>=90)r.oyKt=1;if(r.t==='O'||r.t==='Y')r.oyO=1;if(r.t==='Y')r.oyY=1;});
 return h;}
window.oyEns=ens;
function phs(){const L=[];G.heya.forEach((h,i)=>{if(h&&!h.closed&&isPH(i))L.push(i);});return L;}
function fresh(h){return !isReal(h)||(h.gen||1)>1;}
function nth(c){return c===1;}
/* 場所のあと:幕内優勝 */
const eb0=endBasho;endBasho=function(){const B=G.B;const rk=!!G._rkYu;const r0=eb0.apply(this,arguments);try{if(!rk&&B)oyBasho(B);}catch(e){console.error(e);}return r0;};
function oyBasho(B){phs().forEach(hi=>{const h=ens(hi);if(!h)return;
 Object.keys(B.rec).forEach(id=>{const r=G.R[id];if(!r||r.h!==hi||r.d!==0)return;const rc=B.rec[id];if(!rc||!rc.yu)return;
  const c=++h.oyF.yu;if(c===1)ox(h,r.n+'が幕内優勝。'+(fresh(h)?'師匠として初めての賜杯':'この師匠のもとで初めての賜杯(このゲームで)'),100);
  else if(c%5===0)ox(h,r.n+'が幕内優勝。'+(fresh(h)?'師匠として ':'この師匠のもとで ')+c+' 度目の賜杯',80);
  const yn=oyYu(h);if(yn!=null&&!r.oyOvY&&(r.yu[0]||0)>yn){r.oyOvY=hi+1;
   const t=(yn?'師匠の幕内優勝 '+yn+' 回を超える':'師匠が手にできなかった賜杯を抱く');
   ox(h,r.n+'が'+t+'。「師匠を超えた」',95);storySx(r,t+'(師匠は元'+(oyMo(h)||'力士')+')',90);
   addNews(r.n+'が'+t+'。'+oyN0(h)+'は「弟子が師匠を超えるのが、いちばんの恩返し」。');}});
 /* 師匠ゆずりの型 */
 const ty=h.oyT;Object.values(G.R).forEach(r=>{if(!r||r.ret||r.h!==hi||r.oyKt||r.d>1||!r.tk||r.tk.v<90)return;
  const ok=ty==='押'?r.tk.p==='O':ty==='技'?r.tk.p==='W':ty==='四'?/[RLX]/.test(r.tk.p):false;if(!ok)return;
  r.oyKt=1;const nm={押:'押し相撲',四:'四つ相撲',技:'技'}[ty];ox(h,r.n+'が師匠ゆずりの'+nm+'を完成させる',45);storySx(r,'師匠ゆずりの'+nm+'が完成',45);});});}
function oyN0(h){return String(h.o||'').replace(/[((].*$/,'')+'親方';}
/* 番付発表:新十両・新入幕・大関・横綱・師匠の最高位を超える */
const nc0=nextCycle;nextCycle=function(){const old={};try{const P=phs();Object.values(G.R).forEach(r=>{if(r&&!r.ret&&P.includes(r.h))old[r.id]=[r.d,r.t,r.h];});}catch(e){}
 const res=nc0.apply(this,arguments);
 try{if(res!==false)Object.keys(old).forEach(id=>{const r=G.R[id];if(!r||r.ret)return;const o=old[id];if(r.h!==o[2])return;const h=ens(r.h);if(!h)return;const F=h.oyF;
  if(r.d===1&&o[0]>1&&!r.oySk){r.oySk=1;const c=++F.sk;if(c===1)ox(h,r.n+'が新十両。'+(fresh(h)?'部屋から初めての関取':'この師匠のもとで 1 人目の新十両(このゲームで)'),55);else if(c%5===0)ox(h,r.n+'が新十両。育てた関取は '+c+' 人に',45);}
  if(r.d===0&&o[0]>0&&!r.oyMk){r.oyMk=1;const c=++F.mk;if(c===1)ox(h,r.n+'が新入幕。'+(fresh(h)?'部屋から初めての幕内力士':'この師匠のもとで 1 人目の新入幕(このゲームで)'),60);}
  if(r.t==='O'&&o[1]!=='O'&&o[1]!=='Y'&&!r.oyO){r.oyO=1;const c=++F.O;ox(h,r.n+'が大関に。'+(c===1?(fresh(h)?'師匠として初めての大関':'この師匠のもとで 1 人目の新大関(このゲームで)'):c+' 人目の新大関'),85);}
  if(r.t==='Y'&&o[1]!=='Y'&&!r.oyY){r.oyY=1;const c=++F.Y;ox(h,r.n+'が横綱に。'+(c===1?(fresh(h)?'師匠として初めての横綱':'この師匠のもとで 1 人目の新横綱(このゲームで)'):c+' 人目の新横綱'),110);}
  const b=lvB(oyBest(h));if(b>=0&&b<5&&!r.oyOv&&lvR(r)>b){r.oyOv=r.h+1;const t='師匠の最高位(' +oyBest(h).replace(/[0-9０-９]+枚目/,'')+')を超えて'+nmR(r)+'に';
   ox(h,r.n+'が'+t+'。「師匠を超えた」',95);storySx(r,t+'(師匠は元'+(oyMo(h)||'力士')+')',90);addNews(r.n+'が'+t+'。弟子が師匠を超えました。');}});}catch(e){console.error(e);}
 return res;};
/* 名場面 3 つ */
function oyMem(h){const seen={};return (h.oyX||[]).slice().sort((a,b)=>b.s-a.s||a.b-b.b).filter(x=>{if(seen[x.b])return false;seen[x.b]=1;return true;}).slice(0,3).sort((a,b)=>a.b-b.b).map(x=>({b:x.b,t:bname(x.b)+'、'+x.t}));}
/* 部屋を譲る */
const sc0=succeed;succeed=function(s,mode){const hi=ME();const h=ens(hi);const mo0=oyMo(h),b0n=String(h.o||'').replace(/[((].*$/,'');const old={o:mo0?(b0n===mo0?'師匠(元'+mo0+')':b0n+'親方(元'+mo0+')'):oyN0(h),mo:oyMo(h),gen:h.gen||1,b0:(h.oyX&&h.oyX.length?h.oyX[0].b:G.bnum),mem:oyMem(h)};
 const res=sc0.apply(this,arguments);
 try{const H=G.heya[hi];old.b1=G.bnum;(H.oyP=H.oyP||[]).unshift(old);if(H.oyP.length>12)H.oyP.pop();
  H.oyMo=s.n.replace(/^元・/,'');H.oyBest=s.mo||'';const rr=G.retired.find(x=>x.n===H.oyMo);H.oyYuN=rr&&rr.yu?(rr.yu[0]||0):(OD[H.oyMo]&&OD[H.oyMo].yu!=null?OD[H.oyMo].yu:null);
  H.oyX=[];H.oyF={sk:0,mk:0,yu:0,O:0,Y:0};ox(H,'元'+H.oyMo+'が師匠に。'+old.o+'から部屋を継ぐ',40);
  Object.values(G.R).forEach(r=>{if(!r||r.ret||r.h!==hi)return;r.oyOv=0;r.oyOvY=0;const b=lvB(H.oyBest);if(b>=0&&lvR(r)>b)r.oyOv=hi+1;if(H.oyYuN!=null&&(r.yu[0]||0)>H.oyYuN)r.oyOvY=hi+1;});
  if(old.mem.length){(UI.oyQ=UI.oyQ||[]).push(old);addNews(old.o+'の名場面:'+old.mem.map(m=>m.t).join(' / '));}}catch(e){console.error(e);}
 return res;};
/* 見せ方 */
function rowsHTML(D,X){const rows=(D?D.ev.map(e=>[e[0],e[1],e[2],1]):[]).concat((X||[]).map(x=>[bname(x.b),x.t,'',0]));
 return '<ol class="styl">'+rows.map(e=>'<li class="'+(e[3]?'re':'ge')+'"><b>'+esc(e[0])+'</b><span>'+esc(e[1])+(e[2]?'<small>'+esc(e[2])+'</small>':'')+'</span></li>').join('')+'</ol>';}
function oyStoryHTML(mo,X,full){const D=OD[mo];X=X||[];if(!D&&!X.length)return '';
 return '<div class="sty oys"><h3>土俵の物語<i class="oysk">'+(D?'元'+esc(mo):'師匠')+'</i></h3>'+(D&&D.sum?'<p class="stys">'+esc(D.sum)+'</p>':'')+
  (D&&D.kei?'<p class="oykei">系譜 '+esc(D.kei)+'</p>':'')+rowsHTML(D,X)+
  (full&&D?'<p class="styn">白い行は実際の出来事(出典つき)。金色の行は、このゲームの中で起きたことです。</p>':'')+'</div>';}
window.oyStoryHTML=oyStoryHTML;
function pastHTML(h){const P=h.oyP||[];if(!P.length)return '';
 return '<div class="sty oys"><h3>歴代の師匠<i class="oysk">このゲームの中</i></h3><ol class="oyp">'+P.map(p=>'<li><b>'+esc(p.o)+'</b><span class="mute">'+esc(bname(p.b0))+'〜'+esc(bname(p.b1))+'</span>'+(p.mem&&p.mem.length?'<ul>'+p.mem.map(m=>'<li>'+esc(m.t)+'</li>').join('')+'</ul>':'')+'</li>').join('')+'</ol></div>';}
const sh0=staffHTML;staffHTML=function(){let h=sh0.apply(this,arguments);try{const H=ens(ME());
  const a=oyStoryHTML(oyMo(H),H.oyX,1)+pastHTML(H);
  if(a){const i=h.indexOf('<div class="sks">');const j=i<0?-1:h.indexOf('</div></div>',i);if(j>=0)h=h.slice(0,j+6)+a+h.slice(j+6);}
  G.staff.forEach(s=>{if(s.role!=='co'||!s.real)return;const mo=s.n.replace(/^元・/,'');if(!OD[mo])return;const k='<b class="nm">'+esc(s.n)+'</b>';const i=h.indexOf(k);if(i<0)return;const j=h.indexOf('<div class="btns">',i);if(j<0)return;
   h=h.slice(0,j)+'<details class="oyd"><summary>土俵の物語を読む</summary>'+oyStoryHTML(mo,[],0)+'</details>'+h.slice(j);});}catch(e){console.error(e);}return h;};
/* 部屋えらびの説明 */
const hs0=heyaSheet;heyaSheet=function(n){const res=hs0.apply(this,arguments);try{const x=heyaList().find(h=>h.n===n);const el=$('#hsheet .in');if(x&&el&&OD[x.m]){const dl=el.querySelector('dl');const d=document.createElement('div');d.innerHTML=oyStoryHTML(x.m,[],1);if(dl)dl.after(d.firstChild);else el.appendChild(d.firstChild);}}catch(e){console.error(e);}return res;};
/* 部屋を譲ったときのまど */
function oyModal(){const q=UI.oyQ;if(!q||!q.length||document.querySelector('#mdl.on'))return;const x=q.shift();
 openM('<div class="memx"><div class="memk">部屋を譲る</div><h2>'+esc(x.o)+'</h2><p class="mute">師匠として '+esc(bname(x.b0))+'〜'+esc(bname(x.b1))+'</p><h3>師匠の名場面</h3><ol class="memo">'+x.mem.map((m,i)=>'<li><span class="memn">'+(i+1)+'</span>'+esc(m.t)+'</li>').join('')+'</ol><p class="mute" style="font-size:12px">親方の画面の「歴代の師匠」に残します。</p><button class="btn main" onclick="closeM()">OK</button></div>');}
const rn0=render;render=function(){const x=rn0.apply(this,arguments);try{if(!UI.title&&G&&UI.oyQ&&UI.oyQ.length&&!(UI.memQ&&UI.memQ.length))setTimeout(oyModal,80);}catch(e){}return x;};
document.head.insertAdjacentHTML('beforeend','<style>.oys{margin-top:10px}.oysk{display:inline-block;width:auto;background:none;font-style:normal;vertical-align:middle;font-size:12px;margin-left:8px;padding:1px 8px;border:1px solid #c9a24a;color:#c9a24a;border-radius:3px;letter-spacing:.1em;font-weight:400}.oykei{font-size:13px;margin:2px 0 6px;color:#c9a24a;letter-spacing:.05em}.oyd{margin:6px 0 4px}.oyd summary{cursor:pointer;color:#c9a24a;font-size:13px}.oyp{list-style:none;padding:0;margin:4px 0}.oyp>li{padding:6px 0;border-top:1px dashed rgba(201,162,74,.4)}.oyp>li>b{margin-right:8px}.oyp ul{margin:4px 0 0;padding-left:1.2em;font-size:13px}</style>');
})();
