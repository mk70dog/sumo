# v116:部屋の画面の左側に部屋日誌(見本 dy1)。v115 → v116
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=115;\nconst SAVE='sumoManager115',SAVE114", "const APPV=116;\nconst SAVE='sumoManager116',SAVE115='sumoManager115',SAVE114")
rep('[SAVE114,SAVE113', '[SAVE115,SAVE114,SAVE113')
rep('<title>Grand Sumo Manager v115','<title>Grand Sumo Manager v116')
JS=open(__file__.replace('patch119.py','dy116.js'),encoding='utf-8').read()
rep('</body>','<script>'+JS+'</script></body>')
open(dst,'w',encoding='utf-8').write(s)
print('ok')
