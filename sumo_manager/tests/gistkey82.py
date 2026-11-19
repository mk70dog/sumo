# 鍵(Gist の設定)の読み込み・書き出しのテスト。gist_dummy.json は本物ではない鍵
import os,sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1180,820),'_phone':(390,844)}.items():
    pg=b.new_page(viewport={'width':w,'height':h},accept_downloads=True);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(300)
    pg.evaluate("topSettings()");pg.wait_for_timeout(200)
    pg.set_input_files('.pn input[type=file]',os.path.join(os.path.dirname(os.path.abspath(__file__)),'gist_dummy.json'));pg.wait_for_timeout(300)
    a=pg.evaluate("[localStorage.getItem('gsmTok'),document.querySelector('#mdl h2')&&document.querySelector('#mdl h2').textContent]")
    pg.evaluate("closeM()");pg.screenshot(path='/tmp/v82_top%s.png'%nm)
    pg.evaluate("goStart(null);topMode('one')");pg.click('.st-real');pg.click('.hcard >> nth=0');pg.wait_for_timeout(350);pg.click('#hsheet .btn.main');pg.evaluate("go('sys')")
    pg.evaluate("[...document.querySelectorAll('.pn h2')].find(x=>x.textContent.startsWith('GitHub の鍵')).scrollIntoView()");pg.wait_for_timeout(200);pg.screenshot(path='/tmp/v82_sys%s.png'%nm)
    with pg.expect_download() as d: pg.evaluate("gistExport()")
    path=d.value.path();ex=open(path).read()
    pg.evaluate("gistClear()");c=pg.evaluate("localStorage.getItem('gsmTok')")
    pg.evaluate("gistApply('ghp_PASTEDUMMY99')");d2=pg.evaluate("localStorage.getItem('gsmTok')")
    pg.evaluate("closeM();gistApply('nonsense')");bad=pg.evaluate("document.querySelector('#mdl h2').textContent")
    print(nm,a,'export',('gsm_gist_settings' in ex,'TESTDUMMY' in ex),'clear',c,'paste',d2,'bad',bad,errs[:2],pg.evaluate("[document.documentElement.scrollWidth,innerWidth]"))
  b.close()
