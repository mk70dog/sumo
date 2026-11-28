# v213 の見本:力士の画面の「土俵の物語」(炎鵬=自分の部屋・高安=よその部屋)。iPad 横・スマホ、漆黒・金
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    for who in ['炎鵬','高安']:
      pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
      pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');}");pg.goto('file://'+f)
      pg.evaluate("""(who)=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;UI.view='rikishi';render();
        const r=Object.values(G.R).find(x=>x.n===who);if(who==='高安'){storySx(r,'館内に「高安コール」(ゲームの中の例)');}
        showR(r.id);}""",who)
      pg.wait_for_timeout(500)
      pg.evaluate("()=>{const e=document.querySelector('.sty');if(e)e.scrollIntoView({block:'start'});}")
      pg.wait_for_timeout(300)
      pg.screenshot(path='samples/sto213_'+('enho' if who=='炎鵬' else 'takayasu')+nm+'.png')
      print(who,nm,pe[:2]);pg.close()
  b.close()
