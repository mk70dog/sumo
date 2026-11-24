# 力士の画面のスクロールを減らす見本 rk1〜rk3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# 本体を開いて伊勢ヶ濱部屋(弟子 32 人)で始め、稽古の第 1 週の「力士」画面を組み替えて写真を撮る。
# usage: python3 tools/mkrksamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.racc2{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.racc2>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.racc2>summary::-webkit-details-marker{display:none}
.racc2>summary b{font-size:16px;color:var(--sumi)}.racc2>summary small{color:var(--mute);font-size:12px}
.racc2>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.racc2[open]>summary::after{content:'▲ たたむ'}
.racc2>.pn{margin:0;border:none}.racc2>.pn>h2{display:none}
.rtb{width:100%;border-collapse:collapse}
.rtb th{font-size:12px;color:var(--mute);text-align:left;padding:4px 6px;border-bottom:1px solid var(--line);font-weight:400;white-space:nowrap}
.rtb td{padding:6px;border-bottom:1px solid var(--line);vertical-align:middle;white-space:nowrap}
.rtb tr{cursor:pointer}.rtb tr:hover td{background:rgba(201,162,74,.08)}
.rtb .n{font-weight:700;color:var(--sumi)}.rtb small{display:block;font-size:11px;color:var(--mute)}
.rtb .g{color:var(--midori)}.rtb .r{color:var(--shu)}.rtb .y{color:var(--kin)}
.rgl{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:6px}
.rgc{border:1px solid var(--line);border-radius:6px;background:var(--washi2);padding:6px 8px;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:0 6px}
.rgc .k{font-size:11px;color:var(--mute)}.rgc .n{font-weight:700;color:var(--sumi)}.rgc .so{font-size:20px;font-weight:700;color:var(--kin);grid-row:1/3;grid-column:2;align-self:center}
.rgc .m{grid-column:1/3;font-size:11px;color:var(--mute)}
@media (max-width:760px){.rtb .hs{display:none}.rtb td,.rtb th{padding:5px 3px;font-size:13px}.rtb td.n{white-space:normal}.rtb small{white-space:normal}.rgl{grid-template-columns:1fr 1fr}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const H=t=>[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith(t));
 const tk=H('付け人').parentElement,dz=H('弟子たち').parentElement;
 const fold=(el,t,s,open)=>{const d=document.createElement('details');d.className='racc2';if(open)d.open=true;d.innerHTML='<summary><b>'+t+'</b><small>'+s+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const nS=ownAll().filter(r=>r.d<=1).length;fold(tk,'付け人','関取 '+nS+' 人の身の回りの世話・付け人の割り当て',false);
 const cards=dz.querySelector('.cards');const C=[...cards.children];
 const D=C.map(c=>{const id=+((c.getAttribute('onclick')||'').match(/\d+/)||[0])[0];const r=G.R[id];const s=c.querySelector('.sts').children;
   const val=k=>{for(let i=0;i<s.length;i++)if(s[i].textContent===k)return s[i+2].textContent;return '';};
   return {c,r,rk:c.querySelector('.rk').textContent,info:[...c.querySelector('.info').children].slice(1,3).map(e=>e.textContent).join('・'),
    so:val('素質'),sg:val('総合'),cond:Math.round(r.cond),fat:Math.round(r.fat),pop:val('人気'),prev:(c.querySelector('.info>.mute')||{}).textContent||'',tag:(c.querySelector('.tag')||{}).textContent||''};});
 const cc=x=>x>=70?'g':x<35?'r':'',fc=x=>x>=70?'r':x>=45?'y':'g';
 const table=L=>'<table class="rtb"><tr><th>番付</th><th>四股名</th><th>総合</th><th>素質</th><th>調子</th><th>疲労</th><th class="hs">人気</th><th class="hs">前場所</th></tr>'+L.map(d=>'<tr onclick="showR('+d.r.id+')"><td>'+d.rk+'</td><td class="n">'+d.r.n+(d.tag?' <span class="tag inj">'+d.tag+'</span>':'')+'<small>'+d.info+'</small></td><td>'+d.sg+'</td><td class="y"><b>'+d.so+'</b></td><td class="'+cc(d.cond)+'">'+d.cond+'</td><td class="'+fc(d.fat)+'">'+d.fat+'</td><td class="hs">'+d.pop+'</td><td class="hs">'+d.prev.replace('前場所 ','')+'</td></tr>').join('')+'</table>';
 if(v===1){cards.outerHTML=table(D);}
 if(v===2){cards.outerHTML='<div class="rgl">'+D.map(d=>'<div class="rgc" onclick="showR('+d.r.id+')"><div class="k">'+d.rk+'</div><div class="so">'+d.so+'</div><div class="n">'+d.r.n+'</div><div class="m">総合 '+d.sg+' ・ 調子 '+d.cond+' ・ 疲労 '+d.fat+' ・ '+d.prev+'</div></div>').join('')+'</div>';}
 if(v===3){const G2=[['関取',d=>d.r.d<=1,true],['幕下',d=>d.r.d===2,false],['三段目',d=>d.r.d===3,false],['序二段・序ノ口・前相撲',d=>d.r.d>=4||!(d.r.d>=0),false]];
  const wrap=document.createElement('div');G2.forEach(([t,f,o])=>{const L=D.filter(f);if(!L.length)return;wrap.insertAdjacentHTML('beforeend','<details class="racc2"'+(o?' open':'')+'><summary><b>'+t+'</b><small>'+L.length+' 人</small></summary><div style="padding:0 10px 8px">'+table(L)+'</div></details>');});cards.replaceWith(wrap);}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='rikishi';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'rk%d%s' % (v, nm)
            pg.evaluate("scrollTo(0,0)" if v == 0 else "()=>{const e=document.querySelector('.racc2');scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerWidth<760?220:140))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
