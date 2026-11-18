# v65 -> v66:素質を言葉で(見本 kotoba2:数字はそのまま+親方のひとこと)・取組前の予想印(見本 yoso1:新聞 3 紙の印を表で)
# 部品は patches/kyo69_ui.html(tools/mkkotobasamples.py の見本の script から、見本用の部分を外したもの)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v65</title>', '<title>Sumo Manager v66</title>')
rep("const APPV=65;\nconst SAVE='sumoManager65',SAVE64", "const APPV=66;\nconst SAVE='sumoManager66',SAVE65='sumoManager65',SAVE64")
rep('[SAVE64,SAVE63', '[SAVE65,SAVE64,SAVE63')
rep(" if(g.v===64){g.v=65;}\n return g.v===65?g:null;}", " if(g.v===64){g.v=65;}\n if(g.v===65){g.v=66;}\n return g.v===66?g:null;}")
rep('G={v:65,', 'G={v:66,')
ui = open('patches/kyo69_ui.html', encoding='utf-8').read()
i = s.rfind('</body>')
s = s[:i] + ui + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
