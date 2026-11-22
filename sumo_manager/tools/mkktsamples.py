# 見本 kt1〜kt3:稽古タブをわかりやすく使いやすく(v116 + tools/kt_sample.js)。#kt1〜#kt3
import json
base=open('sumo_manager_v116.html',encoding='utf-8').read()
js=open('tools/kt_sample.js',encoding='utf-8').read()
N={1:'力士ごとの札とボタン',2:'おすすめと番付ごとにまとめて決める',3:'すっきりした表'}
auto="""<script>addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');{let z=9;Math.random=()=>{z=(z*1103515245+12345)>>>0;return (z>>>8)/16777216;};}newGameReal('木瀬');UI.title=0;UI.start=0;doWeek();doWeek();go('keiko');render();
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 kt'+KTV+':'+(%s)[KTV]+'(#kt1〜#kt3 で切りかえ)';document.body.appendChild(d);}catch(e){console.error(e)}},100));addEventListener('hashchange',()=>location.reload());</script>"""%json.dumps({str(k):v for k,v in N.items()},ensure_ascii=False)
open('samples/kt.html','w',encoding='utf-8').write(base.replace('</body>','<script>'+js+'</script>'+auto+'</body>',1))
print('ok')
