# v118:稽古タブに「番付ごとにまとめて決める」欄(見本 kt5)。v117 → v118(kt117.js を kt118.js に差しかえ)
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=117;\nconst SAVE='sumoManager117',SAVE116", "const APPV=118;\nconst SAVE='sumoManager118',SAVE117='sumoManager117',SAVE116")
rep('[SAVE116,SAVE115', '[SAVE117,SAVE116,SAVE115')
rep('<title>Grand Sumo Manager v117','<title>Grand Sumo Manager v118')
d=__file__.replace('patch121.py','')
rep(open(d+'kt117.js',encoding='utf-8').read(),open(d+'kt118.js',encoding='utf-8').read())
open(dst,'w',encoding='utf-8').write(s)
print('ok')
