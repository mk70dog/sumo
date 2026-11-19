# v87 -> v88:実在の部屋を選ぶ画面をすっきり(ダルマさん「ごちゃごちゃしているのでカッコよくする」→ 見本 hs1)
# 屋根の絵と大きな題字をやめ、上に黒と金の帯 1 本(もどる・題・並べ方・一門の選ぶ欄)。注意は赤い札、説明は 1 行の小さな字。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v87</title>', '<title>Grand Sumo Manager v88</title>')
rep("const APPV=87;\nconst SAVE='sumoManager87',SAVE86", "const APPV=88;\nconst SAVE='sumoManager88',SAVE87='sumoManager87',SAVE86")
rep('[SAVE86,SAVE85', '[SAVE87,SAVE86,SAVE85')
rep(" if(g.v===86){g.v=87;}\n return g.v===87?g:null;}", " if(g.v===86){g.v=87;}\n if(g.v===87){g.v=88;}\n return g.v===88?g:null;}")
rep('G={v:87,', 'G={v:88,')
# 屋根・題字・もどる・注意は、部屋選び(real)のときは出さない(帯の中に入れる)
rep("""function nightHTML(body){return '<div class="st-bg4"></div><div class="st-wrap'+(UI.start==='real'||UI.start==='dok'?' wide':'')+'"><div class="st-roof"><div class="r"></div><div class="m"></div><div class="f"><i></i><i></i><i></i><i></i></div></div>'+
 '<div class="st-h">Grand Sumo Manager</div><button class="st-back" onclick="goStart(null)">← 最初の画面にもどる</button>'+(G?'<p class="st-warn">""",
"""function nightHTML(body){if(UI.start==='real')return '<div class="st-bg4"></div><div class="st-wrap wide">'+body+'</div><div class="st-credit">背景:一恵斎芳幾「勧進大相撲土俵入之図」ほか(江戸〜明治の錦絵)</div>';
 return '<div class="st-bg4"></div><div class="st-wrap'+(UI.start==='dok'?' wide':'')+'"><div class="st-roof"><div class="r"></div><div class="m"></div><div class="f"><i></i><i></i><i></i><i></i></div></div>'+
 '<div class="st-h">Grand Sumo Manager</div><button class="st-back" onclick="goStart(null)">← 最初の画面にもどる</button>'+(G?'<p class="st-warn">""")
rep("""return '<p class="hlead">2026 年九州場所の番付(全 592 人・45 部屋)から始めます。部屋を押すと詳しい説明が出ます。<br>能力は番付と年齢からの推定です。これから起きる勝敗・けが・不祥事などは、すべてゲーム内の架空の出来事です。</p>'+
 '<div class="hbar"><b>並べ方</b>'+SO.map(x=>'<button class="hchip'+(so===x[0]?' on':'')+'" onclick="hsSet(\\'so\\',\\''+x[0]+'\\')">'+x[1]+'</button>').join('')+'</div>'+
 '<div class="hbar"><b>一門</b><button class="hchip'+(fi<0?' on':'')+'" onclick="hsSet(\\'fi\\',-1)">すべて</button>'+ICR.map((n,i)=>'<button class="hchip'+(fi===i?' on':'')+'" onclick="hsSet(\\'fi\\','+i+')">'+n+'</button>').join('')+'</div>'+""",
"""return '<div class="hsbar"><button class="bk" onclick="goStart(null)">← もどる</button><h2>実在の部屋を選ぶ</h2><span class="sl">'+
 '<select aria-label="並べ方" onchange="hsSet(\\'so\\',this.value)">'+SO.map(x=>'<option value="'+x[0]+'"'+(so===x[0]?' selected':'')+'>'+x[1]+'</option>').join('')+'</select>'+
 '<select aria-label="一門" onchange="hsSet(\\'fi\\',+this.value)"><option value="-1">一門:すべて</option>'+ICR.map((n,i)=>'<option value="'+i+'"'+(fi===i?' selected':'')+'>'+n+'一門</option>').join('')+'</select></span></div>'+
 (G?'<div class="hswarn">いまの保存データ('+esc(me().n)+'部屋)は消えて、新しく始まります。</div>':'')+
 '<div class="hsnote">2026 年九州場所の番付(592 人・45 部屋)から。部屋を押すと詳しい説明が出ます。能力は推定、これからの出来事はゲーム内の架空のものです。</div>'+""")
rep('</head>', '''<style>.hsbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(180deg,#141210,#2a2018);border:2px solid #c9a24a;border-radius:10px;padding:10px 14px;margin:12px 0 8px;color:#f3e7c9;position:relative;z-index:3}
.hsbar h2{margin:0;font-family:Dela,sans-serif;font-weight:400;color:#f0c75e;font-size:clamp(20px,3vw,30px);letter-spacing:.15em}
.hsbar .sl{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.hsbar select{font-size:15px;padding:6px 8px;border-radius:8px;border:1px solid #c9a24a;background:#1d1a16;color:#f3e7c9}
.hsbar .bk{background:transparent;border:1px solid #c9a24a;color:#f3e7c9;border-radius:20px;padding:6px 12px;font-size:14px;cursor:pointer}
.hswarn{display:inline-block;background:#b3261e;color:#fff;border-radius:14px;padding:3px 12px;font-size:13px;margin:2px 0 6px;position:relative;z-index:3}
.hsnote{font-size:12px;color:#d9ccb0;opacity:.9;margin:4px 2px 10px;position:relative;z-index:3}
@media(max-width:600px){.hsbar .sl{margin-left:0;width:100%}.hsbar select{flex:1;min-width:0}}
</style></head>''')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
