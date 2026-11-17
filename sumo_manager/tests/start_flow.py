from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1];out={}
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,(w,h) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload()
    a=pg.evaluate("!!document.querySelector('.st-cont')")
    pg.click('.st-real');pg.click('.hcard >> nth=0');pg.wait_for_timeout(350);pg.click('#hsheet .btn.main');pg.evaluate("doWeek()")
    wk=pg.evaluate("G.wk")
    pg.reload()
    r=pg.evaluate("[!!G,G&&G.wk,!!document.querySelector('.st-cont')]")
    pg.screenshot(path=f'/tmp/v20_{n}_top.png')
    bb=pg.evaluate("[...document.querySelectorAll('.st-go button')].map(b=>{const r=b.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]})")
    pg.click('.st-new');pg.screenshot(path=f'/tmp/v20_{n}_new.png',full_page=True);warn=pg.evaluate("!!document.querySelector('.st-warn')")
    pg.click('.st-back');pg.click('.st-cont');home=pg.evaluate("[!!document.querySelector('#hdr'),document.body.classList.contains('st-top'),document.documentElement.scrollWidth]")
    pg.reload();pg.click('.st-new');pg.click('button.btn.main');nw=pg.evaluate("[G.real,G.wk,!!document.querySelector('#hdr')]")
    pg.evaluate("resetGame()");rs=pg.evaluate("[G,!!document.querySelector('.st-cont'),!!document.querySelector('.st-go')]")
    out[n]=dict(noContFirst=not a,wk=wk,reload=r,btn=bb,warn=warn,cont=home,newOver=nw,reset=rs,errs=errs)
  for k,v in out.items():print(k,v)
