# スタート画面を 2 択に(入口は見本 1「錦絵まるごと」、入力画面は見本 4「夜の国技館」)  v18 -> v19
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
def uri(f):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(I + f, 'rb').read()).decode()
IMG1 = uri('start_dohyoiri.jpg')        # 錦絵(土俵入り)1200px に縮小
IMG4 = uri('start_torikumi_blur.jpg')   # 錦絵(取組)をぼかしたもの

# --- 版 ---
rep('<title>Sumo Manager v18</title>', '<title>Sumo Manager v19</title>')
rep("const SAVE='sumoManager18',SAVE17", "const SAVE='sumoManager19',SAVE18='sumoManager18',SAVE17")
rep('[SAVE17,SAVE16,SAVE15', '[SAVE18,SAVE17,SAVE16,SAVE15')
rep(" if(g.v===17){mig18(g);g.v=18;}\n return g.v===18?g:null;}", " if(g.v===17){mig18(g);g.v=18;}\n if(g.v===18){g.v=19;}\n return g.v===19?g:null;}")
rep('G={v:18,', 'G={v:19,')

# --- 見た目 ---
CSS = """
/* v19 スタート画面 */
body.st-top{overflow:hidden}
.st-bg1{position:fixed;inset:0;background:#111 url(IMG1) center 40%/cover;z-index:0}
.st-bg1:after{content:"";position:fixed;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,0) 35%,rgba(0,0,0,.75) 100%)}
.st-title{position:fixed;top:6%;left:50%;transform:translateX(-50%);text-align:center;z-index:2;width:92vw;color:#fff}
.st-title h1{display:inline-block;background:#b3261e;border:3px solid #f3e3c3;padding:10px 22px;font-size:clamp(28px,5.5vw,58px);letter-spacing:.06em;line-height:1.3;box-shadow:0 6px 18px rgba(0,0,0,.5);margin:0}
.st-title p{display:inline-block;margin-top:10px;font-size:clamp(15px,2.2vw,22px);letter-spacing:.4em;padding:4px 10px 4px 16px;background:rgba(0,0,0,.6);border-radius:3px}
.st-go{position:fixed;left:50%;bottom:7%;transform:translateX(-50%);display:flex;gap:18px;width:min(900px,92vw);z-index:2}
.st-go button{flex:1;padding:18px 16px;border:2px solid #f3e3c3;color:#fff;text-align:left;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.5);font-family:var(--min);cursor:pointer;-webkit-tap-highlight-color:transparent}
.st-go .st-real{background:rgba(179,38,30,.92)} .st-go .st-new{background:rgba(32,52,92,.92)}
.st-go button:active{transform:translateY(2px)}
.st-go b{display:block;font-size:clamp(18px,2.4vw,26px);margin-bottom:6px} .st-go small{display:block;font:13px/1.6 var(--kaku);opacity:.92}
.st-credit{position:fixed;right:8px;bottom:6px;font:11px/1.3 var(--kaku);color:rgba(255,255,255,.75);text-shadow:0 1px 2px #000;z-index:3;pointer-events:none}
@media(max-aspect-ratio:3/4){.st-bg1{background-position:50% 30%}.st-go{flex-direction:column;gap:12px}}
@media(max-height:560px){.st-go small{display:none}.st-title{top:3%}}
.st-bg4{position:fixed;inset:-20px;background:#111 url(IMG4) center/cover;filter:brightness(.45) saturate(1.1);z-index:0}
.st-wrap{position:relative;z-index:2;max-width:660px;margin:0 auto;padding-bottom:30px}
.st-roof{width:min(620px,86vw);height:70px;margin:0 auto}
.st-roof .r{height:26px;background:linear-gradient(#3a2a12,#1c140a);clip-path:polygon(6% 0,94% 0,100% 100%,0 100%)}
.st-roof .m{height:22px;background:#4b2a6b;border-bottom:3px solid #c9a24a}
.st-roof .f{display:flex;justify-content:space-between;padding:0 6%}
.st-roof .f i{display:block;width:16px;height:22px;border-radius:0 0 8px 8px}
.st-roof .f i:nth-child(1){background:#2a7a4a}.st-roof .f i:nth-child(2){background:#b3261e}.st-roof .f i:nth-child(3){background:#f4f1e8}.st-roof .f i:nth-child(4){background:#1c1c1c}
.st-h{text-align:center;font-size:clamp(28px,5vw,44px);color:#e9c46a;letter-spacing:.06em;text-shadow:0 0 18px rgba(233,196,106,.45),0 3px 6px #000;margin:8px 0 2px}
.st-back{display:block;margin:6px auto 0;background:rgba(10,8,6,.55);border:1.5px solid #e9c46a;color:#f2e8d0;border-radius:999px;padding:6px 18px;font-family:var(--kaku);font-size:14px;cursor:pointer}
.st-wrap .start{margin:14px auto 0;background:rgba(253,249,238,.96);border:2px solid #c9a24a;box-shadow:0 8px 24px rgba(0,0,0,.55)}
.st-wrap .start h2{margin:4px 0 6px;letter-spacing:.1em}
""".replace('IMG1', IMG1).replace('IMG4', IMG4)
rep('</style>', CSS + '</style>')

