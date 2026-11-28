# v218 の見本:本場所の結果を伏せる(見る前・見たあと)。iPad 横・スマホ、漆黒・金
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
JS="""()=>{newGameReal('二所ノ関');UI.title=false;UI.start=null;let k=0;while(G.ev.length&&k++<60)resolveEv(G.ev[0].id,0);nextCycle();while(G.phase==='train')doWeek();UI.bouts=[];go('basho');stepDay();go('basho');return 1;}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');window.alert=()=>{};window.confirm=()=>false;}");pg.goto('file://'+f)
    pg.evaluate(JS);pg.wait_for_timeout(700)
    pg.evaluate("()=>{const e=[...document.querySelectorAll('.pn h2')].find(x=>/日目の結果/.test(x.textContent));if(e)e.scrollIntoView({block:'start'});}");pg.wait_for_timeout(300)
    pg.screenshot(path='samples/fz218_before'+nm+'.png')
    pg.evaluate("()=>{const e=[...document.querySelectorAll('.pn h2')].find(x=>/日目の取組/.test(x.textContent));if(e)e.scrollIntoView({block:'start'});}");pg.wait_for_timeout(300)
    pg.screenshot(path='samples/fz218_blur'+nm+'.png')
    pg.evaluate("()=>{const bt=[...document.querySelectorAll('.r1:not(:has(.dhin)) .dhbtn')][0];if(bt)bt.click();}");pg.wait_for_timeout(2500)
    pg.screenshot(path='samples/fz218_modal'+nm+'.png')
    pg.wait_for_timeout(3600);pg.screenshot(path='samples/fz218_modal_end'+nm+'.png')
    pg.evaluate("()=>{closeM();fzAll();const e=[...document.querySelectorAll('.pn h2')].find(x=>/日目の結果/.test(x.textContent));if(e)e.scrollIntoView({block:'start'});}");pg.wait_for_timeout(500)
    pg.screenshot(path='samples/fz218_after'+nm+'.png');print(nm,pe[:3]);pg.close()
  b.close()
