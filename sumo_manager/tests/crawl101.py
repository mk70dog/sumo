# 巡回テスト:場面ごとに全画面を 3 サイズで開き、ボタンを順に押して、おかしな文字・横あふれ・エラーを探す。
# usage: python3 crawl101.py 本体.html [場面 train,basho,post,dok,old] [サイズ ipad_l,ipad_p,phone]
from playwright.sync_api import sync_playwright
import sys, json, re
f = sys.argv[1]
scenes = (sys.argv[2] if len(sys.argv) > 2 else 'train,basho,post,dok,old').split(',')
SZ = {'ipad_l': (1180, 820), 'ipad_p': (820, 1180), 'phone': (390, 844)}
sizes = (sys.argv[3] if len(sys.argv) > 3 else 'ipad_l,ipad_p,phone').split(',')
VIEWS = ['home', 'rikishi', 'keiko', 'basho', 'banzuke', 'scout', 'staff', 'keiei', 'kiroku', 'sys']
BAD = re.compile(r'NaN|undefined|\[object|Infinity|(?<![A-Za-z])null(?![A-Za-z])')
SKIP = re.compile(r'quitTop|location|doUpd|askUpd|checkUpd|resetAll|reset|newGame|goStart|imp|load|file|mp[A-Z]|topMode|clearLog|copyLog|print|download|exp\(|Exp|delGame|del\(|confirm|saveFile|setSkin|setFont|logFile')
PLAY = """(n)=>{for(let b=0;b<n;b++){while(G.phase==='train'){if(G.wk===2&&G.pros)G.pros.slice(0,3).forEach(p=>{if(ownAll().length<cap()-1)offerPros(p.cid,1);});doWeek();}
 let g=0;while(G.phase!=='train'&&g++<60){if(G.phase==='basho')advanceDay();else if(G.phase==='post'){while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();}else break;}}}"""
SETUP = {
 'train': "()=>{localStorage.clear();newGameReal('伊勢ヶ濱');(%s)(12);}" % PLAY,
 'basho': "()=>{localStorage.clear();newGameReal('二所ノ関');(%s)(3);while(G.phase==='train')doWeek();for(let i=0;i<8;i++)advanceDay();}" % PLAY,
 'post': "()=>{localStorage.clear();newGameReal('高田川');(%s)(4);while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();}" % PLAY,
 'dok': "()=>{localStorage.clear();const x=dokOK()[0];newGameDok(x.n,dokWs(x).slice(0,3).map(w=>w.n),'四');(%s)(3);}" % PLAY,
 'old': "()=>{localStorage.clear();newGameReal('佐渡ヶ嶽');(%s)(90);}" % PLAY,
}
def badtext(pg):
    t = pg.evaluate("()=>{const a=[...document.querySelectorAll('#app, #mdl.on #mbox, #hsheet.on')].map(e=>e.innerText).join('\\n');return a;}")
    out = []
    for line in t.split('\n'):
        if BAD.search(line): out.append(line.strip()[:120])
    return out
