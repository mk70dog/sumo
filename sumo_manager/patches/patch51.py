# 番付:幕下から十両に上がる力士の位置を十両の下のほうに(十両の勝ち越しで下がる不具合を直す)  v47 -> v48
# 前は幕下の 1 勝の重み(17)がそのまま十両の中まで届き、幕下上位の 4 勝 3 敗が十両の中ほどに入っていた。
# そのぶん十両の力士が押し下げられ、十両の 8 勝 7 敗で平均 1.5 枚下がっていた(目安は「1 勝の勝ち越しで 1 枚上がる」)。
# 幕内の負け越しの下がり方を 1.5 倍にする案も試したが、ほかの力士が押し上げられて 8 勝 7 敗が 2.5 枚上がるようになったのでやめた。
# 幕下の力士の並べ替えの値に下限:十両の最後から 7 枚上(幕下筆頭のとき)、幕下の枚数が下がるほど下。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v47</title>', '<title>Sumo Manager v48</title>')
rep("const APPV=47;\nconst SAVE='sumoManager47',SAVE46", "const APPV=48;\nconst SAVE='sumoManager48',SAVE47='sumoManager47',SAVE46")
rep('[SAVE46,SAVE45', '[SAVE47,SAVE46,SAVE45')
rep(" if(g.v===46){g.v=47;}\n return g.v===47?g:null;}", " if(g.v===46){g.v=47;}\n if(g.v===47){g.v=48;}\n return g.v===48?g:null;}")
rep('G={v:47,', 'G={v:48,')
rep("key[id]=r.pos-MV[d]*net*(1-DAMP[d]*Math.abs(net))-(c.yu?(d<=1?3:20):0)+Math.random()*.01;",
    "key[id]=r.pos-MV[d]*net*(1-DAMP[d]*Math.abs(net))-(c.yu?(d<=1?3:20):0)+Math.random()*.01;\n  if(d===2){const ms=divStart(2);key[id]=Math.max(key[id],ms-14+(r.pos-ms)*.5);}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
