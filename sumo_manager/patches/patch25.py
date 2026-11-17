# 見出しに「保存」「終了(トップへ)」、画面の色(スキン)を 6 種類から選べるように  v21 -> v22
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
rep('<title>Sumo Manager v21</title>', '<title>Sumo Manager v22</title>')
rep("const APPV=21;\nconst SAVE='sumoManager21',SAVE20", "const APPV=22;\nconst SAVE='sumoManager22',SAVE21='sumoManager21',SAVE20")
rep('[SAVE20,SAVE19,SAVE18', '[SAVE21,SAVE20,SAVE19,SAVE18')
rep(" if(g.v===20){g.v=21;}\n return g.v===21?g:null;}", " if(g.v===20){g.v=21;}\n if(g.v===21){g.v=22;}\n return g.v===22?g:null;}")
rep('G={v:21,', 'G={v:22,')

# --- スキン(色の組み合わせ) ---
K = ['washi','washi2','paper','sumi','sumi2','mute','shu','shu2','kin','ai','ai2','midori','line',
     'hdr1','hdr2','hdrtx','hdrsub','hdrnum','th','rowline','me','hover','soft','input','btn1','btn2','btnbd',
     'nav1','nav2','main1','main2','hl','hlbd','evbg','dots']
SK = {
 'yoru':   ('墨の夜', '#16130f #1f1b16 #24201a #ece4d3 #c9bfac #968b78 #e0583c #f07a5e #d9b25e #8fb0e0 #a9c3ea #7fbf8c #4a4236 #000000 #0d0b09 #ece4d3 #b8a984 #f1d38e #2e2921 #3a342b #4a2a22 #302a22 #3a342b #1c1814 #3a332a #2c2620 #5a5040 #8a2b1a #6b1f12 #c8432a #9e2d18 #2e2716 #6b5a2e #221d16 rgba(255,240,200,.04)'),
 'ai':     ('藍染め', '#e8edf3 #dbe3ec #f7f9fc #14213a #3a4a66 #6b7890 #b23a2a #d25a44 #9a7a3a #1f3a6b #3d5f99 #2f6b55 #b4c2d6 #13284d #1d3866 #eef3fa #b9c9e3 #ffd98a #d6e0ec #d3dce8 #fde7df #e6edf6 #d6e0ec #fbfdff #f2f6fb #d9e3ef #8fa3c0 #1f3a6b #142a52 #2f5597 #1f3d75 #eef3fb #b9cbe6 #f9fbff rgba(40,70,120,.06)'),
 'sakura': ('桜', '#fbf1f2 #f5e3e6 #fffafb #3a2228 #6a4a52 #9a7f86 #c2405a #e0708a #b08a4a #6b3a5c #8c5a7d #5a7d4a #e6c6cd #6b2e45 #8a3d5a #fff2f5 #f3c9d5 #ffe08a #f6dfe4 #f0dce0 #fde0e6 #fbeaee #f1dde2 #fffdfe #fff5f7 #f4dbe1 #d9a9b5 #a8456a #8a3556 #d4557a #b03a5f #fff3f6 #f0c4d0 #fffafb rgba(200,90,120,.06)'),
 'nishiki':('錦絵', '#f5ecd7 #ecdfc0 #fffaee #1c1408 #4d3d22 #85724f #c0261a #e04a35 #b8892c #3d2a6b #5a4590 #2a7a4a #d9c391 #a01f14 #c0291b #fff6e0 #f7d9a8 #ffe38a #f0dfb4 #eadcb5 #fbdcc8 #f7ead0 #eadcb5 #fffdf5 #fbf1dc #ecd9ae #b8995a #4b2a6b #36204f #c8432a #9e2d18 #fff3d6 #e3c27a #fffaee rgba(160,100,30,.07)'),
 'banzuke':('番付(白黒)', '#f4f4f1 #e8e8e4 #ffffff #000000 #2a2a2a #5c5c5c #b00000 #d03030 #7a5c18 #000000 #333333 #2a6a2a #999999 #000000 #111111 #ffffff #cccccc #ffffff #e8e8e4 #cccccc #f3e0e0 #f0f0ec #dddddd #ffffff #ffffff #eeeeee #777777 #000000 #000000 #b00000 #900000 #f7f7f2 #aaaaaa #ffffff rgba(0,0,0,0)'),
}
css = ['/* v22 スキン */', '.hbtns{display:flex;gap:6px}.hbtn{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.35);color:inherit;border-radius:3px;padding:2px 10px;font:13px/1.6 var(--kaku);min-height:30px}.hbtn:active{background:rgba(255,255,255,.25)}',
       '#toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom));transform:translateX(-50%);background:rgba(20,15,10,.88);color:#fff;padding:8px 18px;border-radius:999px;font:14px var(--kaku);z-index:60;opacity:0;transition:opacity .25s;pointer-events:none}#toast.on{opacity:1}',
       '.skins{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.skins button{display:flex;align-items:center;gap:8px;background:var(--paper);border:2px solid var(--line);border-radius:6px;padding:8px;font:14px var(--kaku);color:var(--sumi);min-height:48px;text-align:left}.skins button.on{border-color:var(--shu);box-shadow:0 0 0 2px var(--shu) inset}.skins i{display:inline-flex;width:42px;height:28px;border-radius:3px;overflow:hidden;flex:none;border:1px solid rgba(0,0,0,.2)}.skins i b{flex:1}']
