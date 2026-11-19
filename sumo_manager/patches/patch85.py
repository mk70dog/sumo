# v81 -> v82:設定に「GitHub の鍵(Gist の設定)」の読み込み・書き出し(ダルマさん「これをインポートさせたい。設定に GIST インポートエクスポート作成」)
# ASL アプリの aslsk_gist_settings(gistToken・gistId)を読み込める。鍵だけ使い、ASL の Gist の ID は使わない。書き出しは gsm_gist_settings(鍵+二人相撲の合言葉)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v81</title>', '<title>Grand Sumo Manager v82</title>')
rep("const APPV=81;\nconst SAVE='sumoManager81',SAVE80", "const APPV=82;\nconst SAVE='sumoManager82',SAVE81='sumoManager81',SAVE80")
rep('[SAVE80,SAVE79', '[SAVE81,SAVE80,SAVE79')
rep(" if(g.v===80){g.v=81;}\n return g.v===81?g:null;}", " if(g.v===80){g.v=81;}\n if(g.v===81){g.v=82;}\n return g.v===82?g:null;}")
rep('G={v:81,', 'G={v:82,')
js = open('patches/mp82.js', encoding='utf-8').read()
i = s.rfind('</body>')
s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
