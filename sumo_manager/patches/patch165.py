# v161 -> v162:本場所(場所中)の画面のスクロールを減らす(見本 bs1「1 番 1 行」。ダルマさん「続ける」→ bs1〜bs3 →「1」)。
#   「○日目の取組」は 1 番 1 行(部屋の力士・相手・新聞 3 紙の予想の印・作戦)。行を押すと今までのカード(予想の表・本人の話・作戦の選び)が開く。
#   「場所中の過ごし方」は 1 行の見出しにたたむ(押すと今までどおり変えられる)。
#   開け閉めは UI に覚える(描き直しても閉じない)。作戦を選び直すと行の「作戦」もすぐ変わる。作り:render の後処理 bsFold()。
#   数値や仕組みは変えない。見出しの形は v161 の稽古(.kacc)と同じ。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=161;\nconst SAVE='sumoManager161',SAVE160", "const APPV=162;\nconst SAVE='sumoManager162',SAVE161='sumoManager161',SAVE160")
rep('[SAVE160,SAVE159', '[SAVE161,SAVE160,SAVE159')
rep('<title>Grand Sumo Manager v161', '<title>Grand Sumo Manager v162')
BLOCK = r"""<style>
/* v162 本場所(場所中):1 番 1 行(見本 bs1) */
.bl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin-top:6px}
.br{display:grid;grid-template-columns:1fr 26px 1fr auto;gap:2px 8px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.br.os{border-left:4px solid var(--kin)}
.br .a{font-weight:700;color:var(--sumi)}.br .a small,.br .c small{display:block;font-weight:400;font-size:11px;color:var(--mute)}
.br .c{text-align:right;font-weight:700;color:var(--sumi)}.br .v{color:var(--kin);text-align:center;font-weight:700}
.br .p{grid-column:1/4;font-size:12px;color:var(--mute)}.br .p b{color:var(--kin);letter-spacing:2px}
.br .x{font-size:11px;color:var(--mute);grid-row:1/3;grid-column:4}.br .x::after{content:'▼'}
.br.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}.br.op .x::after{content:'▲'}
.bopen{grid-column:1/-1}.bopen>.nx{margin:0 0 6px}
.bnote{font-size:12px;margin:2px 0 6px}
@media (max-width:760px){.bl{grid-template-columns:1fr}}
</style>
<script>
(function(){
UI.bsO=UI.bsO||{};UI.bsA=UI.bsA||{};
const R0=render;
render=function(){const r=R0.apply(this,arguments);try{if(UI.view==='basho')bsFold();}catch(e){console.error(e);}return r;};
function acc(key,title,small){const d=document.createElement('details');d.className='kacc';if(UI.bsA[key])d.open=true;d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=title;d.querySelector('small').textContent=small||'';d.addEventListener('toggle',()=>{UI.bsA[key]=d.open;});return d;}
function bsFold(){
 const H=t=>[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.includes(t));
 const hs=H('場所中の過ごし方');
 if(hs){const pn=hs.closest('.pn');if(!pn.closest('.kacc')){const g=[...pn.querySelectorAll('b,h3,div')].map(e=>e.textContent.trim()).filter(t=>/^(関取|幕下|三段目以下)\s*\d+\s*人$/.test(t));
  const d=acc('sug','場所中の過ごし方',(g.length?g.join('・')+'・':'')+'明日の朝稽古と午後。押すと変えられます');pn.parentNode.insertBefore(d,pn);d.appendChild(pn);}}
 const ht=H('日目の取組');if(!ht)return;const tor=ht.closest('.pn');
 const nxs=[...tor.querySelectorAll(':scope>.nx')];if(!nxs.length)return;
 const L=document.createElement('div');L.className='bl';
 nxs.forEach((nx,i)=>{const m=nx.querySelector('.nxm');if(!m||m.children.length<3)return;const s=m.children;
  const nm=x=>(x.querySelector('.nm')||{}).textContent||'',sub=x=>(x.querySelector('.mute')||{}).textContent||'';
  const rows=[...nx.querySelectorAll('table.yt tr')].slice(1);const mk=j=>rows.map(r=>(r.cells[j]||{}).textContent||'').join('').replace(/\s/g,'');
  const sel=[...nx.querySelectorAll('select')];const id=sel.length?((sel[0].getAttribute('onchange')||'').match(/setBT\((\d+)/)||[])[1]:null;const key=id||('i'+i);
  const st=()=>sel.map(x=>x.options[x.selectedIndex].text.replace(/^.*?:/,'')).join('・');
  const row=document.createElement('div');row.className='br'+(nx.classList.contains('os')?' os':'')+(UI.bsO[key]?' op':'');
  row.innerHTML='<div class="a"><span></span><small></small></div><div class="v">対</div><div class="c"><span></span><small></small></div><div class="x"></div><div class="p"></div>';
  row.querySelector('.a span').textContent=(nx.classList.contains('os')?'★':'')+nm(s[0]);row.querySelector('.a small').textContent=sub(s[0]);
  row.querySelector('.c span').textContent=nm(s[2]);row.querySelector('.c small').textContent=sub(s[2]);
  const P=row.querySelector('.p');const setP=()=>{P.innerHTML='';P.append(rows.length?'予想 ':'');if(rows.length){const b=document.createElement('b');b.textContent=mk(1);P.append(b,' 対 '+mk(2));}if(sel.length)P.append((rows.length?' ・ ':'')+'作戦 '+st());};setP();
  sel.forEach(x=>x.addEventListener('change',setP));
  const box=document.createElement('div');box.className='bopen';box.style.display=UI.bsO[key]?'':'none';
  row.addEventListener('click',()=>{UI.bsO[key]=!UI.bsO[key];row.classList.toggle('op',!!UI.bsO[key]);box.style.display=UI.bsO[key]?'':'none';});
  nx.replaceWith(document.createComment(''));box.appendChild(nx);L.appendChild(row);L.appendChild(box);});
 const anchor=tor.querySelector(':scope>.btns')||ht;anchor.insertAdjacentElement('afterend',L);
 ht.insertAdjacentHTML('afterend','<div class="mute kaku bnote">1 番 1 行。押すと新聞の予想・本人の話・作戦が開きます。予想の印は 相撲日報・スポーツ角界・週刊土俵裏 の順。</div>');
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
