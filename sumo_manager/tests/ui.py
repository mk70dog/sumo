import sys, json
from playwright.sync_api import sync_playwright
f = sys.argv[1]; out = sys.argv[2]
sizes = {'ipad_l': (1180, 820), 'ipad_p': (820, 1180), 'phone': (390, 844)}
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (w, h) in sizes.items():
        pg = b.new_page(viewport={'width': w, 'height': h})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto('file://' + f)
        pg.evaluate("""()=>{localStorage.clear();newGameReal('高田川');
          for(let b=0;b<8;b++){while(G.phase==='train'){if(G.wk===2&&G.pros)G.pros.slice(0,3).forEach(p=>{if(ownAll().length<cap()-1)offerPros(p.cid,1);});doWeek();}
            while(G.phase==='basho')advanceDay(); if(b<7){while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();}}
          // 出来事を必ず並べる
          const o=own();const nb=o.find(r=>r.d>=3)||o[0];const sr=o.find(r=>r!==nb)||o[0];
          G.ev.push({k:'yame',rid:nb.id,id:'t1'},{k:'ijime',rid:nb.id,aid:sr.id,id:'t2'},{k:'soudan',rid:sr.id,tp:'nayami',id:'t3'},{k:'scand',rid:sr.id,tp:'bou',hid:2,id:'t4'});
          nb.tlog=[{b:G.bnum,t:'テスト',d:3}];save();UI.view='home';render();}""")
        r = {}
        for v in ['home', 'keiko', 'rikishi', 'keiei', 'kiroku']:
            pg.evaluate(f"()=>{{go('{v}')}}")
            if v == 'home':
                pg.evaluate("()=>{while(G.ev.length)resolveEv(G.ev[0].id,1);nextCycle();UI.view='keiko';render();}")
                pg.evaluate("()=>{go('keiko')}")
                pg.screenshot(path=f'/tmp/shot_{name}_keiko.png', full_page=True)
                pg.evaluate("()=>{go('home')}")
            sw = pg.evaluate("()=>[document.documentElement.scrollWidth,window.innerWidth]")
            r[v] = sw
        # 自分で選ぶ・兄弟子の変更・弟子の詳細
        pg.evaluate("()=>{go('keiko');setMeAuto(0);const o=ownAll();setMe(0,String(o[o.length-1].id));const nb=ownAll().find(r=>isNewbie(r));if(nb){const op=aniOpts(nb);if(op.length>1)setAni(nb.id,String(op[op.length-1][0]));}doWeekUI();}")
        pg.evaluate("()=>{showR(own()[0].id)}")
        r['modal'] = pg.evaluate("()=>[document.documentElement.scrollWidth,window.innerWidth]")
        pg.screenshot(path=f'/tmp/shot_{name}_modal.png')
        r['errors'] = errs[:5]
        res[name] = r
        pg.close()
    b.close()
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
