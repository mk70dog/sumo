# 本場所(場所中)の画面のスクロールを減らす見本 bs1〜bs3(ダルマさん「全体的に下にスクロールが多いので改良する」→「続ける」)
# 本体を開いて伊勢ヶ濱部屋(弟子 32 人)で始め、初場所 5 日目終了まで進めて「本場所」画面を組み替え、写真を撮る。
# usage: python3 tools/mkbssamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.bsx .bacc,.bacc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.bacc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.bacc>summary::-webkit-details-marker{display:none}
.bacc>summary b{font-size:16px;color:var(--sumi)}.bacc>summary small{color:var(--mute);font-size:12px}
.bacc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.bacc[open]>summary::after{content:'▲ たたむ'}
.bacc>.pn{margin:0;border:none}.bacc>.pn>h2{display:none}
.bl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin-top:6px}
.br{display:grid;grid-template-columns:1fr 26px 1fr auto;gap:2px 8px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.br.os{border-left:4px solid var(--kin)}
.br .a{font-weight:700;color:var(--sumi)}.br .a small,.br .c small{display:block;font-weight:400;font-size:11px;color:var(--mute)}
.br .c{text-align:right;font-weight:700;color:var(--sumi)}.br .v{color:var(--kin);text-align:center;font-weight:700}
.br .p{grid-column:1/4;font-size:12px;color:var(--mute)}.br .p b{color:var(--kin);letter-spacing:2px}
.br .x{font-size:11px;color:var(--mute);grid-row:1/3;grid-column:4}
.br.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.bopen{grid-column:1/-1}
.btb{width:100%;border-collapse:collapse;margin-top:6px}
.btb th{font-size:12px;color:var(--mute);text-align:left;padding:4px 6px;border-bottom:1px solid var(--line);font-weight:400}
.btb td{padding:5px 6px;border-bottom:1px solid var(--line);vertical-align:middle}
.btb .a{font-weight:700}.btb small{display:block;font-size:11px;color:var(--mute)}
.btb .mk3{letter-spacing:2px;white-space:nowrap}
.btb select{font-size:12px;padding:3px}
.btb tr.os td:first-child{border-left:4px solid var(--kin)}
.btb .dt{font-size:12px;padding:3px 8px}
@media (max-width:760px){.bl{grid-template-columns:1fr}.btb .hs{display:none}
.btb,.btb tbody{display:block}.btb tr:first-child{display:none}
.btb tr{display:grid;grid-template-columns:1fr 18px 1fr;gap:2px 6px;padding:6px 0;border-bottom:1px solid var(--line)}
.btb td{border:none;padding:1px 2px}.btb .mk3{grid-column:1/4}.btb .s1{grid-column:1/2}.btb .s2{grid-column:3/4}.btb select{width:100%}}
"""
JS = r"""(v)=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const H=t=>[...document.querySelectorAll('.pn h2')].find(e=>e.innerText.includes(t));
 const tor=H('日目の取組').closest('.pn'),sug=H('場所中の過ごし方').closest('.pn');
 const fold=(el,title,small,open)=>{const d=document.createElement('details');d.className='bacc';if(open)d.open=true;d.innerHTML='<summary><b>'+title+'</b><small>'+small+'</small></summary>';el.parentNode.insertBefore(d,el);d.appendChild(el);return d;};
 const grp=[...sug.querySelectorAll('b,h3,div')].filter(e=>/^(関取|幕下|三段目以下)\s*\d+\s*人$/.test(e.innerText.trim())).map(e=>e.innerText.trim());
 fold(sug,'場所中の過ごし方',(grp.length?grp.join('・')+'・':'')+'明日の朝稽古と午後。押すと変えられます',false);
 const nxs=[...tor.querySelectorAll(':scope>.nx')];
 const info=nx=>{const m=nx.querySelector('.nxm');const s=m.children;const nm=x=>x.querySelector('.nm').innerText,sub=x=>x.querySelector('.mute').innerText;
  const rows=[...nx.querySelectorAll('table.yt tr')].slice(1);const mk=i=>rows.map(r=>r.cells[i].innerText.trim()).join('');
  const sel=[...nx.querySelectorAll('select')];const st=sel.map(x=>x.options[x.selectedIndex].text.replace(/^.*?:/,'')).join('・');
  return {a:nm(s[0]),as:sub(s[0]),c:nm(s[2]),cs:sub(s[2]),ma:mk(1),mc:mk(2),st:st,os:nx.classList.contains('os'),sel:sel,seki:/横綱|大関|関脇|小結|前頭|十両/.test(sub(s[0]))};};
 const row=(nx,i)=>{const d=info(nx);const r=document.createElement('div');r.className='br'+(d.os?' os':'')+(i===0?' op':'');
  r.innerHTML='<div class="a">'+(d.os?'★':'')+d.a+'<small>'+d.as+'</small></div><div class="v">対</div><div class="c">'+d.c+'<small>'+d.cs+'</small></div><div class="x">'+(i===0?'▲':'▼')+'</div><div class="p">予想 <b>'+d.ma+'</b> 対 '+d.mc+' ・ 作戦 '+d.st+'</div>';return r;};
 if(v===1||v===3){const L=document.createElement('div');L.className='bl';let first=true;const keep=[];
  nxs.forEach((nx,i)=>{const d=info(nx);if(v===3&&d.seki){keep.push(nx);return;}const r=row(nx,first?0:1);L.appendChild(r);if(first){const o=document.createElement('div');o.className='bopen';nx.parentNode.insertBefore(o,nx);o.appendChild(nx);L.appendChild(o);first=false;}else nx.remove();});
  if(v===1){tor.insertBefore(L,tor.querySelector(':scope>.nx, :scope>.bopen')||null);tor.querySelector('h2').insertAdjacentHTML('afterend','<div class="mute kaku" style="font-size:12px;margin:2px 0 6px">1 番 1 行。押すと新聞の予想・本人の話・作戦が開きます。予想は 相撲日報・スポーツ角界・週刊土俵裏 の順。</div>');}
  else{const last=keep[keep.length-1];const d=document.createElement('details');d.className='bacc';d.innerHTML='<summary><b>幕下から下の取組</b><small>'+L.querySelectorAll('.br').length+' 番・押すと 1 番 1 行で見られます</small></summary>';d.appendChild(L);last.insertAdjacentElement('afterend',d);
   tor.querySelector('h2').insertAdjacentHTML('afterend','<div class="mute kaku" style="font-size:12px;margin:2px 0 6px">関取の取組は今までどおり。幕下から下はたたんであります。</div>');}}
 if(v===2){const t=document.createElement('table');t.className='btb';t.innerHTML='<tr><th>部屋の力士</th><th></th><th>相手</th><th>予想(日報・角界・土俵裏)</th><th>立ち合い</th><th>組み手</th><th class="hs"></th></tr>';
  nxs.forEach(nx=>{const d=info(nx);const tr=document.createElement('tr');if(d.os)tr.className='os';
   tr.innerHTML='<td class="a">'+(d.os?'★':'')+d.a+'<small>'+d.as+'</small></td><td style="color:var(--kin)">対</td><td>'+d.c+'<small>'+d.cs+'</small></td><td class="mk3"><b style="color:var(--kin)">'+d.ma+'</b> / '+d.mc+'</td><td class="s1"></td><td class="s2"></td><td class="hs"><button class="btn sm dt">詳しく</button></td>';
   d.sel.forEach((s,j)=>{[...s.options].forEach(o=>o.text=o.text.replace(/^.*?:/,''));tr.querySelector(j?'.s2':'.s1').appendChild(s);});t.appendChild(tr);nx.remove();});
  tor.appendChild(t);}
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.phase==='train'){doWeek();while(G.ev.length)resolveEv(G.ev[0].id,0);}for(let i=0;i<5;i++)advanceDay();const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='basho';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.wait_for_timeout(200)
            name = 'bs%d%s' % (v, nm)
            pg.evaluate("()=>{const h=[...document.querySelectorAll('.pn h2')].find(e=>e.innerText.includes('日目の取組'));scrollTo(0,h.getBoundingClientRect().top+scrollY-(innerWidth<760?180:130))}")
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '全体 %.1f 画面' % (pg.evaluate("document.documentElement.scrollHeight") / H), '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
