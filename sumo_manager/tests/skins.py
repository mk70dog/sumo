from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,(w,h) in {'ipad_l':(1180,820),'phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload()
    pg.click('.st-real');pg.evaluate("heyaSheet('伊勢ヶ濱')");pg.wait_for_timeout(350);pg.click('#hsheet .btn.main')
    sw={}
    for k in ['std','yoru','ai','sakura','nishiki','banzuke']:
      pg.evaluate(f"setSkin('{k}');go('home')");pg.screenshot(path=f'/tmp/sk_{n}_{k}.png')
      for v in ['banzuke','keiei','kiroku']:
        pg.evaluate(f"go('{v}')");sw[k+v]=pg.evaluate("document.documentElement.scrollWidth")
      if n=='ipad_l':
        pg.evaluate("go('banzuke')");pg.screenshot(path=f'/tmp/sk_{n}_{k}_bz.png')
    pg.evaluate("go('home')");pg.click('.hbtn >> nth=0');t=pg.inner_text('#toast')
    pg.click('.hbtn >> nth=1');top=pg.evaluate("[!!document.querySelector('.st-cont'),document.body.className]")
    pg.reload();keep=pg.evaluate("document.body.className")
    pg.click('.st-cont');ok=pg.evaluate("!!document.querySelector('#hdr')")
    print(n,'maxsw',max(sw.values()),'toast',t,'top',top,'reload',keep,'cont',ok,errs)
