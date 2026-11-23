# ホーム(場所後)のスクロールを減らす見本 sc1〜sc3(ダルマさん「表示が下すぎる」「全体的に下にスクロールが多いので改良する」)
# 本体を開いて伊勢ヶ濱部屋で始め(場所後・悩みごとあり)、画面の部品を並べ替え・たたんで、最初の 1 画面の写真を撮る。
# usage: python3 tools/mkscsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.scx details{margin:6px 0 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.scx details>summary{cursor:pointer;padding:9px 12px;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.scx details>summary::after{content:'▼ ひらく';font-weight:400;font-size:12px;color:var(--mute)}
.scx details[open]>summary::after{content:'▲ たたむ'}
.scx .sm3{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}
.scx .sm3 div{flex:1;min-width:90px;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:6px 10px;text-align:center;font-size:12px;color:var(--mute)}
.scx .sm3 b{display:block;font-size:20px;color:var(--sumi)}
.scx .sm3 .g b{color:var(--midori)}.scx .sm3 .r b{color:var(--shu)}
.scx .todo{border:2px solid var(--kin)!important}
.scx .badge{display:inline-block;background:var(--shu);color:#fff;border-radius:10px;padding:0 8px;font-size:12px;margin-left:6px}
.scx .two{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}
.scx .two>.l{position:sticky;top:8px}
.scx .stab{display:flex;gap:6px;margin:8px 0;flex-wrap:wrap}
.scx .stab button{font:700 14px var(--kaku,sans-serif);padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--sumi)}
.scx .stab button.on{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin);color:var(--kin)}
.scx .hbmini .hbs{max-height:220px;overflow:hidden}
@media (max-width:760px){.scx .two{grid-template-columns:1fr}.scx .two>.l{position:static}}
"""
JS = r"""(v)=>{
 const pns=[...document.querySelectorAll('.pn')];const find=t=>pns.find(e=>(e.querySelector('h2,h3')||{}).innerText?.includes(t));
 const post=find('場所を終えて'),ev=find('親方の悩みごと'),nx=find('次の場所へ'),hb=document.querySelector('.hbs');
 const cb=document.getElementById('cvbub');if(cb)cb.remove();const root=post.parentNode;root.classList.add('scx');
 // 成績表:関取だけ見せて、全員はたたむ
 const tbs=post.querySelectorAll('table.tb');const res=tbs[0],mon=tbs[1];
 const rows=[...res.querySelectorAll('tr')].slice(1);const kk=rows.filter(r=>r.innerText.includes('勝ち越し')).length,mk=rows.length-kk;
 const sek=rows.filter(r=>/横綱|大関|関脇|小結|前頭|十両/.test(r.cells[0].innerText));
 const mini=res.cloneNode(false);mini.appendChild(res.rows[0].cloneNode(true));sek.forEach(r=>mini.appendChild(r.cloneNode(true)));
 const sm=document.createElement('div');sm.className='sm3';sm.innerHTML='<div class="g"><b>'+kk+'</b>勝ち越し</div><div class="r"><b>'+mk+'</b>負け越し</div><div><b>'+sek.length+'</b>関取</div>';
 const d1=document.createElement('details');d1.innerHTML='<summary>全員の成績('+rows.length+' 人)</summary>';res.parentNode.insertBefore(d1,res);d1.appendChild(res);
 d1.parentNode.insertBefore(sm,d1);d1.parentNode.insertBefore(mini,d1);
 const tx=t=>{const r=[...mon.rows].find(r=>r.innerText.includes(t));return r?r.cells[r.cells.length-1].innerText:'';};
 const d2=document.createElement('details');d2.innerHTML='<summary>収入 '+tx('収入の合計')+' ・ 支出 '+tx('支出の合計')+' ・ 差し引き '+tx('差し引き')+'</summary>';mon.parentNode.insertBefore(d2,mon);d2.appendChild(mon);
 ev.classList.add('todo');const h=ev.querySelector('h2,h3');if(h)h.insertAdjacentHTML('beforeend','<span class="badge">'+G.ev.length+' 件</span>');
 const first=hb.closest('.hbs')||hb;const anchor=first;
 if(v===1){root.insertBefore(ev,anchor);root.insertBefore(nx,anchor);}
 if(v===2){const two=document.createElement('div');two.className='two';const l=document.createElement('div');l.className='l';const r=document.createElement('div');r.className='r';
  root.insertBefore(two,anchor);two.appendChild(l);two.appendChild(r);l.appendChild(ev);l.appendChild(nx);r.appendChild(post);}
 if(v===3){const bar=document.createElement('div');bar.className='stab';const G1=[ev,nx],G2=[post],G3=pns.filter(e=>/部屋の様子|部屋日誌/.test((e.querySelector('h2,h3')||{}).innerText||'')).map(e=>e.closest('.pn').parentNode.closest('.pn')||e);
  const groups=[['やること <span class="badge">'+G.ev.length+'</span>',G1],['場所の結果',G2],['部屋の様子・日誌',G3]];
  bar.innerHTML=groups.map((g,i)=>'<button class="'+(i===0?'on':'')+'">'+g[0]+'</button>').join('');root.insertBefore(bar,anchor);
  groups.forEach(g=>g[1].forEach(e=>root.insertBefore(e,anchor)));groups.slice(1).forEach(g=>g[1].forEach(e=>e.style.display='none'));
  const pic=document.createElement('div');pic.className='hbmini';root.insertBefore(pic,anchor);}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;UI.view='home';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'sc%d%s' % (v, nm)
            # 最初の 1 画面(ナビの下まで少し下げた所)
            pg.evaluate("scrollTo(0,0)"); pg.screenshot(path=os.path.join(out, name + '.png'))
            info = pg.evaluate("""()=>{const t=s=>{const e=[...document.querySelectorAll('.pn')].find(e=>(e.querySelector('h2,h3')||{}).innerText?.includes(s));return e?Math.round(e.getBoundingClientRect().top+scrollY):-1};return {全体:document.documentElement.scrollHeight,悩みごと:t('親方の悩みごと'),次の場所へ:t('次の場所へ'),横あふれ:document.documentElement.scrollWidth>innerWidth}}""")
            print(name, info)
    b.close()
