# 起動時に保存データを捨てていた不具合を直し、スタート画面に「続きから」を付ける  v19 -> v20
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

# --- 版 ---
rep('<title>Sumo Manager v19</title>', '<title>Sumo Manager v20</title>')
rep("const SAVE='sumoManager19',SAVE18", "const SAVE='sumoManager20',SAVE19='sumoManager19',SAVE18")
rep('[SAVE18,SAVE17,SAVE16', '[SAVE19,SAVE18,SAVE17,SAVE16')
rep(" if(g.v===18){g.v=19;}\n return g.v===19?g:null;}", " if(g.v===18){g.v=19;}\n if(g.v===19){g.v=20;}\n return g.v===20?g:null;}")
rep('G={v:19,', 'G={v:20,')

# --- 起動:版 12 のときの確認が残っていて、v13 から保存データを読み捨てていた ---
rep("if(G&&(!G.order||G.v!==12))G=null;", "if(G&&!G.order)G=null;\nUI.title=!!G;")

# --- 画面 ---
rep(" document.body.classList.toggle('st-top',!G&&!UI.start);\n"
    " if(!G){app.innerHTML=UI.start?nightHTML(UI.start==='real'?realStartHTML():startHTML()):topHTML();return;}",
    " const ttl=!G||UI.title;\n"
    " document.body.classList.toggle('st-top',ttl&&!UI.start);\n"
    " if(ttl){app.innerHTML=UI.start?nightHTML(UI.start==='real'?realStartHTML():startHTML()):topHTML();return;}")
rep("'<div class=\"st-go\"><button class=\"st-real\"",
    "'<div class=\"st-go\">'+(G?'<button class=\"st-cont\" onclick=\"goStart(\\'cont\\')\"><b>続きから</b><small>'+esc(me().n)+'部屋・'+bname(G.bnum)+'・'+phaseText()+'</small></button>':'')+'<button class=\"st-real\"")
rep("'<div class=\"st-h\">Sumo Manager</div><button class=\"st-back\" onclick=\"goStart(null)\">← 最初の画面にもどる</button>'+body+'</div>'",
    "'<div class=\"st-h\">Sumo Manager</div><button class=\"st-back\" onclick=\"goStart(null)\">← 最初の画面にもどる</button>'+(G?'<p class=\"st-warn\">いまの保存データ('+esc(me().n)+'部屋)は消えて、新しく始まります。</p>':'')+body+'</div>'")
rep("function goStart(k){UI.start=k;render();window.scrollTo(0,0);}",
    "function goStart(k){if(k==='cont'){UI.title=false;UI.start=null;}else UI.start=k;render();window.scrollTo(0,0);}")
rep("function doStartReal(){UI.start=null;", "function doStartReal(){UI.start=null;UI.title=false;")
rep("function doStart(){UI.start=null;const h=", "function doStart(){UI.start=null;UI.title=false;const h=")
rep("G=null;UI.view='home';UI.start=null;render();}", "G=null;UI.view='home';UI.start=null;UI.title=false;render();}")

rep(".st-go .st-real{background:rgba(179,38,30,.92)}",
    ".st-go{flex-wrap:wrap}.st-go .st-cont{flex:1 1 100%;background:rgba(20,16,10,.88);border-color:#e9c46a;text-align:center;padding:12px 16px}.st-go .st-cont b{color:#e9c46a;margin-bottom:2px}\n"
    ".st-warn{margin:10px auto 0;max-width:600px;background:rgba(179,38,30,.92);color:#fff;border:1px solid #f3e3c3;border-radius:4px;padding:6px 10px;font:14px/1.5 var(--kaku);text-align:center}\n"
    ".st-go .st-real{background:rgba(179,38,30,.92)}")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
