# ホーム画面のアプリで上のバーが出ないように:マニフェスト(受け持ち範囲 /sumo/)を読む  v23 -> v24
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v23</title>', '<title>Sumo Manager v24</title>')
rep("const APPV=23;\nconst SAVE='sumoManager23',SAVE22", "const APPV=24;\nconst SAVE='sumoManager24',SAVE23='sumoManager23',SAVE22")
rep('[SAVE22,SAVE21,SAVE20', '[SAVE23,SAVE22,SAVE21,SAVE20')
rep(" if(g.v===22){g.v=23;}\n return g.v===23?g:null;}", " if(g.v===22){g.v=23;}\n if(g.v===23){g.v=24;}\n return g.v===24?g:null;}")
rep('G={v:23,', 'G={v:24,')
rep('<meta name="apple-mobile-web-app-title" content="Sumo Manager">',
    '<meta name="apple-mobile-web-app-title" content="Sumo Manager">\n<meta name="apple-mobile-web-app-status-bar-style" content="black">\n<link rel="manifest" href="../manifest.webmanifest">')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
