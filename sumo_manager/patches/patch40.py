# 場所中の取組結果を見やすく(見本 kekka1)  v36 -> v37
# 結果を翌日の取組より上に出す。部屋の力士ごとに「勝ち/負け」の札・決まり手と相手・その日のあとの成績・
# 「勝ち越し!」「負け越し」「○連勝」「金星!」「勝ち越しまであと○」の札。実況は「取組の様子」を押すと開く。
# 画面が広いときは 2 列(760px 以上)・3 列(1100px 以上)に並べる。幕内上位の取組も 1 行に。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
kk = open(os.path.join(os.path.dirname(__file__), 'kekka40.js'), encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v36</title>', '<title>Sumo Manager v37</title>')
rep("const APPV=36;\nconst SAVE='sumoManager36',SAVE35", "const APPV=37;\nconst SAVE='sumoManager37',SAVE36='sumoManager36',SAVE35")
rep('[SAVE35,SAVE34', '[SAVE36,SAVE35,SAVE34')
rep(" if(g.v===35){g.v=36;}\n return g.v===36?g:null;}", " if(g.v===35){g.v=36;}\n if(g.v===36){g.v=37;}\n return g.v===37?g:null;}")
rep('G={v:36,', 'G={v:37,')
a0 = s.find(" if(day&&UI.bouts.length){const ob=UI.bouts.filter("); a1 = s.find(" h+='<div class=\"pn\"><h2>部屋の星取表")
if a0 < 0 or a1 < 0 or a1 < a0 or s.count(" if(day&&UI.bouts.length){const ob=UI.bouts.filter(") != 1: raise SystemExit('結果の欄が見つからない')
s = s[:a0] + s[a1:]
nar = "(x.b.nar&&x.b.nar.length?'<details><summary>取組の様子</summary><div class=\"nar\">'+x.b.nar.map(esc).join('<br>')+'</div></details>':'')"
topL = "(top.length?'<h3>幕内上位</h3>'+top.map(b=>{const W=G.R[b.w],L=G.R[b.l];return '<div class=\"r1\"><b>'+esc(W.n)+'</b> <span class=\"sm\">'+esc(W.rkS)+'</span> '+esc(b.k)+' '+esc(L.n)+' <span class=\"sm\">'+esc(L.rkS)+'</span>'+(b.nar&&b.nar.length?'<details><summary>取組の様子</summary><div class=\"nar\">'+b.nar.map(esc).join('<br>')+'</div></details>':'')+'</div>';}).join(''):'')"
tags = "(x.tag?'<span class=\"rtag\">'+x.tag+'</span>':'')+(x.need?'<span class=\"rtag g\">'+x.need+'</span>':'')"
body = ("  h+='<div class=\"pn\"><h2>'+day+'日目の結果<span class=\"sub\">部屋の力士</span></h2>'+(ob.length?'<div class=\"rgrid\">'+ob.map(x=>'<div class=\"r1\">'+wlBadge(x.win,x.b.fus)+' <b>'+esc(x.m.n)+'</b> <span class=\"sm\">'+esc(x.m.rkS)+'</span><br>'+(x.win?esc(x.b.k)+'で ':'')+esc(x.o.n)+(x.win?' に':' の'+esc(x.b.k)+'に')+' <span class=\"sm\">('+esc(x.o.rkS)+'・'+esc(G.heya[x.o.h].n)+')</span><br><b>'+x.c.w+'勝'+x.c.l+'敗</b>'+(x.c.ab?x.c.ab+'休':'')+' '+"
        + tags + "+" + nar + "+'</div>').join('')+'</div>':'<p class=\"mute kaku\">部屋の力士の取組はありませんでした。</p>')+" + topL + "+'</div>';")
rep(" // 次の取組", " if(day&&UI.bouts.length){const ob0=UI.bouts.filter(b=>G.R[b.w]&&G.R[b.l]&&(G.R[b.w].h===0||G.R[b.l].h===0));const ob=ob0.map(oRes).map((x,i)=>Object.assign(x,{b:ob0[i]}));\n  const top=UI.bouts.filter(b=>G.R[b.w]&&G.R[b.l]&&G.R[b.w].h!==0&&G.R[b.l].h!==0&&G.R[b.w].d===0&&b.nar).sort((x,y)=>Math.min(G.R[x.w].pos,G.R[x.l].pos)-Math.min(G.R[y.w].pos,G.R[y.l].pos)).slice(0,3);\n" + body + "}\n // 次の取組")
rep("function lvWord(v)", kk + "function lvWord(v)")
rep(".bout{", ".rgrid{display:block}@media(min-width:760px){.rgrid{display:grid;grid-template-columns:1fr 1fr;column-gap:20px}}@media(min-width:1100px){.rgrid{grid-template-columns:1fr 1fr 1fr}}.wlb{display:inline-block;min-width:3.2em;text-align:center;border-radius:4px;padding:1px 4px;font-size:13px;font-weight:bold;color:#fff}.wlb.wn{background:#b8322a}.wlb.ls{background:#5d6b7a}.rtag{display:inline-block;font-size:12px;border:1px solid #b8322a;color:#b8322a;border-radius:10px;padding:0 6px;margin-left:4px}.rtag.g{border-color:#7a6a55;color:#7a6a55}.r1{padding:8px 0;border-bottom:1px dashed #d8cdb4;font-size:15px}.r1 .sm{font-size:12px;color:#7a6a55}.r1 details summary{cursor:pointer;color:#7a6a55;font-size:13px;margin-top:2px}.r1 .nar{font-size:13px;margin-top:4px}\n.bout{")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
