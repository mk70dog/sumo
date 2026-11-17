# プレイヤーは部屋を見守る存在(画面の中には出てこない)  v35 -> v36  見本 koe1
# ⓪スタート画面の副題「親方一代」を外す(今のところ副題なし)
# ①「新しく部屋を作る」のボタンを隠す(作りは残す) ②出来事は「親方の悩みごと」(ひとりごと)として出す
# ③稽古の画面に親方のひとりごと ④部屋の画面に「部屋の声」:親方・おかみさん・部屋付き親方・マネージャー・トレーナー・弟子の話を聞ける
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
koe = open(os.path.join(os.path.dirname(__file__), 'koe36.js'), encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v35</title>', '<title>Sumo Manager v36</title>')
rep("const APPV=35;\nconst SAVE='sumoManager35',SAVE34", "const APPV=36;\nconst SAVE='sumoManager36',SAVE35='sumoManager35',SAVE34")
rep('[SAVE34,SAVE33', '[SAVE35,SAVE34,SAVE33')
rep(" if(g.v===34){g.v=35;}\n return g.v===35?g:null;}", " if(g.v===34){g.v=35;}\n if(g.v===35){g.v=36;}\n return g.v===36?g:null;}")
rep('G={v:35,', 'G={v:36,')
rep('<h1>Sumo Manager</h1><br><p>親方一代</p>', '<h1>Sumo Manager</h1>')  # 副題は今のところなし
rep("'<button class=\"st-new\" onclick=\"goStart(\\'new\\')\">","(0?'<button class=\"st-new\" onclick=\"goStart(\\'new\\')\">")
rep("弟子 7 人から始めます。</small></button></div>'","弟子 7 人から始めます。</small></button>':'')+'</div>'")
rep("2026 年九州場所の番付から。45 部屋・592 人の中から部屋を選び、その師匠になります。","2026 年九州場所の番付から。45 部屋・592 人の中から部屋を選び、その部屋の歩みを見守ります。")
rep('<h2>番付発表を受けて<span class="sub">初日までに決めてください</span></h2>','<h2>親方の悩みごと<span class="sub">初日までに決めてください</span></h2>')
rep('<h2>場所後の出来事<span class="sub">返事をすると次へ進めます</span></h2>','<h2>親方の悩みごと<span class="sub">決めると次へ進めます</span></h2>')
rep("'<div class=\"ev\"><b>'+E.t+'</b><p>'+esc(E.d(e))+'</p><div class=\"btns\">'","evHead(e,E)+'<div class=\"btns\">'",2)
rep("function doEv(id,i){", koe+"function evHead(e,E){const c=typeof E.c==='function'?E.c(e):E.c;const q=c.length>1;return '<div class=\"ev\"><div class=\"sdh\">'+(q?'悩みごと':'できごと')+' ・ '+E.t+'</div><div class=\"sdq\">'+esc(oyN())+(q?'(ひとりごと)':'')+'「'+esc(E.d(e))+(q?'…さて、どうしたものか。':'')+'」</div>';}\n"
    "function koeModal(i){const p=koePeople()[i];if(!p)return;openM('<h2>'+esc(p.who)+' <small style=\"font-size:14px;color:#7a6a55\">'+esc(p.role)+'</small></h2>'+p.lines.map(x=>'<div class=\"sdq\">「'+esc(x)+'」</div>').join('')+'<div class=\"btns\"><button class=\"btn\" onclick=\"closeM()\">閉じる</button></div>');}\nfunction doEv(id,i){")
rep(".ev{border:", ".sdh{font-size:13px;color:#7a6a55;margin-bottom:4px}.sdq{position:relative;background:#fff;color:#2a2018;border:1px solid var(--line);border-radius:12px;padding:8px 12px;margin:2px 0 8px 14px}.sdq:before{content:'';position:absolute;left:-8px;top:12px;border:8px solid transparent;border-right-color:var(--line);border-left:0}.kp{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.kp button{border:1px solid var(--line);background:#fffaf0;color:#2a2018;border-radius:18px;padding:6px 12px;font-size:14px;cursor:pointer}.kp small{color:#7a6a55}\n.ev{border:")
rep("+weekDots()+tourNote()+", "+'<div class=\"sdq\" style=\"margin-left:0\">'+esc(oyN())+'(ひとりごと)「今週の稽古は、どうするか…。」</div>'+weekDots()+tourNote()+")
rep("  h+='<div class=\"pn\"><h2>弟子の様子<span class=\"sub\">押すと詳しく見られます</span></h2>'",
    "  h+='<div class=\"pn\"><h2>部屋の声<span class=\"sub\">押すと話が聞けます</span></h2><div class=\"kp\">'+koePeople().map((p,i)=>'<button onclick=\"koeModal('+i+')\">'+esc(p.who)+' <small>'+esc(p.role)+'</small></button>').join('')+'</div></div>';\n  h+='<div class=\"pn\"><h2>弟子の様子<span class=\"sub\">押すと詳しく見られます</span></h2>'")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
