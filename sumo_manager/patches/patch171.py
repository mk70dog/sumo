# v167 -> v168:経営の画面のスクロールを減らす(見本 ke2。ダルマさん「実施」→ ke1〜ke3 →「2」)。
#   部屋のあらまし・一門・年寄名跡を 1 行の見出しにたたむ(見出しに所属の一門・名跡の数)。
#   前の場所の収支は「収入の合計・支出の合計・差し引き」だけ見せ、「内訳を見る」で全部(と説明)を開く。もう一度押すとたたむ。
#   部屋の施設・評判と後援会・年ごとの収支は今までどおり。開け閉めは UI に覚える。作り:render の後処理 keFold()。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=167;\nconst SAVE='sumoManager167',SAVE166", "const APPV=168;\nconst SAVE='sumoManager168',SAVE167='sumoManager167',SAVE166")
rep('[SAVE166,SAVE165', '[SAVE167,SAVE166,SAVE165')
rep('<title>Grand Sumo Manager v167', '<title>Grand Sumo Manager v168')
BLOCK = r"""<style>
/* v168 経営:見出しにたたむ+収支は合計だけ(見本 ke2) */
.ehid{display:none!important}
.emore{display:block;margin:6px 0;font-size:13px;padding:5px 12px}
</style>
<script>
(function(){
UI.keA=UI.keA||{};
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='keiei')keFold();}catch(e){console.error(e);}return x;};
function keFold(){
 [...document.querySelectorAll('.pn>h2')].forEach(h=>{const pn=h.parentElement;if(pn.closest('.kacc')||pn.parentElement.closest('.pn'))return;
  const t=(h.childNodes[0]&&h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim();
  if(t.startsWith('前の場所の収支')){keSum(pn);return;}
  let sm=null;
  if(t.startsWith('部屋のあらまし'))sm='親方・裏方・所在地・沿革';
  else if(t==='一門')sm=((h.querySelector('.sub')||{}).textContent||'無所属')+'・移る/抜ける';
  else if(t.startsWith('年寄名跡')){const tb=pn.querySelector('table');sm=((h.querySelector('.sub')||{}).textContent||'')+'・売りに出ている名跡';if(!tb)sm=(h.querySelector('.sub')||{}).textContent||'';}
  if(sm===null)return;
  const d=document.createElement('details');d.className='kacc';if(UI.keA[t])d.open=true;
  d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=t;d.querySelector('small').textContent=sm;
  d.addEventListener('toggle',()=>{UI.keA[t]=d.open;});pn.parentNode.insertBefore(d,pn);d.appendChild(pn);});
}
function keSum(pn){const t=pn.querySelector(':scope>table');if(!t)return;const rows=[...t.rows];
 const keep=rows.filter(r=>/収入の合計|支出の合計|差し引き/.test(r.textContent));if(!keep.length)return;
 const hid=rows.filter(r=>!keep.includes(r));const p=pn.querySelector(':scope>p');if(p)hid.push(p);
 const nIn=rows.findIndex(r=>/支出/.test(r.textContent)&&r.querySelector('th'));const ni=nIn>0?rows.slice(1,nIn).filter(r=>!keep.includes(r)).length:0;
 const no=rows.filter(r=>!keep.includes(r)&&!r.querySelector('th')).length-ni;
 const b=document.createElement('button');b.className='btn sm emore';
 const set=()=>{const op=!!UI.keA.sum;hid.forEach(e=>e.classList.toggle('ehid',!op));b.textContent=op?'内訳をたたむ ▲':'内訳を見る(収入 '+ni+' 件・支出 '+no+' 件)▼';};
 b.addEventListener('click',()=>{UI.keA.sum=!UI.keA.sum;set();});t.insertAdjacentElement('afterend',b);set();}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
