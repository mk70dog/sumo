# v105 -> v106:部屋(ホーム)画面の背景に錦絵(相撲部屋の稽古場)。見本 hb2「上に帯」(ダルマさん「ゲーム中のホーム画面の背景に設定、やることなどを両サイドや上部に分けて見やすく、土俵には何も重ねない、サンプル×5」→「2」)。
# 絵は画面の横いっぱい(cover、下そろえ)。上に「今週やること」、左に部屋の声、右に注目選手と部屋の様子。土俵と土俵の上の力士・行司(絵の横 195〜948・縦 320〜896 / 1200×896)には何も置かない。
# iPad 縦・スマホなど左右の空きが狭いときは、絵の上には何も置かず、札を絵の下に並べる。弟子の様子・部屋日誌などはこれまでどおり絵の下。
# 部品は tools/hb_sample.js(見本と同じもの)から作る。絵は img/home_keikoba.jpg(ダルマさん提供の江戸時代の錦絵)。
import sys, os, base64, re
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v105</title>', '<title>Grand Sumo Manager v106</title>')
rep("const APPV=105;\nconst SAVE='sumoManager105',SAVE104", "const APPV=106;\nconst SAVE='sumoManager106',SAVE105='sumoManager105',SAVE104")
rep('[SAVE104,SAVE103', '[SAVE105,SAVE104,SAVE103')
rep(" if(g.v===104){g.v=105;}\n return g.v===105?g:null;}", " if(g.v===104){g.v=105;}\n if(g.v===105){g.v=106;}\n return g.v===106?g:null;}")
rep('G={v:105,', 'G={v:106,')
js = open(os.path.join(here, '..', 'tools', 'hb_sample.js'), encoding='utf-8').read()
from io import BytesIO
try:
    from PIL import Image
    im = Image.open(os.path.join(here, '..', 'img', 'home_keikoba.jpg')).convert('RGB'); bio = BytesIO(); im.save(bio, 'JPEG', quality=80, optimize=True); raw = bio.getvalue()
except Exception:
    raw = open(os.path.join(here, '..', 'img', 'home_keikoba.jpg'), 'rb').read()
b = base64.b64encode(raw).decode()
js = js.replace('__HBIMG__', b).replace('__HBURL__', "'data:image/jpeg;base64," + b + "'")
# 見本の切りかえ(#hb1〜5)をやめて hb2 に固定。見本の札の文字は出典だけに
def jrep(old, new):
    global js
    if js.count(old) != 1: raise SystemExit('部品の一致数: %r' % old[:80])
    js = js.replace(old, new)
jrep("function hbV(){const m=(location.hash||'').match(/hb(\\d)/);return m?+m[1]:1;}", "function hbV(){return 2;}")
jrep("'<div class=\"hbcap\">見本 hb'+hbV()+'「'+v.name+'」 背景:江戸時代の錦絵(相撲部屋の稽古場)</div></div>'", "'<div class=\"hbcap\">背景:江戸時代の錦絵(相撲部屋の稽古場)</div></div>'")
jrep("render0=function(){hbR0();if(!G||UI.title||UI.view!=='home'||G.mp)return;", "render0=function(){hbR0();if(!G||UI.title||UI.view!=='home'||G.over)return;if(UI.mpGuest&&typeof mpIsP==='function'&&!mpIsP())return;")
jrep("addEventListener('resize',()=>requestAnimationFrame(hbFit));addEventListener('hashchange',()=>render());", "addEventListener('resize',()=>requestAnimationFrame(hbFit));")
jrep("/* 見本 hb1〜hb5:", "/* v106(見本 hb2 を採用)。もとは見本 hb1〜hb5:")
# 上の帯は、場面によって高さが変わり絵の上に収まらないことがあるので、いつも絵のすぐ上(絵の外)に置く(見た目は見本 hb2 とほぼ同じ)
jrep("if(t.children.length&&t.scrollHeight>t.clientHeight+4&&!st.dataset.out){", "if(t.children.length&&!st.dataset.out){")
i = s.rfind('</body>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, len(s))
