# 文字の形(フォント)を選べるように(見本 font1・font3・font5)  v50 -> v51
# 字体は SIL Open Font License(fonts/OFL_*.txt)。ゲームで使う文字だけに減らした woff(fonts/、作り方は fontTools の pyftsubset、文字は fonts/chars.txt)を本体に埋め込む。
# 端末ごとに覚える(localStorage の sumoFont)。保存データには入れない。
import sys, os, base64
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(here, '..', 'fonts')
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
def ff(fam, fn, w):
    b = base64.b64encode(open(os.path.join(FD, fn), 'rb').read()).decode()
    return "@font-face{font-family:'%s';src:url(data:font/woff;base64,%s) format('woff');font-weight:%s;font-display:swap}" % (fam, b, w)
rep('<title>Sumo Manager v50</title>', '<title>Sumo Manager v51</title>')
rep("const APPV=50;\nconst SAVE='sumoManager50',SAVE49", "const APPV=51;\nconst SAVE='sumoManager51',SAVE50='sumoManager50',SAVE49")
rep('[SAVE49,SAVE48', '[SAVE50,SAVE49,SAVE48')
rep(" if(g.v===49){g.v=50;}\n return g.v===50?g:null;}", " if(g.v===49){g.v=50;}\n if(g.v===50){g.v=51;}\n return g.v===51?g:null;}")
rep('G={v:50,', 'G={v:51,')
css = ('<style id="fonts">' + ff('SMin','ShipporiMincho-Medium.woff','400') + ff('SMin','ShipporiMincho-Bold.woff','700')
       + ff('ZMG','ZenMaruGothic-Medium.woff','400') + ff('ZMG','ZenMaruGothic-Bold.woff','700') + ff('YSk','YujiSyuku-Regular.woff','400')
       + "body.fn-smin{--min:'SMin',serif}body.fn-maru{--min:'ZMG',sans-serif;--kaku:'ZMG',sans-serif}"
       + "body.fn-fude{--min:'SMin',serif}body.fn-fude h1,body.fn-fude h2,body.fn-fude .fuda,body.fn-fude #hdr .title,body.fn-fude .oc .nm,body.fn-fude .ring .c,body.fn-fude .st-title{font-family:'YSk',serif;font-weight:400}body.fn-fude #hdr .title small{font-family:'SMin',serif}"
       + ".fonts{display:flex;flex-wrap:wrap;gap:8px}.fonts button{border:1px solid var(--line);background:var(--paper);color:var(--sumi);border-radius:8px;padding:8px 12px;min-width:150px;text-align:left;cursor:pointer}.fonts button.on{border:2px solid var(--shu)}.fonts button b{display:block;font-size:20px;font-weight:700;margin-bottom:2px}.fonts button small{font:12px var(--kaku);color:var(--mute)}"
       + '</style>')
rep('</head>', css + '</head>')
rep("function setSkin(k){", """const FONTS=[['std','いつもの字','端末の字(ヒラギノなど)',''],['smin','しっぽり明朝','上品で読みやすい明朝',"'SMin',serif"],['maru','Zen 丸ゴシック','やわらかい丸文字',"'ZMG',sans-serif"],['fude','筆文字の見出し','見出しは佑字 肅、本文はしっぽり明朝',"'YSk',serif"]];
function fontNow(){try{return localStorage.getItem('sumoFont')||'std';}catch(e){return 'std';}}
function applyFont(k){const b=document.body;FONTS.forEach(x=>b.classList.remove('fn-'+x[0]));if(k&&k!=='std')b.classList.add('fn-'+k);}
function setFont(k){try{localStorage.setItem('sumoFont',k);}catch(e){}applyFont(k);render();}
function fontPanel(){const c=fontNow();return '<div class="pn"><h2>文字の形</h2><p class="kaku mute" style="font-size:13px">この端末での見た目だけを変えます。保存データには影響しません。字体は無料で使えるもの(SIL Open Font License)です。</p><div class="fonts">'+FONTS.map(x=>'<button class="'+(x[0]===c?'on':'')+'" onclick="setFont(\\''+x[0]+'\\')"><b'+(x[3]?' style="font-family:'+x[3]+'"':'')+'>相撲部屋</b>'+x[1]+'<br><small>'+x[2]+'</small></button>').join('')+'</div></div>';}
function setSkin(k){""")
rep(" skinPanel()+'<div class=\"pn\"><h2>アプリの更新</h2>", " skinPanel()+fontPanel()+'<div class=\"pn\"><h2>アプリの更新</h2>")
rep("\napplySkin(skinNow());\nrender();", "\napplySkin(skinNow());applyFont(fontNow());\nrender();")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