JSK = []
for k, (name, vals) in SK.items():
    v = dict(zip(K, vals.split()))
    assert len(v) == len(K), k
    b = 'body.sk-' + k
    css.append(b + '{--washi:%(washi)s;--washi2:%(washi2)s;--paper:%(paper)s;--sumi:%(sumi)s;--sumi2:%(sumi2)s;--mute:%(mute)s;--shu:%(shu)s;--shu2:%(shu2)s;--kin:%(kin)s;--ai:%(ai)s;--ai2:%(ai2)s;--midori:%(midori)s;--line:%(line)s;background-color:%(washi)s;background-image:radial-gradient(%(dots)s 1px,transparent 1px),radial-gradient(%(dots)s 1px,transparent 1px)}' % v)
    css.append((b + ' #hdr{background:linear-gradient(%(hdr1)s,%(hdr2)s);color:%(hdrtx)s}' + b + ' #hdr .title small{color:%(hdrsub)s}' + b + ' #hdr .stat b{color:%(hdrnum)s}') % v)
    css.append((b + ' #nav button,' + b + ' .btn,' + b + ' .divbtn button{background:linear-gradient(%(btn1)s,%(btn2)s);border-color:%(btnbd)s;color:%(sumi)s}' +
                b + ' #nav button.on,' + b + ' .btn.ai,' + b + ' .divbtn button.on{background:linear-gradient(%(nav1)s,%(nav2)s);border-color:%(nav2)s;color:#fff}' +
                b + ' .btn.main{background:linear-gradient(%(main1)s,%(main2)s);border-color:%(main2)s;color:#fff}') % v)
    css.append((b + ' .tb th,' + b + ' .bz td.rk{background:%(th)s}' + b + ' .tb td,' + b + ' .bz td,' + b + ' .bout,' + b + ' .log div,' + b + ' .stf,' + b + ' .kr{border-bottom-color:%(rowline)s}' +
                b + ' .tb tr.me td,' + b + ' .bz .me{background:%(me)s}' + b + ' .tb tr.clk:hover td{background:%(hover)s}' +
                b + ' .bar,' + b + ' .gg,' + b + ' .daybar i{background:%(soft)s}' + b + ' .hl{background:%(hl)s;border-color:%(hlbd)s}' + b + ' .ev{background:%(evbg)s}' +
                b + ' .nx,' + b + ' .atc,' + b + ' .spk,' + b + ' select,' + b + ' input[type=text],' + b + ' textarea{background:%(input)s;color:%(sumi)s;border-color:%(line)s}' +
                b + ' .a1{color:%(mute)s}' + b + ' .st-wrap .start{background:%(paper)s}') % v)
    JSK.append("['%s','%s',['%s','%s','%s']]" % (k, name, v['hdr1'], v['paper'], v['shu']))
