from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,(w,h) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});e=[]
    pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(200)
    pg.click('.st-tr .st-upd >> nth=0');pg.wait_for_timeout(350);pg.screenshot(path=f'/tmp/v25_{n}.png')
    imgs=pg.evaluate("document.querySelectorAll('.skpv img').length")
    pg.click('.skpv button >> nth=1');pg.wait_for_timeout(200)
    cls=pg.evaluate("document.body.className");on=pg.inner_text('.skpv button.on')
    pg.click('#ssheet h2 button');pg.wait_for_timeout(300);closed=not pg.evaluate("document.getElementById('ssheet').classList.contains('on')")
    pg.reload();keep=pg.evaluate("document.body.className")
    pg.click('.st-real');pg.click('.hcard >> nth=0');pg.wait_for_timeout(350);pg.click('#hsheet .btn.main');game=pg.evaluate("[!!G,document.body.className]")
    print(n,imgs,cls,on,closed,keep,game,pg.evaluate("document.documentElement.scrollWidth"),e)
