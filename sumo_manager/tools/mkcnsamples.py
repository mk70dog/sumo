# 見本 cn1〜cn3:二人相撲のつながり具合の見せ方(v121 の本体に見本用の表示を足す。通信はしない)
# どの見本も、部屋の画面の「今週のようす」に「相手を待つ時間」と「待たずに進める」を足す。
# 使い方:cd sumo_manager; python3 tools/mkcnsamples.py
base=open('sumo_manager_v121.html',encoding='utf-8').read()
COMMON=r'''
const CN={ok:{c:'#5c5',t:'つながっています',d:'5 秒ごとに相手のようすを受け取っています。'},
 slow:{c:'#fc4',t:'つながりにくい(2 分前から)',d:'受け取りに 3 回失敗しました。30 秒ごとにやり直しています。'},
 off:{c:'#f66',t:'切れています',d:'ネットにつながっていません。電波が戻ると、すぐに受け取り直します。'},
 key:{c:'#f66',t:'GitHub の鍵が使えません',d:'鍵の期限が切れたか、消されたようです。⚙ 設定で鍵を入れ直してください。'},
 away:{c:'#fc4',t:'親の iPad が開いていないようです',d:'親の iPad から 7 分なにも届いていません。親の iPad で二人相撲の画面を開いてもらってください。'}};
window.__cn='ok';
function cnPl(){return '<span class="pl"><span class="dot ok"></span>木瀬部屋(親) 準備できた</span><span class="pl"><span class="dot wait"></span>伊勢ノ海部屋(子) 決めています…</span>';}
function cnWait(){return '<div class="mpc cnw"><h3>今週のようす</h3><div class="mpg"><div class="mpp"><b>木瀬部屋(親)</b><br>関取 4 人・弟子 20 人・資金 2780万円<br><span class="ok2">● 準備できた(1 週間を過ごす)</span></div><div class="mpp"><b>伊勢ノ海部屋(子)</b><br>関取 1 人・弟子 12 人・資金 1650万円<br><span class="wt2">● 決めています…(4 分 10 秒)</span></div></div>'+
 '<div class="cnrow"><b>相手を待つ時間</b>'+['5 分','10 分','30 分','待たない'].map((x,i)=>'<button class="pc'+(i===1?' on':'')+'">'+(i===1?'✓ ':'')+x+'</button>').join('')+'<span class="mute">あと 5 分 50 秒で、子は前の週と同じ設定のまま進みます</span></div>'+
 '<div class="btns"><button class="btn">準備を取り消す</button><button class="btn main">待たずに進める</button></div></div>';}
function cnMount(){document.querySelectorAll('.mpb,.cnx,.mpc,.cnpop').forEach(e=>e.remove());const app=document.querySelector('#app');app.insertAdjacentHTML('afterbegin',cnBar(window.__cn));
 const p=app.querySelector(':scope > .oc')||app.querySelector(':scope > .pn')||app.querySelector('.hbout');if(p)p.insertAdjacentHTML('afterend',cnWait());}
window.__set=s=>{window.__cn=s;cnMount();};
'''
V={
'cn1':('案1:帯の左に状態の札(色の丸+言葉)。うまくいかないときは帯の下に細い帯でわけと、すること',r'''
function cnBar(s){const x=CN[s];const bad=s!=='ok';
 return '<div class="mpb"><span class="cnst" style="border-color:'+x.c+'"><span class="cd" style="background:'+x.c+'"></span>'+x.t+'</span><b>二人相撲</b>'+cnPl()+'<span class="mpt">受け取り 14:52:10</span></div>'+
 (bad?'<div class="cnx" style="border-left-color:'+x.c+'">'+x.d+(s==='slow'||s==='off'?' <button class="btn sm">今すぐやり直す</button>':'')+(s==='key'?' <button class="btn sm">⚙ 設定を開く</button>':'')+'</div>':'');}
''','''.cnst{display:inline-flex;align-items:center;gap:6px;border:2px solid;border-radius:14px;padding:1px 10px;font-weight:bold;background:#0006}.cnst .cd{width:10px;height:10px;border-radius:50%}
.cnx{background:#2b2116;color:#f3e7c9;border-left:6px solid;padding:6px 12px;font:13px sans-serif;position:relative;z-index:59}.cnx .btn{margin-left:8px}'''),
'cn2':('案2:帯の色そのものが変わる(緑・黄・赤の太い線)。右に「最後に受け取ったのは○分前」',r'''
function cnBar(s){const x=CN[s];
 return '<div class="mpb cn2" style="border-bottom:5px solid '+x.c+'"><b>二人相撲</b>'+cnPl()+'<span class="cn2t" style="color:'+x.c+'">● '+x.t+'</span><span class="mpt">最後に受け取ったのは '+(s==='ok'?'3 秒前':s==='away'?'7 分前':'2 分前')+'</span></div>'+
 (s==='ok'?'':'<div class="cnx">'+x.d+'</div>');}
''','''.mpb.cn2 .cn2t{font-weight:bold}.cnx{background:#2b2116;color:#f3e7c9;padding:5px 12px;font:13px sans-serif;position:relative;z-index:59}'''),
'cn3':('案3:帯には色の丸だけ。押すと「つながり」のまど(状態・わけ・最後に受け取った時刻・やり直す)',r'''
function cnBar(s){const x=CN[s];
 return '<div class="mpb"><button class="cn3b" onclick="cnPop()"><span class="cd" style="background:'+x.c+'"></span>'+(s==='ok'?'':'!')+'</button><b>二人相撲</b>'+cnPl()+'<span class="mpt">受け取り 14:52:10</span></div>';}
function cnPop(){const x=CN[window.__cn];document.querySelectorAll('.cnpop').forEach(e=>e.remove());
 document.body.insertAdjacentHTML('beforeend','<div class="cnpop"><h3><span class="cd" style="background:'+x.c+'"></span>'+x.t+'</h3><p>'+x.d+'</p><p class="mute">最後に受け取った時刻 14:52:10<br>合言葉 a1b2c3d4…</p><div class="btns"><button class="btn main">今すぐやり直す</button><button class="btn" onclick="this.closest(\'.cnpop\').remove()">閉じる</button></div></div>');}
''','''.cn3b{width:30px;height:30px;border-radius:50%;border:2px solid #fff6;background:#0006;color:#fff;font-weight:bold;display:inline-flex;align-items:center;justify-content:center;gap:2px;padding:0}.cn3b .cd{width:12px;height:12px;border-radius:50%}
.cnpop{position:fixed;left:50%;top:90px;transform:translateX(-50%);width:min(92vw,440px);background:#f3e7c9;color:#1a140c;border:2px solid #c9a24a;border-radius:12px;padding:14px 16px;z-index:9000;font:14px sans-serif;box-shadow:0 8px 30px #000a}.cnpop h3{display:flex;align-items:center;gap:8px;margin:0 0 6px}.cnpop .cd{width:14px;height:14px;border-radius:50%;display:inline-block}'''),
}
CSS='''.cnrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 8px;font:14px sans-serif}.cnrow .pc{font-size:15px;padding:6px 14px;border-radius:18px;border:2px solid #8a7040;background:#fff;color:#1a140c}.cnrow .pc.on{background:#7a1d10;border-color:#7a1d10;color:#fff;font-weight:bold}.cnrow .mute{font-size:12px}'''
for k,(note,js,css) in V.items():
    inj='<script>'+COMMON+js+'''
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;UI.view='home';render();cnMount();}catch(e){console.error(e)}},500);});
</script><style>'''+CSS+css+'''</style><div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 '''+k+''':'''+note+'''(通信はしません)</div>'''
    s=base.replace('</body>\n</html>',inj+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v121</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
