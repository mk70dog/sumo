# 経営の画面のスクロールを減らす見本 ke1〜ke3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# usage: python3 tools/mkkesamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.eacc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.eacc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.eacc>summary::-webkit-details-marker{display:none}
.eacc>summary b{font-size:16px;color:var(--sumi)}.eacc>summary small{color:var(--mute);font-size:12px}
.eacc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.eacc[open]>summary::after{content:'▲ たたむ'}
.eacc>.pn{margin:0;border:none}.eacc>.pn>h2{display:none}
.ehid{display:none!important}
.emore{display:block;margin:6px 0;font-size:13px;padding:5px 12px}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const P=t=>{const h=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith(t));return h?h.parentElement:null;};
 const head=pn=>{const h=pn.querySelector(':scope>h2');return [(h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim(),(h.querySelector('.sub')||{}).textContent||''];};
 const fold=(el,t,s)=>{const d=document.createElement('details');d.className='eacc';d.innerHTML='<summary><b>'+t+'</b><small>'+s+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const ara=P('部屋のあらまし'),ich=P('一門'),myo=P('年寄名跡'),sh=P('前の場所の収支'),hy=P('評判と後援会');
 const sum={'部屋のあらまし':'親方・裏方・所在地・沿革','一門':'伊勢ヶ濱一門・移る/抜ける','年寄名跡':'所有 '+myo.querySelectorAll('table')[0].rows.length+'・売りに出ている名跡'};
 if(v===1||v===2||v===3){[ara,ich,myo].forEach(pn=>{const [t,s]=head(pn);fold(pn,t,sum[t]||s);});}
 const totals=()=>{const t=sh.querySelector('table');const rows=[...t.rows];const keep=rows.filter(r=>/収入の合計|支出の合計|差し引き/.test(r.textContent));
   rows.forEach(r=>{if(!keep.includes(r))r.classList.add('ehid');});
   t.insertAdjacentHTML('afterend','<button class="btn sm emore">内訳を見る(収入 10 件・支出 8 件)▼</button>');
   const p=sh.querySelector(':scope>p');if(p)p.classList.add('ehid');};
 if(v===2||v===3)totals();
 if(v===3){const p=hy.querySelector(':scope>p');if(p){const d=fold(p,'評判と後援会のしくみ','どうすると増えるか');d.style.margin='6px 0';}
   const fac=P('部屋の施設');const fp=fac.querySelector(':scope>p');if(fp)fp.classList.add('ehid');}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='keiei';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'ke%d%s' % (v, nm)
            pg.evaluate("scrollTo(0,0)" if v in (0,) else "()=>{const h=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith('前の場所の収支'));scrollTo(0,h.getBoundingClientRect().top+scrollY-(innerWidth<760?160:130))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
