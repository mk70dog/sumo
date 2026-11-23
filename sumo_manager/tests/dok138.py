# v138 独立の説得:桐山親方で内弟子を全員選んで独立 → 残ると言った力士の出来事 dokPer → 説得の結果。usage: python3 dok138.py 本体.html
import sys, json
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1180,'height':820});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.wait_for_timeout(800)
    out=[]
    for t in range(6):
        r=pg.evaluate("""()=>{localStorage.clear();G=null;UI.title=true;UI.start='dok';render();const x=dokList().find(y=>y.n==='桐山')||dokOK()[0];dokSheet(x.n);
          document.querySelectorAll('.dkw input').forEach((e,i)=>{if(i<8)e.checked=true;});doStartDok(x.n);
          const ev=G.ev.filter(e=>e.k==='dokPer');const n0=own().length;const res=ev.map(e=>{const d=EVT.dokPer.d(e);return resolveEv(e.id,0);});
          return {h:x.n,own0:n0,own1:own().length,ev:ev.length,res:res,cool:G.dok.cool||0,dek:(dekInfo()||{}).q};}""")
        out.append(r)
    print(json.dumps({'runs':out,'errs':errs},ensure_ascii=False,indent=0)[:3000])
