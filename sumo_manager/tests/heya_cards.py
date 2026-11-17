from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,(w,h) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.click('.st-real')
    cnt=pg.evaluate("document.querySelectorAll('.hcard').length");pg.screenshot(path=f'/tmp/v23_{n}.png')
    pg.click('.hchip >> text=二所ノ関');c2=pg.evaluate("document.querySelectorAll('.hcard').length")
    pg.click('.hchip >> text=歴史の古い順');first=pg.inner_text('.hcard b >> nth=0')
    sw=pg.evaluate("document.documentElement.scrollWidth")
    pg.click('.hcard >> nth=0');pg.wait_for_timeout(350);pg.screenshot(path=f'/tmp/v23_{n}_s.png')
    pg.select_option('#r_t','技');pg.click('#hsheet .btn.main')
    r=pg.evaluate("[me().n, me().oyT||me().t||'', G.money]")
    print(n,cnt,c2,first,sw,r,errs)
