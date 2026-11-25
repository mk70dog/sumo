# v176 -> v177:協会の役員(理事 10 人・理事長)と部屋の数のゆるやかな減少(ダルマさん「実施」→ 見本 ky1)。
#   本物:役員候補選挙は 1 期 2 年・理事の定数 10 人・全親方の投票(デイリー 2018/2/2)。新理事 10 人の理事会で理事長を選ぶ(日刊ゲンダイ 177758)。
#        2026 年 3 月 八角理事長の続投・実質 6 期目(週刊女性PRIME 41018)。2026 年の理事の顔ぶれ(秋田魁新報 2026/3/25)。
#   推定:選ばれやすさ、選挙のとき 64 歳以上は出ない、一門ごとに最低 1 人。部屋の数は 2004 年 55 → 2024 年 44(Number 10878・moneypost 1153439)に合わせ、
#        新しい部屋が開く目安を 45 から年 0.4 ずつ下げる(下限 34)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=176;\nconst SAVE='sumoManager176',SAVE175", "const APPV=177;\nconst SAVE='sumoManager177',SAVE176='sumoManager176',SAVE175")
rep('[SAVE175,SAVE174', '[SAVE176,SAVE175,SAVE174')
rep('<title>Grand Sumo Manager v176', '<title>Grand Sumo Manager v177')
kyo = open(os.path.join(here, 'kyo177.js'), encoding='utf-8').read()
rep('function v8Basho(sum){\n toshiBasho();\n', kyo + 'function v8Basho(sum){\n toshiBasho();\n try{kyoBasho();}catch(e){console.error(e);}\n')
rep('(op.length<42?2:op.length<44?1.2:op.length<46?.5:.06)', '(()=>{const tg=Math.max(34,45-(curYear()-2026)*.4);return op.length<tg-3?2:op.length<tg-1?1.2:op.length<tg+1?.5:.06;})()')
ui = open(os.path.join(here, 'ky177_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
