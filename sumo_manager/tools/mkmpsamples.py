# 見本 mp1〜mp2:マルチプレイ(2 台の iPad・GitHub Gist で受け渡し)の画面。mp0:つなぐ設定の画面
# v76 の本体に見本用の表示だけを足す(通信はしない)。
base=open('sumo_manager_v76.html',encoding='utf-8').read()
CSS='''<style>
.mpb{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:#1d2a3a;color:#fff;padding:6px 12px;font-size:13px}
.mpb .pl{display:flex;align-items:center;gap:6px;background:#ffffff1a;border-radius:14px;padding:2px 10px}
.mpb .dot{width:10px;height:10px;border-radius:50%;background:#888}.mpb .dot.ok{background:#5c5}.mpb .dot.wait{background:#fc4;animation:bl 1s infinite}
@keyframes bl{50%{opacity:.3}}
.mpc{border:2px solid var(--ai);border-radius:10px;padding:12px;margin:10px 0;background:#fffc}
.mpc h3{margin:0 0 8px}.mpg{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:600px){.mpg{grid-template-columns:1fr}}
.mpp{border:1px solid var(--line);border-radius:8px;padding:8px}.mpp b{color:var(--ai)}
.big{font-size:18px;padding:10px 18px}
.fm label{display:block;font-size:13px;margin:8px 0 2px}.fm input{width:100%;max-width:420px;font-size:15px;padding:6px;border:1px solid var(--line);border-radius:6px}
.code{font:bold 22px monospace;letter-spacing:3px;background:#f1e8d4;padding:4px 10px;border-radius:6px}
</style>'''
JS=r'''
<script>
(function(){
const V='__V__';
function bar(){const h='<div class="mpb"><b>対戦中:SUMO-7Q4K</b><span class="pl"><span class="dot ok"></span>木瀬部屋(あなた・親)準備できた</span><span class="pl"><span class="dot wait"></span>伊勢ノ海部屋(相手)稽古を決めています…</span><span style="margin-left:auto;opacity:.8">最後に受け取った時刻 14:52:10</span></div>';document.body.insertAdjacentHTML('afterbegin',h);}
function setup(){go('home');const pn=document.querySelector('.pn');pn.insertAdjacentHTML('beforebegin','<div class="mpc fm"><h3>ふたりで遊ぶ(GitHub でつなぐ)</h3><p class="kaku" style="font-size:13px">1 台が「親」になって世界を作り、もう 1 台は合言葉で参加します。データは GitHub の Gist(小さなファイル置き場)を通して受け渡します。</p>'+
 '<label>GitHub の鍵(gist だけ書ける鍵。この iPad の中だけに保存します)</label><input type="password" value="ghp_xxxxxxxxxxxxxxxxxxxx">'+
 '<div class="btns" style="margin-top:10px"><button class="btn ai big">親になって新しく始める</button><button class="btn big">合言葉で参加する</button></div>'+
 '<div class="mpg" style="margin-top:10px"><div class="mpp"><b>親(世界を作る人)</b><br>実名スタートで部屋を選ぶと、合言葉が出ます。<br>合言葉:<span class="code">SUMO-7Q4K</span><br><span class="mute" style="font-size:12px">LINE などで相手に伝えてください</span></div><div class="mpp"><b>子(参加する人)</b><br><label>合言葉</label><input value="SUMO-7Q4K"><br><span class="mute" style="font-size:12px">参加すると、親が選んでいない部屋から選べます</span></div></div></div>');}
function ready(){bar();go('home');const pn=document.querySelector('.pn');
 const h=V==='mp1'?'<div class="mpc"><h3>稽古 第 3 週:準備</h3><p class="kaku">稽古・作戦を決めたら「準備できた」を押します。ふたりとも押すと 1 週間進みます(10 分たつと、押していない側は前の週と同じ設定で進みます)。</p><div class="btns"><button class="btn main big">準備できた</button><button class="btn">取り消す</button></div></div>'
 :'<div class="mpc"><h3>今週のようす</h3><div class="mpg"><div class="mpp"><b>木瀬部屋(あなた)</b><br>稽古:申し合い中心・強さふつう<br>新弟子:1 人を勧誘中<br><span style="color:#2e7d4f;font-weight:bold">● 準備できた</span></div><div class="mpp"><b>伊勢ノ海部屋(相手)</b><br>関取 1 人・弟子 12 人<br>前の場所:藤ノ川 10 勝 5 敗<br><span style="color:#b5651d;font-weight:bold">● 稽古を決めています…</span></div></div><div class="btns" style="margin-top:8px"><button class="btn main big">準備できた(相手を待つ)</button></div><p class="mute kaku" style="font-size:12px">相手の部屋の能力の見立ては見えません(よその部屋と同じく、記者の見立てだけ)。</p></div>';
 pn.insertAdjacentHTML('beforebegin',h);}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;for(let i=0;i<2;i++)doWeek();if(V==='mp0')setup();else ready();}catch(e){console.error(e)}},400);});
})();
</script>
'''
NOTE={'mp0':'mp0:つなぐ設定(鍵・親になる・合言葉で参加)','mp1':'mp1:上に対戦の帯(ふたりの状態)+「準備できた」ボタン','mp2':'mp2:ふたりの部屋を並べたカード+「準備できた」'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'(通信はしません)</div></body>',1)
    s=s.replace('<title>Sumo Manager v76</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
