/* v207 窓を部屋と同じ色に(部屋の札 .hbp の色を読み取る)。もとは v206 タブを部屋の上の窓(ポップアップ)で開く。後ろはいつも部屋の画面。× か窓の外を押すと部屋に戻る。窓を開いたままほかのタブにも切り替えられる */
(function(){
const PVN={rikishi:['力士','rikishiHTML'],keiko:['稽古','keikoHTML'],yotei:['予定','calHTML'],basho:['本場所','bashoHTML'],banzuke:['番付','banzukeHTML'],scout:['新弟子','scoutHTML'],staff:['スタッフ','staffHTML'],keiei:['経営','keieiHTML'],kiroku:['記録','kirokuHTML']};
function popOn(){try{return localStorage.getItem('smPop')!=='0';}catch(e){return true;}}
window.popSet=function(v){try{localStorage.setItem('smPop',v?'1':'0');}catch(e){}render();};
window.popClose=function(){go('home');};
const r0=render;
render=function(){const v=UI.view;
 if(!G||UI.title||G.over||!PVN[v]||!popOn()||!document.getElementById('app')){document.body.classList.remove('pv-open');return r0();}
 const old=document.querySelector('#pv .pvb');const keep=old&&old.dataset.v===v?old.scrollTop:0;
 const f=window[PVN[v][1]];let body='';
 UI.view='home';try{r0();}finally{UI.view=v;}
 try{body=f();}catch(e){sysLog&&sysLog('エラー',e);throw e;}
 const nav=document.getElementById('nav');if(nav)nav.outerHTML=navHTML();
 const app=document.getElementById('app');
 app.insertAdjacentHTML('beforeend','<div id="pv" onclick="if(event.target.id===\'pv\')popClose()"><div class="pvw"><div class="pvh"><b>'+PVN[v][0]+'</b><span class="pvs">部屋の上で開いています</span><button class="pvx" onclick="popClose()">× 閉じて部屋へ</button></div><div class="pvb" data-v="'+v+'">'+body+'</div></div></div>');
 document.body.classList.add('pv-open');
 try{const hp=document.querySelector('#app .hbp'),hk=document.querySelector('#app .hbk');const pv0=document.getElementById('pv');
  if(hp&&pv0){const c=getComputedStyle(hp);const fg=c.color;const m=fg.match(/\d+/g)||[0,0,0];const dark=(+m[0]+ +m[1]+ +m[2])/3>140;
   pv0.style.setProperty('--pvbg',c.backgroundColor);pv0.style.setProperty('--pvfg',fg);pv0.style.setProperty('--pvbf',c.backdropFilter&&c.backdropFilter!=='none'?c.backdropFilter:'none');
   pv0.style.setProperty('--pvac',hk?getComputedStyle(hk).color:fg);pv0.style.setProperty('--pvln',hk?getComputedStyle(hk).borderBottomColor:'rgba(0,0,0,.2)');
   pv0.classList.toggle('pvdk',dark);}}catch(e){}
 const n=document.getElementById('nav'),pv=document.getElementById('pv');
 if(n&&pv){const b=n.getBoundingClientRect().bottom;pv.style.top=Math.max(0,Math.round(b+4))+'px';}
 const nb=document.querySelector('#pv .pvb');if(nb&&keep)nb.scrollTop=keep;};
/* 窓の中のスクロールを戻す関数(scrollTo)は窓に向ける */
const st0=window.scrollTo.bind(window);
window.scrollTo=function(x,y){const nb=document.querySelector('#pv .pvb');if(nb&&document.body.classList.contains('pv-open')){if(typeof x==='object')nb.scrollTop=x.top||0;else nb.scrollTop=y||0;return;}return st0.apply(null,arguments);};
try{Object.defineProperty(window,'scrollY',{configurable:true,get(){const nb=document.querySelector('#pv .pvb');return nb&&document.body.classList.contains('pv-open')?nb.scrollTop:(document.scrollingElement||document.documentElement).scrollTop;}});}catch(e){}
/* 設定:窓で開く/画面ごと切り替える */
const sh0=sysHTML;sysHTML=function(){const on=popOn();return sh0()+'<div class="pn"><h2>タブの開き方</h2><div class="btns"><button class="btn'+(on?' main':'')+'" onclick="popSet(1)">部屋の上の窓で開く</button><button class="btn'+(on?'':' main')+'" onclick="popSet(0)">画面ごと切り替える(前の形)</button></div><p class="mute" style="font-size:13px">窓で開くと、後ろはいつも部屋の画面です。× か窓の外を押すと部屋に戻ります。</p></div>';};
document.head.insertAdjacentHTML('beforeend','<style>'+
 '#pv{position:fixed;left:0;right:0;bottom:0;z-index:40;background:rgba(0,0,0,.18);display:flex!important;justify-content:center;align-items:stretch;padding:0 1.5% 1.2%}'+
 '#pv .pvw{width:100%;max-width:1200px;background:transparent;-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);border-radius:10px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.4)}'+
 '#pv .pvh{display:flex;align-items:center;gap:10px;padding:8px 12px;margin:0 0 6px;background:var(--pvbg);color:var(--pvfg);-webkit-backdrop-filter:var(--pvbf);backdrop-filter:var(--pvbf);border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.25)}'+
 '#pv .pvh b{font-size:18px;letter-spacing:.12em;color:var(--pvac)}#pv .pvs{font-size:12px;opacity:.65}'+
 '#pv .pvx{margin-left:auto;font-size:15px;padding:6px 14px;border:1px solid var(--pvac);border-radius:6px;background:transparent;color:var(--pvac);min-height:36px}'+
 '#pv .pvb{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:0 2px 6px}'+
 '#pv .pvb .pn{background:var(--pvbg)!important;color:var(--pvfg);border:0!important;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.25);margin:0 0 8px}'+
 '#pv .pvb .pn h2{color:var(--pvac);border-bottom:1px dashed var(--pvln)}#pv .pvb .pn h2 .sub{color:var(--pvfg);opacity:.7}'+
 '#pv.pvdk .pvb .hl,#pv.pvdk .pvb .kaku.hl{background:rgba(255,255,255,.07)!important;color:var(--pvfg)!important;border-color:var(--pvln)!important}'+
 '#pv.pvdk .pvb .mute{color:var(--pvfg);opacity:.62}'+
 '#pv.pvdk .pvb .pkall{background:var(--pvbg)!important;color:var(--pvfg)!important;border-color:var(--pvln)!important;border-radius:10px}#pv.pvdk .pvb .pkall *{color:inherit}#pv .pvb .pkall{border-radius:10px;margin-bottom:8px}#pv.pvdk .pvb .pkm{background:rgba(255,255,255,.07)!important;color:var(--pvfg)!important;border-color:var(--pvln)!important}#pv.pvdk .pvb .pkm *{color:inherit}'+
 '#pv.pvdk .pvb h3{color:var(--pvac)!important}#pv.pvdk .pvb .hyrt td:first-child{color:var(--pvac)!important}'+
 '#pv.pvdk .pvb .hyc{background:rgba(255,255,255,.08)!important;color:var(--pvfg)!important;border-color:var(--pvac)!important}#pv.pvdk .pvb .hyc *{color:inherit!important}'+
 '#pv.pvdk .pvb .tb th{background:rgba(255,255,255,.08)!important;color:var(--pvac)!important}#pv.pvdk .pvb .tb td{border-color:rgba(255,255,255,.12)!important}'+
 'body.pv-open{overflow:hidden}#mdl{z-index:60}'+
 '@media (max-width:760px){#pv{padding:0 4px 4px}#pv .pvs{display:none}}'+
 '</style>');
})();
