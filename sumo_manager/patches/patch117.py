# v114:漆黒の画面で部屋の画面の左右の欄を暗いグレーの半透明(70%)+ぼかし+字の影に(見本 dk1)。v113 → v114
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=113;\nconst SAVE='sumoManager113',SAVE112", "const APPV=114;\nconst SAVE='sumoManager114',SAVE113='sumoManager113',SAVE112")
rep('[SAVE112,SAVE111', '[SAVE113,SAVE112,SAVE111')
rep('<title>Grand Sumo Manager v113','<title>Grand Sumo Manager v114')
CSS=open(__file__.replace('patch117.py','dk114.css'),encoding='utf-8').read().strip()
rep("</head>","<style>/* v114 漆黒の左右の欄を半透明(見本 dk1) */"+CSS+"</style></head>")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