css.append('body.sk-nishiki #hdr .cal{background:#4b2a6b;border:1px solid #d9b25e}body.sk-nishiki #hdr{border-bottom:3px solid #d9b25e}body.sk-nishiki .pn{border-top:3px solid #4b2a6b}')
css.append('body.sk-banzuke .pn{border-color:#000}body.sk-banzuke .pn h2{border-left-color:#000}body.sk-yoru .pn{box-shadow:none}body.sk-yoru #mdl .box{color:var(--sumi)}')
rep('</style>', '\n'.join(css) + '\n</style>', 1)

rep('<div id="mdl">', '<div id="toast"></div>\n<div id="mdl">')

# --- 見出しのボタン ---
rep("<span class=\"cal\">'+bname(G.bnum)+'・'+phaseText()+'</span>'+",
    "<span class=\"cal\">'+bname(G.bnum)+'・'+phaseText()+'</span><span class=\"hbtns\"><button class=\"hbtn\" onclick=\"saveNow()\">保存</button><button class=\"hbtn\" onclick=\"quitTop()\">終了(トップへ)</button></span>'+")

rep("function goStart(k){",
    "function toast(t){const e=$('#toast');if(!e)return;e.textContent=t;e.classList.add('on');clearTimeout(toast._t);toast._t=setTimeout(()=>e.classList.remove('on'),1600);}\n"
    "function saveNow(){save();toast('保存しました');}\n"
    "function quitTop(){save();UI.title=true;UI.start=null;closeM();render();window.scrollTo(0,0);toast('保存しました。「続きから」で戻れます');}\n"
    "const SKINS=[['std','和紙(標準)',['#1d1a16','#fbf8f1','#b5361f']]," + ','.join(JSK) + "];\n"
    "function skinNow(){try{return localStorage.getItem('sumoSkin')||'std';}catch(e){return 'std';}}\n"
    "function applySkin(k){const b=document.body;SKINS.forEach(x=>b.classList.remove('sk-'+x[0]));if(k&&k!=='std')b.classList.add('sk-'+k);\n"
    " const sk=SKINS.find(x=>x[0]===k)||SKINS[0];const m=document.querySelector('meta[name=theme-color]');if(m)m.setAttribute('content',sk[2][0]);}\n"
    "function setSkin(k){try{localStorage.setItem('sumoSkin',k);}catch(e){}applySkin(k);render();}\n"
    "function skinPanel(){const c=skinNow();return '<div class=\"pn\"><h2>画面の色(スキン)</h2><p class=\"kaku mute\" style=\"font-size:13px\">この端末での見た目だけを変えます。保存データには影響しません。</p><div class=\"skins\">'+\n"
    " SKINS.map(x=>'<button class=\"'+(x[0]===c?'on':'')+'\" onclick=\"setSkin(\\''+x[0]+'\\')\"><i>'+x[2].map(col=>'<b style=\"background:'+col+'\"></b>').join('')+'</i>'+x[1]+'</button>').join('')+'</div></div>';}\n"
    "function goStart(k){")

rep("'<div class=\"pn\"><h2>アプリの更新</h2>", "skinPanel()+'<div class=\"pn\"><h2>アプリの更新</h2>")

rep("applyMode(!!(G&&G.real));\nrender();\ncheckUpd(0);\n", "applyMode(!!(G&&G.real));\napplySkin(skinNow());\nrender();\ncheckUpd(0);\n")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
