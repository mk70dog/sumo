# 見本 gun1〜3:行司の軍配と終盤の観客(v61 に patches/gun65.py を当て、取組のまどを自動で開く)
import sys;sys.path.insert(0,'patches');import gun65
base=open('sumo_manager_v61.html',encoding='utf-8').read()
NOTE={1:'gun1:軍配をぐっと上げて差し出す+観客の波',2:'gun2:軍配+客席から歓声の吹き出し',3:'gun3:軍配+総立ち・横綱が負けると座布団が舞う'}
for v in (1,2,3):
    s=gun65.apply(base,v)
    js="<script>window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;go('home');while(G.phase==='train')doWeek();let x=null;for(let d=0;d<15&&!x;d++){const bs=advanceDay();x=bs.find(y=>!y.fus&&G.R[y.l].t==='Y'&&G.R[y.w].d===0&&!G.R[y.w].t)||(d===14?bs.find(y=>!y.fus&&G.R[y.w].d===0):null);}render();UI.dhT=[x];dhOpen('t',0);document.querySelector('#modal h2,.modal h2')&&0;}catch(e){console.error(e)}},80);});</script>"
    s=s.replace('</body>',js+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'(「もう一度見る」で繰り返し)</div></body>',1).replace('<title>Sumo Manager v61</title>','<title>見本 gun%d</title>'%v,1)
    open('samples/gun%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
