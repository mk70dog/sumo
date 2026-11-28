/* v206 タブを部屋の上の窓(ポップアップ)で開く。後ろはいつも部屋の画面。× か窓の外を押すと部屋に戻る。窓を開いたままほかのタブにも切り替えられる */
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
 '#pv{position:fixed;left:0;right:0;bottom:0;z-index:40;background:rgba(20,16,10,.35);display:flex!important;justify-content:center;align-items:stretch;padding:0 1.5% 1.2%}'+
 '#pv .pvw{width:100%;max-width:1200px;background:var(--wa,#f4ecdb);border:2px solid #8a6b3a;border-top:4px solid #8a2b1a;border-radius:6px;box-shadow:0 8px 30px rgba(0,0,0,.45);display:flex;flex-direction:column;overflow:hidden}'+
 '#pv .pvh{display:flex;align-items:center;gap:10px;padding:6px 10px;background:linear-gradient(#efe6d3,#e0d4ba);border-bottom:1px solid #b9a988}#pv .pvh b{font-size:17px;letter-spacing:.1em}#pv .pvs{font-size:12px;opacity:.6}'+
 '#pv .pvx{margin-left:auto;font-size:15px;padding:6px 14px;border:1px solid #8a6b3a;border-radius:4px;background:#2c3e5c;color:#fff;min-height:36px}'+
 '#pv .pvb{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:8px 10px}#pv .pvb>.pn:first-child{margin-top:0}'+
 'body.pv-open{overflow:hidden}#mdl{z-index:60}'+
 'body.sk-yoru #pv .pvw{background:#221d18;border-color:#5a5040}body.sk-yoru #pv .pvh{background:linear-gradient(#3a332a,#2c2620);color:#ece4d3}'+
 '@media (max-width:760px){#pv{padding:0}#pv .pvw{border-radius:0;border-left:0;border-right:0}#pv .pvs{display:none}#pv .pvb{padding:6px}}'+
 '</style>');
})();
