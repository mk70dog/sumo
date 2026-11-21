# 見本 ht1〜ht3:スタート画面の題字を「sumo」(小文字)+下に「相撲部屋経営 × 力士育成」(一人相撲と同じ字)。GRAND・MANAGER は消す。v109 から
base=open('sumo_manager_v109.html',encoding='utf-8').read()
OLD='<small>GRAND</small><b>SUMO</b><small>MANAGER</small>'
assert base.count(OLD)==1
GOLD="background:linear-gradient(180deg,#fff3c4,#e2b54a 55%,#a5741e);-webkit-background-clip:text;background-clip:text;color:transparent"
V={
1:('「一人相撲」と同じ字(Dela・金)で一行',
 '<b>sumo</b><i class="hn">相撲部屋経営<em>×</em>力士育成</i>',
 ".t1 b{letter-spacing:.04em!important}.t1 .hn{display:block;font-style:normal;font-family:Dela,sans-serif;color:#f0c75e;font-size:min(3.3vw,3.8vh,34px);letter-spacing:.12em;margin:.3em 0 .05em;white-space:nowrap}.t1 .hn em{font-style:normal;font-family:sans-serif;font-weight:700;color:#f3e3c3;margin:0 .35em}"),
2:('「一人相撲」のボタンと同じ箱(ドットの黒地・金の縁)に入れる',
 '<b>sumo</b><i class="hn"><span>相撲部屋経営<em>×</em>力士育成</span></i>',
 ".t1 b{letter-spacing:.04em!important}.t1 .hn{display:block;font-style:normal;margin:.35em 0 .1em}.t1 .hn span{display:inline-block;position:relative;isolation:isolate;font-family:Dela,sans-serif;color:#f0c75e;font-size:min(3vw,3.5vh,30px);letter-spacing:.12em;padding:.35em .9em;border:2px solid #f0c75e;border-radius:6px;background:#2a2018;white-space:nowrap}.t1 .hn span:before{content:'';position:absolute;inset:0;border-radius:inherit;z-index:-1;background-image:radial-gradient(#f0c75e .6px,transparent 1px);background-size:3px 3px;opacity:.14}.t1 .hn em{font-style:normal;font-family:sans-serif;font-weight:700;color:#f3e3c3;margin:0 .35em}"),
3:('二段:「相撲部屋経営」「×」「力士育成」を大きめに',
 '<b>sumo</b><i class="hn"><span>相撲部屋経営</span><em>×</em><span>力士育成</span></i>',
 ".t1 b{letter-spacing:.04em!important}.t1 .hn{display:flex;align-items:center;justify-content:center;gap:.4em;font-style:normal;font-family:Dela,sans-serif;color:#f0c75e;font-size:min(3.8vw,4.3vh,40px);letter-spacing:.1em;margin:.3em 0 .05em;white-space:nowrap}.t1 .hn em{font-style:normal;font-family:sans-serif;font-weight:700;color:#f3e3c3;font-size:.8em}"),
}
for k,(note,html,css) in V.items():
    s=base.replace(OLD,html).replace('</head>','<style>'+css+'</style></head>',1)
    s=s.replace('</body>',"<div style='position:fixed;left:6px;top:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999'>見本 ht%d:%s</div></body>"%(k,note),1)
    open('samples/ht%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
