<script>
/* v132 画面:力士の画面に「ライバル」、本場所の取組に「因縁の一番」、記録の画面に「土俵の時代」 */
var RV_V=window.RV_V||1;
STK.rv=['#8a3a8a','競'];
function rvTag(a,o){const p=rvPair(a,o);if(!p)return '';const hh=(a.h2h&&a.h2h[o.id])||[0,0];return '<div class="rvt"><b>因縁の一番</b> ライバル('+RVK[p.k]+')・対戦 '+hh[0]+'勝'+hh[1]+'敗。両者とも気持ちが入ります。</div>';}
function rvRecent(r,o){const t=h2rOf(r,o);return t?t.split('').map(c=>c==='o'?'<span class="rvo">○</span>':'<span class="rvx">●</span>').join(''):'';}
function rvHTML(r){if(!r)return '';const L=rvOf(r);const E=(G.era||[]).filter(e=>e.a===r.id||e.b===r.id);if(!L.length&&!E.length)return '';
 const row=x=>{const o=G.R[x.a===r.id?x.b:x.a];if(!o)return '';const hh=(r.h2h&&r.h2h[o.id])||[0,0];
  if(RV_V===2)return '<tr><td class="nm clk2" onclick="showR('+o.id+')">'+esc(o.n)+'</td><td>'+esc(o.rkS||'')+'・'+esc(G.heya[o.h].n)+'</td><td class="wl">'+hh[0]+'勝'+hh[1]+'敗</td><td>'+rvRecent(r,o)+'</td><td class="mute" style="font-size:12px">'+RVK[x.k]+'</td></tr>';
  return '<div class="rvc"><div><b class="nm clk2" onclick="showR('+o.id+')">'+esc(o.n)+'</b> <span class="mute">'+esc(o.rkS||'')+'・'+esc(G.heya[o.h].n)+'部屋</span></div><div class="rvs">'+hh[0]+'<small>勝</small> '+hh[1]+'<small>敗</small></div><div>直近 '+(rvRecent(r,o)||'—')+'</div><div class="mute" style="font-size:12px">きっかけ:'+RVK[x.k]+'('+bname(x.b0)+'から)</div></div>';};
 return '<div class="rvp"><h3>ライバル</h3>'+(E.length?E.map(e=>'<p class="rve">🏯 「'+esc(e.n)+'」('+esc(e.an)+'・'+esc(e.bn)+')</p>').join(''):'')+(RV_V===2?'<table class="tb">'+L.map(row).join('')+'</table>':'<div class="rvg">'+L.map(row).join('')+'</div>')+'<p class="mute" style="font-size:12px;margin:4px 0">ライバルとの一番は両者とも気持ちが入り、気力に応じて少し強くなります。勝てば気力 +3、負ければ −2(推定)。</p></div>';}
const rvSR0=showR;showR=function(id){const x=rvSR0.apply(this,arguments);try{const r=G.R[id];const h=rvHTML(r);if(h)document.getElementById('mbox').insertAdjacentHTML('beforeend',h);}catch(e){}return x;};
function eraPanel(){const E=(G.era||[]).slice().reverse();if(!E.length)return '';
 return '<div class="pn"><h2>土俵の時代<span class="sub">横綱・大関のライバルが優勝を分け合った時代</span></h2><table class="tb">'+E.map(e=>'<tr><td class="nm">'+esc(e.n)+'</td><td>'+esc(e.an)+'・'+esc(e.bn)+'</td><td>'+esc(bname(e.b0))+'〜'+(e.b1&&e.b1!==e.b0?esc(bname(e.b1)):'')+'</td></tr>').join('')+'</table></div>';}
const rvK0=kirokuHTML;kirokuHTML=function(){const h=rvK0();const i=h.indexOf('<div class="grid2"><div class="pn"><h2>幕内優勝の歴史');return i<0?h+eraPanel():h.slice(0,i)+eraPanel()+h.slice(i);};
</script><style>
.rvt{font:13px sans-serif;background:#8a3a8a18;border-left:4px solid #8a3a8a;border-radius:4px;padding:3px 8px;margin:4px 0}
.rvg{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}.rvc{border:1px solid #8a3a8a66;border-radius:8px;padding:6px 8px;background:#fff8fd;color:#1a140c}.rvs{font:bold 22px serif;color:#8a3a8a}.rvs small{font-size:12px}
.rvo{color:#b5361f}.rvx{color:#333}.rve{background:#fff3cf;color:#1a140c;border-radius:6px;padding:4px 8px;margin:4px 0}
</style>
