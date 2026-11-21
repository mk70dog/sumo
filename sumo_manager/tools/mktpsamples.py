# 見本 tp1〜tp3:部屋の画面の左右のグレーの欄を半透明に(漆黒の画面、v113)。#tp1〜#tp3
import json
base=open('sumo_manager_v113.html',encoding='utf-8').read()
SEL=lambda x:','.join('body.sk-%s %s .hbp%s'%(sk,sl,x) for sk in ('urushi','urushik','urushig') for sl in ('.hbleft','.hbright'))
def css(a,blur,ts):
    c=SEL('')+'{background:radial-gradient(rgba(255,255,255,.12) .7px,transparent 1.1px) 0 0/3px 3px,rgba(74,72,69,%s)!important;%s}'%(a,('-webkit-backdrop-filter:blur(%dpx);backdrop-filter:blur(%dpx);'%(blur,blur)) if blur else '')
    if ts:c+=SEL('')+'{text-shadow:0 1px 2px rgba(0,0,0,.8)}'
    return c
V={1:('少しだけすける(不透明度 80%)',css(.8,0,False)),2:('半分すける+後ろを少しぼかす(60%)',css(.6,4,True)),3:('よくすける+後ろを強くぼかす(45%)',css(.45,8,True))}
js="""<script>(function(){const C=%s,N=%s;const v=+((location.hash.match(/tp(\\d)/)||[])[1]||1);document.head.insertAdjacentHTML('beforeend','<style>'+C[v]+'</style>');
addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;go('home');render();}catch(e){console.error(e)}
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 tp'+v+':'+N[v]+'(#tp1〜#tp3 で切りかえ)';document.body.appendChild(d);},80));
addEventListener('hashchange',()=>location.reload());})();</script>"""%(json.dumps({k:v[1] for k,v in V.items()},ensure_ascii=False),json.dumps({k:v[0] for k,v in V.items()},ensure_ascii=False))
open('samples/tp.html','w',encoding='utf-8').write(base.replace('</body>',js+'</body>',1))
print('ok')
