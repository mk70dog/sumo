# v214 の見本:引退のまど(名場面 3 つ)と殿堂の札。iPad 横・スマホ、漆黒・金
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
JS="""()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;
 const r=Object.values(G.R).find(x=>x.n==='熱海富士');
 storySx(r,'優勝次点 3 回。「あと一歩の男」と呼ばれ始める',55);G.bnum+=6;storySx(r,'9日目、横綱 大の里 を破って金星',60);G.bnum+=6;
 storySx(r,'悲願の幕内初優勝。優勝次点 4 回、決定戦 1 度の涙を越えて',120);G.bnum+=12;storySx(r,'大関に昇進',90);
 r.age=34;doRetire(r,'');UI.view='kiroku';render();return (UI.memQ||[]).length;}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');window.alert=()=>{};window.confirm=()=>false;}");pg.goto('file://'+f)
    print(pg.evaluate(JS));pg.wait_for_timeout(600)
    pg.screenshot(path='samples/mem214_modal'+nm+'.png')
    pg.evaluate("()=>{closeM();UI.memQ=[];UI.view='kiroku';render();const e=document.querySelector('.hyh');if(e)e.scrollIntoView({block:'center'});}");pg.wait_for_timeout(400)
    pg.screenshot(path='samples/mem214_hall'+nm+'.png');print(nm,pe[:2]);pg.close()
  b.close()
