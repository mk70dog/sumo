# 見本 dt1〜dt5:部屋の画面の白い欄(今週やること・部屋の声・注目選手・部屋の様子)を細かいドットに。v108 に CSS を足す。#dt1〜#dt5
base=open('sumo_manager_v108.html',encoding='utf-8').read()
G='#4a4845';B='#c8ad86'
def dots(bg,dot,a,size=3):return "background:%s radial-gradient(%s .7px,transparent 1.1px) 0 0/%dpx %dpx!important"%(bg,dot,size,size) if a is None else "background:radial-gradient(%s .7px,transparent 1.1px) 0 0/%dpx %dpx,%s!important"%(dot,size,size,bg)
DARK="color:#ece6da!important;border-color:#1c1b1a!important}B .hbp a,B .hbp h3{color:#fff!important}B .hbp small,B .hbp .mute{color:#bdb6a8!important}B .hbp .kp button small{color:#bdb6a8!important}B .hbp .hbk,B .hbp .hbl b,B .hbp .hbk small{color:#d4af4a!important}B .hbp .ostab button.on{background:#9a2b1d;color:#fff;border-color:#9a2b1d}B .hbp .otag{color:#ddd5c6;border-color:#8a847a}B .hbp .ostab button{background:#3a3836;color:#ddd;border-color:#6a665e}B .hbp .chg{background:#3a3836;color:#eee;border-color:#6a665e}B .hbp .hbk{border-color:rgba(255,255,255,.25)!important}"
LIGHT="color:#2a1d12!important;border-color:#6a4a2a!important}B .hbp a,B .hbp h3{color:#1d140c!important}B .hbp small,B .hbp .mute{color:#5a4632!important}B .hbp .kp button small{color:#bdb6a8!important}B .hbp .otag{color:#3a2a1a;border-color:#7a5e3e}B .hbp .ostab button{background:#e3d2b5;color:#2a1d12;border-color:#8a6a48}B .hbp .ostab button.on{background:#9a2b1d;color:#fff}"
V={
1:('暗いグレー地に細かい白っぽいドット',"B .hbp{"+dots(G,'rgba(255,255,255,.13)',1)+";"+DARK),
2:('ライトブラウン地に細かい茶色のドット',"B .hbp{"+dots(B,'rgba(80,50,20,.22)',1)+";"+LIGHT),
3:('ライトブラウン地に暗いグレーのドット(ドット強め)',"B .hbp{"+dots(B,'rgba(50,50,50,.45)',1)+";"+LIGHT),
4:('暗いグレー地にライトブラウンのドット',"B .hbp{"+dots(G,'rgba(200,173,134,.35)',1)+";"+DARK),
5:('組み合わせ:上の帯は暗いグレー、左右の欄はライトブラウン',"B .hbp{"+dots(B,'rgba(80,50,20,.22)',1)+";"+LIGHT+"B .hbout .hbp{"+dots(G,'rgba(255,255,255,.13)',1)+";color:#ece6da!important}B .hbout .hbp h3{color:#fff!important}B .hbout .hbp small{color:#bdb6a8!important}B .hbout .hbp .hbk{color:#d4af4a!important}"),
}
import json
css={k:v[1].replace('B ','body.dtx ') for k,v in V.items()}
js="""<script>(function(){const C=%s,N=%s;const v=+((location.hash.match(/dt(\\d)/)||[])[1]||1);document.head.insertAdjacentHTML('beforeend','<style>'+C[v]+'</style>');
addEventListener('load',()=>{setTimeout(()=>{try{document.body.classList.add('dtx');localStorage.clear();localStorage.setItem('sumoSkin','urushik');applySkin('urushik');newGameReal('木瀬');UI.title=0;UI.start=0;const o=own().slice().sort((a,b)=>a.pos-b.pos);G.oshi=[o[0].id,o[1].id,o[2].id];go('home');render();}catch(e){console.error(e)}
const d=document.createElement('div');d.style.cssText='position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999';d.textContent='見本 dt'+v+':'+N[v]+'(#dt1〜#dt5 で切りかえ)';document.body.appendChild(d);},80);});
addEventListener('hashchange',()=>location.reload());})();</script>"""%(json.dumps(css,ensure_ascii=False),json.dumps({k:v[0] for k,v in V.items()},ensure_ascii=False))
open('samples/dt.html','w',encoding='utf-8').write(base.replace('</body>',js+'</body>',1))
print('ok')
