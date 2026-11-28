# v210 の見本:新しい出来事と稽古タブの「出稽古先とのつきあい」を撮る
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]; od='samples/'
JS=r"""(k)=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;
 const ans=()=>{let g=0;while(G.ev.length&&g++<60){resolveEv(G.ev[0].id,0);}};
 for(let b=0;b<4;b++){let w=0;while(G.phase==='train'&&w++<20){ans();own().filter(r=>r.d<=2).forEach(r=>r.menu='出');doWeek();}
  let g=0;while(G.phase==='basho'&&g++<20)advanceDay();if(G.phase==='post'){ans();nextCycle();}}
 ans();const sk=own().filter(r=>r.d<=1);const r=sk[0];G.ev=[];const T=(spInit().tm||[]);
 if(k==='tanomi'){const t=T[0];G.ev.push({k:'tanomi',id:'s1',rid:r.id,what:'子ども相撲教室',ji:1,tn:t?t.n:null,who:t?'タニマチの'+t.n+'さん('+t.job+')':'後援会'});}
 if(k==='kesho2'){G.ev.push({k:'kesho2',id:'s2',rid:r.id,why:'S',opt:[{k:'tm',n:T[0]?T[0].n:'',t:'タニマチの'+(T[0]?T[0].n:'')+'さんから'},{k:'home',t:'出身地('+r.home+')の後援者一同から'},{k:'kai',t:'部屋の後援会一同から'}]});}
 if(k==='tmriv'){while(T.length<2)T.push({n:['石川','岡田'][T.length],job:'会社経営',cl:50});G.ev.push({k:'tmriv',id:'s3',a:T[0].n,b:T[1].n});}
 if(k==='golf'){G.ev.push({k:'golf',id:'s4'});}
 UI.view=k==='dek'?'keiko':'home';render();return Object.keys(G.dekR||{}).length;}"""
def shot_ev(pg,path):
  bb=pg.evaluate("()=>{const e=[...document.querySelectorAll('.ev')].map(x=>x.closest('.pn')||x).find(x=>x.getBoundingClientRect().width>0);const r=e.getBoundingClientRect();return [r.x,r.y+window.scrollY,r.width,r.height];}")
  pg.screenshot(path=path,full_page=True,clip={'x':bb[0],'y':bb[1],'width':bb[2],'height':min(bb[3],900)})
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(w,h) in {'':(1133,744),'_phone':(390,844)}.items():
    for k in ['kesho2','tanomi','tmriv','golf','dek']:
      pg=b.new_page(viewport={'width':w,'height':h})
      pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('sumoSkin','urushik');window.alert=()=>{};window.confirm=()=>false;}")
      pg.goto('file://'+f)
      n=pg.evaluate(JS,k)
      if k!='dek' and nm=='':
        for _ in range(8):
          if pg.evaluate("()=>[...document.querySelectorAll('button')].some(b=>/doEv/.test(b.getAttribute('onclick')||'')&&b.getBoundingClientRect().width>0)"):break
          ok=pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.includes('次へ')&&b.getBoundingClientRect().width>0);if(b){b.click();return 1;}return 0;}")
          if not ok:break
          pg.wait_for_timeout(300)
      if k=='dek':
        pg.evaluate("()=>{const e=[...document.querySelectorAll('.pn h2')].find(x=>x.textContent.includes('出稽古先とのつきあい'));if(e)e.scrollIntoView();}")
      pg.wait_for_timeout(400)
      (shot_ev(pg,od+'sp210_'+k+nm+'.png') if k!='dek' else pg.screenshot(path=od+'sp210_'+k+nm+'.png'));pg.close()
  b.close()
print('ok')
