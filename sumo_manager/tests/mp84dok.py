# 二人相撲:親を「部屋付き親方として独立」で始め、子が参加して 1 週進める(#mpmock)
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':1180,'height':820});errs=[]
  h=ctx.new_page();h.on('pageerror',lambda e:errs.append('H:'+str(e)))
  h.goto('file://'+f+'#mpmock');h.evaluate("localStorage.clear()");h.reload();h.wait_for_timeout(400)
  h.click('.st-two');h.screenshot(path='/tmp/v84_two.png');h.click('.st-dok2');h.wait_for_timeout(300)
  n=h.evaluate("dokList()[0].n");h.evaluate("n=>dokSheet(n)",n);h.wait_for_timeout(300)
  h.check('.dkw input >> nth=0');h.wait_for_timeout(200);h.click('#dkgo')
  # v142:独立の場面(① 師匠 ② 声かけ ③ 理事会 ④ 門出)を最後まで進める
  h.evaluate("()=>{for(let k=0;k<40&&document.getElementById('dpx')&&UI.dp;k++){const bs=[...document.querySelectorAll('#dpx button')];(bs.find(x=>x.classList.contains('ai'))||bs[0]).click();}}")
  h.wait_for_function("()=>G&&G.mp&&G.mp.id",timeout=15000);code=h.evaluate("G.mp.id");hn=h.evaluate("G.heya[0].n")
  g=ctx.new_page();g.on('pageerror',lambda e:errs.append('G:'+str(e)))
  g.goto('file://'+f+'#mpmock');g.wait_for_timeout(400);g.click('.st-two');g.click('.st-go2 .st-dok:not(.st-dok2)');g.fill('#mp_code',code);g.click('.mpkey .btn.main')
  g.wait_for_selector('.mpsel .btn');names=g.evaluate("[...document.querySelectorAll('.mpsel .btn')].map(b=>b.textContent.split('部屋')[0])");g.click('.mpsel .btn >> nth=0')
  h.wait_for_function("()=>G.mp.gh>0",timeout=15000);g.wait_for_function("()=>mpIsP()",timeout=20000);g.evaluate("doWeekUI()")
  h.evaluate("doWeekUI()");h.wait_for_function("()=>G.mp.n===2",timeout=20000)
  print(json.dumps(dict(dok=n,host=hn,hostInGuestList=hn in names,wk=h.evaluate("G.wk"),errs=errs[:3]),ensure_ascii=False))
  b.close()
