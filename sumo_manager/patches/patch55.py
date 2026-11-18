# 取組を上から見た土俵で動かす(見本 kaiga13〜kaiga20)  v51 -> v52
# 大一番(b.big)は結果の欄でそのまま動く。ほかの取組も「▶ 土俵で見る」で開ける(部屋の力士・幕内上位)。
# 力士は四角(B)、体重(r.wT)で大きさ。調子・突っ張り・まわしで色が変わる。行司と満員の観客。数値・演出はすべて見せ方で、勝ち負けには影響しない。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
mod = open(os.path.join(here,'dohyo57.js'),encoding='utf-8').read().replace('function mix(','function dhMix(').replace("mix('#f0c998'","dhMix('#f0c998'")
ui = open(os.path.join(here,'dohyo58_ui.js'),encoding='utf-8').read()
rep('<title>Sumo Manager v51</title>', '<title>Sumo Manager v52</title>')
rep("const APPV=51;\nconst SAVE='sumoManager51',SAVE50", "const APPV=52;\nconst SAVE='sumoManager52',SAVE51='sumoManager51',SAVE50")
rep('[SAVE50,SAVE49', '[SAVE51,SAVE50,SAVE49')
rep(" if(g.v===50){g.v=51;}\n return g.v===51?g:null;}", " if(g.v===50){g.v=51;}\n if(g.v===51){g.v=52;}\n return g.v===52?g:null;}")
rep('G={v:51,', 'G={v:52,')
rep("/* ========== 画面 ========== */", "/* ========== 画面 ========== */\n"+mod+"\n"+ui+"\n")
# 部屋の力士の結果:大一番は動く図、ほかはボタン
rep("h+='<div class=\"pn\"><h2>'+day+'日目の結果<span class=\"sub\">部屋の力士</span></h2>'+(ob.length?'<div class=\"rgrid\">'+ob.map(x=>'<div class=\"r1'+(x.os?' os':'')+'\">'",
    "UI.dhO=ob.map(x=>x.b);UI.dhT=top;let dhBig=-1;ob.forEach((x,i)=>{if(dhBig<0&&x.b.big)dhBig=i;});if(dhBig>=0)setTimeout(()=>{if(document.getElementById('dhi'))dhRun('dhi',ob[dhBig].b);},80);\n  h+='<div class=\"pn\"><h2>'+day+'日目の結果<span class=\"sub\">部屋の力士</span></h2>'+(ob.length?'<div class=\"rgrid\">'+ob.map((x,ix)=>'<div class=\"r1'+(x.os?' os':'')+'\">'+(ix===dhBig?'<div class=\"dhin\">'+dhHTML('dhi',x.b,0)+'</div>':'')")
rep("(x.b.nar&&x.b.nar.length?'<details><summary>取組の様子</summary><div class=\"nar\">'+x.b.nar.map(esc).join('<br>')+'</div></details>':'')+'</div>').join('')",
    "'<button class=\"dhbtn\" onclick=\"dhOpen(\\'o\\','+ix+')\">▶ 土俵で見る</button>'+(x.b.nar&&x.b.nar.length?'<details><summary>取組の様子</summary><div class=\"nar\">'+x.b.nar.map(esc).join('<br>')+'</div></details>':'')+'</div>').join('')")
rep("'<h3>幕内上位</h3>'+top.map(b=>{const W=G.R[b.w],L=G.R[b.l];return '<div class=\"r1\"><b>'+esc(W.n)+'</b> <span class=\"sm\">'+esc(W.rkS)+'</span> '+esc(b.k)+' '+esc(L.n)+' <span class=\"sm\">'+esc(L.rkS)+'</span>'",
    "'<h3>幕内上位</h3>'+top.map((b,ti)=>{const W=G.R[b.w],L=G.R[b.l];return '<div class=\"r1\"><b>'+esc(W.n)+'</b> <span class=\"sm\">'+esc(W.rkS)+'</span> '+esc(b.k)+' '+esc(L.n)+' <span class=\"sm\">'+esc(L.rkS)+'</span><button class=\"dhbtn\" onclick=\"dhOpen(\\'t\\','+ti+')\">▶ 土俵で見る</button>'")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
