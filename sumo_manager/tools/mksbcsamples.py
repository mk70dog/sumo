# 見本 sbc1〜sbc2:勝負の形を選ぶ画面に「点の数え方」(育てた力士だけ/全員)を足す案(v120 の本体に見本用の表示を足す)
# 使い方:cd sumo_manager; python3 tools/mksbcsamples.py
base=open('sumo_manager_v120.html',encoding='utf-8').read()
JS=r'''
UI.mpSb.c=UI.mpSb.c||'ik';
const SBC_T={ik:'育てた力士だけ',all:'全員'};
const SBC_D={ik:'始めたときに幕下以下だった力士と、そのあと入った力士だけを数えます。始めからいる関取・横綱の点は入りません。大きな部屋とも対等に競えます。',all:'始めからいる関取・横綱も数えます。始めの部屋の強さの差がそのまま点に出ます。'};
function sbcChips(o){return ['ik','all'].map(c=>'<button class="pc'+(o.c===c?' on':'')+'" onclick="sbSet(\'c\',\''+c+'\')">'+(o.c===c?'✓ ':'')+SBC_T[c]+(c==='ik'?'(おすすめ)':'')+'</button>').join('');}
const sbO0=sbOpts;
'''
V={
'sbc1':('案1:「選んだ形」の欄の中に、期間・目標の下に 1 行足す',r'''
sbOpts=function(o,cls){let h=sbO0(o,cls);if(o.k===4)return h;return h+'<div class="'+cls+'"><span class="lb">点の数え方</span>'+sbcChips(o)+'</div><div class="sbcd">'+SBC_D[o.c]+'</div>';};
''','''.sbcd{font-size:13px;color:#5a4a30;margin:-2px 0 8px;line-height:1.6}'''),
'sbc2':('案2:タイルの下に「点の数え方」を別の欄で(2 つの大きな札から選ぶ)',r'''
const sbP0=sbPanel;sbPanel=function(){let h=sbP0();const o=UI.mpSb;if(o.k===4)return h;
 const card=c=>'<button class="sbcc'+(o.c===c?' on':'')+'" onclick="sbSet(\'c\',\''+c+'\')"><b>'+(o.c===c?'◉ ':'○ ')+SBC_T[c]+(c==='ik'?' <em>おすすめ</em>':'')+'</b><small>'+SBC_D[c]+'</small></button>';
 const box='<div class="sbcbox"><div class="hd3">点の数え方</div><div class="sbcg">'+card('ik')+card('all')+'</div></div>';
 const i=h.indexOf('<div class="hd"><span class="no">2</span>');return i<0?h:h.slice(0,i)+box+h.slice(i);};
''','''.sbcbox{margin:4px 0 10px}.sbcbox .hd3{font:bold 16px sans-serif;color:#ffe9a8;margin:2px 0 6px}
.sbcg{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:700px){.sbcg{grid-template-columns:1fr}}
.sbcc{display:block!important;width:100%!important;text-align:left!important;background:#2a2116!important;border:2px solid #6b5630!important;border-radius:10px!important;color:#e9dcc0!important;padding:10px 12px!important;font-family:sans-serif!important;cursor:pointer}
.sbcc b{display:block;font-size:17px}.sbcc em{font-style:normal;font-size:11px;background:#7a1d10;color:#fff;padding:1px 8px;border-radius:9px;margin-left:4px;vertical-align:middle}.sbcc small{display:block;font-size:12px;opacity:.85;margin-top:4px;line-height:1.5}
.sbcc.on{background:#f3e7c9!important;border-color:#c9a24a!important;color:#1a140c!important}'''),
}
for k,(note,js,css) in V.items():
    inj='<script>'+JS+js+'''
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();UI.mpSb={k:1,y:10,g:'yok',c:'ik'};const b=document.querySelector('.st-two');if(b)b.click();window.__set=(k,c)=>{UI.mpSb={k:k,y:10,g:'yu3',c:c||'ik'};render();};}catch(e){console.error(e)}},500);});
</script><style>'''+css+'''</style><div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 '''+k+''':'''+note+'''</div>'''
    s=base.replace('</body>\n</html>',inj+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v120</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
