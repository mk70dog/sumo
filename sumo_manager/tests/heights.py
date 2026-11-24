# 各画面の縦の長さを測る(スクロールの多さの確認)。usage: python3 tests/heights.py 本体.html
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1])
VIEWS = ['home','rikishi','keiko','basho','banzuke','scout','staff','keiei','kiroku']
with sync_playwright() as p:
    b = p.chromium.launch()
    for nm, (W, H) in {'iPad横': (1180, 820), 'スマホ': (390, 844)}.items():
        pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto('file://' + f); pg.evaluate("localStorage.clear()")
        pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();}")
        for ph in ['稽古', '本場所']:
            if ph == '本場所':
                pg.evaluate("()=>{while(G.phase==='train'){doWeek();while(G.ev.length)resolveEv(G.ev[0].id,0);}for(let i=0;i<5;i++)advanceDay();const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();}")
            row = []
            for v in VIEWS:
                pg.evaluate("(v)=>{UI.view=v;render();scrollTo(0,0)}", v); pg.wait_for_timeout(120)
                hh = pg.evaluate("document.documentElement.scrollHeight")
                row.append('%s %.1f' % (v, hh / H))
            print(nm, ph, ' / '.join(row))
    b.close()
