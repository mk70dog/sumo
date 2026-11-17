# ホーム画面に追加して使う:アイコンと「アプリを更新」ボタン(latest.json で新しい版を確かめる)  v20 -> v21
import os, sys, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

I = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img') + os.sep
ICON = 'data:image/png;base64,' + base64.b64encode(open(I + 'icon180.png', 'rb').read()).decode()

# --- 版 ---
rep('<title>Sumo Manager v20</title>', '<title>Sumo Manager v21</title>')
rep("const SAVE='sumoManager20',SAVE19", "const APPV=21;\nconst SAVE='sumoManager21',SAVE20='sumoManager20',SAVE19")
rep('[SAVE19,SAVE18,SAVE17', '[SAVE20,SAVE19,SAVE18,SAVE17')
rep(" if(g.v===19){g.v=20;}\n return g.v===20?g:null;}", " if(g.v===19){g.v=20;}\n if(g.v===20){g.v=21;}\n return g.v===21?g:null;}")
rep('G={v:20,', 'G={v:21,')

# --- ホーム画面のアイコンと名前 ---
rep('<meta name="apple-mobile-web-app-title" content="相撲部屋">',
    '<meta name="apple-mobile-web-app-title" content="Sumo Manager">\n<link rel="apple-touch-icon" href="' + ICON + '">\n<link rel="icon" href="' + ICON + '">')

# --- 見た目 ---
rep(".st-go .st-real{background:rgba(179,38,30,.92)}",
    ".st-upd{position:fixed;top:calc(8px + env(safe-area-inset-top));right:8px;z-index:4;background:rgba(10,8,6,.6);border:1.5px solid #e9c46a;color:#f2e8d0;border-radius:999px;padding:5px 14px;font:13px/1.4 var(--kaku);cursor:pointer}\n"
    ".st-upd.new{background:#c9a24a;color:#1d1a16;font-weight:bold;animation:stpulse 1.6s ease-in-out infinite}@keyframes stpulse{50%{box-shadow:0 0 0 6px rgba(233,196,106,.35)}}\n"
    ".updbar{display:block;width:100%;margin:8px 0 0;background:#c9a24a;color:#1d1a16;border:0;border-radius:4px;padding:8px 12px;font:bold 14px/1.4 var(--kaku);text-align:center;cursor:pointer}\n"
    ".st-go .st-real{background:rgba(179,38,30,.92)}")

# --- 更新の仕組み ---
rep("function goStart(k){",
    "/* アプリの更新:同じフォルダの latest.json に最新の版と本体のファイル名を書いておく */\n"
    "function checkUpd(manual){\n"
    " if(!/^https?:/.test(location.protocol)){if(manual)alertM('更新を確かめられません','ファイルから直接開いているときは確かめられません。https://mk70dog.github.io/sumo/ から開いてください。');return;}\n"
    " fetch('latest.json?t='+Date.now(),{cache:'no-store'}).then(r=>r.json()).then(j=>{\n"
    "  if(j&&j.v>APPV&&j.file){UI.upd=j;if(manual)askUpd();else render();}\n"
    "  else if(manual)alertM('最新の版です','いまの版は v'+APPV+' です。');\n"
    " }).catch(()=>{if(manual)alertM('更新を確かめられません','インターネットにつながっているか確かめてください。');});}\n"
    "function askUpd(){const j=UI.upd;openM('<h2>新しい版 v'+j.v+' があります</h2>'+(j.note?'<p class=\"kaku\">'+esc(j.note)+'</p>':'')+'<p class=\"kaku mute\" style=\"font-size:13px\">いまは v'+APPV+' です。保存データはそのまま引き継がれます。</p><div class=\"btns\"><button class=\"btn main\" onclick=\"doUpd()\">更新する</button><button class=\"btn\" onclick=\"closeM()\">あとで</button></div>');}\n"
    "function doUpd(){if(G)save();location.replace(UI.upd.file+'?t='+Date.now());}\n"
    "function updBtnHTML(){return UI.upd?'<button class=\"st-upd new\" onclick=\"askUpd()\">新しい版 v'+UI.upd.v+' に更新</button>':'<button class=\"st-upd\" onclick=\"checkUpd(1)\">アプリを更新(v'+APPV+')</button>';}\n"
    "function goStart(k){")
rep("function topHTML(){return '<div class=\"st-bg1\"></div>", "function topHTML(){return updBtnHTML()+'<div class=\"st-bg1\"></div>")
rep(" app.innerHTML=hdrHTML()+navHTML()+(V[UI.view]||homeHTML)();",
    " app.innerHTML=hdrHTML()+(UI.upd?'<button class=\"updbar\" onclick=\"askUpd()\">新しい版 v'+UI.upd.v+' があります。押すと更新します(保存データはそのまま)</button>':'')+navHTML()+(V[UI.view]||homeHTML)();")
rep("<button class=\"btn\" onclick=\"confirmReset()\">はじめからやり直す</button></div></div>';",
    "<button class=\"btn\" onclick=\"confirmReset()\">はじめからやり直す</button></div></div>'+\n"
    " '<div class=\"pn\"><h2>アプリの更新</h2><p class=\"kaku mute\" style=\"font-size:13px\">いまの版は v'+APPV+' です。ホーム画面から開いているときも、ここで新しい版に切り替えられます。保存データはそのまま引き継がれます。</p><div class=\"btns\"><button class=\"btn main\" onclick=\"checkUpd(1)\">アプリを更新</button></div></div>';")

# --- 起動時に新しい版を確かめる ---
rep("applyMode(!!(G&&G.real));\nrender();\n", "applyMode(!!(G&&G.real));\nrender();\ncheckUpd(0);\n")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
