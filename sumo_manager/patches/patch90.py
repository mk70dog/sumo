# v86 -> v87:二人相撲の画面を短く(ダルマさん「GitHub の鍵設定は設定内にする。他の 3 ボタンの表記が長い」)
# 鍵の入力欄は二人相撲の画面から外し、⚙ 設定の中だけに。鍵がないときは短い案内と「⚙ 設定を開く」。ボタンの字を短く。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v86</title>', '<title>Grand Sumo Manager v87</title>')
rep("const APPV=86;\nconst SAVE='sumoManager86',SAVE85", "const APPV=87;\nconst SAVE='sumoManager87',SAVE86='sumoManager86',SAVE85")
rep('[SAVE85,SAVE84', '[SAVE86,SAVE85,SAVE84')
rep(" if(g.v===85){g.v=86;}\n return g.v===86?g:null;}", " if(g.v===85){g.v=86;}\n if(g.v===86){g.v=87;}\n return g.v===87?g:null;}")
rep('G={v:86,', 'G={v:87,')
rep("""<b>親:実在の部屋を選んで始める</b><small>実在の部屋を選んで世界を作ります。合言葉が出るので、相手に伝えます。</small>""", """<b>実在の部屋で始める</b><small>親になる</small>""")
rep("""<b>親:部屋付き親方として独立して始める</b><small>実在の部屋付き親方を選び、内弟子を連れて新しい部屋を興して世界を作ります。</small>""", """<b>独立して始める</b><small>親になる(部屋付き親方が独立)</small>""")
rep("""<b>合言葉で参加する</b><small>相手から聞いた合言葉を入れて、残りの部屋から選びます。</small>""", """<b>合言葉で参加</b><small>子になる</small>""")
rep("""'<div class="mpkey">'+(UI.mpJoin?'<label>合言葉</label><input id="mp_code" placeholder="親の画面に出ている合言葉"><button class="btn main" onclick="mpJoin()">参加する</button><br>':'')+
  '<label>GitHub の鍵(gist だけ書ける鍵。この端末の中だけに保存。ふたりとも同じ鍵を使います)</label><input id="mp_tok" type="password" value="'+esc(mpTok())+'"><button class="btn" onclick="mpSaveTok()">鍵を保存</button></div>';""",
    """(UI.mpJoin?'<div class="mpkey"><label>合言葉</label><input id="mp_code" placeholder="親の画面に出ている合言葉"><button class="btn main" onclick="mpJoin()">参加する</button></div>':'')+
  (mpTok()||MPT.mock?'':'<div class="mpkey mpnokey">GitHub の鍵がまだありません。<button class="btn sm" onclick="topSettings()">⚙ 設定を開く</button></div>');""")
rep("alertM('鍵がありません','先に GitHub の鍵を入れてください。')", "alertM('鍵がありません','⚙ 設定で GitHub の鍵を読み込んでください。')", 2)
rep(".mpkey input{", ".st-go2 .st-real b,.st-go2 .st-dok b{font-size:clamp(18px,2.4vw,24px)}.st-go2 .st-real,.st-go2 .st-dok{text-align:center;padding:12px}.mpnokey{text-align:center}.mpkey input{")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
