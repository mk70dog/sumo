# v217 -> v218:①予定の画面の文字が暗い着せ替え(漆黒・金など)で見えない不具合を直す(札の色を着せ替えの色に合わせる。見本 cal218 の A)。
#   ②本場所の結果を伏せる(ダルマさん「本場所 動画確認前に結果がわかってしまう」→ 見本 fz218 →「A 千秋楽も入れる」。部品 patches/fz221_ui.js)。
#     千秋楽も、取ったあと本場所の画面で取組を見てから「場所を締める」で結果のまとめを出す。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=217;\nconst SAVE='sumoManager217',SAVE216", "const APPV=218;\nconst SAVE='sumoManager218',SAVE217='sumoManager217',SAVE216")
rep('[SAVE216,SAVE215', '[SAVE217,SAVE216,SAVE215')
rep('<title>Grand Sumo Manager v217', '<title>Grand Sumo Manager v218')
FZ = "(typeof fzC==='function'?fzC(%s):'')"
# 部屋の力士の結果の札
rep("'<div class=\"r1'+(x.os?' os':'')+'\">'", "'<div class=\"r1'+(x.os?' os':'')+" + FZ % 'x.b' + "+'\" data-k=\"'+(typeof fzK==='function'?fzK(x.b):'')+'\">'")
rep("wlBadge(x.win,x.b.fus)+' '+(x.os?", "'<span class=\"rsv\">'+wlBadge(x.win,x.b.fus)+'</span><span class=\"fz fzb\">取組</span> '+(x.os?")
rep("'</span><br>'+(x.win?esc(x.b.k)+'で ':'')+esc(x.o.n)+(x.win?' に':' の'+esc(x.b.k)+'に')+' <span class=\"sm\">('",
    "'</span><br><span class=\"rsv\">'+(x.win?esc(x.b.k)+'で ':'')+esc(x.o.n)+(x.win?' に':' の'+esc(x.b.k)+'に')+'</span><span class=\"fz\">対 '+esc(x.o.n)+'</span> <span class=\"sm\">('")
rep("')</span><br><b>'+x.c.w+'勝'+x.c.l+'敗</b>'+(x.c.ab?x.c.ab+'休':'')+' '+(x.tag?'<span class=\"rtag\">'+x.tag+'</span>':'')+(x.need?'<span class=\"rtag g\">'+x.need+'</span>':'')+'<button class=\"dhbtn\" onclick=\"dhOpen(\\'o\\','+ix+')\">▶ 土俵で見る</button>'+(x.b.nar&&x.b.nar.length?'<details><summary>取組の様子</summary><div class=\"nar\">'+x.b.nar.map(esc).join('<br>')+'</div></details>':'')",
    "')</span><br><span class=\"rsv\"><b>'+x.c.w+'勝'+x.c.l+'敗</b>'+(x.c.ab?x.c.ab+'休':'')+' '+(x.tag?'<span class=\"rtag\">'+x.tag+'</span>':'')+(x.need?'<span class=\"rtag g\">'+x.need+'</span>':'')+'</span><button class=\"dhbtn\" onclick=\"dhOpen(\\'o\\','+ix+')\">▶ 土俵で見る</button><button class=\"fz fzbtn\" onclick=\"fzShow(\\''+(typeof fzK==='function'?fzK(x.b):'')+'\\')\">結果だけ見る</button>'+(x.b.nar&&x.b.nar.length?'<details class=\"rsv\"><summary>取組の様子</summary><div class=\"nar\">'+x.b.nar.map(esc).join('<br>')+'</div></details>':'')")
# 幕内上位
rep("return '<div class=\"r1\"><b>'+esc(W.n)+'</b> <span class=\"sm\">'+esc(W.rkS)+'</span> '+esc(b.k)+' '+esc(L.n)+' <span class=\"sm\">'+esc(L.rkS)+'</span><button class=\"dhbtn\" onclick=\"dhOpen(\\'t\\','+ti+')\">▶ 土俵で見る</button>'+(b.nar&&b.nar.length?'<details><summary>取組の様子</summary>",
    "const E0=W.pos<L.pos?W:L,W0=E0===W?L:W;return '<div class=\"r1'+" + FZ % 'b' + "+'\" data-k=\"'+(typeof fzK==='function'?fzK(b):'')+'\"><span class=\"rsv\"><b>'+esc(W.n)+'</b> <span class=\"sm\">'+esc(W.rkS)+'</span> '+esc(b.k)+' '+esc(L.n)+' <span class=\"sm\">'+esc(L.rkS)+'</span></span><span class=\"fz\"><b>'+esc(E0.n)+'</b> <span class=\"sm\">'+esc(E0.rkS)+'</span> 対 <b>'+esc(W0.n)+'</b> <span class=\"sm\">'+esc(W0.rkS)+'</span></span><button class=\"dhbtn\" onclick=\"dhOpen(\\'t\\','+ti+')\">▶ 土俵で見る</button><button class=\"fz fzbtn\" onclick=\"fzShow(\\''+(typeof fzK==='function'?fzK(b):'')+'\\')\">結果だけ見る</button>'+(b.nar&&b.nar.length?'<details class=\"rsv\"><summary>取組の様子</summary>")
# 土俵で見るまどの見出しの決まり手
rep("openM('<h2>'+esc(p.E.n)+' と '+esc(p.Wt.n)+' <span class=\"sub\">'+esc(b.k)+'</span></h2>'",
    "openM('<h2>'+esc(p.E.n)+' と '+esc(p.Wt.n)+' <span class=\"sub'+((typeof fzC==='function'&&fzC(b))?' rsvH':'')+'\" id=\"dhmk\" data-k=\"'+(typeof fzK==='function'?fzK(b):'')+'\">'+esc(b.k)+'</span></h2>'")
# 予定の画面:札の色を着せ替えの色に合わせる(暗い着せ替えで文字が見えなかった)
CAL = (".cwk,.cyr td{background:var(--paper)!important;border-color:var(--line)!important;color:var(--sumi)}"
 ".cwh{border-bottom-color:var(--line)!important}.cyr th{background:var(--washi2)!important;color:var(--sumi);border-color:var(--line)!important}"
 ".cwk.past,.cyr td.past{background:var(--washi2)!important;opacity:.55}"
 ".cwk.bs,.cyr td.bs{background:linear-gradient(rgba(224,88,60,.14),rgba(224,88,60,.14)),var(--paper)!important}"
 ".cyr td.can:hover{background:var(--washi2)!important}"
 "#mdl input:not([type]),#mdl input[type=text]{background:var(--paper);color:var(--sumi);border:1px solid var(--line)}")
ui = open(os.path.join(here, 'fz221_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', '<style>' + CAL + '</style><script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
