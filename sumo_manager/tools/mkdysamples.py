# 見本 dy1〜dy3:部屋の画面の左側に部屋日誌(v115 + tools/dy_sample.js)。#dy1〜#dy3
import json
base=open('sumo_manager_v115.html',encoding='utf-8').read()
js=open('tools/dy_sample.js',encoding='utf-8').read()
N={1:'部屋の声の下に、新しい 3 件',2:'部屋日誌を上に 5 件(いちばん新しいのは太字)+部屋の声を小さく',3:'部屋の声の下に、日付つき 8 件(中で動かせる)+「すべて」'}
auto="""<script>addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;{let z=7;Math.random=()=>{z=(z*1103515245+12345)>>>0;return (z>>>8)/16777216;};}for(let i=0;i<4;i++)doWeek();go('home');render();
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 dy'+DYV+':'+(%s)[DYV]+'(#dy1〜#dy3 で切りかえ)';document.body.appendChild(d);}catch(e){console.error(e)}},100));addEventListener('hashchange',()=>location.reload());</script>"""%json.dumps({str(k):v for k,v in N.items()},ensure_ascii=False)
open('samples/dy.html','w',encoding='utf-8').write(base.replace('</body>','<script>'+js+'</script>'+auto+'</body>',1))
print('ok')
