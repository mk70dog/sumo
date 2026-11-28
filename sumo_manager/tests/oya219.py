# v216 親方の物語のテスト:実名モードで場所を回し、師匠の物語・師匠を超えた・部屋を譲る を確かめる
import sys,json
from playwright.sync_api import sync_playwright
f=sys.argv[1];heya=sys.argv[2] if len(sys.argv)>2 else '二所ノ関';N=int(sys.argv[3]) if len(sys.argv)>3 else 30
JS="""([hy,N])=>{newGameReal(hy);UI.title=false;UI.start=null;const out={};
 UI.view='staff';render();out.st0=document.body.innerHTML.includes('土俵の物語');
 for(let i=0;i<N;i++){let k=0;while(G.phase==='train'&&k++<20)doWeek();k=0;while(G.phase==='basho'&&k++<20)advanceDay();
  k=0;while(G.ev.length&&k++<60)resolveEv(G.ev[0].id,0);nextCycle();}
 const h=me();out.oyX=(h.oyX||[]).map(x=>bname(x.b)+' '+x.t);out.F=h.oyF;out.o=h.o;
 const co=G.staff.find(s=>s.role==='co');out.co=co?co.n:null;
 if(co){succeed(co,'in');out.after=me().oyX;out.P=me().oyP;out.q=(UI.oyQ||[]).length;}
 UI.view='staff';render();out.err=0;return out;}"""
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':1133,'height':744});pe=[];pg.on('pageerror',lambda e:pe.append(str(e)))
  pg.on('console',lambda m:pe.append(m.text) if m.type=='error' else None)
  pg.goto('file://'+f);pg.evaluate("()=>{localStorage.clear();window.alert=()=>{};window.confirm=()=>false;}");pg.goto('file://'+f)
  r=pg.evaluate(JS,[heya,N]);print(json.dumps(r,ensure_ascii=False,indent=1));print('errors',pe[:5]);b.close()
