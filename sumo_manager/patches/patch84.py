# v80 -> v81:スタート画面の大きさ(見本 sz1、ダルマさん「SZ1」):題字 1.3 倍、一人相撲・二人相撲のボタンを横に細長く(高さ半分)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v80</title>', '<title>Grand Sumo Manager v81</title>')
rep("const APPV=80;\nconst SAVE='sumoManager80',SAVE79", "const APPV=81;\nconst SAVE='sumoManager81',SAVE80='sumoManager80',SAVE79")
rep('[SAVE79,SAVE78', '[SAVE80,SAVE79,SAVE78')
rep(" if(g.v===79){g.v=80;}\n return g.v===80?g:null;}", " if(g.v===79){g.v=80;}\n if(g.v===80){g.v=81;}\n return g.v===81?g:null;}")
rep('G={v:80,', 'G={v:81,')
CSS = ('<style id="sz1">.t1 b{font-size:clamp(60px,13vw,136px)}.t1 small{font-size:clamp(14px,2.8vw,26px)}.t1{padding:14px 44px 16px}'
 '.st-go button.big{padding:10px 12px}.st-go button.big b{font-size:clamp(22px,4vw,34px);margin:0}.st-go button.big small{font-size:12px}'
 '@media(max-height:560px){.t1{padding:4px 20px 6px}.t1 b{font-size:44px}}</style>\n')
i = s.rfind('</body>')
s = s[:i] + CSS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
