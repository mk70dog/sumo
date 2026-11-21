# 見本 sbp1〜sbp3:二人相撲の「勝負の形」を選ぶ画面を、わかりやすくする案(v102 の本体に見本用の sbPanel を上書き)
# 使い方:cd sumo_manager; python3 tools/mksbpicksamples.py
base=open('sumo_manager_v102.html',encoding='utf-8').read()
COMMON=r'''
const SBX={1:{ic:'点',nm:'点数勝負',one:'期間内に点数を多く取ったほうの勝ち'},2:{ic:'旗',nm:'目標レース',one:'目標に先に届いたほうの勝ち'},3:{ic:'番',nm:'部屋番付',one:'場所ごとに順位。終わりなし'},4:{ic:'録',nm:'記録だけ',one:'勝ち負けなし。成績を並べる'}};
function sbSum(o){if(o.k===1)return o.y+' 年('+o.y*6+' 場所)たったとき、点数の多いほうが勝ち。<br>点数の例:関取 1 人 1 点・横綱 5 点・幕内優勝 10 点・新入幕 3 点(場所ごと)';
 if(o.k===2)return '「'+SB_GOAL[o.g]+'」に先に届いたほうが勝ち。<br>届いた時点でお知らせ。そのあとも続けられます。';
 if(o.k===3)return '場所が終わるたびに、ふたりの部屋の格をくらべて 1 位・2 位。<br>通算で 1 位を取った回数を競います。終わりはありません。';
 return '勝ち負けはつけません。<br>場所ごとの関取の数と最高位を、記録の画面に並べるだけです。';}
function sbOpts(o,cls){if(o.k===1)return '<div class="'+cls+'"><span class="lb">期間</span>'+[5,10,20].map(y=>'<button class="pc'+(o.y===y?' on':'')+'" onclick="sbSet(\'y\','+y+')">'+(o.y===y?'✓ ':'')+y+' 年</button>').join('')+'</div>';
 if(o.k===2)return '<div class="'+cls+'"><span class="lb">目標</span>'+Object.keys(SB_GOAL).map(g=>'<button class="pc'+(o.g===g?' on':'')+'" onclick="sbSet(\'g\',\''+g+'\')">'+(o.g===g?'✓ ':'')+SB_GOAL[g].replace('自分の部屋から','')+'</button>').join('')+'</div>';
 return '';}
'''
V={
'sbp1':('案1:4 つを横に並べたタイル。選んだタイルは金色にぬる。下に「選んだ形」のまとめと細かい設定',r'''
sbPanel=function(){const o=UI.mpSb;
 return '<div class="sbpick sx1"><div class="hd"><span class="no">1</span>勝負の形を選ぶ<small>親が決めます。子の画面にも出ます</small></div>'+
 '<div class="tiles">'+[1,2,3,4].map(k=>'<button class="tile'+(o.k===k?' on':'')+'" onclick="sbSet(\'k\','+k+')"><i>'+SBX[k].ic+'</i><b>'+SBX[k].nm+'</b><small>'+SBX[k].one+'</small>'+(o.k===k?'<em>選択中</em>':'')+'</button>').join('')+'</div>'+
 '<div class="sumbox"><div class="hd2">選んだ形:<b>'+SBX[o.k].nm+'</b></div>'+sbOpts(o,'opts')+'<div class="sum">'+sbSum(o)+'</div></div>'+
 '<div class="hd"><span class="no">2</span>始め方を選ぶ<small>下のボタン</small></div></div>';};
''','''
.sx1{background:rgba(16,12,8,.94)!important;padding:14px 18px!important}
.sx1 .hd{font:bold 20px sans-serif;color:#ffe9a8;display:flex;align-items:center;gap:10px;margin:4px 0 10px}.sx1 .hd small{font-size:13px;color:#d8c9a4;font-weight:normal}
.sx1 .no{display:inline-flex;width:30px;height:30px;border-radius:50%;background:#c9a24a;color:#1a140c;align-items:center;justify-content:center;font-size:17px}
.sx1 .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}@media(max-width:700px){.sx1 .tiles{grid-template-columns:1fr 1fr}}
.sx1 .tile{position:relative;background:#2a2116;border:2px solid #6b5630;border-radius:12px;color:#e9dcc0;padding:14px 8px;text-align:center;cursor:pointer}
.sx1 .tile i{display:block;font:bold 34px serif;font-style:normal;color:#c9a24a;margin-bottom:4px}.sx1 .tile b{display:block;font-size:19px}.sx1 .tile small{display:block;font-size:12px;opacity:.85;margin-top:4px}
.sx1 .tile.on{background:linear-gradient(#f4d37c,#c9a24a);border-color:#fff3c4;color:#1a140c;box-shadow:0 0 0 3px #ffe9a855,0 4px 14px #0008}.sx1 .tile.on i{color:#7a1d10}
.sx1 .tile em{position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:#7a1d10;color:#fff;font:bold 12px sans-serif;font-style:normal;padding:2px 10px;border-radius:10px}
.sx1 .sumbox{margin:12px 0 6px;background:#f3e7c9;color:#1a140c;border-radius:10px;padding:12px 16px}.sx1 .hd2{font-size:16px;margin-bottom:6px}.sx1 .sum{font-size:14px;line-height:1.7}
.sx1 .opts{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 8px}.sx1 .lb{font-weight:bold;margin-right:4px}
.sx1 .pc{font-size:16px;padding:8px 16px;border-radius:20px;border:2px solid #8a7040;background:#fff;color:#1a140c}.sx1 .pc.on{background:#7a1d10;border-color:#7a1d10;color:#fff;font-weight:bold}
'''),
'sbp2':('案2:縦の一覧のまま。選んだ行だけ明るい紙の色にして大きく開き、ほかは 1 行にたたむ',r'''
sbPanel=function(){const o=UI.mpSb;
 return '<div class="sbpick sx2"><div class="hd">勝負の形を選ぶ<small>親が決めます。子の画面にも出ます</small></div>'+[1,2,3,4].map(k=>o.k===k?
  '<div class="row on"><div class="t"><span class="rd">●</span><b>'+SBX[k].nm+'</b><span class="cur">選択中</span></div>'+sbOpts(o,'opts')+'<div class="sum">'+sbSum(o)+'</div></div>':
  '<button class="row" onclick="sbSet(\'k\','+k+')"><span class="rd">○</span><b>'+SBX[k].nm+'</b><small>'+SBX[k].one+'</small><span class="go">選ぶ ›</span></button>').join('')+
 '<div class="sbnx">↓ 形が決まったら、下の「実在の部屋で始める」か「独立して始める」を押します</div></div>';};
''','''
.sx2{background:rgba(16,12,8,.94)!important;padding:14px 18px!important}
.sx2 .hd{font:bold 20px sans-serif;color:#ffe9a8;margin:2px 0 10px}.sx2 .hd small{font-size:13px;color:#d8c9a4;font-weight:normal;margin-left:10px}
.sx2 .row{display:flex;align-items:center;gap:10px;width:100%;background:#2a2116;border:1px solid #6b5630;border-radius:10px;color:#e9dcc0;padding:10px 14px;margin:6px 0;text-align:left;font:15px sans-serif;cursor:pointer}
.sx2 .row b{font-size:18px;min-width:7em}.sx2 .row small{font-size:13px;opacity:.8;flex:1}.sx2 .row .go{color:#c9a24a;font-weight:bold}.sx2 .rd{font-size:20px;color:#c9a24a}
.sx2 .row.on{display:block;background:#f3e7c9;color:#1a140c;border:3px solid #c9a24a;padding:12px 16px;cursor:default}
.sx2 .row.on .t{display:flex;align-items:center;gap:10px}.sx2 .row.on b{font-size:22px}.sx2 .row.on .rd{color:#7a1d10}
.sx2 .cur{background:#7a1d10;color:#fff;font:bold 12px sans-serif;padding:2px 10px;border-radius:10px}
.sx2 .opts{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 8px}.sx2 .lb{font-weight:bold}
.sx2 .pc{font-size:16px;padding:8px 16px;border-radius:20px;border:2px solid #8a7040;background:#fff;color:#1a140c}.sx2 .pc.on{background:#7a1d10;border-color:#7a1d10;color:#fff;font-weight:bold}
.sx2 .sum{font-size:14px;line-height:1.7;border-top:1px dashed #b89c5c;padding-top:8px}
.sx2 .sbnx{margin-top:8px;color:#ffe9a8;font-size:14px;text-align:center}
'''),
'sbp3':('案3:左に 4 つのボタン、右に選んだ形の説明と絵(勝ち方の図)。番号つきの手順で「次に押すところ」を示す',r'''
function sbPic(o){if(o.k===1)return '<div class="pic"><div class="bar a" style="width:78%">木瀬 156 点</div><div class="bar b" style="width:62%">伊勢ノ海 124 点</div><div class="cap">'+o.y+' 年後に多いほうが勝ち</div></div>';
 if(o.k===2)return '<div class="pic"><div class="rail"><span>スタート</span><span>…</span><span class="gl">🏁 '+SB_GOAL[o.g].replace('自分の部屋から','')+'</span></div><div class="cap">先に旗に届いたほうが勝ち</div></div>';
 if(o.k===3)return '<div class="pic"><div class="rk"><b>1 位</b> 木瀬部屋</div><div class="rk">2 位 伊勢ノ海部屋</div><div class="cap">場所ごとに入れかわる</div></div>';
 return '<div class="pic"><div class="cap">表に並べるだけ</div></div>';}
sbPanel=function(){const o=UI.mpSb;
 return '<div class="sbpick sx3"><div class="steps"><span class="s on">① 勝負の形</span><span class="ar">›</span><span class="s">② 始め方(下のボタン)</span><span class="ar">›</span><span class="s">③ 部屋を選ぶ</span></div>'+
 '<div class="cols"><div class="left">'+[1,2,3,4].map(k=>'<button class="pk'+(o.k===k?' on':'')+'" onclick="sbSet(\'k\','+k+')"><i>'+SBX[k].ic+'</i><span><b>'+SBX[k].nm+'</b><small>'+SBX[k].one+'</small></span></button>').join('')+'</div>'+
 '<div class="right"><div class="ttl">'+SBX[o.k].nm+'</div>'+sbOpts(o,'opts')+sbPic(o)+'<div class="sum">'+sbSum(o)+'</div></div></div></div>';};
''','''
.sx3{background:rgba(16,12,8,.94)!important;padding:14px 18px!important}
.sx3 .steps{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:12px;font:14px sans-serif}.sx3 .s{padding:4px 12px;border-radius:14px;background:#2a2116;color:#bfae88}.sx3 .s.on{background:#c9a24a;color:#1a140c;font-weight:bold}.sx3 .ar{color:#8a7040}
.sx3 .cols{display:grid;grid-template-columns:minmax(220px,1fr) 1.6fr;gap:14px}@media(max-width:700px){.sx3 .cols{grid-template-columns:1fr}}
.sx3 .pk{display:flex;align-items:center;gap:10px;width:100%;background:#2a2116;border:2px solid #6b5630;border-radius:10px;color:#e9dcc0;padding:10px;margin:0 0 8px;text-align:left;cursor:pointer}
.sx3 .pk i{font:bold 26px serif;font-style:normal;color:#c9a24a;width:38px;height:38px;display:flex;align-items:center;justify-content:center;border:2px solid #c9a24a;border-radius:8px;flex:none}
.sx3 .pk b{display:block;font-size:18px}.sx3 .pk small{display:block;font-size:12px;opacity:.8}
.sx3 .pk.on{background:linear-gradient(#f4d37c,#c9a24a);border-color:#fff3c4;color:#1a140c}.sx3 .pk.on i{color:#7a1d10;border-color:#7a1d10;background:#fff8e0}
.sx3 .right{background:#f3e7c9;color:#1a140c;border-radius:12px;padding:14px 16px}.sx3 .ttl{font:bold 22px sans-serif;margin-bottom:6px}
.sx3 .opts{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 10px}.sx3 .lb{font-weight:bold}
.sx3 .pc{font-size:16px;padding:8px 16px;border-radius:20px;border:2px solid #8a7040;background:#fff;color:#1a140c}.sx3 .pc.on{background:#7a1d10;border-color:#7a1d10;color:#fff;font-weight:bold}
.sx3 .pic{background:#fff;border-radius:8px;padding:10px;margin-bottom:8px;font:13px sans-serif}.sx3 .bar{font:bold 12px sans-serif!important;line-height:18px!important;color:#fff!important;padding:3px 8px;border-radius:4px;margin:3px 0;white-space:nowrap}.sx3 .bar.a{background:#b5391f}.sx3 .bar.b{background:#3b7fc4}
.sx3 .cap{color:#666;font-size:12px;margin-top:4px}.sx3 .rail{display:flex;justify-content:space-between;border-bottom:4px solid #c9a24a;padding-bottom:4px}.sx3 .gl{font-weight:bold;color:#7a1d10}
.sx3 .rk{padding:3px 8px;border-bottom:1px solid #eee}.sx3 .sum{font-size:14px;line-height:1.7}
'''),
}
for k,(note,js,css) in V.items():
    css=css+'''
.sbpick .pc{display:inline-block!important;width:auto!important;flex:none!important;margin:0!important;font:16px sans-serif!important;line-height:1.3!important;white-space:nowrap}
.sbpick .lb{background:none!important;border:0!important;padding:0!important;font:bold 15px sans-serif!important;color:inherit!important}
.sbpick .tile,.sbpick .pk,.sbpick .row{font-family:sans-serif!important}
'''
    inj='<script>'+COMMON+js+'''
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();UI.mpSb={k:1,y:10,g:'yok'};const b=document.querySelector('.st-two');if(b)b.click();window.__set=(k,y,g)=>{UI.mpSb={k:k,y:y||10,g:g||'yok'};render();};}catch(e){console.error(e)}},500);});
</script><style>'''+css+'''</style><div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 '''+k+''':'''+note+'''</div>'''
    s=base.replace('</body>\n</html>',inj+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v102</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
