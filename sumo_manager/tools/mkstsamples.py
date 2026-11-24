# スタッフの画面のスクロールを減らす見本 st1〜st3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# usage: python3 tools/mkstsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.sacc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.sacc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.sacc>summary::-webkit-details-marker{display:none}
.sacc>summary b{font-size:16px;color:var(--sumi)}.sacc>summary small{color:var(--mute);font-size:12px}
.sacc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.sacc[open]>summary::after{content:'▲ たたむ'}
.sacc>.pn{margin:0;border:none}.sacc>.pn>h2{display:none}
.sacc.in{margin:6px 0}
.sl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin:4px 0 8px}
.sr{display:grid;grid-template-columns:1fr auto;gap:2px 8px;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.sr .n{font-weight:700;color:var(--sumi)}.sr .n small{font-weight:400;font-size:11px;color:var(--mute);margin-left:6px}
.sr .s{font-size:12px;color:var(--mute);grid-column:1/3}.sr .x{font-size:11px;color:var(--mute)}
.sr.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.sopen{grid-column:1/-1}
@media (max-width:760px){.sl{grid-template-columns:1fr}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const P=t=>{const h=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith(t));return h?h.parentElement:null;};
 const head=pn=>{const h=pn.querySelector(':scope>h2');return [(h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim(),(h.querySelector('.sub')||{}).textContent||''];};
 const fold=(el,t,s,open,cls)=>{const d=document.createElement('details');d.className='sacc'+(cls?' '+cls:'');if(open)d.open=true;d.innerHTML='<summary><b>'+t+'</b><small>'+s+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const zu=P('部屋の人の図'),ok=P('おかみさん'),stf=P('部屋のスタッフ'),kon=P('こんな親方'),yat=P('雇える人');
 if(v===1||v===2){[zu,ok,kon,yat].forEach(pn=>{if(!pn)return;const [t,s]=head(pn);fold(pn,t,s,false);});}
 if(v===2){const kids=[...stf.children];let L=null;kids.forEach(c=>{if(c.tagName==='H3'){L=document.createElement('div');L.className='sl';c.insertAdjacentElement('afterend',L);return;}
   if(c.classList.contains('stf')&&L){const t=c.textContent.replace(/\s+/g,' ');const nm=(c.querySelector('b,.nm')||{}).textContent||t.slice(0,6);
     const sub=(t.match(/\d+歳[^押目]*/)||[''])[0].trim();const st=(t.match(/(押し指導.*?目利き \d+|目利き \d+ 人脈 \d+)/)||[''])[0];
     const r=document.createElement('div');r.className='sr';r.innerHTML='<div class="n">'+nm+'<small>'+sub+'</small></div><div class="x">▼</div><div class="s">'+st.replace(/(\d+)(?=[^\d\s])/g,'$1 ・ ')+'</div>';L.appendChild(r);c.remove();}});}
 if(v===3){const sw=zu.querySelector('.sw3'),ul=zu.querySelector(':scope>ul'),pp=zu.querySelector(':scope>p');
   const side=[...sw.children].filter((c,i)=>i!==1);
   const dd=ul?fold(ul,'後援する人・医師・図の見方','後援会・タニマチ・かかりつけ医・役目の説明',false,'in'):null;if(pp)pp.remove();
   [kon,yat].forEach(pn=>{if(!pn)return;const [t,s]=head(pn);fold(pn,t,s,false);});
   sw.style.gridTemplateColumns='1fr';if(dd)side.forEach(c=>dd.insertBefore(c,ul));
}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='staff';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'st%d%s' % (v, nm)
            pg.evaluate("scrollTo(0,0)" if v in (0, 3) else "()=>{const e=document.querySelector('.sacc');scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?260:300))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
