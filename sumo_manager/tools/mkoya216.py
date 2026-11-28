# v216 の見本:親方の画面(土俵の物語・歴代の師匠)、部屋えらびの説明、部屋を譲るまど。iPad 横・スマホ、漆黒・金
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
JS="""()=>{newGameReal('二所ノ関');UI.title=false;UI.start=null;const h=oyEns(ME());
 const r=Object.values(G.R).find(x=>x.n==='大の里');G.bnum+=3;oyStorySx(h,'白熊が新十両。この師匠のもとで 1 人目の新十両(このゲームで)',55);
 G.bnum+=5;oyStorySx(h,'大の里が幕内優勝。この師匠のもとで初めての賜杯(このゲームで)',100);
 G.bnum+=4;oyStorySx(h,'白熊が師匠ゆずりの四つ相撲を完成させる',45);
 UI.view='staff';render();return 1;}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');window.alert=()=>{};window.confirm=()=>false;}");pg.goto('file://'+f)
    pg.evaluate(JS);pg.wait_for_timeout(500)
    pg.evaluate("()=>{const e=document.querySelector('.oys');if(e)e.scrollIntoView({block:'start'});window.scrollBy(0,-120);}");pg.wait_for_timeout(300)
    pg.screenshot(path='samples/oya216_staff'+nm+'.png')
    pg.evaluate("()=>{G.bnum+=30;const c={sid:999,role:'co',n:'元・白熊',mo:'前頭2枚目',age:44,sk:{osh:10,yot:14,waz:10,tai:10,sei:10,meki:10}};G.staff.push(c);succeed(c,'in');UI.view='staff';render();}");pg.wait_for_timeout(700)
    pg.screenshot(path='samples/oya216_jou'+nm+'.png')
    pg.evaluate("()=>{closeM();UI.oyQ=[];render();const e=[...document.querySelectorAll('.oys h3')].find(x=>x.textContent.includes('歴代'));if(e)e.scrollIntoView({block:'center'});}");pg.wait_for_timeout(300)
    pg.screenshot(path='samples/oya216_past'+nm+'.png')
    pg.goto('file://'+f);pg.wait_for_timeout(400)
    pg.close();pg=b.new_page(viewport={'width':w,'height':h});pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');}");pg.reload();pg.wait_for_timeout(500);pg.evaluate("goStart('real')");pg.wait_for_timeout(400);pg.evaluate("heyaSheet('伊勢ヶ濱')");pg.wait_for_timeout(500)
    pg.screenshot(path='samples/oya216_sel'+nm+'.png');print(nm,pe[:3]);pg.close()
  b.close()
