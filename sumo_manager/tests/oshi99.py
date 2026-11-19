# まわり(追い風・向かい風)の割合を測る:関取(sek)とそれ以外、開始時と数年後。usage: python3 oshi99.py 本体.html [年数]
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1];yrs=int(sys.argv[2]) if len(sys.argv)>2 else 0
js="""(yrs)=>{const res={};
 const tally=()=>{const t={};own().forEach(r=>oshiItems(r).forEach(it=>{const g=r.d<=1?'sek':'low';const k=g+':'+it.lb;t[k]=t[k]||{p:0,z:0,n:0};t[k][it.c==='p'?'p':it.c==='n'?'n':'z']++;}));return t;};
 const add=(a,b)=>{for(const k in b){a[k]=a[k]||{p:0,z:0,n:0};for(const c in b[k])a[k][c]+=b[k][c];}};
 const tot={};
 for(const hn of ['佐渡ヶ嶽','伊勢ヶ濱','二所ノ関','高田川','木瀬','時津風','出羽海','春日野','追手風','玉ノ井']){newGameReal(hn);
  for(let b=0;b<yrs*6;b++){while(G.phase==='train')doWeek();let g=0;while(G.phase!=='train'&&g++<40){if(G.phase==='basho')stepAll();else if(G.phase==='post'){while(G.ev.length)resolveEv(G.ev[0].id,0);doNext();}else break;}}
  add(tot,tally());}
 return tot;}"""
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[]
  pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(300)
  r=pg.evaluate(js,yrs)
  for k in sorted(r):
    c=r[k];n=sum(c.values());print('%-14s n=%3d 追い風 %3.0f%% ふつう %3.0f%% 向かい風 %3.0f%%'%(k,n,100*c['p']/n,100*c['z']/n,100*c['n']/n))
  print(errs[:3])
