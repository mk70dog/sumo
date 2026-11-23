# 稽古の週のホーム「弟子の様子」のスクロールを減らす見本 tw1〜tw3(ダルマさん「全体的に下にスクロールが多いので改良する」→「実施」)
# 本体を開いて伊勢ヶ濱部屋(弟子 32 人)で始め、稽古の第 1 週へ進め、ownTable を見本の形に差し替えて写真を撮る。
# usage: python3 tools/mktwsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.twx details{margin:6px 0;border:1px solid var(--line);border-radius:8px;background:var(--washi2)}
.twx details>summary{cursor:pointer;padding:8px 12px;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.twx details>summary::-webkit-details-marker{display:none}
.twx details>summary::after{content:'▼ ひらく';font-weight:400;font-size:12px;color:var(--mute)}
.twx details[open]>summary::after{content:'▲ たたむ'}
.twx details>summary small{font-weight:400;color:var(--mute);font-size:12px;margin-left:6px}
.twx details>summary .shu{color:var(--shu)}
.twx .sm4{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 8px}
.twx .sm4 div{flex:1;min-width:70px;background:var(--washi2);border:1px solid var(--line);border-radius:8px;padding:5px 8px;text-align:center;font-size:12px;color:var(--mute)}
.twx .sm4 b{display:block;font-size:20px;color:var(--sumi)}
.twx .sm4 .r b{color:var(--shu)}.twx .sm4 .y b{color:var(--kin)}
.twx h4{font-size:14px;margin:10px 0 4px;color:var(--sumi2);border-left:3px solid var(--shu);padding-left:8px}
.twx .tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:6px}
.twx .tl{background:var(--washi2);border:1px solid var(--line);border-radius:6px;padding:5px 8px;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:0 6px;align-items:center}
.twx .tl.warn{border-color:var(--shu)}
.twx .tl .rk{font-size:11px;color:var(--mute)}
.twx .tl .n{font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.twx .tl .mt{grid-column:1/3;display:flex;gap:4px;align-items:center;font-size:11px;color:var(--mute)}
.twx .dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#888}
.twx .dot.g{background:var(--midori)}.twx .dot.r{background:var(--shu)}.twx .dot.y{background:var(--kin)}
.twx .tl .tag{font-size:10px;padding:0 4px}
@media (max-width:760px){.twx .tiles{grid-template-columns:1fr 1fr}.twx table .hide-s{display:none}}
"""
JS = r"""(v)=>{
 const o0=ownTable;
 const warn=r=>r.inj||r.fat>=70||r.cond<35||r.kad;
 const row=r=>'<tr class="clk" onclick="showR('+r.id+')"><td><b>'+esc(r.rkS)+'</b></td><td class="nm" style="font-family:var(--kaku);font-weight:700">'+esc(r.n)+'</td><td>'+condG(r)+'</td><td>'+fatG(r)+'</td><td>'+(injTag(r)||'<span class="mute">—</span>')+(r.kad?'<span class="tag shu">角番</span>':'')+'</td></tr>';
 const tb=L=>'<table class="tb"><tr><th>番付</th><th>四股名</th><th>調子</th><th>疲労</th><th>状態</th></tr>'+L.map(row).join('')+'</table>';
 window.ownTable=function(){const o=ownAll();const sek=o.filter(r=>r.d<=1),W=o.filter(r=>r.d>1&&warn(r));
  const cnt='<div class="sm4"><div><b>'+sek.length+'</b>関取</div><div class="r"><b>'+o.filter(r=>r.inj).length+'</b>けが</div><div class="y"><b>'+o.filter(r=>r.fat>=70).length+'</b>疲れ</div><div class="r"><b>'+o.filter(r=>r.cond<35).length+'</b>不調</div></div>';
  let h='<div class="twx">';
  if(v===1){h+=cnt+'<h4>関取</h4>'+tb(sek)+(W.length?'<h4>気になる弟子(けが・疲れ・不調)</h4>'+tb(W):'')+'<details><summary>全員('+o.length+' 人)</summary>'+o0()+'</details>';}
  if(v===2){h+=cnt;const D=[[0,'幕内'],[1,'十両'],[2,'幕下'],[3,'三段目'],[4,'序二段'],[5,'序ノ口']];
   D.forEach(([d,nm])=>{const L=o.filter(r=>r.d===d);if(!L.length)return;const w=L.filter(warn).length;
    h+='<details'+(d<=1?' open':'')+'><summary><span>'+nm+'<small>'+L.length+' 人</small>'+(w?'<small class="shu">気になる '+w+' 人</small>':'')+'</span></summary>'+tb(L)+'</details>';});}
  if(v===3){h+=cnt+'<div class="tiles">'+o.map(r=>{const c=r.cond>=70?'g':r.cond<35?'r':'',fz=r.fat>=70?'r':r.fat>=45?'y':'g';
    return '<div class="tl'+(warn(r)?' warn':'')+'" onclick="showR('+r.id+')"><div><div class="rk">'+esc(r.rkS)+'</div><div class="n">'+esc(r.n)+'</div></div><div>'+(injTag(r)||'')+(r.kad?'<span class="tag shu">角番</span>':'')+'</div><div class="mt"><span class="dot '+c+'"></span>調子 '+Math.round(r.cond)+' <span class="dot '+fz+'"></span>疲労 '+Math.round(r.fat)+'</div></div>';}).join('')+'</div><p class="mute kaku" style="font-size:12px;margin-top:6px">● 緑=良い・金=注意・朱=悪い。朱の枠=けが・疲れ・不調・角番</p>';}
  return h+'</div>';};
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (0, 1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const o=ownAll();o[5].fat=78;o[9].cond=28;o[14].inj=o[14].inj||{p:'右膝',s:1,w:2};G.cvS=cvScene().key;G.cvW=cvKey();UI.view='home';applySkin('urushik');}")
            if v: pg.add_style_tag(content=CSS); pg.evaluate(JS, v)
            pg.evaluate("render()"); pg.wait_for_timeout(400)
            name = 'tw%d%s' % (v, nm)
            pg.evaluate("()=>{const h=[...document.querySelectorAll('.pn h2')].find(e=>e.innerText.includes('弟子の様子'));scrollTo(0,h.getBoundingClientRect().top+scrollY-100)}")
            pg.wait_for_timeout(200); pg.screenshot(path=os.path.join(out, name + '.png'))
            info = pg.evaluate("""()=>{const h=[...document.querySelectorAll('.pn')].find(e=>(e.querySelector('h2')||{}).innerText?.includes('弟子の様子'));return {全体:document.documentElement.scrollHeight,弟子の様子:Math.round(h.offsetHeight),横あふれ:document.documentElement.scrollWidth>innerWidth}}""")
            print(name, info)
    b.close()
