# 見本 ws1〜ws3:部屋の画面の「弟子の様子」を見やすく(v114 + tools/ws_sample.js)。#ws0=今のまま
import json
base=open('sumo_manager_v114.html',encoding='utf-8').read()
js=open('tools/ws_sample.js',encoding='utf-8').read()
N={0:'今のまま',1:'力士タブと同じ札',2:'小さな札(画面の幅に合わせて並ぶ)',3:'見やすい表(数字付き・しま模様)'}
auto="""<script>addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;doWeek();go('home');render();const h=[...document.querySelectorAll('h2')].find(x=>x.textContent.includes('弟子の様子'));if(h)h.scrollIntoView();
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 ws'+WSV+':'+(%s)[WSV]+'(#ws0〜#ws3 で切りかえ)';document.body.appendChild(d);}catch(e){console.error(e)}},100));addEventListener('hashchange',()=>location.reload());</script>"""%json.dumps({str(k):v for k,v in N.items()},ensure_ascii=False)
open('samples/ws.html','w',encoding='utf-8').write(base.replace('</body>','<script>'+js+'</script>'+auto+'</body>',1))
print('ok')
