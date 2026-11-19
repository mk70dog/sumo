# v78 -> v79:名前を「Grand Sumo Manager」に(見本 ttl1:黒漆の札に金の字、ボタンも黒地に金の枠。ダルマさん「1」)
# ファイル名(sumo_manager_vNN.html)と URL・保存のキーは変えない。ホーム画面の名前は短く「Grand Sumo」(iPhone は長い名前が切れるため)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v78</title>', '<title>Grand Sumo Manager v79</title>')
rep("const APPV=78;\nconst SAVE='sumoManager78',SAVE77", "const APPV=79;\nconst SAVE='sumoManager79',SAVE78='sumoManager78',SAVE77")
rep('[SAVE77,SAVE76', '[SAVE78,SAVE77,SAVE76')
rep(" if(g.v===77){g.v=78;}\n return g.v===78?g:null;}", " if(g.v===77){g.v=78;}\n if(g.v===78){g.v=79;}\n return g.v===79?g:null;}")
rep('G={v:78,', 'G={v:79,')
rep('<meta name="apple-mobile-web-app-title" content="Sumo Manager">', '<meta name="apple-mobile-web-app-title" content="Grand Sumo">')
rep("'# Sumo Manager 不具合の報告'", "'# Grand Sumo Manager 不具合の報告'")
rep('<div class="st-title"><h1>Sumo Manager</h1></div>', '<div class="st-title"><h1 class="gsm"><div class="t1"><small>GRAND</small><b>SUMO</b><small>MANAGER</small></div></h1></div>')
rep("'<div class=\"st-h\">Sumo Manager</div>", "'<div class=\"st-h\">Grand Sumo Manager</div>")
CSS = ('<style id="gsmTitle">.st-title h1.gsm{all:unset;display:inline-block}'
 '.t1{display:inline-block;background:linear-gradient(180deg,#141210,#2a2018);border:2px solid #c9a24a;outline:1px solid #c9a24a;outline-offset:5px;padding:10px 34px 12px;box-shadow:0 10px 30px #000a;text-align:center}'
 '.t1 b{display:block;font-family:Dela,sans-serif;font-weight:400;font-size:clamp(46px,10vw,104px);line-height:1;letter-spacing:.12em;background:linear-gradient(180deg,#fff3c4,#e2b54a 55%,#a5741e);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 0 #000)}'
 '.t1 small{display:block;font:700 clamp(12px,2.2vw,20px)/1.6 Georgia,serif;letter-spacing:.9em;color:#e2c37a;margin-left:.9em}'
 '.st-go .st-real,.st-go .st-dok{background:linear-gradient(180deg,#1a1612,#2b2119);border-color:#c9a24a}.st-go button.big b{color:#f0c75e}.st-go .st-real b,.st-go .st-dok b{color:#f0c75e}'
 '@media(max-height:560px){.t1{padding:4px 20px 6px}.t1 b{font-size:40px}}</style>\n')
i = s.rfind('</body>')
s = s[:i] + CSS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
