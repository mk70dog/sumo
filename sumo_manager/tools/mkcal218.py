# v218 の見本:予定の画面の文字が見えない(漆黒・金などの暗い色)の直し。A=着せ替えの色に合わせる / B=札はいつも生成り色で文字を濃く
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
A=""".cwk,.cyr td{background:var(--paper)!important;border-color:var(--line)!important;color:var(--sumi)}
.cwh{border-bottom-color:var(--line)!important}.cyr th{background:var(--washi2)!important;color:var(--sumi);border-color:var(--line)!important}
.cwk.past,.cyr td.past{background:var(--washi2)!important;opacity:.55}
.cwk.bs,.cyr td.bs{background:linear-gradient(rgba(224,88,60,.14),rgba(224,88,60,.14)),var(--paper)!important}
.cyr td.can:hover{background:var(--washi2)!important}"""
B=""".cwk,.cyr td,.cyr th{color:#2a2218!important}.cwk .mute,.cyr .mute{color:#6b5f4a!important}"""
JS="""(css)=>{newGameReal('二所ノ関');UI.title=false;UI.start=null;let k=0;while(G.ev.length&&k++<60)resolveEv(G.ev[0].id,0);nextCycle();doWeek();if(css){const s=document.createElement('style');s.textContent=css;document.head.appendChild(s);}UI.view='yotei';UI.calV='m';render();return 1;}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for sk in ['urushik','std']:
   for nm,css in [('A',A),('B',B),('now','')]:
    if sk=='std' and nm!='A':continue
    for dv,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
      pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
      pg.goto('file://'+f);pg.evaluate("(sk)=>{localStorage.clear();localStorage.setItem('sumoSkin',sk);}",sk);pg.goto('file://'+f)
      pg.evaluate(JS,css);pg.wait_for_timeout(400)
      pg.evaluate("()=>{const e=document.querySelector('.cmo');if(e)e.scrollIntoView({block:'center'});}");pg.wait_for_timeout(200)
      pg.screenshot(path='samples/cal218_'+sk+'_'+nm+'_m'+dv+'.png')
      pg.evaluate("()=>{UI.calV='y';render();const e=document.querySelector('.cyr');if(e)e.scrollIntoView({block:'center'});}");pg.wait_for_timeout(300)
      pg.screenshot(path='samples/cal218_'+sk+'_'+nm+'_y'+dv+'.png');print(sk,nm,dv,pe[:2]);pg.close()
  b.close()
