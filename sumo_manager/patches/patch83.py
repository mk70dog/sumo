# v79 -> v80:二人相撲 第 1 段階(見本 mp3:どの画面にも上に帯、部屋の画面にふたりの部屋のカード。ダルマさん「実施」)
# 親の iPad が計算し、GitHub の Gist(world.txt=圧縮した世界、host.json、guest.json)で受け渡す。子は稽古・強さ・取組の作戦・新弟子の勧誘を決める。
# 子の部屋のお金・スタッフ・施設は、ほかの部屋と同じく自動。ふたりとも準備できたら進む。10 分で親は前の設定のまま進める。
# 親の記録は 'gsmMP'、子の状態は 'gsmGuest'、鍵は 'gsmTok'(一人相撲の記録とは別)。テスト用に URL の #mpmock で Gist の代わりに localStorage を使う。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v79</title>', '<title>Grand Sumo Manager v80</title>')
rep("const APPV=79;\nconst SAVE='sumoManager79',SAVE78", "const APPV=80;\nconst SAVE='sumoManager80',SAVE79='sumoManager79',SAVE78")
rep('[SAVE78,SAVE77', '[SAVE79,SAVE78,SAVE77')
rep(" if(g.v===78){g.v=79;}\n return g.v===79?g:null;}", " if(g.v===78){g.v=79;}\n if(g.v===79){g.v=80;}\n return g.v===80?g:null;}")
rep('G={v:79,', 'G={v:80,')
# 子の部屋の稽古は子が決めたもの(r.gm・r.gi)
rep("let mk=isOwn?r.menu:(r.inj?'休':aiMenu(r)),it=isOwn?r.it:(G.heya[r.h].hard&&Math.random()<.4?2:1);",
    "const gsel=!isOwn&&G.mp&&r.h===G.mp.gh&&r.gm;let mk=isOwn?r.menu:(r.inj?'休':(gsel?r.gm:aiMenu(r))),it=isOwn?r.it:(gsel?r.gi:(G.heya[r.h].hard&&Math.random()<.4?2:1));")
# スタート画面の二人相撲は準備中ではなくなる(v80 の上書きで中身を出す)
rep("ふたりで別々の部屋を見守り、同じ番付で戦う(準備中)", "ふたりで別々の部屋を見守り、同じ番付で戦う")
mp = open('patches/mp80.js', encoding='utf-8').read()
i = s.rfind('</body>')
s = s[:i] + mp + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
