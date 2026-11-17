# 現実とのマッチング(2):力の伸びしろを縮めて、上位の強さ・優勝の分かれ方を実際に合わせる  v28 -> v29
# 実際(sumodb の優勝一覧、2015 年 1 月〜2025 年 11 月の 65 場所):横綱 29・大関 12・関脇 12・小結 2・前頭 10 回、優勝の勝ち星の平均 13.15。
# v28 は年月とともに全員の力が上限 20 近くまで上がり(15 年で幕下の平均 11.1→14.5)、横綱 25%・平幕 40% 超の優勝、平均 12.35 勝だった。
# 新しく作る力士の伸びしろを 日本出身 0.75 倍・外国出身 0.85 倍に(外国出身は選ばれた人が来日するため。2026 年九州の幕内は外国出身 31%)。倍率は測定に合わせた推定。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
JP = float(sys.argv[3]) if len(sys.argv) > 3 else .75
FR = float(sys.argv[4]) if len(sys.argv) > 4 else .85
rep('<title>Sumo Manager v28</title>', '<title>Sumo Manager v29</title>')
rep("const APPV=28;\nconst SAVE='sumoManager28',SAVE27", "const APPV=29;\nconst SAVE='sumoManager29',SAVE28='sumoManager28',SAVE27")
rep('[SAVE27,SAVE26', '[SAVE28,SAVE27,SAVE26')
rep(" if(g.v===27){g.v=28;}\n return g.v===28?g:null;}", " if(g.v===27){g.v=28;}\n if(g.v===28){g.v=29;}\n return g.v===29?g:null;}")
rep('G={v:28,', 'G={v:29,')
rep("const rm=o.room*(MIND.includes(k)?.6:1)+randn()*.8;", "const rm=o.room*(o.fr?%s:%s)*(MIND.includes(k)?.6:1)+randn()*.8;" % (FR, JP))
open(dst, 'w', encoding='utf-8').write(s)
print('ok', JP, FR)