# --- 画面 ---
rep(" if(!G){app.innerHTML=startHTML()+realStartHTML();return;}",
    " document.body.classList.toggle('st-top',!G&&!UI.start);\n"
    " if(!G){app.innerHTML=UI.start?nightHTML(UI.start==='real'?realStartHTML():startHTML()):topHTML();return;}")

rep("""'<div class="start pn"><div class="dohyo"></div><h1 style="letter-spacing:.08em">Sumo Manager</h1><p class="lead">親方として部屋を開き、弟子を育てて横綱を目指します。<br>週ごとの稽古、一番ごとの取り口、けが、スタッフ、スカウト、部屋の経営まで。</p>'""",
    """'<div class="start pn"><h2>新しく部屋を作る</h2><p class="lead">親方として部屋を開き、弟子を育てて横綱を目指します。<br>週ごとの稽古、一番ごとの取り口、けが、スタッフ、スカウト、部屋の経営まで。</p>'""")
rep("""'<div class="start pn" style="margin-top:12px"><h2 style="letter-spacing:.1em">実名で始める</h2>""",
    """'<div class="start pn"><h2>実在の部屋を選ぶ</h2>""")

CREDIT = "'<div class=\"st-credit\">背景:一恵斎芳幾「勧進大相撲土俵入之図」ほか(江戸〜明治の錦絵)</div>'"
rep("function doStartReal(){",
    "function topHTML(){return '<div class=\"st-bg1\"></div><div class=\"st-title\"><h1>Sumo Manager</h1><br><p>親方一代</p></div>'+\n"
    " '<div class=\"st-go\"><button class=\"st-real\" onclick=\"goStart(\\'real\\')\"><b>実在の部屋を選ぶ</b><small>2026 年九州場所の番付から。45 部屋・592 人の中から部屋を選び、その師匠になります。</small></button>'+\n"
    " '<button class=\"st-new\" onclick=\"goStart(\\'new\\')\"><b>新しく部屋を作る</b><small>自分で部屋を開きます。部屋の名前・親方・一門を決め、弟子 7 人から始めます。</small></button></div>'+" + CREDIT + ";}\n"
    "function nightHTML(body){return '<div class=\"st-bg4\"></div><div class=\"st-wrap\"><div class=\"st-roof\"><div class=\"r\"></div><div class=\"m\"></div><div class=\"f\"><i></i><i></i><i></i><i></i></div></div>'+\n"
    " '<div class=\"st-h\">Sumo Manager</div><button class=\"st-back\" onclick=\"goStart(null)\">← 最初の画面にもどる</button>'+body+'</div>'+" + CREDIT + ";}\n"
    "function goStart(k){UI.start=k;render();window.scrollTo(0,0);}\n"
    "function doStartReal(){UI.start=null;")
rep("function doStart(){const h=", "function doStart(){UI.start=null;const h=")
rep("G=null;UI.view='home';render();}", "G=null;UI.view='home';UI.start=null;render();}")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
