# 見本 bk1〜bk3:部屋の画面の左右の欄を半透明、右側の欄の字を黒に(漆黒の画面、v113)。#bk1〜#bk3
import json
base=open('sumo_manager_v113.html',encoding='utf-8').read()
def S(slot,x=''):return ','.join('body.sk-%s %s .hbp%s'%(sk,slot,x) for sk in ('urushi','urushik','urushig'))
L=S('.hbleft')+'{background:radial-gradient(rgba(255,255,255,.12) .7px,transparent 1.1px) 0 0/3px 3px,rgba(74,72,69,.6)!important;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);text-shadow:0 1px 2px rgba(0,0,0,.8)}'
def R(bg,blur,glow):
    c=S('.hbright')+'{background:radial-gradient(rgba(0,0,0,.10) .7px,transparent 1.1px) 0 0/3px 3px,%s!important;-webkit-backdrop-filter:blur(%dpx);backdrop-filter:blur(%dpx);color:#111!important;text-shadow:%s}'%(bg,blur,blur,glow)
    for x,v in ((' a','#000'),(' h3','#000'),(' small','#333'),(' .mute','#333'),(' b','#000')):c+=S('.hbright',x)+'{color:%s!important}'%v
    c+=S('.hbright',' .hbk')+','+S('.hbright',' .hbk small')+','+S('.hbright',' .hbl b')+'{color:#7a1f12!important}'
    c+=S('.hbright',' .otag')+'{color:#111!important;border-color:rgba(0,0,0,.45)!important;background:rgba(255,255,255,.25)}'
    c+=S('.hbright',' .chg')+','+S('.hbright',' .ostab button')+'{background:rgba(255,255,255,.55)!important;color:#111!important;border-color:rgba(0,0,0,.35)!important}'
    c+=S('.hbright',' .ostab button.on')+'{background:#9a2b1d!important;color:#fff!important}'
    return c
V={1:('右の欄は明るい半透明(60%)+黒い字。左は半透明のグレー',L+R('rgba(245,238,224,.6)',5,'none')),
   2:('右の欄はうすい半透明(35%)+強いぼかし+黒い字(字のまわりを白くふちどり)',L+R('rgba(245,238,224,.35)',10,'0 0 3px rgba(255,255,255,.9),0 0 1px #fff')),
   3:('右の欄はグレーの半透明(45%)のまま、字だけ黒(白くふちどり)',L+R('rgba(150,148,144,.45)',8,'0 0 3px rgba(255,255,255,.95),0 0 1px #fff'))}
js="""<script>(function(){const C=%s,N=%s;const v=+((location.hash.match(/bk(\\d)/)||[])[1]||1);document.head.insertAdjacentHTML('beforeend','<style>'+C[v]+'</style>');
addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;go('home');render();}catch(e){console.error(e)}
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 bk'+v+':'+N[v]+'(#bk1〜#bk3 で切りかえ)';document.body.appendChild(d);},80));
addEventListener('hashchange',()=>location.reload());})();</script>"""%(json.dumps({k:v[1] for k,v in V.items()},ensure_ascii=False),json.dumps({k:v[0] for k,v in V.items()},ensure_ascii=False))
open('samples/bk.html','w',encoding='utf-8').write(base.replace('</body>',js+'</body>',1))
print('ok')
