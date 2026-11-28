/* v218 本場所の結果を伏せる(ダルマさん「本場所 動画確認前に結果がわかってしまう」)。
   その日の取組の結果(勝ち負け・決まり手・成績・取組の様子)を、土俵で見終わるか「結果だけ見る」を押すまで伏せる。
   伏せている間は、下の欄(次の取組・星取表・優勝争いなど。成績で結果がわかるため)をぼかす。
   「結果を伏せる」はオン・オフでき、端末に覚える(sumoFz)。 */
(function(){
function on(){try{return localStorage.getItem('sumoFz')!=='0';}catch(e){return true;}}
function key(b){return (G?G.bnum+'-'+(G.B?G.B.day:(G.lastB?15:'x')):'x')+'-'+b.w+'-'+b.l;}
/* 千秋楽:取ったあとも本場所の画面に残り、取組を見てから「場所を締める」で結果のまとめを出す。G.B は場所のあと空になるので、描くあいだだけ仮に置く */
function endOn(){return G&&G.phase==='post'&&UI.fzEnd&&G.lastB&&on();}
function shim(){const sv={B:G.B,ph:G.phase};G.B={day:15,rec:G.lastB.rec,cur:[],tac:{},kin:[]};G.phase='basho';return sv;}
function unshim(sv){G.B=sv.B;G.phase=sv.ph;}
const bh0=bashoHTML;bashoHTML=function(){if(endOn()){const sv=shim();try{const h=bh0.apply(this,arguments);unshim(sv);const i=h.indexOf('<div class="pn"><h2>15日目の結果'),j=h.indexOf('<div class="pn"><h2>16日目の取組');
  if(i>=0)return '<div class="pn"><h2>'+bname(G.bnum)+'<span class="sub">千秋楽 終了</span></h2><div class="daybar">'+Array.from({length:15},()=>'<i class="d"></i>').join('')+'</div><div class="btns"><button class="btn main" onclick="fzEndGo()">場所を締める(結果のまとめへ)</button></div></div>'+h.slice(i,j<0?undefined:j).replace('15日目の結果','千秋楽の結果');}catch(e){unshim(sv);console.error(e);}}
 return bh0.apply(this,arguments);};
window.fzEndGo=function(){UI.fzEnd=0;UI.view='home';render();window.scrollTo(0,0);bashoEndModal();};
const sd0=stepDay;stepDay=function(){if(on()&&G.phase==='basho'&&G.B&&G.B.day===14){UI.bouts=advanceDay();save();if(G.phase==='post'){UI.fzEnd=1;UI.view='basho';render();window.scrollTo(0,0);return;}render();return;}return sd0.apply(this,arguments);};
['dhOpen','dhRun'].forEach(n=>{const f0=window[n];window[n]=function(){if(endOn()){const sv=shim();try{return f0.apply(this,arguments);}finally{unshim(sv);}}return f0.apply(this,arguments);};});
window.fzK=key;
window.fzC=function(b){return on()&&!(UI.seenB&&UI.seenB[key(b)])?' fuse':'';};
function seen(k){UI.seenB=UI.seenB||{};UI.seenB[k]=1;document.querySelectorAll('[data-k="'+k+'"]').forEach(e=>e.classList.remove('fuse'));const m=document.getElementById('dhmk');if(m&&m.dataset.k===k)m.classList.remove('rsvH');wait();}
window.fzShow=function(k){seen(k);};
window.fzAll=function(){document.querySelectorAll('.r1.fuse').forEach(e=>seen(e.dataset.k));};
window.fzTog=function(){try{localStorage.setItem('sumoFz',on()?'0':'1');}catch(e){}const y=window.scrollY;render();window.scrollTo(0,y);};
function resPn(){return [...document.querySelectorAll('.pn')].find(p=>{const h=p.querySelector('h2');return h&&/日目の結果|千秋楽の結果/.test(h.textContent)&&p.querySelector('.r1');});}
function wait(){const P=resPn();if(!P)return;const w=on()&&!!P.querySelector('.r1.fuse');let e=P.nextElementSibling;while(e){e.classList.toggle('fzw',w);e=e.nextElementSibling;}
 const n=P.querySelector('.fznote');if(n)n.style.display=w?'':'none';const a=P.querySelector('.fzall');if(a)a.style.display=w?'':'none';}
const dr0=dhRun;dhRun=function(id,b){const r=dr0.apply(this,arguments);try{const k=key(b);const t0=Date.now();setTimeout(()=>{if(G)seen(k);},5400);}catch(e){}return r;};
const rn0=render;render=function(){if(UI.fzEnd&&UI.view!=='basho'&&G&&G.phase==='post'){UI.fzEnd=0;setTimeout(bashoEndModal,60);}const x=rn0.apply(this,arguments);try{if(UI.view==='basho'){const P=resPn();if(P&&!P.querySelector('.fzbar')){
  P.querySelector('h2').insertAdjacentHTML('afterend','<div class="fzbar"><button class="btn sm fzall" onclick="fzAll()">全部の結果を見る</button><button class="btn sm" onclick="fzTog()">結果を伏せる:'+(on()?'オン':'オフ')+'</button><span class="fznote mute">'+(UI.fzEnd?'見終わったら「場所を締める」で、場所の結果のまとめが出ます。':'下の欄(次の取組・星取表・優勝争い)は、今日の取組を見終わると表示します。')+'</span></div>');}
  wait();}}catch(e){console.error(e);}return x;};
document.head.insertAdjacentHTML('beforeend','<style>.fz{display:none}.r1.fuse .rsv{display:none}.r1.fuse .fz{display:inline}.r1.fuse div.fz,.r1.fuse button.fz{display:inline-block}.rsvH{visibility:hidden}'+
 '.fzb{background:#555;color:#fff;font-size:12px;padding:1px 6px;border-radius:3px}.fzbtn{margin-left:6px;font-size:12px;padding:3px 8px;border-radius:12px;border:1px solid var(--line);background:none;color:var(--mute);cursor:pointer}'+
 '.fzbar{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:-2px 0 8px}.fznote{font-size:12px}'+
 '.fzw{filter:blur(7px);pointer-events:none;user-select:none;transition:filter .4s}</style>');
})();
