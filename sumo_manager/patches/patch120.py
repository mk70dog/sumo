# v117:稽古タブを見やすく(見本 kt2 のおすすめ+kt1 の札)。v116 → v117
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=116;\nconst SAVE='sumoManager116',SAVE115", "const APPV=117;\nconst SAVE='sumoManager117',SAVE116='sumoManager116',SAVE115")
rep('[SAVE115,SAVE114', '[SAVE116,SAVE115,SAVE114')
rep('<title>Grand Sumo Manager v116','<title>Grand Sumo Manager v117')
JS=open(__file__.replace('patch120.py','kt117.js'),encoding='utf-8').read()
rep('</body>','<script>'+JS+'</script></body>')
open(dst,'w',encoding='utf-8').write(s)
print('ok')
