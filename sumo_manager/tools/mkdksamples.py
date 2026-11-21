# 見本 dk1〜dk3:部屋の画面の左右の欄を「暗いグレーの半透明」のまま読みやすく(漆黒の画面、v113)。#dk1〜#dk3
import json
base=open('sumo_manager_v113.html',encoding='utf-8').read()
def S(x=''):return ','.join('body.sk-%s %s .hbp%s'%(sk,sl,x) for sk in ('urushi','urushik','urushig') for sl in ('.hbleft','.hbright'))
def C(bg,blur,ts,tag):
    c=S()+'{background:radial-gradient(rgba(255,255,255,.10) .7px,transparent 1.1px) 0 0/3px 3px,%s!important;-webkit-backdrop-filter:blur(%dpx) saturate(.8);backdrop-filter:blur(%dpx) saturate(.8);text-shadow:%s}'%(bg,blur,blur,ts)
    c+=S(' .otag')+'{background:%s;border-color:rgba(255,255,255,.35)!important;color:#f3ede2!important}'%tag
    return c
V={1:('濃いめのグレー(70%)+ぼかし。字に影',C('rgba(48,46,43,.7)',6,'0 1px 2px #000','rgba(0,0,0,.25)')),
   2:('グレー(55%)+強いぼかし。字に影、札にも黒い下地',C('rgba(48,46,43,.55)',14,'0 1px 2px #000,0 0 6px rgba(0,0,0,.6)','rgba(0,0,0,.4)')),
   3:('上が濃く下がうすいグレー(80%→50%)+ぼかし',C('linear-gradient(rgba(40,38,35,.8),rgba(40,38,35,.5))',8,'0 1px 2px #000,0 0 4px rgba(0,0,0,.5)','rgba(0,0,0,.3)'))}
js="""<script>(function(){const C=%s,N=%s;const v=+((location.hash.match(/dk(\\d)/)||[])[1]||1);document.head.insertAdjacentHTML('beforeend','<style>'+C[v]+'</style>');
addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;go('home');render();}catch(e){console.error(e)}
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 dk'+v+':'+N[v]+'(#dk1〜#dk3 で切りかえ)';document.body.appendChild(d);},80));
addEventListener('hashchange',()=>location.reload());})();</script>"""%(json.dumps({k:v[1] for k,v in V.items()},ensure_ascii=False),json.dumps({k:v[0] for k,v in V.items()},ensure_ascii=False))
open('samples/dk.html','w',encoding='utf-8').write(base.replace('</body>',js+'</body>',1))
print('ok')
