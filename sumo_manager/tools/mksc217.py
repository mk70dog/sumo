# v217 の見本:新弟子の札(よその部屋の声かけ・断られた回数・見込み)、稽古の「関取の申し合い相手」、叩き上げの物語。iPad 横・スマホ、漆黒・金
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
JS="""()=>{newGameReal('二所ノ関');UI.title=false;UI.start=null;
 // 候補を 3 人:S に見える注目の候補(よその部屋が 4 部屋)、1 回断られた A、ふつうの B
 G.pros=[];for(let i=0;i<3;i++){const p=mkProspect(i===0?-1:RI(0,5),i===0);G.pros.push(p);}
 const [a,b,c]=G.pros;a.riv=4;viewPros(a,15);viewPros(a,15);a.ep=16.6;a.eo=7.5;a.err=1.4;a.int=55;a.src='高校の監督の紹介';
 b.riv=1;viewPros(b,12);b.ep=14.2;b.ng=1;b.cool=0;b.int=35;b.src='後援会からの情報';c.riv=0;viewPros(c,10);c.ep=11.8;c.int=10;c.src='同郷のつながり';
 UI.view='scout';render();return 1;}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');window.alert=()=>{};window.confirm=()=>false;}");pg.goto('file://'+f)
    pg.evaluate(JS);pg.wait_for_timeout(500)
    pg.evaluate("()=>{const e=document.querySelector('.cards.sc');if(e)e.scrollIntoView({block:'start'});}");pg.wait_for_timeout(300)
    pg.screenshot(path='samples/sc217_pros'+nm+'.png')
    pg.evaluate("()=>{UI.view='keiko';render();window.scrollTo(0,0);const e=document.querySelector('.mshp');if(e)e.scrollIntoView({block:'start'});window.scrollBy(0,-90);}");pg.wait_for_timeout(400)
    pg.screenshot(path='samples/sc217_keiko'+nm+'.png')
    pg.evaluate("""()=>{const r=own().filter(x=>x.d>=3)[0];r.pot0=9.5;r.ep0=9.8;G.bnum+=12;storySx(r,'入門のときは素質 C の見立て。叩き上げで関取に',75);G.bnum+=8;storySx(r,'叩き上げで幕内へ。素質 C から番付を上りつめる',85);
      UI.rid=r.id;UI.view='rikishi';UI.sel=r.id;showR(r.id);const s=document.querySelector('.sty');if(s)s.scrollIntoView({block:'start'});}""");pg.wait_for_timeout(500)
    pg.screenshot(path='samples/sc217_story'+nm+'.png');print(nm,pe[:3]);pg.close()
  b.close()
