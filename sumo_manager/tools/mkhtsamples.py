# 見本 ht1〜ht3:スタート画面の題字を「sumo」(小文字)+下に「力士ノ花道」。GRAND・MANAGER は消す。v109 から
base=open('sumo_manager_v109.html',encoding='utf-8').read()
OLD='<small>GRAND</small><b>SUMO</b><small>MANAGER</small>'
assert base.count(OLD)==1
GOLD="background:linear-gradient(180deg,#fff3c4,#e2b54a 55%,#a5741e);-webkit-background-clip:text;background-clip:text;color:transparent"
V={
1:('Dela の金の字で「力士ノ花道」(sumo と同じ字体)',
 '<b>sumo</b><i class="hn">力士ノ花道</i>',
 ".t1 b{letter-spacing:.04em!important;text-transform:none}.t1 .hn{display:block;font-style:normal;font-family:Dela,sans-serif;font-size:min(4.2vw,4.8vh,44px);letter-spacing:.35em;margin:.25em 0 .05em .35em;"+GOLD+";filter:drop-shadow(0 1px 0 #000)}"),
2:('朱の帯に白い明朝の字で「力士ノ花道」',
 '<b>sumo</b><i class="hn"><span>力士ノ花道</span></i>',
 ".t1 b{letter-spacing:.04em!important}.t1 .hn{display:block;font-style:normal;margin:.35em -.2em .1em}.t1 .hn span{display:inline-block;background:#b5361f;color:#fff8ea;font:700 min(3.6vw,4.2vh,36px)/1.5 SMin,'Hiragino Mincho ProN','Yu Mincho',serif;letter-spacing:.5em;padding:.1em .6em .1em 1.1em;border:1px solid #e2c37a;box-shadow:0 2px 6px #0008}"),
3:('金の線ではさんだ白い明朝の字で「—— 力士ノ花道 ——」',
 '<b>sumo</b><i class="hn">力士ノ花道</i>',
 ".t1 b{letter-spacing:.04em!important}.t1 .hn{display:flex;align-items:center;gap:.7em;font-style:normal;color:#f3e6c4;font:700 min(3.4vw,4vh,34px)/1.6 SMin,'Hiragino Mincho ProN','Yu Mincho',serif;letter-spacing:.45em;margin:.3em 0 .05em}.t1 .hn:before,.t1 .hn:after{content:'';flex:1;height:2px;background:linear-gradient(90deg,transparent,#c9a24a)}.t1 .hn:after{background:linear-gradient(90deg,#c9a24a,transparent)}"),
}
for k,(note,html,css) in V.items():
    s=base.replace(OLD,html).replace('</head>','<style>'+css+'</style></head>',1)
    s=s.replace('</body>',"<div style='position:fixed;left:6px;top:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999'>見本 ht%d:%s</div></body>"%(k,note),1)
    open('samples/ht%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
