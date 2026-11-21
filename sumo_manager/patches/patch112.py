# v109:漆黒(朱・金・銀)の部屋の画面の欄を、少し薄い暗いグレーの細かいドット地に、枠なし(見本 dt1)。v108 → v109
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=108;\nconst SAVE='sumoManager108',SAVE107", "const APPV=109;\nconst SAVE='sumoManager109',SAVE108='sumoManager108',SAVE107")
rep('[SAVE107,SAVE106', '[SAVE108,SAVE107,SAVE106')
rep('<title>Grand Sumo Manager v108','<title>Grand Sumo Manager v109')
CSS=open(__file__.replace('patch112.py','dt109.css'),encoding='utf-8').read().strip()
rep("</head>","<style>/* v109 漆黒の部屋の画面の欄(見本 dt1) */"+CSS+"</style></head>")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
