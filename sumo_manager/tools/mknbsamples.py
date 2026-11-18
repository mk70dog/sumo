# 見本 nb1〜3:土俵の中の文字を減らす・名前をバッジに・行司の位置(v61 に patches/nb66.py を当てる)
import sys;sys.path.insert(0,'patches');import nb66
base=open('sumo_manager_v61.html',encoding='utf-8').read()
NOTE={1:'nb1:名前を色の札(バッジ)に・土俵の中の文字なし・行司は離れた側',2:'nb2:名前は頭の 1 字の丸バッジ・行司は俵の近くを回る',3:'nb3:nb1+技や土俵際は上の帯に 1 行だけ'}
for v in (1,2,3):
    s=nb66.apply(base,v)
    js="<script>window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;go('home');while(G.phase==='train')doWeek();let x=null;for(let d=0;d<3&&!x;d++){const bs=advanceDay();x=bs.filter(y=>!y.fus&&y.ev&&y.ev.length>8&&G.R[y.w].d===0).sort((a,b)=>b.ev.length-a.ev.length)[0];}render();UI.dhT=[x];dhOpen('t',0);}catch(e){console.error(e)}},80);});</script>"
    s=s.replace('</body>',js+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'(「もう一度見る」で繰り返し)</div></body>',1).replace('<title>Sumo Manager v61</title>','<title>見本 nb%d</title>'%v,1)
    open('samples/nb%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
