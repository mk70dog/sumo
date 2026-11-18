# v66 -> v67:新聞の予想印の当たり外れ(見本 tekichu1:記録の画面に表+大当たりの一覧)
# 部品は patches/tek70_ui.html(tools/mktekichusamples.py の見本の script から、見本用の部分を外したもの)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v66</title>', '<title>Sumo Manager v67</title>')
rep("const APPV=66;\nconst SAVE='sumoManager66',SAVE65", "const APPV=67;\nconst SAVE='sumoManager67',SAVE66='sumoManager66',SAVE65")
rep('[SAVE65,SAVE64', '[SAVE66,SAVE65,SAVE64')
rep(" if(g.v===65){g.v=66;}\n return g.v===66?g:null;}", " if(g.v===65){g.v=66;}\n if(g.v===66){g.v=67;}\n return g.v===67?g:null;}")
rep('G={v:66,', 'G={v:67,')
ui = open('patches/tek70_ui.html', encoding='utf-8').read()
i = s.rfind('</body>')
s = s[:i] + ui + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
