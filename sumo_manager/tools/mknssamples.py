# 新弟子の画面のスクロールを減らす見本 ns1〜ns3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# 本体を開いて伊勢ヶ濱部屋で始め、稽古の第 1 週の「新弟子」画面を組み替えて写真を撮る。
# usage: python3 tools/mknssamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.nl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin-top:6px}
.nr{display:grid;grid-template-columns:44px 1fr auto;gap:2px 8px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.nr .pf{grid-row:1/3;writing-mode:vertical-rl;font-weight:700;color:var(--sumi2);font-size:13px;text-align:center}
.nr .n{font-weight:700;color:var(--sumi)}.nr .n small{font-weight:400;font-size:11px;color:var(--mute);margin-left:6px}
.nr .s{font-size:12px;color:var(--mute);grid-column:2/4}.nr .s b{color:var(--kin)}
.nr .x{font-size:11px;color:var(--mute);text-align:right;white-space:nowrap}
.nr.hot{border-color:var(--kin)}
.nr.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.nopen{grid-column:1/-1}.nopen>.card{max-width:none!important;width:auto!important}
.ntl{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:6px;margin-top:6px}
.nt{border:1px solid var(--line);border-radius:6px;background:var(--washi2);padding:6px 8px;cursor:pointer}
.nt.hot{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.nt .k{font-size:11px;color:var(--mute)}.nt .n{font-weight:700;color:var(--sumi)}.nt .s{font-size:12px;color:var(--mute)}.nt .s b{color:var(--kin);font-size:15px}
.nacc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.nacc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.nacc>summary::-webkit-details-marker{display:none}
.nacc>summary b{font-size:16px;color:var(--sumi)}.nacc>summary small{color:var(--mute);font-size:12px}
.nacc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.nacc[open]>summary::after{content:'▲ たたむ'}
.nacc>.skc>h3{display:none}
.k3 .card .oyk,.k3 .card .sts,.k3 .card>.info>div:nth-child(3){display:none!important}
.k3 .cards.sc{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))!important}
@media (max-width:760px){.nl{grid-template-columns:1fr}.ntl{grid-template-columns:1fr 1fr}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const h2=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith('新弟子'));const pn=h2.parentElement;
 const hl=pn.querySelector(':scope>.hl'),skc=pn.querySelector(':scope>.skc'),cards=pn.querySelector('.cards.sc');
 const acc=(el,t,s,open)=>{const d=document.createElement('details');d.className='nacc';if(open)d.open=true;d.innerHTML='<summary><b>'+t+'</b><small>'+s+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const nOk=[...skc.querySelectorAll('.st.ok')].length;
 acc(hl,'新弟子集めのしくみ','スカウトの流れ・新弟子検査・入門の条件',false);
 acc(skc,'学校とのつきあい','紹介してくれる学校 '+nOk+' 校・挨拶や出稽古で関係を深める',false);
 const C=[...cards.children];const inf=c=>{const i=c.querySelector('.info');const t=x=>[...i.children].find(e=>e.textContent.startsWith(x));
  const ko=(c.querySelector('.sts')||{});const w=((ko.querySelector&&ko.querySelector('i'))||{style:{}}).style.width||'0';
  return {pf:c.querySelector('.fuda').textContent,rk:[...i.querySelector('.rk').childNodes].filter(x=>x.nodeType===3).map(x=>x.textContent).join('').trim(),n:i.querySelector('.nm').textContent,tag:[...i.querySelectorAll('.tag')].map(x=>x.textContent).join('・'),
   now:(t('今の力')||{textContent:''}).textContent.replace('今の力:',''),so:((t('素質')||{}).querySelector||(()=>null)).call(t('素質')||{},'b'),hot:parseFloat(w)>=60,kw:Math.round(parseFloat(w))};};
 if(v===1){const L=document.createElement('div');L.className='nl';C.forEach((c,i)=>{const d=inf(c);const r=document.createElement('div');r.className='nr'+(d.hot?' hot':'')+(i===3?' op':'');
   r.innerHTML='<div class="pf">'+d.pf+'</div><div class="n">'+d.n+'<small>'+d.rk+(d.tag?' ・'+d.tag:'')+'</small></div><div class="x">'+(i===3?'▲':'▼')+'</div><div class="s">素質 <b>'+(d.so?d.so.textContent:'?')+'</b> ・ 今の力 '+d.now+' ・ 他部屋の関心 '+d.kw+'</div>';L.appendChild(r);
   if(i===3){const o=document.createElement('div');o.className='nopen';o.appendChild(c);L.appendChild(o);}});cards.replaceWith(L);}
 if(v===2){const L=document.createElement('div');L.className='ntl';C.forEach(c=>{const d=inf(c);const t=document.createElement('div');t.className='nt'+(d.hot?' hot':'');
   t.innerHTML='<div class="k">'+d.pf+' ・ '+d.rk+'</div><div class="n">'+d.n+'</div><div class="s">素質 <b>'+(d.so?d.so.textContent:'?')+'</b> 今の力 '+d.now+'</div>';L.appendChild(t);});cards.replaceWith(L);
   L.insertAdjacentHTML('beforebegin','<p class="mute kaku" style="font-size:12px;margin:4px 0">押すと、会いに行く・勧誘のボタンが出ます。金の枠=ほかの部屋も狙っている。</p>');}
 if(v===3){pn.classList.add('k3');}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='scout';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'ns%d%s' % (v, nm)
            pg.evaluate("scrollTo(0,0)" if v == 0 else "()=>{const e=document.querySelector('.nacc');scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?220:140))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
