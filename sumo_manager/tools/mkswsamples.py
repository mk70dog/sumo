# 見本 sw1〜sw3:スタート画面の次の画面(一人相撲)の文言をシンプルに。v110+見本 bt2(ボタンの枠線なし)
base=open('sumo_manager_v110.html',encoding='utf-8').read()
BT2='.st-go button{border-color:transparent!important;border-width:0!important}'
R0="<b>実在の部屋を選ぶ</b><small>2026 年九州場所の番付から。45 部屋・592 人の中から部屋を選び、その部屋の歩みを見守ります。</small>"
D0="<b>部屋付き親方として独立する</b><small>実在の部屋付き親方を選び、内弟子を連れて新しい部屋を興します。</small>"
K0="<b>← 一人相撲・二人相撲を選び直す</b>"
V={1:('二人相撲の画面と同じ言い方(題+ひとこと)',"<b>実在の部屋で始める</b><small>45 部屋から選ぶ</small>","<b>独立して始める</b><small>部屋付き親方が新しい部屋を興す</small>","<b>← 戻る</b>"),
   2:('題だけ(説明なし)',"<b>実在の部屋</b>","<b>親方として独立</b>","<b>← 戻る</b>"),
   3:('題+数字だけの短い説明',"<b>実在の部屋を選ぶ</b><small>45 部屋・592 人</small>","<b>親方として独立する</b><small>内弟子を連れて新しい部屋へ</small>","<b>← 戻る</b>")}
for k,(n,r,d,bk) in V.items():
    s=base
    for a,b in ((R0,r),(D0,d)):
        assert s.count(a)==1;s=s.replace(a,b)
    assert s.count(K0)==2;s=s.replace(K0,bk)
    s=s.replace('</head>','<style>'+BT2+'</style></head>',1).replace('</body>',"<div style='position:fixed;left:6px;top:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999'>見本 sw%d:%s</div><script>addEventListener('load',()=>setTimeout(()=>{try{topMode('one')}catch(e){}},300));</script></body>"%(k,n),1)
    open('samples/sw%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
