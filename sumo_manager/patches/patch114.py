# v111:スタート画面のボタンの枠線なし(見本 bt2)+一人相撲の次の画面の文言を短く(見本 sw3)。v110 → v111
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=110;\nconst SAVE='sumoManager110',SAVE109", "const APPV=111;\nconst SAVE='sumoManager111',SAVE110='sumoManager110',SAVE109")
rep('[SAVE109,SAVE108', '[SAVE110,SAVE109,SAVE108')
rep('<title>Grand Sumo Manager v110','<title>Grand Sumo Manager v111')
rep("<b>実在の部屋を選ぶ</b><small>2026 年九州場所の番付から。45 部屋・592 人の中から部屋を選び、その部屋の歩みを見守ります。</small>","<b>実在の部屋を選ぶ</b><small>45 部屋・592 人</small>")
rep("<b>部屋付き親方として独立する</b><small>実在の部屋付き親方を選び、内弟子を連れて新しい部屋を興します。</small>","<b>親方として独立する</b><small>内弟子を連れて新しい部屋へ</small>")
rep("<b>← 一人相撲・二人相撲を選び直す</b>","<b>← 戻る</b>",2)
rep("</head>","<style>/* v111 スタート画面のボタンの枠線なし(見本 bt2) */.st-go button{border-color:transparent!important;border-width:0!important}</style></head>")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
