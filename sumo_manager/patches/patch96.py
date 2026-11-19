# v92 -> v93:「部屋付き親方として独立する」画面の上部を、実在の部屋を選ぶ画面(v88・見本 hs1)と同じにする(ダルマさん「上部を同じにする」)
# 屋根の絵・大きな題字・「最初の画面にもどる」をやめ、黒と金の帯 1 本(← もどる・題・一門の選ぶ欄)。注意は赤い札、説明は小さな字。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v92</title>', '<title>Grand Sumo Manager v93</title>')
rep("const APPV=92;\nconst SAVE='sumoManager92',SAVE91", "const APPV=93;\nconst SAVE='sumoManager93',SAVE92='sumoManager92',SAVE91")
rep('[SAVE91,SAVE90', '[SAVE92,SAVE91,SAVE90')
rep(" if(g.v===91){g.v=92;}\n return g.v===92?g:null;}", " if(g.v===91){g.v=92;}\n if(g.v===92){g.v=93;}\n return g.v===93?g:null;}")
rep('G={v:92,', 'G={v:93,')
rep("function nightHTML(body){if(UI.start==='real')return", "function nightHTML(body){if(UI.start==='real'||UI.start==='dok')return")
rep(""" return '<p class="hlead">2026 年九州場所の部屋付き親方のうち、部屋を新しく興せる条件(横綱・大関、三役 25 場所以上、幕内 60 場所以上のどれか)に近い、最高位が小結以上で 65 歳の定年前の親方('+dokList().length+' 人)から、独立する親方を選びます。押すと詳しい説明と、連れて行く内弟子を選ぶ画面が出ます。<br>独立には協会の承認が必要です。元の部屋から連れて行けるのは自分の内弟子が原則です。</p>'+
 '<div class="hbar"><b>一門</b><button class="hchip'+(fi<0?' on':'')+'" onclick="UI.dk.fi=-1;render()">すべて</button>'+ICR.map((n,i)=>'<button class="hchip'+(fi===i?' on':'')+'" onclick="UI.dk.fi='+i+';render()">'+n+'</button>').join('')+'</div>'+""",
""" return '<div class="hsbar"><button class="bk" onclick="goStart(null)">← もどる</button><h2>独立する親方を選ぶ</h2><span class="sl">'+
 '<select aria-label="一門" onchange="UI.dk.fi=+this.value;render()"><option value="-1">一門:すべて</option>'+ICR.map((n,i)=>'<option value="'+i+'"'+(fi===i?' selected':'')+'>'+n+'一門</option>').join('')+'</select></span></div>'+
 (G?'<div class="hswarn">いまの保存データ('+esc(me().n)+'部屋)は消えて、新しく始まります。</div>':'')+
 '<div class="hsnote">2026 年九州場所の部屋付き親方のうち、最高位が小結以上で 65 歳の定年前の親方('+dokList().length+' 人)から選びます(部屋を興す条件:横綱・大関、三役 25 場所以上、幕内 60 場所以上のどれかに近い人)。押すと詳しい説明と、連れて行く内弟子を選ぶ画面が出ます。独立には協会の承認が必要で、連れて行けるのは自分の内弟子が原則です。</div>'+""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
