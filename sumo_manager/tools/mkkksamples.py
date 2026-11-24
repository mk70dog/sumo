# 稽古の画面のスクロールを減らす見本 kk1〜kk3(ダルマさん「全体的に下にスクロールが多いので改良する」→ 画面の長さを測って長い順に →「実施」)
# 本体を開いて伊勢ヶ濱部屋(弟子 32 人)で始め、稽古の第 1 週の「稽古」画面を並べ替え・たたんで写真を撮る。
# usage: python3 tools/mkkksamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.kkx .kl{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:4px}
.kkx .kr{display:grid;grid-template-columns:62px 1fr auto;gap:6px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.kkx .kr .rk{font-size:11px;color:var(--mute)}.kkx .kr .n{font-weight:700}.kkx .kr .w{font-size:12px;color:var(--mute);grid-column:2/3}
.kkx .kr .st{font-size:11px;color:var(--mute);white-space:nowrap;text-align:right}
.kkx .kr::after{content:'▼';font-size:11px;color:var(--mute);grid-column:3;grid-row:1}
.kkx .kr.op{border-color:var(--kin)}.kkx .kr.op::after{content:'▲'}
.kkx .kopen{grid-column:1/-1}
.kkx .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 2px 0 6px;background:#888}.kkx .dot.g{background:var(--midori)}.kkx .dot.y{background:var(--kin)}.kkx .dot.r{background:var(--shu)}
.kkx .ktab{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0;position:sticky;top:0;z-index:5;background:var(--paper);padding:6px 0}
.kkx .ktab button{font:700 14px var(--kaku,sans-serif);padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:var(--washi2);color:var(--sumi)}
.kkx .ktab button.on{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin);color:var(--kin)}
.kkx.k3 .kcs{grid-template-columns:repeat(auto-fill,minmax(270px,1fr))!important;gap:6px!important}
.kkx.k3 .kc{padding:6px 8px!important}
.kkx.k3 .kc .stc,.kkx.k3 .kc .kgc,.kkx.k3 .kc .pkm,.kkx.k3 .kc .kfoot{display:none!important}
.kkx.k3 .kc .krow{margin:2px 0!important}.kkx.k3 .kc .kseg button{padding:2px 7px!important;font-size:12px!important}
.kkx .ktb{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:12px 0 4px}
.kkx .ktb button{font:700 15px var(--kaku,sans-serif);padding:9px 10px;border-radius:8px;border:1px solid var(--line);background:var(--washi2);color:var(--sumi);text-align:left;line-height:1.3}
.kkx .ktb button small{display:block;font-weight:400;font-size:11px;color:var(--mute)}
.kkx .ktb button.on{border:2px solid var(--kin);color:var(--kin);background:rgba(212,175,74,.08)}
.kkx .ktbh{font-size:12px;color:var(--mute);margin:0 0 6px}
.kkx .ktt{font-size:17px;margin:10px 0 6px;padding:6px 10px;border-left:4px solid var(--kin);background:var(--washi2)}
.acc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.acc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.acc>summary::-webkit-details-marker{display:none}
.acc>summary b{font-size:16px;color:var(--sumi)}.acc>summary small{color:var(--mute);font-size:12px}
.acc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.acc[open]>summary::after{content:'▲ たたむ'}
.acc>.pn{margin:0;border:none}
@media (max-width:760px){.kkx .ktb{grid-template-columns:1fr 1fr}}
.kkx .note{font-size:12px;color:var(--mute);margin:4px 0 8px}
@media (max-width:760px){.kkx .kl{grid-template-columns:1fr}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const h3=[...document.querySelectorAll('h3')].find(e=>e.innerText.trim()==='ひとりずつ決める');const kcs=h3.nextElementSibling;const pn=h3.closest('.pn');pn.classList.add('kkx');
 const dots=c=>{const t=c.querySelector('.kst');const g=[...t.querySelectorAll('.gg')].map(x=>parseInt(x.title.replace(/\D/g,'')));const a=g[0],f=g[1];return '<span class="dot '+(a>=70?'g':a<35?'r':'')+'"></span>調子 '+a+'<span class="dot '+(f>=70?'r':f>=45?'y':'g')+'"></span>疲労 '+f;};
 const wk=c=>{const w=c.querySelector('.kcw');const on=[...c.querySelectorAll('.krow')].map(r=>(r.querySelector('button.on')||{}).innerText).filter(Boolean);return (w?w.innerText.replace(/^師匠\s*/,'').replace(/^.{0,4}\s/,''):'')+(on.length?'・'+on.join('・'):'');};
 if(v===1){const cards=[...kcs.children];const L=document.createElement('div');L.className='kl';
  cards.forEach((c,i)=>{const id=(c.querySelector('[onclick^="showR"]')||{}).getAttribute?.('onclick');const r=document.createElement('div');r.className='kr'+(i===1?' op':'');
   r.innerHTML='<span class="rk">'+c.querySelector('.wsr').innerText+'</span><span class="n">'+c.querySelector('.wsnm').innerText+'</span><span class="st">'+dots(c)+'</span><span></span><span class="w">'+wk(c)+'</span>';L.appendChild(r);
   if(i===1){const o=document.createElement('div');o.className='kopen';o.appendChild(c);L.appendChild(o);}});
  kcs.replaceWith(L);h3.insertAdjacentHTML('afterend','<div class="note">押すと、その力士の稽古を細かく決められます(目標・型・初日の見込みもここ)。</div>');}
 if(v===2){const sub=document.createElement('div');sub.className='ktab';sub.innerHTML='<button class="on">まとめて決める</button><button>ひとりずつ(32 人)</button><button>親方・師弟</button><button>ちゃんこ・巡業・しくみ</button>';
  const b1=[...pn.querySelectorAll('button')].find(b=>b.innerText.includes('1 週間を過ごす'));const top=b1.closest('div');top.insertAdjacentElement('afterend',sub);
  h3.style.display='none';kcs.style.display='none';
  [...document.querySelectorAll('.pn')].filter(e=>e!==pn&&!e.closest('.kkx')&&!/稽古を決める人/.test((e.querySelector('h2')||{}).innerText||'')).forEach(e=>e.style.display='none');}
 const listify=()=>{const cards=[...kcs.children];const L=document.createElement('div');L.className='kl';
  cards.forEach((c,i)=>{const r=document.createElement('div');r.className='kr';r.innerHTML='<span class="rk">'+c.querySelector('.wsr').innerText+'</span><span class="n">'+c.querySelector('.wsnm').innerText+'</span><span class="st">'+dots(c)+'</span><span></span><span class="w">'+wk(c)+'</span>';L.appendChild(r);});kcs.replaceWith(L);return L;};
 if(v===4){const sub=document.createElement('div');sub.innerHTML='<div class="ktb"><button class="on">まとめて決める<small>おすすめ・稽古日・番付ごと</small></button><button>ひとりずつ<small>32 人を 1 人ずつ</small></button><button>親方と師弟<small>担当・目をかける弟子</small></button><button>ちゃんこ・巡業<small>体作り・しくみの説明</small></button></div><div class="ktbh">↑ 押すと、下に出る中身が切り替わります</div><div class="ktt">まとめて決める</div>';
  const b1=[...pn.querySelectorAll('button')].find(b=>b.innerText.includes('1 週間を過ごす'));b1.closest('div').insertAdjacentElement('afterend',sub);
  h3.style.display='none';kcs.style.display='none';
  [...document.querySelectorAll('.pn')].filter(e=>e!==pn&&!e.closest('.kkx')&&!/稽古を決める人/.test((e.querySelector('h2')||{}).innerText||'')).forEach(e=>e.style.display='none');}
 if(v===5){listify();const sum={'部屋付き親方の担当':'だれがどの段を見るか','師弟':'目をかける弟子・接し方・兄弟子','ちゃんこと体作り':'部屋の方針','巡業':'','稽古の種類':'しくみの説明','部屋の指導力':'','部屋の育つ環境':''};
  const wrap=(el,title,small,open)=>{const d=document.createElement('details');d.className='acc';if(open)d.open=true;d.innerHTML='<summary><b>'+title+'</b><small>'+small+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);};
  const L=pn.querySelector('.kl');const d=document.createElement('details');d.className='acc';d.innerHTML='<summary><b>ひとりずつ決める</b><small>32 人・押すと 1 人ずつの稽古を決められます</small></summary>';h3.replaceWith(d);d.appendChild(L);
  [...document.querySelectorAll('.pn')].filter(e=>e!==pn&&!e.closest('.kkx')&&!e.closest('.acc')&&!/稽古を決める人/.test((e.querySelector('h2')||{}).innerText||'')).forEach(e=>{const h=e.querySelector('h2');if(!h)return;const t=(h.childNodes[0]||{}).textContent||h.innerText;const sm=(h.querySelector('.sub')||{}).innerText||'';wrap(e,t.trim(),sm,false);h.style.display='none';});}
 if(v===3){pn.classList.add('k3');h3.insertAdjacentHTML('afterend','<div class="note">目標・型・初日の見込みは、四股名を押すと見られます。</div>');}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3, 4, 5):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='keiko';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'kk%d%s' % (v, nm)
            tgt = "ひとりずつ決める" if v not in (2, 4, 5) else "番付ごとにまとめて決める"
            pg.evaluate("(t)=>{const h=[...document.querySelectorAll('h3')].find(e=>e.innerText.trim()===t);scrollTo(0,h.getBoundingClientRect().top+scrollY-(innerWidth<760?150:110))}", tgt)
            if v in (2, 4): pg.evaluate("()=>{const e=document.querySelector('.ktab,.ktb');scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?260:330))}")
            if v == 5: pg.evaluate("()=>{const e=document.querySelector('.acc');scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?500:420))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
