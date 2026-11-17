# v26 経歴タブ:力士(大の里・朝玉勢・番付だけの人)と親方(甲山)の画面、家族のリンク、3 サイズ
import sys
from playwright.sync_api import sync_playwright
f = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    for name,(w,h) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
        pg = b.new_page(viewport={'width':w,'height':h}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://'+f)
        r = pg.evaluate("""()=>{localStorage.clear();newGameReal('二所ノ関');UI.title=false;render();
          const id=n=>G.order.find(i=>G.R[i].n===n);const out={};
          UI.rtab=1;showR(id('大の里'));out.onosato=document.querySelector('#mbox .kc').innerText.slice(0,60);
          out.wide=document.querySelector('#mdl').scrollWidth>document.querySelector('#mdl').clientWidth+2;
          showR(id('朝玉勢'));out.asa=document.querySelector('#mbox .kc').innerText.includes('近畿大学');
          const plain=G.order.find(i=>{const r=G.R[i];return !KEI[r.kk||r.n];});showR(plain);out.plain=document.querySelector('#mbox .src').innerText;
          UI.rtab=0;showR(id('大の里'));out.tab0=!!document.querySelector('#mbox .atw');
          UI.rtab=2;showR(id('大の里'));out.tab2=document.querySelector('#mbox .rtbx').innerText.slice(0,20);
          const k=G.toshi.findIndex(t=>t.n==='甲山');UI.ttab=1;showT(k);out.kab=document.querySelector('#mbox .kc').innerText.includes('同志社');
          const a=[...document.querySelectorAll('#mbox .kc a.lk')].map(x=>x.innerText);out.links=a;
          document.querySelector('#mbox .kc a.lk').click();out.after=document.querySelector('#mbox .fuda').innerText.replace(/\\n/g,'');
          const hi=G.heya.findIndex(h=>h.n==='伊勢ノ海');showHeya(hi);out.heyaLinks=document.querySelectorAll('#mbox a.tlk').length;
          return out;}""")
        pg.screenshot(path='/tmp/kei26_%s.png'%name)
        print(name, errs, r)
    b.close()
