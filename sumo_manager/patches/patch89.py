# v85 -> v86:お知らせの窓のボタン「わかった」を「OK」に(ダルマさん「わかった を OK に変更」)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v85</title>', '<title>Grand Sumo Manager v86</title>')
rep("const APPV=85;\nconst SAVE='sumoManager85',SAVE84", "const APPV=86;\nconst SAVE='sumoManager86',SAVE85='sumoManager85',SAVE84")
rep('[SAVE84,SAVE83', '[SAVE85,SAVE84,SAVE83')
rep(" if(g.v===84){g.v=85;}\n return g.v===85?g:null;}", " if(g.v===84){g.v=85;}\n if(g.v===85){g.v=86;}\n return g.v===86?g:null;}")
rep('G={v:85,', 'G={v:86,')
rep('onclick="closeM()">わかった</button>', 'onclick="closeM()">OK</button>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
