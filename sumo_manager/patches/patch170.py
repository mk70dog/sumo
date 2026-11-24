# v166 -> v167:スタッフの画面のスクロールを減らす(見本 st2。ダルマさん「実施」→ st1〜st3 →「2」)。
#   親方と部屋のスタッフは開いたまま。部屋の人の図・おかみさん・こんな親方に来てほしい・雇える人は 1 行の見出しにたたむ。
#   部屋付き親方とマネージャーは 1 人 1 行(名前・年齢と最高位/担当・指導の数字)。行を押すと今までの欄(教える型・人柄・契約を終える)が開く。
#   ついでに直す:スタッフの欄の「教える型・指導の色・人柄・教え方」(div.cot)の字が #1a140c 固定で、暗い色の組だと読めなかった → 色の組の字の色に。
#   開け閉めは UI に覚える(スタッフは契約を終えるボタンの id で)。作り:render の後処理 stFold()。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=166;\nconst SAVE='sumoManager166',SAVE165", "const APPV=167;\nconst SAVE='sumoManager167',SAVE166='sumoManager166',SAVE165")
rep('[SAVE165,SAVE164', '[SAVE166,SAVE165,SAVE164')
rep('<title>Grand Sumo Manager v166', '<title>Grand Sumo Manager v167')
BLOCK = r"""<style>
/* v167 スタッフ:見出しにたたむ+1 人 1 行(見本 st2) */
.sl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin:4px 0 8px}
.sr{display:grid;grid-template-columns:1fr auto;gap:2px 8px;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.sr .n{font-weight:700;color:var(--sumi)}.sr .n small{font-weight:400;font-size:11px;color:var(--mute);margin-left:6px}
.sr .s{font-size:12px;color:var(--mute);grid-column:1/3}.sr .s b{color:var(--sumi);font-weight:700}
.sr .x{font-size:11px;color:var(--mute)}.sr .x::after{content:'▼'}
.sr.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}.sr.op .x::after{content:'▲'}
.sopen{grid-column:1/-1}.sopen>.stf{margin:0 0 6px}
div.cot{color:var(--sumi2)}div.cot b{color:var(--sumi)}
@media (max-width:760px){.sl{grid-template-columns:1fr}}
</style>
<script>
(function(){
UI.stO=UI.stO||{};UI.stA=UI.stA||{};
const FOLD=/^(部屋の人の図|おかみさん|こんな親方に来てほしい|雇える人)/;
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='staff')stFold();}catch(e){console.error(e);}return x;};
function stFold(){
 [...document.querySelectorAll('.pn>h2')].forEach(h=>{const pn=h.parentElement;if(pn.closest('.kacc')||pn.parentElement.closest('.pn'))return;
  const t=(h.childNodes[0]&&h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim();
  if(t.startsWith('部屋のスタッフ')){stRows(pn);return;}
  if(!FOLD.test(t))return;const d=document.createElement('details');d.className='kacc';if(UI.stA[t])d.open=true;
  d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=t;d.querySelector('small').textContent=(h.querySelector('.sub')||{}).textContent||'';
  d.addEventListener('toggle',()=>{UI.stA[t]=d.open;});pn.parentNode.insertBefore(d,pn);d.appendChild(pn);});
}
function stRows(pn){let L=null;
 [...pn.children].forEach((c,i)=>{if(c.tagName==='H3'){L=null;return;}
  if(!c.classList.contains('stf'))return;
  if(!L){L=document.createElement('div');L.className='sl';c.insertAdjacentElement('beforebegin',L);}
  const fb=c.querySelector('[onclick*="askFire("]');const key=fb?((fb.getAttribute('onclick')||'').match(/askFire\((\d+)/)||[])[1]:'i'+i;
  const row=document.createElement('div');row.className='sr'+(UI.stO[key]?' op':'');
  row.innerHTML='<div class="n"><span></span><small></small></div><div class="x"></div><div class="s"></div>';
  row.querySelector('.n span').textContent=(c.querySelector('.nm')||{}).textContent||'';
  row.querySelector('.n small').textContent=((c.firstElementChild||{}).querySelector?((c.firstElementChild.querySelector('.mute')||{}).textContent||''):'');
  const S=row.querySelector('.s');[...c.querySelectorAll('.sks>.sk')].forEach((k,j)=>{if(j)S.append(' ・ ');const b=k.querySelector('b');S.append((k.firstChild&&k.firstChild.textContent||'').trim()+' ');const bb=document.createElement('b');bb.textContent=b?b.textContent:'';S.append(bb);});
  const box=document.createElement('div');box.className='sopen';box.style.display=UI.stO[key]?'':'none';
  row.addEventListener('click',()=>{UI.stO[key]=!UI.stO[key];row.classList.toggle('op',!!UI.stO[key]);box.style.display=UI.stO[key]?'':'none';});
  c.replaceWith(document.createComment(''));box.appendChild(c);L.appendChild(row);L.appendChild(box);});
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
