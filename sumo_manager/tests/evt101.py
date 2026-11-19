# 出来事(EVT)を種類ごとに確かめる:長く遊びながら、出てきた出来事を部屋の画面に並べ、おかしな文字がないか見て、選択肢を順に選んで答える。
# usage: python3 evt101.py 本体.html [場所数] [部屋,...]
from playwright.sync_api import sync_playwright
import sys, json
f = sys.argv[1]; nb = int(sys.argv[2]) if len(sys.argv) > 2 else 60
heyas = (sys.argv[3] if len(sys.argv) > 3 else '伊勢ヶ濱,高田川,佐渡ヶ嶽,木瀬').split(',')
JS = r"""([hn,nb])=>{const BAD=/NaN|undefined|\[object|Infinity|(?<![A-Za-z])null(?![A-Za-z])/;const seen={},bad=[],err=[];let rot=0;
 newGameReal(hn);UI.title=false;UI.start=null;
 const look=()=>{UI.view=G.phase==='train'?'keiko':'basho';try{render();}catch(e){err.push('render:'+e.message);}
  const t=document.querySelector('#app').innerText;
  G.ev.forEach(e=>{seen[e.k]=(seen[e.k]||0)+1;});
  t.split('\n').forEach(l=>{if(BAD.test(l))bad.push(G.ev.map(e=>e.k).join(',')+' | '+l.slice(0,120));});
  UI.view='home';try{render();}catch(e){err.push('render home:'+e.message);}
  document.querySelector('#app').innerText.split('\n').forEach(l=>{if(BAD.test(l))bad.push('home | '+l.slice(0,120));});};
 const answer=()=>{let g=0;while(G.ev.length&&g++<50){const e=G.ev[0];const E=EVT[e.k];let no=null;try{no=typeof E.c==='function'?E.c(e):E.c;}catch(x){err.push('c '+e.k+':'+x.message);}const n=Array.isArray(no)&&no.length?no.length:3;const i=(rot++)%n;
   try{const m=resolveEv(e.id,i);if(m&&BAD.test(m))bad.push('ans '+e.k+'#'+i+' | '+String(m).slice(0,120));}catch(x){err.push(e.k+'#'+i+':'+x.message);G.ev=G.ev.filter(y=>y!==e);}}};
 for(let b=0;b<nb&&!G.over;b++){
  let w=0;while(G.phase==='train'&&w++<20){if(G.wk===2&&G.pros)G.pros.slice(0,3).forEach(p=>{if(ownAll().length<cap()-1)offerPros(p.cid,1);});if(G.ev.length){look();answer();}try{doWeek();}catch(x){err.push('doWeek:'+x.message);break;}}
  let g=0;while(G.phase==='basho'&&g++<20){try{advanceDay();}catch(x){err.push('day:'+x.message);break;}}
  if(G.phase==='post'){look();answer();try{nextCycle();}catch(x){err.push('next:'+x.message);}}}
 let over='';if(G.over){UI.view='home';render();over=document.querySelector('#app').innerText.slice(0,200);}
 return {hn,bnum:G.bnum,seen,bad:[...new Set(bad)].slice(0,20),err:[...new Set(err)].slice(0,20),over};}"""
out = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for hn in heyas:
        pg = b.new_page(viewport={'width': 1180, 'height': 820}); pe = []
        pg.on('pageerror', lambda e: pe.append(str(e)[:200]))
        pg.goto('file://' + f); pg.evaluate("()=>{localStorage.clear();window.alert=()=>{};window.confirm=()=>false;}")
        r = pg.evaluate(JS, [hn, nb]); r['pageerr'] = pe[:5]; out.append(r); pg.close()
    b.close()
allk = {}
for r in out:
    for k, v in r['seen'].items(): allk[k] = allk.get(k, 0) + v
print(json.dumps(out, ensure_ascii=False, indent=1))
print('kinds', len(allk), json.dumps(allk, ensure_ascii=False))
