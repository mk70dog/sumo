<script>
/* 見本 os1〜os3:注目選手を 3 人まで。#os1〜#os3 で切りかえ */
function osV(){const m=(location.hash||'').match(/os(\d)/);return m?+m[1]:1;}
function oshiIds(){let a=G.oshi;if(a==null)a=[];if(!Array.isArray(a))a=[a];return a.filter(id=>{const r=G.R[id];return r&&!r.ret&&r.h===ME();}).slice(0,3);}
function oshiL(){const a=oshiIds().map(id=>G.R[id]);if(!a.length){const t=heyaTop();if(t)a.push(t);}return a;}
oshiR=function(){return oshiL()[0]||null;};
function isOshi(r){return oshiL().some(x=>x.id===r.id);}
function osDots(r){return '<span class="osd">'+oshiItems(r).map(x=>'<i class="d'+x.c+'" title="'+esc(x.lb+':'+x.t)+'"></i>').join('')+'</span>';}
function osHot(r){const L=oshiItems(r).filter(x=>x.c==='p'||x.c==='n');return L.length?'<div class="otg">'+L.map(x=>'<span class="otag s'+x.c+'">'+x.lb+':'+esc(x.t)+'</span>').join('')+'</div>':'<div class="mute" style="font-size:11px">まわりは落ち着いています</div>';}
function osHead(){return '<div class="hbk">★ 注目選手 <small>'+oshiL().length+'/3 人</small><button class="chg" onclick="oshiPick()">選ぶ</button></div>';}
function osCard1(){return '<div class="hbp hbo">'+osHead()+oshiL().map((r,i)=>'<div class="osc"><h3><span class="osn">'+'①②③'[i]+'</span><a onclick="showR('+r.id+')">'+esc(r.n)+'</a><small>'+esc(r.rk)+'・'+Math.floor(r.age)+' 歳</small></h3><div class="hbg">'+oshiGoal(r)+'</div>'+osHot(r)+'</div>').join('')+'</div>';}
let OS_TAB=0;
function osCard2(){const L=oshiL();const k=Math.min(OS_TAB,L.length-1);const r=L[k];return '<div class="hbp hbo">'+osHead()+'<div class="ostab">'+L.map((x,i)=>'<button class="'+(i===k?'on':'')+'" onclick="OS_TAB='+i+';render()">'+esc(x.n)+'</button>').join('')+'</div><h3><a onclick="showR('+r.id+')">'+esc(r.n)+'</a><small>'+esc(r.rk)+'・'+Math.floor(r.age)+' 歳</small></h3><div class="hbg">'+oshiGoal(r)+'</div>'+oshiTags(r)+'</div>';}
function osCard3(){return '<div class="hbp hbo">'+osHead()+oshiL().map((r,i)=>'<div class="osr" onclick="showR('+r.id+')"><div><b>'+esc(r.n)+'</b> <small>'+esc(r.rk)+'</small>'+osDots(r)+'</div><div class="hbg">'+oshiGoal(r)+'</div></div>').join('')+'<div class="osleg"><i class="dp"></i>追い風 <i class="dn"></i>向かい風 <i class="dm"></i>ふつう(6 項目)</div></div>';}
hbOshi=function(){return [osCard1,osCard2,osCard3][osV()-1]();};
oshiPick=function(){const o=own().slice().sort((a,b)=>a.pos-b.pos);const cur=oshiIds();
 openM('<h2>注目選手を選ぶ(3 人まで)</h2><p class="kaku mute">追いかけたい力士を 3 人まで選びます。押した順に ①②③ になります。成績には影響しません。</p><div class="opl">'+o.map(r=>{const i=cur.indexOf(r.id);return '<button class="btn'+(i>=0?' main':'')+'" onclick="osTog('+r.id+')">'+(i>=0?'①②③'[i]+' ':'')+esc(r.n)+' <small>'+esc(r.rkS)+'</small></button>';}).join('')+'</div><div class="row" style="margin-top:10px"><button class="btn" onclick="G.oshi=null;save();closeM();render()">部屋頭だけにもどす(自動)</button><button class="btn" onclick="closeM()">閉じる</button></div>');};
function osTog(id){let a=oshiIds();const i=a.indexOf(id);if(i>=0)a.splice(i,1);else{if(a.length>=3){toast('注目選手は 3 人までです');return;}a.push(id);}G.oshi=a.length?a:null;save();oshiPick();render();}
addEventListener('hashchange',()=>render());
addEventListener('load',()=>{setTimeout(()=>{try{const o=own().slice().sort((a,b)=>a.pos-b.pos);G.oshi=[o[0].id,o[3].id,o[8].id];render();}catch(e){}},50);});
</script>
<style>
.osc{border-top:1px dashed rgba(120,80,40,.3);padding-top:4px;margin-top:4px}.osc:first-of-type{border-top:none}
.osn{color:#9a2b1d;margin-right:4px}.osc h3{font-size:15px;margin:0}.osc .hbg{margin:2px 0}
.ostab{display:flex;gap:4px;margin:2px 0 6px}.ostab button{flex:1;font-size:12px;padding:3px 4px;border:1px solid rgba(120,80,40,.4);background:#f3ead6;border-radius:5px}.ostab button.on{background:#9a2b1d;color:#fff}
.osr{padding:5px 0;border-top:1px dashed rgba(120,80,40,.3);cursor:pointer}.osr:first-of-type{border-top:none}
.osd{margin-left:6px}.osd i,.osleg i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:2px;vertical-align:middle;border:1px solid #8a7a66}
.osd i.dp,.osleg i.dp{background:#c0392b;border-color:#c0392b}.osd i.dn,.osleg i.dn{background:#2c3e5c;border-color:#2c3e5c}.osd i.dm,.osleg i.dm{background:#fff}
.osleg{font-size:10px;color:#6b5a48;margin-top:4px}
</style>
