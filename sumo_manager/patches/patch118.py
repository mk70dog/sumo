# v115:部屋の画面の「弟子の様子」を小さな札に(見本 ws2)。v114 → v115
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=114;\nconst SAVE='sumoManager114',SAVE113", "const APPV=115;\nconst SAVE='sumoManager115',SAVE114='sumoManager114',SAVE113")
rep('[SAVE113,SAVE112', '[SAVE114,SAVE113,SAVE112')
rep('<title>Grand Sumo Manager v114','<title>Grand Sumo Manager v115')
JS=open(__file__.replace('patch118.py','ws115.js'),encoding='utf-8').read()
rep('</body>','<script>'+JS+'</script></body>')
open(dst,'w',encoding='utf-8').write(s)
print('ok')
