# 見本 dg0〜dg5:取組の動画の絵(v107 に tools/dg_sample.js を足し、取組のまどを自動で開く)。#dg0〜#dg5 で切りかえ
base=open('sumo_manager_v107.html',encoding='utf-8').read()
js=open('tools/dg_sample.js',encoding='utf-8').read()
auto="""<script>window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();{let z=20261121;Math.random=()=>{z=(z*1103515245+12345)>>>0;return (z>>>8)/16777216;};}newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;go('home');let n=0;while(G.phase==='train'&&n++<40)doWeek();let x=null;for(let d=0;d<15&&!x;d++){const bs=advanceDay();x=bs.find(y=>!y.fus&&y.ev&&y.ev.length>3&&G.R[y.w].d===0&&G.R[y.l].d===0&&/投げ/.test(y.k))||(d===14?bs.find(y=>!y.fus&&G.R[y.w].d===0):null);}render();UI.dhT=[x];window.DGB=x;dhOpen('t',0);}catch(e){console.error(e)}},80);});</script>"""
NOTE={0:'dg0:今のまま',1:'dg1:本物に近い土俵',2:'dg2:錦絵風',3:'dg3:中継風(斜め上から)',4:'dg4:見やすさ重視',5:'dg5:夜の国技館'}
note="<div id=dgnote style='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999'></div><script>document.getElementById('dgnote').textContent='見本 '+(%s)[DGV]+'(「もう一度見る」で繰り返し。#dg0〜#dg5 で切りかえ)';window.addEventListener('hashchange',()=>location.reload());</script>"%__import__('json').dumps(NOTE,ensure_ascii=False).replace('"0"','0').replace('"1"','1').replace('"2"','2').replace('"3"','3').replace('"4"','4').replace('"5"','5')
s=base.replace('</body>','<script>'+js+'</script>'+auto+note+'</body>',1)
open('samples/dg.html','w',encoding='utf-8').write(s)
print('ok')
