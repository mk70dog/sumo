# v67 -> v68:幕内上位の取組にも予想印(見本 jo1)・メディアの表に新聞の「予想の腕」
# 部品は patches/jo71_ui.html(tools/mkjosamples.py の見本の script から、見本用の部分を外したもの)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v67</title>', '<title>Sumo Manager v68</title>')
rep("const APPV=67;\nconst SAVE='sumoManager67',SAVE66", "const APPV=68;\nconst SAVE='sumoManager68',SAVE67='sumoManager67',SAVE66")
rep('[SAVE66,SAVE65', '[SAVE67,SAVE66,SAVE65')
rep(" if(g.v===66){g.v=67;}\n return g.v===67?g:null;}", " if(g.v===66){g.v=67;}\n if(g.v===67){g.v=68;}\n return g.v===68?g:null;}")
rep('G={v:67,', 'G={v:68,')
ui = open('patches/jo71_ui.html', encoding='utf-8').read()
i = s.rfind('</body>')
s = s[:i] + ui + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
