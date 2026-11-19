# 見本 hs1〜3:実在の部屋を選ぶ画面の上の部分をすっきり(ダルマさん「ごちゃごちゃしているのでカッコよくする サンプル x3」)。v87 に見本用の作りかえを足す。
base=open('sumo_manager_v87.html',encoding='utf-8').read()
CSS='''<style>
.xs-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(180deg,#141210,#2a2018);border:2px solid #c9a24a;border-radius:10px;padding:10px 14px;margin:10px 0;color:#f3e7c9;position:relative;z-index:3}
.xs-bar .ttl{font-family:Dela,sans-serif;color:#f0c75e;font-size:clamp(20px,3vw,30px);letter-spacing:.15em}
.xs-bar select{font-size:15px;padding:6px 8px;border-radius:8px;border:1px solid #c9a24a;background:#1d1a16;color:#f3e7c9}
.xs-bar .bk{background:transparent;border:1px solid #c9a24a;color:#f3e7c9;border-radius:20px;padding:6px 12px;font-size:14px}
.xs-warn{display:inline-block;background:#b3261e;color:#fff;border-radius:14px;padding:3px 12px;font-size:13px;margin:2px 0 6px}
.xs-note{font-size:12px;color:#d9ccb0;opacity:.85;margin:4px 2px 8px}
.xs-mini{display:inline-block;background:linear-gradient(180deg,#141210,#2a2018);border:2px solid #c9a24a;outline:1px solid #c9a24a;outline-offset:4px;padding:6px 26px;margin:14px auto 8px}
.xs-mini b{font-family:Dela,sans-serif;font-weight:400;font-size:clamp(28px,5vw,48px);letter-spacing:.2em;background:linear-gradient(180deg,#fff3c4,#e2b54a 55%,#a5741e);-webkit-background-clip:text;color:transparent}
.xs-chips{display:flex;gap:6px;overflow-x:auto;padding:4px 0;white-space:nowrap;scrollbar-width:none}
.xs-chips .hchip{font-size:13px!important;padding:5px 12px!important}
.xs-chips .sep{width:1px;background:#c9a24a;margin:0 6px;flex:none}
.xs-sticky{position:sticky;top:0;z-index:20;border-radius:0 0 10px 10px;margin-top:0}
details.xs-d{font-size:12px;color:#d9ccb0;margin:2px 0 8px}details.xs-d summary{cursor:pointer}
</style>'''
JS=r'''<script>
(function(){const V='__V__';
const SO=[['sk','関取の多い順'],['c','力士の多い順'],['est','歴史の古い順'],['money','お金の多い順']];
function sel(id,opts,cur,fn){return '<select onchange="'+fn+'">'+opts.map(o=>'<option value="'+o[0]+'"'+(String(cur)===String(o[0])?' selected':'')+'>'+o[1]+'</option>').join('')+'</select>';}
const R0=render0;render0=function(){R0();if(UI.start!=='real')return;const w=document.querySelector('.st-wrap');if(!w)return;
 const roof=w.querySelector('.st-roof'),h=w.querySelector('.st-h'),bk=w.querySelector('.st-back'),wn=w.querySelector('.st-warn'),ld=w.querySelector('.hlead'),bars=[...w.querySelectorAll('.hbar')];
 [roof,h,bk,ld].forEach(e=>e&&e.remove());bars.forEach(e=>e.remove());const wtxt=wn?wn.textContent:'';if(wn)wn.remove();
 const so=UI.hs.so,fi=UI.hs.fi;const soS=sel('so',SO,so,"hsSet('so',this.value)"),fiS=sel('fi',[[-1,'一門:すべて']].concat(ICR.map((n,i)=>[i,n+'一門'])),fi,"hsSet('fi',+this.value)");
 const note='2026 年九州場所の番付(592 人・45 部屋)から。能力は推定、これからの出来事はゲーム内の架空のものです。';
 const grid=w.querySelector('.hgrid');let top='';
 if(V==='hs1')top='<div class="xs-bar"><button class="bk" onclick="goStart(null)">← もどる</button><span class="ttl">実在の部屋を選ぶ</span><span style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap">'+soS+fiS+'</span></div>'+(wtxt?'<div class="xs-warn">'+wtxt+'</div>':'')+'<div class="xs-note">'+note+'</div>';
 if(V==='hs2'){const chips=SO.map(x=>'<button class="hchip'+(so===x[0]?' on':'')+'" onclick="hsSet(\'so\',\''+x[0]+'\')">'+x[1]+'</button>').join('')+'<span class="sep"></span><button class="hchip'+(fi<0?' on':'')+'" onclick="hsSet(\'fi\',-1)">すべて</button>'+ICR.map((n,i)=>'<button class="hchip'+(fi===i?' on':'')+'" onclick="hsSet(\'fi\','+i+')">'+n+'</button>').join('');
  top='<div style="text-align:center"><div class="xs-mini"><b>部屋を選ぶ</b></div><div><button class="st-back" onclick="goStart(null)" style="position:static">← 最初の画面にもどる</button></div>'+(wtxt?'<div class="xs-warn">'+wtxt+'</div>':'')+'</div><div class="xs-chips">'+chips+'</div><details class="xs-d"><summary>この画面について</summary>'+note+' 部屋を押すと詳しい説明が出ます。</details>';}
 if(V==='hs3')top='<div class="xs-bar xs-sticky"><button class="bk" onclick="goStart(null)">←</button><span class="ttl">部屋を選ぶ</span><span style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap">'+soS+fiS+'</span></div>'+(wtxt?'<div style="text-align:center"><div class="xs-warn">⚠ '+wtxt+'</div></div>':'');
 grid.insertAdjacentHTML('beforebegin',top);if(V==='hs3')grid.insertAdjacentHTML('afterend','<div class="xs-note" style="text-align:center;margin-top:12px">'+note+'</div>');};
window.addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');save();UI.title=true;goStart('real');}catch(e){console.error(e)}},300));})();
</script>'''
NOTE={'hs1':'hs1:上に黒と金の帯 1 本(もどる・題・並べ方と一門は選ぶ欄)','hs2':'hs2:小さな題字の札+並べ方と一門を 1 列の小さな札に、説明は「この画面について」に畳む','hs3':'hs3:上に固定の細い帯(スクロールしても残る)、説明はいちばん下'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'</div></body>',1).replace('<title>Grand Sumo Manager v87</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