def wide(pg):
    return pg.evaluate("""()=>{const W=innerWidth;const r=[];if(document.documentElement.scrollWidth>W+1)r.push('page '+document.documentElement.scrollWidth);
      document.querySelectorAll('#app *, #mdl.on #mbox *').forEach(e=>{const b=e.getBoundingClientRect();if(b.width&&b.right>W+2&&getComputedStyle(e).position!=='fixed'){let p=e,sc=false;while(p&&p!==document.body){const o=getComputedStyle(p).overflowX;if(o==='auto'||o==='scroll'||o==='hidden'){sc=true;break;}p=p.parentElement;}if(!sc)r.push((e.className||e.tagName)+':'+Math.round(b.right));}});return [...new Set(r)].slice(0,5);}""")
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for sc in scenes:
        for sz in sizes:
            W, H = SZ[sz]
            pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
            pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
            pg.goto('file://' + f); pg.wait_for_timeout(200)
            pg.evaluate("()=>{window.alert=()=>{};window.confirm=()=>false;window.prompt=()=>null;}")
            try:
                pg.evaluate(SETUP[sc])
            except Exception as e:
                res[sc + '/' + sz] = {'setup': str(e)[:300]}; pg.close(); continue
            pg.evaluate("()=>{UI.title=false;UI.start=null;UI.view='home';render();}")
            found = {'bad': {}, 'wide': {}, 'clickerr': [], 'errs': None, 'clicks': 0}
            for v in VIEWS:
                pg.evaluate("v=>{try{closeM&&closeM()}catch(e){};go(v)}", v); pg.wait_for_timeout(60)
                bt = badtext(pg); wd = wide(pg)
                if bt: found['bad'][v] = bt[:4]
                if wd: found['wide'][v] = wd
                n = pg.evaluate("()=>[...document.querySelectorAll('#app button[onclick], #app [onchange]')].length")
                for i in range(min(n, 70)):
                    oc = pg.evaluate("i=>{const e=[...document.querySelectorAll('#app button[onclick], #app [onchange]')][i];return e?(e.getAttribute('onclick')||e.getAttribute('onchange')||''):null}", i)
                    if oc is None: break
                    if SKIP.search(oc) or "go('" in oc: continue
                    e0 = len(errs)
                    try:
                        pg.evaluate("i=>{const e=[...document.querySelectorAll('#app button[onclick], #app [onchange]')][i];if(e.tagName==='SELECT'){if(e.options.length>1){e.selectedIndex=e.options.length-1;e.dispatchEvent(new Event('change'));}}else if(e.tagName==='INPUT'){e.click();}else e.click();}", i)
                    except Exception as ex:
                        found['clickerr'].append(v + ':' + oc[:60] + ':' + str(ex)[:80])
                    pg.wait_for_timeout(15); found['clicks'] += 1
                    bt = badtext(pg)
                    if bt: found['bad'].setdefault(v + '>' + oc[:40], bt[:3])
                    wd = wide(pg)
                    if wd: found['wide'].setdefault(v + '>' + oc[:40], wd)
                    if len(errs) > e0: found['clickerr'].append(v + '>' + oc[:60] + ' => ' + errs[-1][:120])
                    pg.evaluate("v=>{try{closeM&&closeM()}catch(e){};const ok=G&&!UI.title;if(!ok){UI.title=false;UI.start=null;}if(UI.view!==v)UI.view=v;render();}", v)
            # 力士・親方・部屋の小窓
            ids = pg.evaluate("()=>{const o=own().sort((a,b)=>a.pos-b.pos);const ai=G.order.map(i=>G.R[i]).filter(r=>r&&!r.ret&&r.h!==ME()).slice(0,3);return o.slice(0,3).concat(o.slice(-2)).concat(ai).map(r=>r.id);}")
            for rid in ids:
                for t in range(5):
                    pg.evaluate("([t,id])=>{UI.rtab=t;showR(id)}", [t, rid]); pg.wait_for_timeout(30)
                    bt = badtext(pg); wd = wide(pg)
                    if bt: found['bad'].setdefault('showR%d/%d' % (rid, t), bt[:3])
                    if wd: found['wide'].setdefault('showR%d/%d' % (rid, t), wd)
            nt = pg.evaluate("()=>G.toshi?G.toshi.length:0")
            for k in range(0, nt, 9):
                for t in range(3):
                    pg.evaluate("([t,k])=>{UI.ttab=t;showT(k)}", [t, k]); pg.wait_for_timeout(20)
                    bt = badtext(pg)
                    if bt: found['bad'].setdefault('showT%d/%d' % (k, t), bt[:3])
            nh = pg.evaluate("()=>G.heya.length")
            for k in range(nh):
                pg.evaluate("k=>showHeya(k)", k); pg.wait_for_timeout(10)
                bt = badtext(pg); wd = wide(pg)
                if bt: found['bad'].setdefault('showHeya%d' % k, bt[:3])
                if wd: found['wide'].setdefault('showHeya%d' % k, wd)
            found['errs'] = list(dict.fromkeys(errs))[:8]
            res[sc + '/' + sz] = found
            pg.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
