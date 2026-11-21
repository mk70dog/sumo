/* 見本 ws1〜ws3:部屋の画面の「弟子の様子」を見やすく。#ws1 力士タブと同じ札 / #ws2 小さな札 / #ws3 見やすい表 */
(function(){
const V=+((location.hash.match(/ws(\d)/)||[])[1]||1);window.WSV=V;
const _ot=ownTable;
function wk(r){return tourOn(r)?'巡業':MENU[r.inj&&r.inj.s>=2?'休':r.menu].n+'・'+INT[r.it].n;}
function rk(r){const pd=G.pend.includes(r.id);return pd?(r.tsuke?'付出予定':'前相撲'):r.rk;}
function bar(v,c){return '<span class="wsb"><i style="width:'+Math.round(cl(v,0,100))+'%;background:'+c+'"></i></span><span class="wsn">'+Math.round(v)+'</span>';}
ownTable=function(){const o=ownAll();if(!o.length||V===0)return _ot();
 if(V===1)return '<div class="cards">'+o.map(r=>cardHTML(r,G.pend.includes(r.id))).join('')+'</div>';
 if(V===2)return '<div class="wsg">'+o.map(r=>'<div class="wsc'+(r.d<=1?' sk':'')+'" onclick="showR('+r.id+')"><div class="wsr">'+esc(rk(r))+'</div><div class="wsnm">'+esc(r.n)+'</div><div class="wsx">総合 '+hyOW(r)+(injTag(r)||'')+(r.kad?'<span class="tag shu">角番</span>':'')+'</div>'+
  '<div class="wsl"><span>調子</span>'+bar(r.cond,'#9db8e8')+'</div><div class="wsl"><span>疲労</span>'+bar(r.fat,r.fat>75?'#e07a5a':'#8fbf8f')+'</div><div class="wsw">'+wk(r)+'</div></div>').join('')+'</div>';
 return '<div style="overflow-x:auto"><table class="tb wst"><tr><th>力士</th><th>総合</th><th>調子</th><th>疲労</th><th class="hide-s">今週の稽古</th><th>状態</th></tr>'+o.map((r,i)=>'<tr class="clk" onclick="showR('+r.id+')"><td><div class="wsr">'+esc(rk(r))+'</div><div class="wsnm">'+esc(r.n)+'</div></td><td class="num">'+hyOW(r)+'</td><td>'+bar(r.cond,'#9db8e8')+'</td><td>'+bar(r.fat,r.fat>75?'#e07a5a':'#8fbf8f')+'</td><td class="hide-s wsw">'+wk(r)+'</td><td>'+(injTag(r)||'<span class="mute">—</span>')+(r.kad?'<span class="tag shu">角番</span>':'')+'</td></tr>').join('')+'</table></div>';};
document.head.insertAdjacentHTML('beforeend','<style>'+
 '.wsb{display:inline-block;vertical-align:middle;width:80px;height:9px;border-radius:5px;background:rgba(127,127,127,.25);overflow:hidden}.wsb i{display:block;height:100%}.wsn{display:inline-block;width:2.2em;text-align:right;font-variant-numeric:tabular-nums;margin-left:4px;font-size:13px}'+
 '.wsg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}.wsc{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:8px 10px;cursor:pointer;background:rgba(127,127,127,.08)}.wsc.sk{border-color:#c9a24a}.wsc:hover{background:rgba(201,162,74,.12)}'+
 '.wsr{font-size:12px;color:#8fa9d8}.wsnm{font-family:Dela,sans-serif;font-size:19px;letter-spacing:.04em;line-height:1.25}.wsx{font-size:13px;margin:2px 0 4px}.wsl{display:flex;align-items:center;gap:6px;font-size:12px}.wsl>span:first-child{width:2.4em;opacity:.8}.wsw{font-size:12px;opacity:.75;margin-top:3px}'+
 '.wst td{padding-top:8px;padding-bottom:8px}.wst tr:nth-child(even) td{background:rgba(127,127,127,.07)}.wst .wsnm{font-size:17px}'+
 '</style>');
})();
