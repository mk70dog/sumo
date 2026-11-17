# スタート画面の右上に「画面の色」:ゲーム画面の写真を見て選ぶ(見本 skin5)  v24 -> v25
import os, sys, base64, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
I = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img', 'skin') + os.sep
IMG = {k: 'data:image/jpeg;base64,' + base64.b64encode(open(I + k + '.jpg', 'rb').read()).decode() for k in ['std','yoru','ai','sakura','nishiki','banzuke']}

rep('<title>Sumo Manager v24</title>', '<title>Sumo Manager v25</title>')
rep("const APPV=24;\nconst SAVE='sumoManager24',SAVE23", "const APPV=25;\nconst SAVE='sumoManager25',SAVE24='sumoManager24',SAVE23")
rep('[SAVE23,SAVE22,SAVE21', '[SAVE24,SAVE23,SAVE22,SAVE21')
rep(" if(g.v===23){g.v=24;}\n return g.v===24?g:null;}", " if(g.v===23){g.v=24;}\n if(g.v===24){g.v=25;}\n return g.v===25?g:null;}")
rep('G={v:24,', 'G={v:25,')

CSS = r"""
/* v25 スタート画面の「画面の色」 */
.st-tr{position:fixed;top:calc(8px + env(safe-area-inset-top));right:8px;z-index:4;display:flex;gap:6px}.st-tr .st-upd{position:static}
#scover{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:20;display:none}#scover.on{display:block}
#ssheet{position:fixed;left:0;right:0;bottom:0;z-index:21;transform:translateY(105%);transition:transform .25s;padding:0 10px calc(10px + env(safe-area-inset-bottom))}#ssheet.on{transform:none}
#ssheet .in{max-width:820px;margin:0 auto;background:#fffaf0;color:#1d1a16;border:2px solid #c9a24a;border-radius:10px 10px 6px 6px;box-shadow:0 -6px 24px rgba(0,0,0,.5);padding:14px 16px;max-height:80vh;overflow:auto}
#ssheet h2{font-size:20px;letter-spacing:.1em;display:flex;align-items:center;margin:0}#ssheet h2 button{margin-left:auto;background:none;border:1px solid #b9a988;border-radius:4px;padding:2px 10px;font:14px var(--kaku);color:#1d1a16}
#ssheet p{font:13px var(--kaku);color:#7d7365;margin:4px 0 10px}
.skpv{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.skpv button{flex:none;width:150px;scroll-snap-align:start;background:#fff;border:2px solid #d8c9a6;border-radius:8px;padding:6px;font:14px var(--kaku);color:#1d1a16;text-align:center}
.skpv img{display:block;width:100%;border-radius:4px;margin-bottom:4px;border:1px solid #ddd}
.skpv button.on{border-color:#b5361f;box-shadow:0 0 0 2px #b5361f inset}
"""
rep('</style>', CSS + '</style>', 1)

rep("function topHTML(){return updBtnHTML()+",
    "function topHTML(){return '<div class=\"st-tr\"><button class=\"st-upd\" onclick=\"skinSheet()\">画面の色</button>'+updBtnHTML()+'</div><div id=\"scover\" onclick=\"skinClose()\"></div><div id=\"ssheet\"><div class=\"in\"></div></div>'+")
rep("function goStart(k){",
    "const SKIMG=" + json.dumps(IMG) + ";\n"
    "function skinSheet(){const c=skinNow();$('#ssheet .in').innerHTML='<h2>画面の色(スキン)<button onclick=\"skinClose()\">閉じる</button></h2><p>ゲームの画面がどう見えるかを見て選べます。横にすべらせてください。この端末だけの設定で、保存データには影響しません。</p><div class=\"skpv\">'+\n"
    " SKINS.map(x=>'<button class=\"'+(x[0]===c?'on':'')+'\" onclick=\"skinPick(\\''+x[0]+'\\')\"><img src=\"'+SKIMG[x[0]]+'\" alt=\"\">'+x[1]+'</button>').join('')+'</div>';\n"
    " $('#ssheet').classList.add('on');$('#scover').classList.add('on');document.body.classList.add('hs-open');}\n"
    "function skinPick(k){try{localStorage.setItem('sumoSkin',k);}catch(e){}applySkin(k);const sk=SKINS.find(x=>x[0]===k);toast('「'+sk[1]+'」にしました');skinSheet();}\n"
    "function skinClose(){const a=$('#ssheet'),b=$('#scover');if(a)a.classList.remove('on');if(b)b.classList.remove('on');document.body.classList.remove('hs-open');}\n"
    "function goStart(k){")
rep(" const ttl=!G||UI.title;", " document.body.classList.remove('hs-open');const ttl=!G||UI.title;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
