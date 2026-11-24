# 記録の画面のスクロールを減らす見本 kr1〜kr3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# 本体を開いて伊勢ヶ濱部屋で始め、稽古の第 1 週の「記録」画面を組み替えて写真を撮る。
# usage: python3 tools/mkkrsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.racc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.racc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.racc>summary::-webkit-details-marker{display:none}
.racc>summary b{font-size:16px;color:var(--sumi)}.racc>summary small{color:var(--mute);font-size:12px}
.racc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.racc[open]>summary::after{content:'▲ たたむ'}
.racc>.pn{margin:0;border:none}.racc>.pn>h2{display:none}
.rmore{display:block;margin:6px 0;font-size:13px;padding:5px 12px}
.rgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 10px}
@media (max-width:760px){.rgrid{grid-template-columns:1fr}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const fold=(el,title,small,open)=>{const d=document.createElement('details');d.className='racc';if(open)d.open=true;d.innerHTML='<summary><b>'+title+'</b><small>'+small+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const secs=[...document.querySelectorAll('.pn>h2')].map(h=>({h,pn:h.parentElement,t:(h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.innerText).trim(),s:(h.querySelector('.sub')||{}).innerText||''}));
 const shorten=(n)=>{document.querySelectorAll('.pn table').forEach(t=>{const rows=[...t.rows].filter(r=>!r.querySelector('th'));if(rows.length<=n+2)return;rows.slice(n).forEach(r=>r.style.display='none');
   const b=document.createElement('button');b.className='btn sm rmore';b.textContent='残り '+(rows.length-n)+' 件を見る ▼';t.insertAdjacentElement('afterend',b);});
  const nik=secs.find(x=>x.t.startsWith('部屋日誌'));if(nik){const L=[...nik.pn.children].filter(e=>e!==nik.h);if(L.length===1&&L[0].children.length>6){[...L[0].children].slice(5).forEach(e=>e.style.display='none');L[0].insertAdjacentHTML('afterend','<button class="btn sm rmore">残り '+(L[0].children.length-5)+' 件を見る ▼</button>');}}};
 const rare=/^(相撲部屋の一覧|給金番付|角界の部屋|取材の記事|不祥事の記録|部屋日誌|育成の成績|メディア|新聞の予想)/;
 if(v===1){secs.forEach(x=>{if(x.t==='達成')return;fold(x.pn,x.t,x.s,x.t==='部屋の歩み');});}
 if(v===2){shorten(5);}
 if(v===3){shorten(5);secs.forEach(x=>{if(rare.test(x.t))fold(x.pn,x.t,x.s,false);});}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='kiroku';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'kr%d%s' % (v, nm)
            if v in (2, 3): pg.evaluate("()=>{const h=[...document.querySelectorAll('.pn h2')].find(e=>e.innerText.startsWith('達成'));scrollTo(0,h.getBoundingClientRect().top+scrollY-(innerWidth<760?180:130))}")
            elif v == 1: pg.evaluate("()=>{const e=document.querySelectorAll('.racc')[1];scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?260:360))}")
            else: pg.evaluate("scrollTo(0,0)")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
