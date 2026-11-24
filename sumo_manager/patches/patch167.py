# v163 -> v164:記録の画面のスクロールを減らす(見本 kr3。ダルマさん「実施」→ kr1〜kr3 →「3」)。
#   長い表(8 行以上)は上から 5 件だけ見せて「残り N 件を見る ▼」で開く(もう一度押すとたたむ)。部屋日誌も 5 件まで。
#   あまり見ないもの(育成の成績・メディア・新聞の予想・相撲部屋の一覧・給金番付・角界の部屋・取材の記事・不祥事の記録・部屋日誌)は 1 行の見出しにたたむ。
#   部屋の歩み・達成・部屋番付などは開いたまま。開け閉めは UI に覚える。作り:render の後処理 krFold()。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=163;\nconst SAVE='sumoManager163',SAVE162", "const APPV=164;\nconst SAVE='sumoManager164',SAVE163='sumoManager163',SAVE162")
rep('[SAVE162,SAVE161', '[SAVE163,SAVE162,SAVE161')
rep('<title>Grand Sumo Manager v163', '<title>Grand Sumo Manager v164')
BLOCK = r"""<style>
/* v164 記録:長い表は 5 件+たたむ(見本 kr3) */
.rmore{display:block;margin:6px 0;font-size:13px;padding:5px 12px}
.krh{display:none!important}
</style>
<script>
(function(){
UI.krA=UI.krA||{};UI.krM=UI.krM||{};
const RARE=/^(育成の成績|メディア|新聞の予想|相撲部屋の一覧|給金番付|角界の部屋|取材の記事|不祥事の記録|部屋日誌)/;
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='kiroku')krFold();}catch(e){console.error(e);}return x;};
function more(key,items,after){if(items.length<=5)return;const n=items.length-5;const set=()=>{const op=!!UI.krM[key];items.slice(5).forEach(e=>e.classList.toggle('krh',!op));b.textContent=op?'たたむ ▲':'残り '+n+' 件を見る ▼';};
 const b=document.createElement('button');b.className='btn sm rmore';b.addEventListener('click',()=>{UI.krM[key]=!UI.krM[key];set();});after.insertAdjacentElement('afterend',b);set();}
function krFold(){
 document.querySelectorAll('.pn table').forEach((t,i)=>{const rows=[...t.rows].filter(r=>!r.querySelector('th'));if(rows.length<=7)return;const h=t.closest('.pn').querySelector('h2');more('t'+i+':'+(h?h.textContent.slice(0,8):''),rows,t);});
 [...document.querySelectorAll('.pn>h2')].forEach(h=>{const t=(h.childNodes[0]&&h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim();
  const pn=h.parentElement;if(pn.parentElement.closest('.kacc'))return;
  if(t.startsWith('部屋日誌')){const L=[...pn.children].filter(e=>e!==h);if(L.length===1&&L[0].children.length>6)more('nisshi',[...L[0].children],L[0]);else if(L.length>6)more('nisshi',L,L[L.length-1]);}
  if(!RARE.test(t))return;const d=document.createElement('details');d.className='kacc';if(UI.krA[t])d.open=true;
  d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=t;d.querySelector('small').textContent=(h.querySelector('.sub')||{}).textContent||'';
  d.addEventListener('toggle',()=>{UI.krA[t]=d.open;});pn.parentNode.insertBefore(d,pn);d.appendChild(pn);});
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
