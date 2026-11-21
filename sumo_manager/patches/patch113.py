# v110:スタート画面の題字を「sumo」(小文字)+「相撲部屋経営 × 力士育成」、GRAND・MANAGER と金の枠をなくす(見本 ht1)。v109 → v110
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=109;\nconst SAVE='sumoManager109',SAVE108", "const APPV=110;\nconst SAVE='sumoManager110',SAVE109='sumoManager109',SAVE108")
rep('[SAVE108,SAVE107', '[SAVE109,SAVE108,SAVE107')
rep('<title>Grand Sumo Manager v109','<title>Grand Sumo Manager v110')
rep('<small>GRAND</small><b>SUMO</b><small>MANAGER</small>','<b>sumo</b><i class="hn">相撲部屋経営<em>×</em>力士育成</i>')
CSS=open(__file__.replace('patch113.py','ht110.css'),encoding='utf-8').read().strip()
rep("</head>","<style>/* v110 題字(見本 ht1) */"+CSS+"</style></head>")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
