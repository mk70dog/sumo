# v78 のスタート画面(一人相撲・二人相撲)の流れ:3 サイズ
from playwright.sync_api import sync_playwright
import sys
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,(w,h) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(500)
    top=pg.evaluate("[!!document.querySelector('.st-one'),!!document.querySelector('.st-two'),!!document.querySelector('.st-real')]")
    pg.click('.st-two');two=pg.evaluate("[...document.querySelectorAll('.st-go button')].map(x=>x.disabled)")
    pg.screenshot(path=f'/tmp/v78_{n}_two.png')
    pg.click('.st-back2');pg.click('.st-one');pg.click('.st-real');pg.click('.hcard >> nth=0');pg.wait_for_timeout(350);pg.click('#hsheet .btn.main');pg.evaluate("doWeek()")
    ingame=pg.evaluate("[!!document.querySelector('#hdr'),G.wk]")
    pg.reload();pg.wait_for_timeout(500);pg.screenshot(path=f'/tmp/v78_{n}_top.png')
    pg.click('.st-one');cont=pg.evaluate("!!document.querySelector('.st-cont:not(.st-back2)')");pg.screenshot(path=f'/tmp/v78_{n}_one.png')
    pg.click('.st-cont:not(.st-back2)');back=pg.evaluate("[!!document.querySelector('#hdr'),G.wk,document.documentElement.scrollWidth<=innerWidth]")
    pg.evaluate("quitTop()");q=pg.evaluate("!!document.querySelector('.st-one')")
    bb=pg.evaluate("[...document.querySelectorAll('.st-go button')].map(b=>{const r=b.getBoundingClientRect();return r.bottom<=innerHeight})")
    print(n,dict(top=top,two=two,ingame=ingame,cont=cont,back=back,quitTop=q,inView=bb,errs=errs[:2]))
  b.close()
