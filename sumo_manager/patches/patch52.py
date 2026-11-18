# 取組のまぐれの幅を少し小さく(BE.sd 48 -> 44)  v48 -> v49
# v48 で幕下→十両の並びを直したあと、平幕の優勝が 22%(実際 15%)・横綱 38%(実際 45%)・優勝の勝ち星 12.7(実際 13.15)・決定戦 34%(実際 22%)とずれたため。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v48</title>', '<title>Sumo Manager v49</title>')
rep("const APPV=48;\nconst SAVE='sumoManager48',SAVE47", "const APPV=49;\nconst SAVE='sumoManager49',SAVE48='sumoManager48',SAVE47")
rep('[SAVE47,SAVE46', '[SAVE48,SAVE47,SAVE46')
rep(" if(g.v===47){g.v=48;}\n return g.v===48?g:null;}", " if(g.v===47){g.v=48;}\n if(g.v===48){g.v=49;}\n return g.v===49?g:null;}")
rep('G={v:48,', 'G={v:49,')
rep("const BE={k:2.5,sd:48};", "const BE={k:2.5,sd:44};")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
