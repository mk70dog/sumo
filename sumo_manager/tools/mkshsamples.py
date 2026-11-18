# 見本 sh1〜5:「勝負あり」の見せ方(v61 に nb66 v1 → sh67 を当てる)
import sys;sys.path.insert(0,'patches');import nb66,sh67
base=nb66.apply(open('sumo_manager_v61.html',encoding='utf-8').read(),1)
NOTE={1:'sh1:行司の横に縦書きの筆文字',2:'sh2:土俵の真ん中にドンと大きく',3:'sh3:勝った側の色で土俵が光り、軍配の上に「東/西 ○○」の札',4:'sh4:土俵の上の帯に「勝負あり ○○の勝ち」',5:'sh5:行司の声の吹き出し'}
for v in range(1,6):
    s=sh67.apply(base,v)
    js="<script>window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;go('home');while(G.phase==='train')doWeek();const bs=advanceDay();const x=bs.filter(y=>!y.fus&&y.ev&&G.R[y.w].d===0).sort((a,b)=>a.ev.length-b.ev.length)[0];render();UI.dhT=[x];dhOpen('t',0);}catch(e){console.error(e)}},80);});</script>"
    s=s.replace('</body>',js+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'(「もう一度見る」で繰り返し)</div></body>',1).replace('<title>Sumo Manager v61</title>','<title>見本 sh%d</title>'%v,1)
    open('samples/sh%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
