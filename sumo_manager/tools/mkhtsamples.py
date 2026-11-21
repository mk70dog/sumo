# 見本 ht1〜ht3:スタート画面の題字を「sumo」(小文字)+下に「相撲部屋経営 × 力士育成」(一人相撲と同じ字)。GRAND・MANAGER は消す。v109 から
base=open('sumo_manager_v109.html',encoding='utf-8').read()
OLD='<small>GRAND</small><b>SUMO</b><small>MANAGER</small>'
assert base.count(OLD)==1
GOLD="background:linear-gradient(180deg,#fff3c4,#e2b54a 55%,#a5741e);-webkit-background-clip:text;background-clip:text;color:transparent"
T='相撲部屋経営<em>×</em>力士育成'
HN=".t1 b{letter-spacing:.04em!important}.t1 .hn{display:block;font-style:normal;font-family:Dela,sans-serif;color:#f0c75e;font-size:min(2.2vw,2.6vh,22px);letter-spacing:.14em;margin:.45em 0 .1em;white-space:nowrap}.t1 .hn em{font-style:normal;font-family:sans-serif;font-weight:700;color:#f3e3c3;margin:0 .35em}"
V={
1:('黒い板はそのまま、金の枠を消す',
 '<b>sumo</b><i class="hn">'+T+'</i>',
 HN+".t1{border:none!important;outline:none!important}"),
2:('板も枠も消して、絵の上に字だけ(影で読みやすく)',
 '<b>sumo</b><i class="hn">'+T+'</i>',
 HN+".t1{border:none!important;outline:none!important;background:none!important;box-shadow:none!important}.t1 b{filter:drop-shadow(0 3px 2px #000) drop-shadow(0 0 12px #000c)!important}.t1 .hn{text-shadow:0 2px 3px #000,0 0 10px #000}"),
3:('枠を消し、板を半分すける黒にして絵が少し見える',
 '<b>sumo</b><i class="hn">'+T+'</i>',
 HN+".t1{border:none!important;outline:none!important;background:rgba(20,16,12,.62)!important;box-shadow:0 0 40px 20px rgba(20,16,12,.45)!important;border-radius:6px}"),
}
for k,(note,html,css) in V.items():
    s=base.replace(OLD,html).replace('</head>','<style>'+css+'</style></head>',1)
    s=s.replace('</body>',"<div style='position:fixed;left:6px;top:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999'>見本 ht%d:%s</div></body>"%(k,note),1)
    open('samples/ht%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
