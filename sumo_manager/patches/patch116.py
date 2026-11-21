# v113:「育つ環境」を力士のまどと稽古の画面に出す(見本 ev1)。v112 → v113
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=112;\nconst SAVE='sumoManager112',SAVE111", "const APPV=113;\nconst SAVE='sumoManager113',SAVE112='sumoManager112',SAVE111")
rep('[SAVE111,SAVE110', '[SAVE112,SAVE111,SAVE110')
rep('<title>Grand Sumo Manager v112','<title>Grand Sumo Manager v113')
JS=open(__file__.replace('patch116.py','ev113.js'),encoding='utf-8').read()
rep('</body>','<script>'+JS+'</script></body>')
open(dst,'w',encoding='utf-8').write(s)
print('ok')
