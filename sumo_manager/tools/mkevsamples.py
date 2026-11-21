# 見本 ev1〜ev3:「育つ環境」を力士のまどと稽古の画面に出す(v112 + tools/ev_sample.js)。#ev1〜#ev3
base=open('sumo_manager_v112.html',encoding='utf-8').read()
js=open('tools/ev_sample.js',encoding='utf-8').read()
NOTE={1:'くわしく(4 つの棒グラフ+伸ばし方)',2:'点数とひとこと',3:'◎○△の印'}
auto="""<script>addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;doWeek();doWeek();go('keiko');render();
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 ev'+EVV+':'+(%s)[EVV]+'(#ev1〜#ev3 で切りかえ)';document.body.appendChild(d);}catch(e){console.error(e)}},100));addEventListener('hashchange',()=>location.reload());</script>"""%(__import__('json').dumps({str(k):v for k,v in NOTE.items()},ensure_ascii=False))
open('samples/ev.html','w',encoding='utf-8').write(base.replace('</body>','<script>'+js+'</script>'+auto+'</body>',1))
print('ok')
