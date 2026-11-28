# v209 -> v210:後援会・タニマチ・出稽古・巡業を本物らしく(二本目の化粧まわし・頼みごと・張り合い・親睦ゴルフ・出稽古先とのつきあい・巡業の地元の声援)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=209;\nconst SAVE='sumoManager209',SAVE208", "const APPV=210;\nconst SAVE='sumoManager210',SAVE209='sumoManager209',SAVE208")
rep('[SAVE208,SAVE207', '[SAVE209,SAVE208,SAVE207')
rep('<title>Grand Sumo Manager v209', '<title>Grand Sumo Manager v210')
# 不具合直し(v195 から):iPad 横の部屋の画面で、絵の下の「親方の悩みごと」が隠れて答えられなかった → 悩みごとがあるときは 1 画面にまとめない
rep("document.body.classList.toggle('vh1',UI.view==='home');", "document.body.classList.toggle('vh1',UI.view==='home'&&!(G&&G.ev&&G.ev.length));")
ui = open(os.path.join(here,'sp213_ui.js'),encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
